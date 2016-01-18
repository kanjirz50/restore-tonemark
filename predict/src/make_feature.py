#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from predict_util import *
from collections import defaultdict

def feature_mapping(model_dir, target_syllable_lower, features):
    feature_map_path = os.path.join(model_dir, '{}.feature_map'.format(target_syllable_lower))

    # 音節に対するクラスマッピングファイルを読み込み
    syllable_feature_map = load_syllable_class_map(feature_map_path)

    mapped = defaultdict(int)
    for feature in features.get_features():
        ad = syllable_feature_map.get(feature)
        if ad != None:
            mapped[int(ad)] += 1
    return mapped

def class_mapping(model_dir, target_syllable_lower, p_label):
    syllable_map_path = os.path.join(model_dir, '{}.class_map'.format(target_syllable_lower))
    # 音節に対するマッピングファイルを読み込み
    syllable_class_map = load_syllable_map(syllable_map_path)

    s = syllable_class_map.get(unicode(int(p_label)))

    if s != None:
        return s
    else:
        return 1
