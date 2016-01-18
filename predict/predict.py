#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ConfigParser
from src.liblinear.liblinear import *
from src.liblinear.liblinearutil import *
from src.make_feature import *
from src.train_utils import *


def main():
    inifile = ConfigParser.SafeConfigParser()
    inifile.read("./config.ini")
    model_dir = inifile.get("settings", "model_dir")
    file_path = set([p.split('.')[0] for p in os.listdir(model_dir)])
    window_size = 2
    # test_sentence = 'Toi la sinh vien'
    for line in sys.stdin:
        syllables = line.rstrip().decode('utf-8').split(u' ')

        predicted_syllables = [tone_predict(i, syllables, model_dir, file_path, window_size) for i in xrange(len(syllables))]
        print u' '.join(predicted_syllables).encode('utf-8')

def tone_predict(i, syllables, model_dir, file_path, window_size):
    target_syllable = syllables[i]
    target_syllable_lower = syllables[i].lower()

    if target_syllable_lower not in file_path:
        return u'[{}]'.format(target_syllable)

    model_path = os.path.join(model_dir, '{}.model'.format(target_syllable_lower))

    # 素性の作成
    features = get_feature(target_syllable, i, syllables, window_size)
    mapped_feature = feature_mapping(model_dir, target_syllable_lower, features)

    # 推定
    # モデルの読み込み
    model = load_model(model_path)
    p_label, p_acc, p_val = predict([1], [mapped_feature], model, '-q')

    # 推定したクラス番号を音節へと復元する
    mapped_class = class_mapping(model_dir, target_syllable_lower, p_label[0])

    return mapped_class

if __name__ == "__main__":
    main()
