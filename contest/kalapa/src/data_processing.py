import pandas as pd

train_data = pd.read_csv('/home/phthinh/Projects/PycharmProjects/test_only/contest/kalapa/data/train.csv', low_memory=False)
test_data = pd.read_csv('/home/phthinh/Projects/PycharmProjects/test_only/contest/kalapa/data/test.csv', low_memory=False)
for i in test_data:
    a = list(test_data[i].unique())
    print('{}: {}'.format(i, a))
print()
