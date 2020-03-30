from random import randint
import pandas as pd


def random_label():
    rand = randint(1, 10)
    return int(rand <= 7)


data = dict()
data['id'] = list(range(30000, 50000))
data['label'] = [random_label() for x in data['id']]
test_submission = pd.DataFrame(data, dtype='uint16')
test_submission.to_csv('../data/test_submission2.csv', index=False)
print()
