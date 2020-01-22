import pandas

def load_data(file='data.csv'):
    return pandas.read_csv(file)

def check_data(data):
    no_id = data.loc[:, 'PhanKhuc': 'TieuThu']
    train = no_id.loc[:14, :]
    test = no_id.loc[15:, :]
    train_records = train.shape[0]
    fields = train.shape[1] - 1
    test_records = test.shape[0]
    for i in range(17):
        for j in range(i+1, 18):
            first = no_id.iloc[i, 0:fields]
            second = no_id.iloc[j, 0:fields]
            count = 0
            for k in range(fields):
                if first[k] == second[k]:
                    count += 1
            if count == 5:
                print(i)
                print(no_id.iloc[i, 0:fields])
                print(j)
                print(no_id.iloc[j, 0:fields])
                print()
data = load_data()
check_data(data)