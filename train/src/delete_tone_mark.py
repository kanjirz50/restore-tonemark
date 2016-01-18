#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from viet_preprocessing.vietprepro import BoDau

def no_tone_open(filename):
    result = []
    for line in open(filename, 'r'):
        sentence = line.rstrip().decode('utf-8')
        no_tone_mark_sentence = delete_tonemark_from_sentence(sentence)
        result.append(no_tone_mark_sentence.lower().encode('utf-8'))
    return result

def delete_tonemark_from_sentence(sentence):
    return u''.join([BoDau(a) for a in sentence])

