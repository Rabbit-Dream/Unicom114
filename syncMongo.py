# 将mongodb中的数据同步到Es中
from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
import datetime

# 一次同步的数据量，批量同步
syncCountPer = 100000

# Es 数据库地址
es_url = 'http://127.0.0.1:9200/'

# mongodb 数据库地址
mongo_url='127.0.0.1:27017'

# mongod 需要同步的数据库名
DB = 'Unicom'
# mongod 需要同步的表名
COLLECTION = 'searchdb6'

count = 0

if __name__ == '__main__':
    es = Elasticsearch(es_url)
    client = MongoClient(mongo_url)
    db_mongo = client[DB]
    syncDataLst = []
    exclude = ['_id']
    mongoRecordRes = db_mongo[COLLECTION].find({},{x: 0 for x in exclude})
    for record in mongoRecordRes:
        count += 1

        syncDataLst.append({
            "_index": DB.lower(),      
            "_type": COLLECTION,       
            "_id": record['unitId'],
            "_source": record,
        })

        if len(syncDataLst) == syncCountPer:
            # 批量同步到Es中，就是发送http请求一样，数据量越大request_timeout越要拉长
            helpers.bulk(es, 
                         syncDataLst, 
                         request_timeout = 180)
            # 清空数据列表
            syncDataLst[:]=[]
            print(f"Had sync {count} records at {datetime.datetime.now()}")
    # 同步剩余部分
    if syncDataLst:
        helpers.bulk(es, 
                     syncDataLst, 
                     request_timeout = 180)
        print(f"Had sync {count} records rest at {datetime.datetime.now()}")
