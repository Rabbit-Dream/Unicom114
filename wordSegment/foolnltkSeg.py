import fool


def get_segmentation(line, print_=False):
    '''
    获取分词文本
    '''
    load_dict('F:\\114代码\\i\\wordSegment\\kw.txt')
    res = fool.cut(line.strip())
    if print_:
        print(','.join(res[0]))
    return res[0]


def get_keywords(line):
    '''
    获取关键词
    '''
    fool.analysis
    load_dict('F:\\114代码\\i\\wordSegment\\kw.txt')
    word, keywords = fool.analysis(line)
    return [keyword[3] for keyword in keywords[0]]


def load_dict(path):
    fool.load_userdict(path)


