from .extensions import celery



@celery.task()
def add(x, y):
    return x + y


@celery.task()
def mul(x, y):
    return x * y


@celery.task()
def xsum(numbers):
    return sum(numbers)


@celery.task()
def t_print(num):
    return '{}번째 일을 끝! '.format(num)


@celery.task()
def what():
    return 'awesome! it works :)'


@celery.on_after_configure.connect
def add_periodic(**kwargs):
    celery.add_periodic_task(10.0, add.s(2,3), name='add every 10')