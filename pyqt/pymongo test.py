import os
from pymongo import MongoClient

mongo_url = os.environ.get("MONGODB_URL")
if not mongo_url:
    raise RuntimeError("MONGODB_URL 환경변수를 설정한 뒤 실행하세요.")

client = MongoClient(mongo_url)
db = client['test']

for d, cnt in zip(db['sensors'].find(), range(10)):
    print(d['pm1'], d['pm2'], d['pm10'])
    # print(d)
