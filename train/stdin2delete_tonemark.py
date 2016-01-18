#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from src.viet_preprocessing.vietprepro import BoDau

def main():
    for line in sys.stdin:
        sentence = line.rstrip().decode('utf-8')
        no_tone_mark_sentence = u''.join([BoDau(a) for a in sentence])
        print no_tone_mark_sentence.lower().encode('utf-8')

if __name__ == "__main__":
    main()
