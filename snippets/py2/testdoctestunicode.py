# coding: utf-8

# Source:
# https://joernhees.de/blog/2010/12/15/python-unicode-doctest-howto-in-a-doctest/

ur"""
Non ascii letters in doctests actually are tricky. The reason why
things work here that usually don't (each marked with a #BAD!) is
explained quite in the end of this doctest, but the essence is: we
didn't only fix the encoding of this file, but also the
sys.defaultencoding, which you should never do.

This file has a utf8 input encoding, which python is informed about by
the first line: # -*- coding: utf-8 -*-. This means that for example an
ä is 2 bytes: 11000011 10100100 (hexval "c3a4").

There are two types of strings in Python 2.x: "" aka byte strings and
u"" aka unicode string. For these two types two different things happen
when parsing a file:

If python encounters a non ascii char in a byte string (e.g., "ä") it
will check if there's an input encoding given (yes, utf8) and then check
if the 2 bytes ä is a valid utf-8 encoded char (yes it is). It will then
simply keep the ä as its 2 byte utf-8 encoding in this byte-string
internal representation. If you print it and you're lucky to have a utf8
console you'll see an ä again. If you're not lucky and for example have
a iso-8859-15 encoding on your console you'll see 2 strange chars
(probably Ã€) instead. So python will simply write the byte-string to
output.

    >>> print "ä" #BAD!
    ä

If there was no encoding given, we'd get a SyntaxError: Non-ASCII
character 'xc3' in file ..., which is the first byte of our 2 byte ä.
Where did the 'xc3' come from? Well, this is python's way of writing a
non ascii byte to ascii output (which is always safe, so perfect for
this error message): it will write a x and then two hex chars for each
byte. Python does the same if we call:

    >>> print repr("ä")
    '\xc3\xa4'

    Or just
    >>> "ä"
    '\xc3\xa4'

It also works the other way around, so you can give an arbitrary byte by
using the same xXX escape sequences:

    >>> print "\xc3\xa4" #BAD!
    ä

Oh look, we hit the utf8 representation of an ä, what a luck. You'll ask
how do I then print "\xc3\xa4" to my console? You can either double all
"\\" or tell python it's a raw string:

    >>> print "\\xc3\\xa4"
    \xc3\xa4
    >>> print r"\xc3\xa4"
    \xc3\xa4


If python encounters a unicode string in our document (e.g., u"ä") it
will use the specified file encoding to convert our 2 byte utf8 ä into a
unicode string. This is the same as calling "ä".decode(myFileEncoding):

    >>> print u"ä" # BAD for another reason!
    ä
    >>> u"ä"
    u'\xe4'
    >>> "ä".decode("utf-8")
    u'\xe4'

Python's internal unicode representation of this string is never exposed
to the user (it could be UTF-16 or 32 or anything else, anyone?).
The hex e4 corresponds to 11100100, the unicode ord value of the char ä,
which is decimal 228.

    >>> ord(u'ä')
    228

And the same again backwards, we can use the xXX escaping to denote a
hex unicode point or raw not to interpret such escaping:

    >>> print u"\xe4"
    ä
    >>> print ur"\xe4"
    \xe4

Oh, noticed the difference? This time print did some magic. I told
you, you'll never see python's internal representation of a unicode
string. So whenever print receives a unicode string it will try to
convert it to your output encoding (sys.out.encoding), which works in a
terminal, but won't work if you're for example redirecting output to a
file. In such cases you have to convert the string into the desired
encoding explicitly:

    >>> u"ä".encode("utf8")
    '\xc3\xa4'
    >>> print u"ä".encode("utf8") #BAD!
    ä

If that last line confused you a bit: We converted the unicode string
to a byte-string, which was then simply copied byte-wise by print and
voila, we got an ä.


This all is done before the string even reaches doctest.
So you might have written something like all the above in doctests,
and probably saw them failing. In most cases you probably just
forgot the ur'''prefix''', but sometimes you had it and were confused.
Well this is good, as all of the above #BAD! examples don't make much sense.

Bummer, right.

The reason is: we made assumptions on the default encoding all over the
place, which is not a thing you would ever want to do in production
code. We did this by setting sys.setdefaultencoding("UTF-8")
below. Without this you'll usually get unicode warnings like this one:
"UnicodeWarning: Unicode equal comparison failed to convert both
arguments to Unicode - interpreting them as being unequal".
Just fire up a python interpreter (not pydev, as I noticed it seems to
fiddle with the default setting).
Try: u"ä" == "ä"
You should get:
    __main__:1: UnicodeWarning: Unicode equal comparison failed to convert both
        arguments to Unicode - interpreting them as being unequal
    False

This actually is very good, as it warns you that you're comparing some
byte-string from whatever location (could be a file) to a unicode string.
Shall python guess the encoding? Silently? Probably a bad idea.

Now if you do the following in your python interpreter:

    import sys
    reload(sys)
    sys.setdefaultencoding("utf8")
    u"ä" == "ä"

You should get:

    True

No wonder, you explicitly told python to interpret the "ä" as utf8
encoded when nothing else specified.

So what's the problem in our docstrings again? We had these bad
examples:

    >>> print "ä" #BAD!
    ä
    >>> print "\xc3\xa4" #BAD!
    ä
    >>> print u"ä".encode("utf8") #BAD!
    ä

Well, we're in a ur'''docstring''' here, so what doctest does is: it
takes the part after >>> and exec(utes) it. There's one special feature
of exec i wasn't aware of: if you pass a unicode string to it, it will
revert the char back to utf-8:

    >>> exec u'print repr("ä")'
    '\xc3\xa4'
    >>> exec u'print repr("\xe4")'
    '\xc3\xa4'

This means that even though one might think that print "ä" in this
unicode docstring will get print "xe4", it will print as if you wrote
print "ä" outside of a unicode string, so as if you wrote print
"xc3xa4". Let this twist your mind for a second. The doctest will
execute as if there had been no conversion to a unicode string, which is
what you want. But now comes the comparison. It will see what comes out
of that and compare to the next line from this docstring, which now is a
unicode "ä", so xe4. Hence we're now comparing u'xe4' == 'xc3xa4'.
If you didn't notice, this is the same we did in the python interpreter
above: we were comparing u"ä" == "ä". And again python tells us "Hmm,
don't know shall I guess how to convert "ä" to u"ä"? Probably not, so
evaluate to False.


Summary:
Always specify the source encoding: # -*- coding: utf-8 -*-
and _ALWAYS_, no excuse, use utf-8. Repeat it: I will never use
iso-8859-x, latin-1 or anything else, I'll use UTF-8 so I can write
Jörn and he can actually read his name once.
Use ur'''...''' surrounded docstrings (so a raw unicode docstring).
You can also use ru'''...''', but I always think Russian strings?
Never compare a unicode string with a byte string. This means: don't
use u"ä" and "ä" mixed, they're not the same. Also the result line can
only match unicode strings plain ascii, no other encoding.

The following are bad comparisons, as they will compare byte- and
unicode strings. They'll cause warnings and eval to false:

    #>>> u"ä" == "ä"
    #False
    #>>> "ä".decode("utf8") == "ä"
    #False
    #>>> print "ä"
    #ä


So finally a few working examples:

    >>> "ä" # if file encoding is utf8
    '\xc3\xa4'
    >>> u"ä"
    u'\xe4'

Here both are unicode, so no problem, but nevertheless a bad idea to
match output of print due to the print magic mentioned above and think
about i18n: time formats, commas, dots, float precision, etc.

    >>> print u"ä" # unicode even after exec, no prob.
    ä

Better:

    >>> "ä" == "ä" # compares byte-strings
    True
    >>> u"ä".encode("utf8") == "ä" # compares byte-strings
    True
    >>> u"ä" == u"ä" # compares unicode-strings
    True
    >>> "ä".decode("utf8") == u"ä" # compares unicode-strings
    True

"""

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("UTF-8") # DON'T DO THIS. READ THE ABOVE @UndefinedVariable
    import doctest
    doctest.testmod()
