#!/usr/bin/env python3

import sys
import re
import unicodedata
from collections import namedtuple

RE_WORD = re.compile('\w+')

CharDescription = namedtuple('CharDescription', 'code_str name')


def parse_query(query):
    if '?' in query or any(ord(char) > 127 for char in query):
        question_marks = query.count('?')
        if question_marks > 0 and len(query) > 1:
            chars = list(query)
            chars.remove('?')
            query = ''.join(chars)
        return '?' + query
    return query


def describe(char):
    code_str = 'U+{:04X}'.format(ord(char))
    name = unicodedata.name(char)
    return CharDescription(code_str, name)


def describe_str(char):
    return '{1:7}\t{0}\t{2}'.format(char, *describe(char))


def simple_iter(chars, start=0, stop=None):
    return iter(chars[start:stop])


def main(*args):
    query = parse_query(' '.join(args))
    if query.startswith('?'):
        chars_iter = simple_iter(query[1:])
    else:
        raise NotImplementedError()

    for char in chars_iter:
        print(describe_str(char))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(*sys.argv[1:])
    else:
        usage = [('word1 [word2]', 'chars from descriptive words'),
                 ('non-ASCII-chars', 'descriptions for chars'),
                 ('? ASCII-chars', 'descriptions for chars')]
        print('Usage:')
        for form, help in usage:
            print('  {} {:16} # find {}'.format(sys.argv[0], form, help))

