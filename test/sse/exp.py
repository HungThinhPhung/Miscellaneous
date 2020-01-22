from functools import wraps


def print_result(func):
    @wraps(func)
    def exec(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result)
        return result

    return exec


@print_result
def ex_gain_from_sk(end_lv=100, start_lv=15):
    return sum(range(start_lv + 1, end_lv + 1))


@print_result
def ex_need_to_pl_lv(end_lv=100, start_lv=1):
    result = 0
    for i in range(start_lv + 1, end_lv + 1):
        result += 75 + 25 * i
    return result


a = ex_gain_from_sk()
b = ex_need_to_pl_lv(40)
print(b/a)
