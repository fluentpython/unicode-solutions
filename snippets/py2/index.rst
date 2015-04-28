.. Unicode Solutions - Py2 documentation master file, created by
   sphinx-quickstart on Mon Apr 27 21:40:31 2015.

Unicode Solutions - Py2
=======================

.. doctest::

    >>> text = u'café'
    >>> len(text)
    4
    >>> list(text)
    [u'c', u'a', u'f', u'é']
    >>> print(text)
    café
    >>> octets = text.encode('utf8')
    >>> octets
    'caf\xc3\xa9'
    >>> len(octets)
    5
    >>> list(octets)
    [99, 97, 102, 195, 169]
    >>> print(octets)
    b'caf\xc3\xa9'
    >>> octets.decode('utf8')
    'café'
