# What's this？

This is simple package of SoA(Strength of Association).

With SoA, you can get (label, word, Association_score).

SoA formula is following Mohammad Saif M, Kiritchenko Svetlana, "Using Hashtags to Capture Fine Emotion Categories from Tweets", 2013


# Setting up

This library is confirmed to work under python 2.7.3

This library has no dependencies.

```
[sudo] python setup.py install
```

# Usage

## input data

input data must be dict structure.

Key is label name. Value is 2-dimension list. like `[ ["word"] ]`

For example, 

```
{
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
```
    
## how to use

### initialize

`n_thread` is optional argument. If you don't specify, SoA is calculated with single thread.

```
n_thread = 5
soa_obj = SoaClass(labeled_corpus=input_dict, n_thread=n_thread)
```


### calculate

`calc_soa` method returns SoA calculated score.

`is_Zero` is optional. Default is `False`

If you give `is_Zero==True`, you can get all word including score is Zero.
 

```
soa_score = soa_obj.calc_soa(is_zero=True)
```


### output format

output data is dict type. Key is label name and Value is list.

`{'word': unicode or string, 'score': float}` inside value list.


```
{'label_a': [
{'score': 5.0, 'word': 'aa'}, {'score': 1.4150374992788437, 'word': 'ok'}, {'score': 0.4150374992788437, 'word': 'hero'}, {'score': -1.7548875021634687, 'word': 'bb'}
], 
'label_b': [
{'score': 2.807354922057604, 'word': 'bb'}, {'score': 1.8073549220576042, 'word': 'hero'}, {'score': 0.8073549220576041, 'word': 'ok'}, {'score': -2.0, 'word': 'cc'}
], 
'label_c': [
{'score': 3.6147098441152083, 'word': 'cc'}, {'score': -2.3625700793847084, 'word': 'bb'}, {'score': -2.777607578663552, 'word': 'aa'}
]}
```

