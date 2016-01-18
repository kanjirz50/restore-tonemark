#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LIBLINEAR用に数字に変換する。
"""
from collections import defaultdict

class PrintFeatures():
    def __init__(self):
        """素性を書き出す際に必要となる変数"""
        # クラス番号と素性番号
        self.class_num = 1
        self.feature_num = 1

        # 音節に対するクラス番号、素性番号を保持する
        self.class_dict = {}
        self.feature_dict = {}

        # LIBLINEAR用
        self.class_list = []
        self.feature_list = []

    def add_liblinear_format(self, feature):
        """入力した素性をLIBLINEAR形式で得る"""
        class_number = self.get_class_num(feature.cur_syllable)
        features = self.get_feature_nums(feature.get_features())

        features = self.feature_nums2liblinear_format(features)

        # 追加
        self.class_list.append(float(class_number))
        self.feature_list.append(features)

    def get_class_num(self, cur_syllable):
        # 音節に対するクラス番号を取得する
        if cur_syllable not in self.class_dict:
            self.class_dict[cur_syllable] = self.class_num
            self.class_num += 1

        return self.class_dict.get(cur_syllable)

    def get_feature_nums(self, features):
        # 素性に対する番号を取得する
        feature_nums = []
        for feature in features:
            if feature not in self.feature_dict:
                self.feature_dict[feature] = self.feature_num
                self.feature_num += 1

            feature_nums.append(self.feature_dict.get(feature))
        # 素性番号は行内で昇順である必用があるため昇順に並び替え
        return sorted(feature_nums)

    def feature_nums2liblinear_format(self, feature_nums):
        # 素性番号をLIBLINEAR形式のフォーマットへ変換する
        d = defaultdict(int)
        for feature_num in feature_nums:
            d[feature_num] += 1

        return dict([(int(feature_num), float(freq)) for feature_num, freq in sorted(d.items())])

    def save_class_dict(self, save_path):
        """クラス番号辞書を保存"""
        with open(save_path, 'w') as fout:
            lines = [u'{}\t{}'.format(k, v) for k, v in sorted(self.class_dict.items(), key=lambda x:x[1])]
            fout.write(u'\n'.join(lines).encode('utf-8'))


    def save_feature_dict(self, save_path):
        """素性辞書を保存"""
        with open(save_path, 'w') as fout:
            lines = [u'{}\t{}'.format(k, v) for k, v in sorted(self.feature_dict.items(), key=lambda x:x[1])]
            fout.write(u'\n'.join(lines).encode('utf-8'))

    def print_features(self):
        for c, f in zip(self.class_list, self.feature_list):
            f = [u'{}:{}'.format(k,v) for k, v in sorted(f.items())]
            print u'{} {}'.format(c, u' '.join(f)).encode('utf-8')
