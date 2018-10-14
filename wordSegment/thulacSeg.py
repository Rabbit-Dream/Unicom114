import thulac
import numpy as np


def get_segmentation(line, print_=False, filt=False):
    '''
    获取分词文本
    '''
    thu1 = thulac.thulac(seg_only=True, filt=filt)

    def _get_segmentation():

        res = np.array(thu1.cut(line.strip()))
        if print_:
            print(','.join(res[:, 0]))

        return ','.join(res[:, 0])
    
    return _get_segmentation


def get_keywords(line):
    return get_segmentation(line, filt=True)().split(',')