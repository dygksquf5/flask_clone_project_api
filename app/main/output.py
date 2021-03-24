# 데이터베이스
DATABASE_ERROR = 'Database error, can not change anything'
NO_RESULT_ERROR = "해당 정보가 존재하지 않음."
NO_RESULT_NAME_ERROR = "해당 이름은 존재하지 않음"
NO_RESULT_EMAIL_ERROR = "해당 이메일은 존재하지 않음"
CHECK_DATA_TYPE_ERROR = "옳바르지 않은 데이터값입니다."
EXISTS_ERROR = "이미 존재합니다."

# params
NOTHING_PARAMS_ERROR = "해당 파라미터에 값이 없습니다."
CHECK_PARAMS_ERROR = "파라미터 값을 확인 해 주세요"
CHECK_PARAMS_LENGTH_ERROR = "params length error"
CHECK_UUID_VALUE_ERROR = "UUID value 확인 해 주세요"
WRONG_ENUM_ERROR = '옳바르지 않은 enum 입니다.'
WRONG_EMAIL_TYPE = "옳바르지 않은 이메일 양식 입니다."
WRONG_DATE_TYPE_ERROR = "옳바르지 않은 date type 입니다. "

# Auth
REVOKED_SUCCESS = "Access token and Refresh token revoked"
WRONG_P_PWD_ERROR = "틀린 결제 비밀번호"
WRONG_PWD_ERROR = "틀린 비밀번호"

# success
CHECKED_P_PWD_SUCCESS = "pay-password checked, success"
CREATED_P_PWD_SUCCESS = "결제 비밀번호 생성 완료"
REORDER_CREATE_SUCCESS = "재주문이 성공하였습니다!"

# order
CHECK_MENU_ID_ERROR = '메뉴 아이디가 잘못됐어요! 다시 확인하세요'
NO_RESULT_MENU_ERROR = '메뉴 아이디와 일치하는 메뉴가 없어요'
INVALID_MENU_WITH_STORE_ERROR = '해당 스토어의 메뉴아이디가 아닙니다 재확인!'
CHECK_OPTION_ID_ERROR = '옵션 아이디가 잘못됐어요! 다시 확인하세요 '
NO_RESULT_OPTION_ERROR = '옵션 아이디와 일치하는 옵션이 없어요 '
INVALID_OPTION_WITH_STORE_ERROR = '해당 스토어의 옵션 아이디가 아닙니다 재확인!'
INVALID_TOTAL_ORDER_PRICE_ERROR = '주문 총 금액이 맞지 않습니다. 다시 요청 해 주세요! '
NO_RESULT_ORDER_DETAIL = "해당하는 order 가 없습니다"
CHECK_ORDER_ID_ERROR = '오더 아이디가 잘못됐어요! 다시 확인하세요'
WRONG_USER_WITH_ORDER_ERROR = '해당 유저가 주문한 주문id가 아닙니다.'

# order status
STATUS_ERROR_1 = "아직 수락이 되지 않은 주문입니다."
STATUS_ERROR_2 = "이미 수락된 주문입니다."
STATUS_ERROR_3 = "수령 완료된 주문입니다."
STATUS_ERROR_4 = "패써가 이미 취소한 주문입니다."
STATUS_ERROR_5 = "시간초과로 자동취소된 주문입니다."
STATUS_ERROR_6 = "매장에서 주문취소 한 주문입니다."

# others
UNEXPECTED_ERROR = "Unexpected error, checking the params"
AWS_ERROR = "aws 저장 에러."
FAIL = "fail"
SUCCESS = "success"

ORDERED_AND_WAITING = 'ordered, waiting for confirm'
ORDERED_AUTO_CANCELED = 'auto-canceled  over 10 minutes'
INVALID_ACCESS = "Not a proper access"
TIME_OVER = "time over"

# checking params
NEW_ORDER_CHECK_LIST_1 = ['store_id', 'order_total_price',
                          'way_of_payment', 'expect_time',
                          'extra_require', 'menus']

NEW_ORDER_CHECK_LIST_2 =['menu_id', 'quantity', 'option']