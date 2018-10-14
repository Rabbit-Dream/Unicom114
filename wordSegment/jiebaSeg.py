import jieba
from jieba import analyse
import jieba.posseg as pseg


def use_parallel(n=4):
    # 并行计算
    try:
        jieba.enable_parallel(n)
    except NotImplementedError as err:
        print(err)


def get_segmentation(line, print_=False):
    '''
    获取分词文本
    '''
    # analyse.set_idf_path('F:\\114代码\\i\\wordSegment\\kw.txt')
    load_dict('F:\\114代码\\i\\wordSegment\\kw.txt')
    res = list(jieba.cut(line.strip()))
    # res = analyse.tfidf(line.strip())
    print(res)
    return res
    if print_:
        print(','.join(list(res)))
    return ' '.join(list(res))


def get_keywords(line):
    '''
    获取句子关键词
    '''
    t = analyse.TFIDF(idf_path='F:\\114代码\\i\\wordSegment\\kw.txt')
    t.set_stop_words('F:\\114代码\\i\\wordSegment\\stop.txt')
    res = t.extract_tags(line.strip(),topK=2)
    print(res)
    return res
    # analyse.set_idf_path('F:\\114代码\\i\\wordSegment\\kw.txt')
    # analyse.set_stop_words('F:\\114代码\\i\\wordSegment\\kw.txt')
    # return analyse.textrank(line)


def get_posseg(line):
    return ' '.join(f'{word}/{flag}' for word, flag in pseg.cut(line, HMM=False))


def load_dict(path):
    jieba.load_userdict(path)
    # with open(path) as file:
    #     jieba.load_userdict(file)





if __name__ == '__main__':
    pass