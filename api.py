import json
from threading import Thread
import binascii
from elasticsearch import Elasticsearch

from mongo import get_mongo_collection


def _save_query(question,
                jieba_segment,
                fool_segment,
                jieba_keywords,
                fool_keywords,
                fool_search_result,
                jieba_search_result
                ):
    database = 'Unicom'
    collection = 'query'

    document = {
        'question': question, 
        'jiebaSegment': jieba_segment,
        'foolSegment': fool_segment,
        'jiebaKeywords': jieba_keywords,
        'foolKeywords': fool_keywords,
        'foolSearchResult': fool_search_result,
        'jiebaSearchResult': jieba_search_result,
    }



    try:
        conn = get_mongo_collection(database, collection)
        conn.insert_one(document)
    except Exception as err:
        print(err)
        return False, err

    return True


def _search():
    '''
    使用elasticsearch对word进行匹配
    '''

    with open('cfg.json') as cfg:
        config = json.load(cfg)

    es = Elasticsearch(':'.join([config['esHost'], config['esPort']]))
    query = {
        "query": {
            "match": {
                "allName": {
                    "query": "",
                    "fuzziness": "AUTO",
                    "operator":  "and",
                    # "minimum_should_match": "75%",
                }
            }
        },
        'size': 20,
    }

    from wordSegment import foolnltkSeg, jiebaSeg
    

    def __search(line, index='unicom'):

        words = foolnltkSeg.get_keywords(line)
        jieba_words = jiebaSeg.get_keywords(line)
        print(words)
        query['query']['match']['allName']['query'] = ' '.join(words)
        search_result = es.search(index=index, body=query)

        query['query']['match']['allName']['query'] = ' '.join(jieba_words)
        jieba_search_result = es.search(index=index, body=query)

        return search_result, jieba_search_result


    return __search


def format(data):
    return [
        (
            binascii.a2b_hex(result['_source']['phoneNum']).decode(), 
            # result['_source']['address'].replace(',', ' '), 
            result['_source']['allName'].replace(',', ' '), 
        )
        for result in sorted(data['hits']['hits'], key=lambda d: d['_source']['frequency'])
    ]


def assignment(fun):
    global query
    query = fun()

query = None
Thread(target=assignment, args=(_search,)).start()
