import time


def deco_plus(func):
    def exec(number):
        number = number + 3
        func(number)
    return exec

def deco_mul(func):
    def exec(number):
        pass
        d = func(number)
        d['num'] *= 2
        return d
    return exec


def cal_time(func):
    def exec(*a):
        begin = time.time()
        d= func(*a)
        t = time.time() - begin
        print(str(t))
        return d
    return exec


def param_deco(param):
    def deco(func):
        def exec(*args):
            print(param)
            return func(*args)

        return exec
    return deco

@param_deco(param='My pr')
def run(number):
    time.sleep(1)

    return {'num': number, 'exec_time': 0}

a = run(2)
print(a)