#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
コーパスからユニークな音節の辞書を作成する。
なお音節はすべて小文字とする。
"""

__author__ = "takahashi <takahashi@jnlp.org>"
__version__ = "1"
__date__ = "dd m yyyy"

import sys
from collections import defaultdict
from viet_preprocessing.vietprepro import delete_tonemark

def make_syllable(filename):
    # ユニークな音節を保持するための辞書
    syllable_dic = defaultdict(int)

    # コーパスから読み込み
    for line in open(filename, 'r'):
        sentence = line.rstrip().decode('utf-8')
        syllables = sentence.split(u' ')

        for syllable in syllables:
            # 声調記号を削除する
            no_tonemark_syllable = delete_tonemark(syllable)

            # 声調記号を削除して、アルファベットのみであれば追加
            if no_tonemark_syllable.isalpha():
                syllable_dic[no_tonemark_syllable.lower()] += 1

            # アルファベットから始まり、記号で終わる文字列に対して処理を行う
            elif no_tonemark_syllable[0].isalpha() and not no_tonemark_syllable[-1].isalpha():
                # . , ! ?が文字列の末端にある場合に削除し、小文字にする。
                syllable = no_tonemark_syllable.rstrip('.').rstrip(',').rstrip('!').rstrip('?').lower()
                # 上記処理のあと、アルファベットのみで構成されていれば、追加する。
                if syllable.isalpha():
                    syllable_dic[syllable] += 1

    return [k for k, v in sorted(syllable_dic.items())]

if __name__ == "__main__":
    main()
