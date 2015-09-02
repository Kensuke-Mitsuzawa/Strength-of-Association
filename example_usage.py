#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
from SoA.SoA import SoaClass

def example_usage():
    input_dict = {
        "label_a": [
            ["I", "aa", "aa", "aa", "aa", "aa"],
            ["bb", "aa", "aa", "aa", "aa", "aa"],
            ["I", "aa", "hero", "some", "ok", "aa"]
        ],
        "label_b": [
            ["bb", "bb", "bb"],
            ["bb", "bb", "bb"],
            ["hero", "ok", "bb"],
            ["hero", "cc", "bb"],
        ],
        "label_c": [
            ["cc", "cc", "cc"],
            ["cc", "cc", "bb"],
            ["xx", "xx", "cc"],
            ["aa", "xx", "cc"],
        ]
    }
    # multi thread
    n_thread = 5
    soa_obj = SoaClass(labeled_corpus=input_dict, n_thread=n_thread)
    assert isinstance(soa_obj, SoaClass)
    soa_score = soa_obj.calc_soa(is_zero=False)
    print soa_score

    # single thread
    soa_obj_single = SoaClass(labeled_corpus=input_dict)
    assert isinstance(soa_obj, SoaClass)
    soa_score = soa_obj.calc_soa(is_zero=False)



if __name__=='__main__':
    import time
    start = time.time()
    example_usage()

    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"