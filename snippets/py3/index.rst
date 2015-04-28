.. Unicode Solutions - Py3 documentation master file, created by
   sphinx-quickstart on Mon Apr 27 21:42:24 2015.

Unicode Solutions - Py3
=======================

.. doctest::

    >>> text = 'café'
    >>> len(text)
    4
    >>> list(text)
    ['c', 'a', 'f', 'é']
    >>> print(text)
    café
    >>> octets = text.encode('utf8')
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
