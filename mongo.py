import json
from pymongo import MongoClient


class MongoConn:
    def __init__(self, host, port, user=None, password=None, database=None):
        if user is None and password is None:
            conn_string = 'mongodb://' + host + ':' + port
        else:
            conn_string = 'mongodb://' + user + ':' + password + '@' + host + ':' + port
        if database is not None:
            conn_string += '/' + database
        self.client = MongoClient(conn_string)


def get_mongo_collection(database, collection):
    with open('cfg.json') as cfg:
        config = json.load(cfg)

    mongo_conn = MongoConn(host=config['mongoHost'], port=config['mongoPort'])
    client = mongo_conn.client
    db = client[database]
    return db[collection]


def bulk_update(collection, condition, update, skip=0, limit=1000):
    documents = collection.find(condition, skip=skip, limit=limit)
    if collection.count_documents(condition, skip=skip, limit=limit) > 0:
        bulk = collection.initialize_unordered_bulk_op()
        for doc in documents:
            bulk.find({'unitId': doc['unitId']}).update({'$set': update})
        
        bulk.execute()


def multi_thread_update(collection, condition, operation, batch_size, thread_num=50, join=True):
    from threading import Thread

    def _update(docs, condition, operation):
        pass
    
    docs_count = collection.count_documents(condition)
    docs_count = docs_count \
                if docs_count % batch_size == 0 \
                else (docs_count // batch_size + 1) * batch_size

    docs = (
        collection.find(
            condition,
            skip=skip,
            limit=batch_size,
            no_cursor_timeout=True
        ).batch_size(10000)
        for skip in range(0, docs_count, batch_size)
    )

    tasks = [Thread(target=_update, args=(doc, condition, operation)) for doc in docs]

    for task in tasks:
        task.start()

    if join:
        for task in tasks:
            task.join()



if __name__ == '__main__':
    pass
