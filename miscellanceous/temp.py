import sys


def is_email(emai):
    return '@' in emai


def is_lock(lock):
    return lock in ['lock', 'unlock']


if __name__ == '__main__':
    args = sys.argv[1:]
    email = None
    lock=None
    for a in args:
        if is_email(a):
            email = a
            continue
        if is_lock(a):
            lock = a

    if email is None:
        print('Missing email')
    if lock is None:
        print('Missing lock')
