#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
学習を行う
"""

import sys
import ConfigParser
from itertools import izip
from src.train_utils import *
from src.train_format import *
from src.liblinear.liblinear import *
from src.liblinear.liblinearutil import *
from src.make_syllable import *
from src.delete_tone_mark import *


def main():
    inifile = ConfigParser.SafeConfigParser()
    inifile.read("./config.ini")

    path1 = inifile.get("settings", "path1")
    path2 = inifile.get("settings", "path2")
    preserve_dir_path = inifile.get("settings", "preserve_dir_path")
    window_size = int(inifile.get("settings", "window_size"))

    # 学習対象の音節リストを読み込み
    print 'loading syllable list'
    syllable_list = make_syllable(path1)

    print 'pick feature and training'
    cannot_output = 0
    for target_syllable in syllable_list:
        print 'target:{}'.format(target_syllable),
        pf = PrintFeatures()
        for syllable_indexs, sentence in iter_pick_sentence(target_syllable, path1, path2):
            # class_id, feature, feature_idを作成しながら素性を作成
            for index, syllable in syllable_indexs:
                f = get_feature(syllable, index, sentence, window_size)
                pf.add_liblinear_format(f)

        # 学習を行う。
        print '\ttraining',
        prob = problem(pf.class_list, pf.feature_list)
        m = train(prob, '-q')

        # class_id, feature, modelを保存する。
        print '\twriting'
        try:
            target_syllable = target_syllable.encode('utf-8')
            pf.save_class_dict("{}/{}.class_map".format(preserve_dir_path, target_syllable))
            pf.save_feature_dict("{}/{}.feature_map".format(preserve_dir_path, target_syllable))
            save_model("{}/{}.model".format(preserve_dir_path, target_syllable), m)
        except:
            cannot_output += 1
            continue
    print "Can't train:{}".format(cannot_output)


def iter_pick_sentence(keyword, path1, path2):
    """対象の音節が含まれる文をyieldする"""
    for sentence, no_tonemark_sentence in izip(open(path1, 'r'), open(path2, 'r')):
        no_tonemark_lower_syllables = no_tonemark_sentence.rstrip().decode('utf-8').split(u' ')

        if keyword in no_tonemark_lower_syllables:
            sentence = sentence.rstrip().decode('utf-8').split(u' ')
            # 音節とそのインデックス
            syllable_index = [(i, sentence[i]) for i, w in enumerate(no_tonemark_lower_syllables) if w == keyword]

            yield syllable_index, no_tonemark_lower_syllables


if __name__ == "__main__":
    main()
