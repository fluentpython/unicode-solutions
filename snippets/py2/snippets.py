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

"""

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

