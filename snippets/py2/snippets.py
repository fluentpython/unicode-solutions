# coding: utf-8

ur"""

Text versus bytes:

>>> text = u'café'
>>> type(text)
<type 'unicode'>
>>> len(text)
4
>>> list(text)
[u'c', u'a', u'f', u'\xe9']
>>> print(text)
café
>>> octets = text.encode('utf8')
>>> type(octets)
<type 'str'>
>>> octets
'caf\xc3\xa9'
>>> len(octets)
5
>>> list(octets)
['c', 'a', 'f', '\xc3', '\xa9']
>>> print(octets)
café
>>> octets.decode('utf8')
u'caf\xe9'
>>> str is bytes
True


The ``bytearray`` type:

>>> octets = bytes('café')
>>> octets
'caf\xc3\xa9'
>>> octets[0]
'c'
>>> octets[:1]
'c'
>>> octet_arr = bytearray(octets)
>>> octet_arr
bytearray(b'caf\xc3\xa9')
>>> octet_arr[-1:]
bytearray(b'\xa9')


Essential codecs:

>>> for codec in ['latin_1', 'utf_8', 'utf_16']:
...     print '{:8} {!r}'.format(codec, u'El Niño'.encode(codec))
...
latin_1  'El Ni\xf1o'
utf_8    'El Ni\xc3\xb1o'
utf_16   '\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'


Encoding success and error handling:

>>> city = u'São Paulo'
>>> city.encode('utf_8')
'S\xc3\xa3o Paulo'
>>> city.encode('utf_16')
'\xff\xfeS\x00\xe3\x00o\x00 \x00P\x00a\x00u\x00l\x00o\x00'
>>> city.encode('iso8859_1')
'S\xe3o Paulo'
>>> city.encode('cp437')
Traceback (most recent call last):
  ...
UnicodeEncodeError: 'charmap' codec can't encode character u'\xe3' in position 1: character maps to <undefined>
>>> city.encode('cp437', errors='ignore')
'So Paulo'
>>> city.encode('cp437', errors='replace')
'S?o Paulo'
>>> city.encode('cp437', errors='xmlcharrefreplace')
'S&#227;o Paulo'


Coping with ``UnicodeDecodeError``:

>>> octets = b'Montr\xe9al'
>>> octets.decode('cp1252')
u'Montr\xe9al'
>>> print _
Montréal
>>> octets.decode('iso8859_7') == u'Montr\u03b9al'
True
>>> print octets.decode('iso8859_7')
Montrιal
>>> octets.decode('koi8_r') == u'Montr\u0418al'
True
>>> print octets.decode('koi8_r')
MontrИal
>>> octets.decode('utf_8')
Traceback (most recent call last):
  ...
UnicodeDecodeError: 'utf8' codec can't decode byte 0xe9 in position 5: invalid continuation byte
>>> octets.decode('utf_8', errors='replace') == u'Montr\ufffdal'
True
>>> print octets.decode('utf_8', errors='replace')
Montr�al


Moldy sandwich -- using octets as text:

>>> with open('cafe.txt', 'w') as fp:
...     fp.write('café')
...
>>> with open('cafe.txt', 'r') as fp:
...     octets = fp.read()
...
>>> octets
'caf\xc3\xa9'


Unicode sandwich -- encode text only on output:

>>> import io
>>> with io.open('cafe.txt', 'w', encoding='utf_8') as fp:
...     write_count = fp.write(u'café')
...
>>> write_count
4L
>>> with io.open('cafe.txt', 'r', encoding='utf_8') as fp:
...     text = fp.read()
...
>>> text
u'caf\xe9'


``io.open`` also works with binary files:

>>> with io.open('cafe.txt', 'wb') as fp:
...     write_count = fp.write('café')
...
>>> write_count
5L
>>> with io.open('cafe.txt', 'rb') as fp:
...     octets = fp.read()
...
>>> octets
'caf\xc3\xa9'


Normalizing Unicode for saner comparisons

>>> s1 = u'café'
>>> s2 = u'cafe\u0301'
>>> import unicodedata
>>> unicodedata.name(s2[-1])
'COMBINING ACUTE ACCENT'
>>> print(s1, s2)  # doctest:+SKIP
café café
>>> len(s1), len(s2)
(4, 5)
>>> list(s1)
[u'c', u'a', u'f', u'\xe9']
>>> list(s2) == [u'c', u'a', u'f', u'e', u'\u0301']
True
>>> s1 == s2
False


Utility functions for normalized text matching

>>> from unicodedata import normalize
>>> def nfc_equal(str1, str2):
...     return normalize('NFC', str1) == normalize('NFC', str2)
...
>>> s1 = u'café'
>>> s2 = u'cafe\u0301'
>>> s1 == s2
False
>>> nfc_equal(s1, s2)
True


The ``unicode`` class has no ``casefold`` method.


Sorting Unicode text does not work as expected:

>>> fruits = [u'caju', u'atemoia', u'cajá', u'açaí', u'acerola']
>>> for fruit in sorted(fruits):
...     print fruit
...
acerola
atemoia
açaí
caju
cajá


Sorting Unicode text requires ``locale`` settings:

>>> import locale
>>> locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
'pt_BR.UTF-8'
>>> fruits = [u'caju', u'atemoia', u'cajá', u'açaí', u'acerola']
>>> sorted_fruits = sorted(fruits, key=locale.strxfrm)
>>> for fruit in sorted_fruits:  # doctest:+SKIP
...     print fruit
...
açaí
acerola
atemoia
cajá
caju


Locale-independent sorting with UCA, the Unicode Collation Algorithm:

>>> import pyuca
>>> coll = pyuca.Collator()
>>> fruits = [u'caju', u'atemoia', u'cajá', u'açaí', u'acerola']
>>> sorted_fruits = sorted(fruits, key=coll.sort_key)  # doctest:+SKIP
>>> for fruit in sorted_fruits:  # doctest:+SKIP
...     print fruit
...
açaí
acerola
atemoia
cajá
caju



"""

#########################################################

HEADER = u"""
Unicode Solutions - Py2
=======================
"""

import io
import sys

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("UTF-8") # DON'T DO THIS. READ THE ABOVE @UndefinedVariable
    import doctest
    res = doctest.testmod()
    if res.failed == 0:
        with io.open('index.rst', 'wt', encoding='utf-8') as fp:
            fp.write(HEADER)
            fp.write(__doc__)
    sys.exit(res.failed)

