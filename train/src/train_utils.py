#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Feature():
    def __init__(self, feature):
        """素性"""
        self.cur_syllable = feature[0]
        self.syllables = feature[1]
        self.ngram_syllables = feature[2]
        self.uni_gram_syllable_kinds = feature[3]
        self.bi_gram_syllable_kinds = feature[4]

    def get_cur_syllable(self):
        return self.cur_syllable

    def get_features(self):
        # 素性を取得する
        all_features = []
        all_features.extend(self.syllables)
        all_features.extend(self.ngram_syllables)
        all_features.extend(self.uni_gram_syllable_kinds)
        all_features.extend(self.bi_gram_syllable_kinds)
        return all_features


def get_feature(cur_keyword, index, syllables, window_size):
    """素性を取得"""
    # print cur_keyword.encode('utf-8'), index, syllables, len(syllables)
    target_syllable = get_window_syllables(syllables, index, window_size)

    # 素性取得のためのとbigram
    bi_gram = list2ngram(target_syllable, 2)

    feature = (
        cur_keyword, # 対象とする音節
        target_syllable, # 窓幅分の音節
        ngram2feature_form(bi_gram),
        get_syllable_type_feature(target_syllable),
        get_syllable_type_feature(bi_gram),
    )
    return Feature(feature)

def get_window_syllables(syllables, index, window_size):
    """指定された音節の前後窓幅分の音節を取得"""
    if index < window_size:
        return syllables[0:index+window_size+1]
    else:
        return syllables[index-window_size:index+window_size+1]

def get_syllable_type_feature(syllable_ngrams):
    """音節の種類素性を取得"""
    syllable_type_stack = []
    for syllable_ngram in syllable_ngrams:
        syllable_type = ''.join([syllable2type(syllable) for syllable in syllable_ngram])
        syllable_type_stack.append(syllable_type)

    return list(set(syllable_type_stack))

def syllable2type(syllable):
    """入力した音節に対して、音節の種類を返す"""
    # 音節が数値の場合はN
    if syllable.isdigit():
        return u'N'
    # 音節が大文字から始まる場合
    elif syllable[0].isupper():
        return u'U'
    # 音節が小文字から始まる場合
    elif syllable[0].islower():
        return u'L'
    # それ以外の場合（記号）
    else:
        return u'O'

def list2ngram(uni, n=1):
    """リストからn-gramを生成する"""
    ngram_result = []
    loop = 0
    while loop + n <= len(uni):
        ngram_result.append(uni[loop:loop + n])
        loop += 1
    return ngram_result

def ngram2feature_form(ngrams):
    """ngram素性を素性のフォーマットへ変換"""
    return [' '.join(ngram) for ngram in ngrams]
