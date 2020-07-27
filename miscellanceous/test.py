import time
from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=1)


def new_thread(func):
    def inner(*args, **kwargs):
        thread = pool.apply_async(func, args, kwargs)
        return thread.get()

    return inner


@new_thread
def run(x):
    for i in range(x):
        print('x-{}'.format(i))
        time.sleep(1)
    return -1


if __name__ == '__main__':
    a = run(4)
    for i in range(6):
        print('y-{}'.format(i))
        time.sleep(1)
    print(a)
