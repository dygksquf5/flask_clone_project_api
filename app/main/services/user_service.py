from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError, DataError
from werkzeug.utils import secure_filename

from app.main import output
from app.main.connection import connect_s3, upload_s3

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import current_user

# service
from app.main.services.global_service import object_as_dict

# password
import bcrypt

import re
import uuid


class UserService:
    def __init__(self, usersdao, app):
        self.app = app
        self.usersdao = usersdao

    def new_user(self, new_user, profile_img):
        new_user_id = uuid.uuid4()
        # hash 하는 부분에서 db 에 해시드 된 암호 넣을때 다시 마지막에 .decode() 해주지 않으면 .encode() 된 상태에서 앞에
        # 'b <ㅡ  이부분 바이트가 붙어버리니까 이거 빼주기 !
        password = bcrypt.hashpw(new_user['password'].encode('UTF-8'),
                                 bcrypt.gensalt()).decode()

        check_email = self._checking_email_regex(new_user.get('email'))
        if check_email is False:
            return jsonify(msg=output.WRONG_EMAIL_TYPE), 400

        if profile_img:
            filename = secure_filename(profile_img.filename)
            image_url = self.save_profile_picture(picture=profile_img,
                                                  filename=filename)
            if image_url == Exception:
                return jsonify(msg=output.AWS_ERROR), 400


            result = self.usersdao.create_user(new_user=new_user,
                                               password=password,
                                               new_user_id=new_user_id,
                                               image_url=image_url)

        else:
            image_url = None
            result = self.usersdao.create_user(new_user=new_user,
                                               password=password,
                                               new_user_id=new_user_id,
                                               image_url=image_url)
        if result is IntegrityError:
            return jsonify(msg=output.EXISTS_ERROR), 400
        elif result is Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400
        else:
            return result

    # 사진파일 저장 s3 (AWS)

    def save_profile_picture(self, picture, filename):
        try:
            # s3 커넥트
            s3 = connect_s3()
            image_url = upload_s3(s3=s3, picture=picture, filename=filename)

            return image_url
        except Exception:
            return Exception

    def update_profile_picture(self, picture, filename, user_id):
        try:
            # s3 커넥트
            s3 = connect_s3()
            image_url = upload_s3(s3=s3, picture=picture, filename=filename)

            # db에 s3 url 저장
            result = self.usersdao.save_user_profile_img(image_url=image_url)
            if result == InterruptedError:
                return jsonify(msg=output.DATABASE_ERROR), 400
            return result

        except Exception:
            return jsonify(msg=output.AWS_ERROR), 400

    def get_terms(self):
        terms = self.usersdao.get_all_terms()
        if terms == NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif terms == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400
        return jsonify(object_as_dict(terms)), 200

    def user_login(self, login_info):
        try:
            email = login_info['email']
            password = login_info['password']
        except KeyError:
            return jsonify(msg=output.CHECK_PARAMS_ERROR), 400

        check_email = self._checking_email_regex(login_info['email'])
        if check_email is False:
            return jsonify(msg=output.WRONG_EMAIL_TYPE), 400

        row = self.usersdao.get_user_info_by_email(email)
        if row == NoResultFound:
            return jsonify(msg=output.NO_RESULT_EMAIL_ERROR), 404
        elif row == Exception:
            return jsonify(mss=output.UNEXPECTED_ERROR), 400

        if row and bcrypt.checkpw(password.encode('UTF-8'), row.password.encode('UTF-8')):

            user_info = self.usersdao.get_user_info_by_email(email)

            access_token = create_access_token(identity=user_info.uuid,
                                               expires_delta=self.app.config['ACCESS_EXPIRES'])
            refresh_token = create_refresh_token(identity=user_info.uuid)
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token
            })

        else:
            return jsonify(msg=output.WRONG_PWD_ERROR), 401

    def get_user_info_by_id(self, user_id):
        result = self.usersdao.get_user_info_by_id(user_id=user_id)
        if result == NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif result == DataError:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400

        return jsonify(result), 200

    def update_user_info(self, user, payload):
        if 'password' in payload and 'pay_password' in payload:
            return self.reset_pay_password(data=payload)
        elif 'password' in payload and 'new_password' in payload:
            return self.reset_password(user, payload=payload)
        elif 'name' in payload:
            return self.reset_name(user=user, payload=payload)
        elif 'email' in payload:

            check_email = self._checking_email_regex(payload['email'])
            if check_email is False:
                return jsonify(msg=output.WRONG_EMAIL_TYPE), 400

            return self.reset_email(user=user, payload=payload)
        else:
            return jsonify(msg=output.CHECK_PARAMS_ERROR), 400

    def reset_email(self, user, payload):
        try:
            email = payload['email']
        except:
            return jsonify(msg=output.CHECK_PARAMS_ERROR), 400
        check_email = self.usersdao.get_user_info_by_email(email=email)
        if check_email == NoResultFound:
            result = self.usersdao.set_new_email(user=user, new_email=email)
            if result == IntegrityError:
                return jsonify(msg=output.DATABASE_ERROR), 400
            elif result == DataError:
                return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
            return result
        elif check_email:
            return jsonify(msg=output.EXISTS_ERROR), 400

    def reset_password(self, user, payload):
        try:
            password = payload['password']
            new_password = payload['new_password']
        except:
            return jsonify(msg=output.CHECK_PARAMS_ERROR), 400
        if user.password and bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
            new_password_hashed = bcrypt.hashpw(new_password.encode('UTF-8'), bcrypt.gensalt()).decode()
            result = self.usersdao.set_new_password(user=user, new_password=new_password_hashed)
            if result == IntegrityError:
                return jsonify(msg=output.DATABASE_ERROR), 400
            elif result == DataError:
                return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
            return result
        else:
            return jsonify(msg=output.WRONG_PWD_ERROR), 401

    def reset_name(self, user, payload):
        try:
            new_name = payload['name']
        except:
            return jsonify(msg=output.CHECK_PARAMS_ERROR), 400
        if user.name:
            result = self.usersdao.set_new_name(user=user, new_name=new_name)
            if result == IntegrityError:
                return jsonify(msg=output.DATABASE_ERROR), 400
            elif result == DataError:
                return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
            return result
        else:
            return jsonify(msg=output.NO_RESULT_NAME_ERROR), 404

    def reset_pay_password(self, data):
        try:
            password = data['password']
            pay_password = data['pay_password']
        except:
            return jsonify(msg=output.CHECK_PARAMS_ERROR), 400

        if len(pay_password) != 8:
            return jsonify(msg=output.CHECK_PARAMS_LENGTH_ERROR), 400

        user = current_user

        if user.password and bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
            new_pay_password = bcrypt.hashpw(pay_password.encode('UTF-8'), bcrypt.gensalt()).decode()
            result = self.usersdao.set_new_pay_password(pay_password=new_pay_password)
            if result == IntegrityError:
                return jsonify(msg=output.DATABASE_ERROR), 400

            return jsonify(msg=output.CREATED_P_PWD_SUCCESS), 200
        else:
            return jsonify(msg=output.WRONG_PWD_ERROR), 401

            # 결제 pw 설정

    def new_or_check_pay_password(self, datas):
        try:
            password = datas['password']
            pay_password = datas['pay_password']
        except:
            return jsonify(msg=output.CHECK_PARAMS_ERROR), 400

        if len(pay_password) != 8:
            return jsonify(msg=output.CHECK_PARAMS_LENGTH_ERROR), 400

        user = current_user

        if user.pay_password is None:
            if user.password and bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
                new_pay_password = bcrypt.hashpw(pay_password.encode('UTF-8'), bcrypt.gensalt()).decode()
                result = self.usersdao.set_new_pay_password(pay_password=new_pay_password)
                if result == IntegrityError:
                    return jsonify(msg=output.DATABASE_ERROR), 400
                return jsonify(msg=output.CREATED_P_PWD_SUCCESS), 200
            else:
                return jsonify(msg=output.WRONG_PWD_ERROR), 401
        elif user.pay_password and pay_password:
            if bcrypt.checkpw(pay_password.encode('UTF-8'), user.pay_password.encode('UTF-8')):
                return jsonify(msg=output.CHECKED_P_PWD_SUCCESS), 200
            else:
                return jsonify(msg=output.WRONG_P_PWD_ERROR), 401
        else:
            return jsonify(msg=output.CHECK_PARAMS_ERROR), 400

    def delete_user(self, user):
        result = self.usersdao.delete_user_info(user=user)
        return result

    def _checking_email_regex(self, email):
        check = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        result = check.match(email) is not None
        return result

