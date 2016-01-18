#!/usr/bin/env python
# -*- coding: utf-8 -*-

def load_syllable_map(filename):
    return dict(
        [reversed(line.rstrip().decode('utf-8').split(u'\t'))
         for line in open(filename, 'r')]
    )

def load_syllable_class_map(filename):
    return dict(
        [line.rstrip().decode('utf-8').split(u'\t')
         for line in open(filename, 'r')]
    )

