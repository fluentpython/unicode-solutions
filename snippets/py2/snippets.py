# coding: utf-8

ur"""

    >>> text = u'café'
    >>> len(text)
    4
    >>> list(text)
    [u'c', u'a', u'f', u'\xe9']
    >>> print(text)
    café
    >>> octets = text.encode('utf8')
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

"""

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("UTF-8") # DON'T DO THIS. READ THE ABOVE @UndefinedVariable
    import doctest
    doctest.testmod()
