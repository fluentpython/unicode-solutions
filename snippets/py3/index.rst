.. Unicode Solutions - Py3 documentation master file, created by
   sphinx-quickstart on Mon Apr 27 21:42:24 2015.

Unicode Solutions - Py3
=======================

Text versus bytes:

>>> text = 'café'
>>> type(text)
<class 'str'>
>>> len(text)
4
>>> list(text)
['c', 'a', 'f', 'é']
>>> print(text)
café
>>> octets = text.encode('utf8')
>>> type(octets)
<class 'bytes'>
>>> octets
b'caf\xc3\xa9'
>>> len(octets)
5
>>> list(octets)
[99, 97, 102, 195, 169]
>>> print(octets)
b'caf\xc3\xa9'
>>> octets.decode('utf8')
'café'
>>> str is bytes
False


The ``bytearray`` type:

>>> octets = bytes('café', encoding='utf_8')
>>> octets
b'caf\xc3\xa9'
>>> octets[0]
99
>>> octets[:1]
b'c'
>>> octet_arr = bytearray(octets)
>>> octet_arr
bytearray(b'caf\xc3\xa9')
>>> octet_arr[-1:]
bytearray(b'\xa9')


Essential codecs:

>>> for codec in ['latin_1', 'utf_8', 'utf_16']:
...     print('{:8} {!r}'.format(codec, u'El Niño'.encode(codec)))
...
latin_1  b'El Ni\xf1o'
utf_8    b'El Ni\xc3\xb1o'
utf_16   b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'


Encoding success and error handling:

>>> city = 'São Paulo'
>>> city.encode('utf_8')
b'S\xc3\xa3o Paulo'
>>> city.encode('utf_16')
b'\xff\xfeS\x00\xe3\x00o\x00 \x00P\x00a\x00u\x00l\x00o\x00'
>>> city.encode('iso8859_1')
b'S\xe3o Paulo'
>>> city.encode('cp437')
Traceback (most recent call last):
  ...
UnicodeEncodeError: 'charmap' codec can't encode character '\xe3' in position 1: character maps to <undefined>
>>> city.encode('cp437', errors='ignore')
b'So Paulo'
>>> city.encode('cp437', errors='replace')
b'S?o Paulo'
>>> city.encode('cp437', errors='xmlcharrefreplace')
b'S&#227;o Paulo'


Coping with ``UnicodeDecodeError``:

>>> octets = b'Montr\xe9al'
>>> octets.decode('cp1252')
'Montréal'
>>> octets.decode('iso8859_7')
'Montrιal'
>>> octets.decode('koi8_r')
'MontrИal'
>>> octets.decode('utf_8')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 5: invalid continuation byte
>>> octets.decode('utf_8', errors='replace')
'Montr�al'


Unicode sandwich -- encode text only on output:

>>> with open('cafe.txt', 'w', encoding='utf_8') as fp:
...     write_count = fp.write('café')
...
>>> write_count
4
>>> with open('cafe.txt', 'r', encoding='utf_8') as fp:
...     text = fp.read()
...
>>> text
'café'


Normalizing Unicode for saner comparisons:

>>> s1 = 'café'
>>> s2 = 'cafe\u0301'
>>> import unicodedata
>>> unicodedata.name(s2[-1])
'COMBINING ACUTE ACCENT'
>>> print(s1, s2)  # doctest:+SKIP
café café
>>> len(s1), len(s2)
(4, 5)
>>> list(s1), list(s2)
(['c', 'a', 'f', 'é'], ['c', 'a', 'f', 'e', '́'])
>>> s1 == s2
False


Utility functions for normalized text matching:

>>> from unicodedata import normalize
>>> def nfc_equal(str1, str2):
...     return normalize('NFC', str1) == normalize('NFC', str2)
...
>>> s1 = 'café'
>>> s2 = 'cafe\u0301'
>>> s1 == s2
False
>>> nfc_equal(s1, s2)
True


Case folding:

>>> def fold_equal(str1, str2):
...     return (normalize('NFC', str1).casefold() ==
...             normalize('NFC', str2).casefold())
...
>>> s3 = 'Straße'
>>> s4 = 'strasse'
>>> s3 == s4
False
>>> nfc_equal(s3, s4)
False
>>> fold_equal(s3, s4)
True
>>> fold_equal(s1, s2)
True
>>> fold_equal('A', 'a')
True


Sorting Unicode text does not work as expected:

>>> fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
>>> sorted(fruits)
['acerola', 'atemoia', 'açaí', 'caju', 'cajá']


Sorting Unicode text requires ``locale`` settings:

>>> import locale
>>> locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
'pt_BR.UTF-8'
>>> fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
>>> sorted_fruits = sorted(fruits, key=locale.strxfrm)
>>> sorted_fruits  # doctest:+SKIP
['açaí', 'acerola', 'atemoia', 'cajá', 'caju']


Locale-independent sorting with UCA, the Unicode Collation Algorithm:

>>> import pyuca
>>> coll = pyuca.Collator()
>>> fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
>>> sorted_fruits = sorted(fruits, key=coll.sort_key)
>>> sorted_fruits
['açaí', 'acerola', 'atemoia', 'cajá', 'caju']


