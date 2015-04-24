import unicodedata
import re

re_digit = re.compile(r'\d')

sample = '1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'

for char in sample:
    print('U+%04x' % ord(char),                       # <A>
          char.center(6),                             # <B>
          're_dig' if re_digit.match(char) else '-',  # <C>
          'isdig' if char.isdigit() else '-',         # <D>
          'isnum' if char.isnumeric() else '-',       # <E>
          format(unicodedata.numeric(char), '5.2f'),  # <F>
          unicodedata.name(char),                     # <G>
          sep='\t')
