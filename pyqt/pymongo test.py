from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://***REMOVED-SECRET***/?retryWrites=true&w=majority")

db = client['test']

for d, cnt in zip(db['sensors'].find(), range(10)):
    print(d['pm1'], d['pm2'], d['pm10'])
    # print(d)
