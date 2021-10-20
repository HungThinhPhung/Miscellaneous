import time

from progress.bar import Bar


def processing_bar():
    bar = Bar('Processing', max=20)
    for i in range(20):
        # Do some work
        time.sleep(0.2)
        bar.next()
    bar.finish()


def charging_bar():
    with Bar('ChargingBar', max=20) as bar:
        for i in range(20):
            # Do some work
            time.sleep(0.2)
            bar.next()


charging_bar()
