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



