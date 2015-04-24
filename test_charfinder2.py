import pytest

from charfinder2 import *

G_CLEF = '𝄞'  # \u1d11e : MUSICAL SYMBOL G CLEF

def test_parse_name_query():
    assert parse_query('sun') == 'sun'


def test_parse_char_query_non_ascii():
    assert parse_query('ç') == '?ç'
    assert parse_query('ação') == '?ação'
    assert parse_query('ação?') == '?ação'
    assert parse_query('ação??') == '?ação?'


def test_parse_char_query_ASCII():
    assert parse_query('?') == '??'
    assert parse_query('0123?') == '?0123'
    assert parse_query('? sun') == '? sun'
    assert parse_query('??') == '??'
    assert parse_query('?? sun') == '?? sun'
    assert parse_query('?0123?') == '?0123?'


def test_chars_iter():
    assert list(chars_iter('01234')) == list('01234')
    assert list(chars_iter('01234', 3)) == list('34')
    assert list(chars_iter('01234', 1, 4)) == list('123')


def test_describe():
    assert describe('A') == CharDescription(
                                'U+0041', 'LATIN CAPITAL LETTER A')
    assert describe('ª') == CharDescription(
                                'U+00AA', 'FEMININE ORDINAL INDICATOR')


def test_describe_str():
    assert describe_str('A') == 'U+0041 \tA\tLATIN CAPITAL LETTER A'
    assert describe_str('ª') == 'U+00AA \tª\tFEMININE ORDINAL INDICATOR'
    assert describe_str(G_CLEF) == 'U+1D11E\t𝄞\tMUSICAL SYMBOL G CLEF'
