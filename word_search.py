#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Word-Guesser for the Wordle game.

Made by rzx."""

from json import loads as _l
from os.path import dirname as _d, abspath as _a
from re import match as _m
from json.decoder import JSONDecodeError as _JsonDecode


__all__ = ['make_re', 'make_not_re', 'search_word']
__author__ = 'rxzyx | rzx.'

__license__ = 'MIT'
__maintainer__ = 'rxzyx | rzx.'


print("[+] Made by rxzyx on GitHub.")

alphabet_lowercase = [chr(i) for i in range(97, 123)]
alphabet_uppercase = [chr(i) for i in range(65, 91)]


def make_re(uncomplete_word: str):
    result = ''
    for i in uncomplete_word:
        if not i == '?':
            if i not in alphabet_lowercase and \
                    i not in alphabet_uppercase:
                print("[!] Unknown Character %s, Skipping..." % i)
            else:
                result += i
        else:
            result += '[a-z]'
    return result


def make_not_re(uncomplete_word: str):
    result = ''
    for i in uncomplete_word:
        if not i == '?':
            if i not in alphabet_lowercase and \
                    i not in alphabet_uppercase:
                print("[!] Unknown Character %s, Skipping..." % i)
            else:
                result += '[^%s +-]' % i
        else:
            result += '[a-z]'
    return result


def search_word(word: str, contains=None, does_not_contain=None, not_in_pos=None, extra=None):
    if not word:
        raise ValueError("Word input cannot be None")
    final = []
    try:
        with open('%s/dictionary.json' % _d(_a(__file__))) as file:
            file_content = _l(file.read())
    except (FileNotFoundError, _JsonDecode) as _e:
        print(f"[!] A File Error has occurred! {_e}")
        raise _e
    print("[+] Dictionary Info Found")
    print("[+] Standby For Results!")
    for i in range(len(file_content)):
        file_word = file_content[i]
        if len(file_word) == len(word) and \
                _m(make_re(word), file_word):
            final.append(file_word)
    if contains:
        print("[+] Running Configuration Setting 'Contains'")
        containing_final = []
        for c in final:
            tries = 1
            for i in contains:
                if tries == len(contains):
                    if contains[-1] in c:
                        containing_final.append(c)
                    tries = 1
                if i in c:
                    tries += 1
        print("[+] Decreased Result Amount From %i -> %i" % (
            len(final), len(containing_final)))
        final = containing_final
    if not does_not_contain:
        print("[+] Returned %i Results from Normal Mode!" % len(final))
    else:
        new_final = []
        for i in final:
            tries = 1
            for c in does_not_contain:
                if tries == len(does_not_contain):
                    if not does_not_contain[-1] in i:
                        new_final.append(i)
                    tries = 1
                if not (c in i):
                    tries += 1
        final = new_final
        print("[+] Returned %i Results from Not-Contains Mode!" % len(final))
    if extra:
        extra_count = []
        for i in final:
            for c in extra:
                if i.count(c) > 1:
                    extra_count.append(i)
        final = extra_count
        print("[+] Returned %i Results from Extra Mode!" % len(final))
    if not_in_pos:
        pos_count = []
        for i in final:
            if _m(make_not_re(not_in_pos), i):
                pos_count.append(i)
        final = pos_count
        print("[+] Returned %i Results from Not-In-Pos Mode!" % len(final))
    print("[+] Full Stage Process is Finished. Returning %i Results..." % len(
        final
    ))
    return final


if __name__ == '__main__':
    print("[+] Click Enter without inputing anything to skip!")
    word = input("- Word (? for unkown letter): ")
    contains = input("- Letters that are in the word but have an unkown position: ")
    does_not_contain = input("- Letters that are not in the word: ")
    not_in_pos = input("- Letters that are not in the position (? for all other letters): ")
    extra = input("- Letters that are in the word more than once:  ")
    print(search_word(word, contains, does_not_contain, not_in_pos, extra))
