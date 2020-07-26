from pymongo import MongoClient

mongo_client = MongoClient('localhost:27017',
                           username='chatt',
                           password='chattgroup',
                           # authSource='chatt-store',
                           # authMechanism='SCRAM-SHA-256',
                           )
db = mongo_client['chatt-store']
col = db['sheets']
a = col.find_one({'sheet_id': '1GhaecQN90w-XOv2pt4IUAl-Q40OasDtP5WLNV2LPm6o'})

print()