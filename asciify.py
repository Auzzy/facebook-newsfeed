# -*- coding: utf-8 -*-

# Source: http://chmullig.com/2009/12/python-unicode-ascii-ifier/

# use a dynamically populated translation dictionary to remove accents
# from a string
 
import unicodedata, sys
 
class unaccented_map(dict):
# Translation dictionary.  Translation entries are added to this dictionary as needed.
    CHAR_REPLACEMENT = {
        0xc6: u"AE", # � LATIN CAPITAL LETTER AE
        0xd0: u"D",  # � LATIN CAPITAL LETTER ETH
        0xd8: u"OE", # � LATIN CAPITAL LETTER O WITH STROKE
        0xde: u"Th", # � LATIN CAPITAL LETTER THORN
        0xc4: u'Ae', # � LATIN CAPITAL LETTER A WITH DIAERESIS
        0xd6: u'Oe', # � LATIN CAPITAL LETTER O WITH DIAERESIS
        0xdc: u'Ue', # � LATIN CAPITAL LETTER U WITH DIAERESIS
 
        0xc0: u"A", # � LATIN CAPITAL LETTER A WITH GRAVE
        0xc1: u"A", # � LATIN CAPITAL LETTER A WITH ACUTE
        0xc3: u"A", # � LATIN CAPITAL LETTER A WITH TILDE
        0xc7: u"C", # � LATIN CAPITAL LETTER C WITH CEDILLA
        0xc8: u"E", # � LATIN CAPITAL LETTER E WITH GRAVE
        0xc9: u"E", # � LATIN CAPITAL LETTER E WITH ACUTE
        0xca: u"E", # � LATIN CAPITAL LETTER E WITH CIRCUMFLEX
        0xcc: u"I", # � LATIN CAPITAL LETTER I WITH GRAVE
        0xcd: u"I", # � LATIN CAPITAL LETTER I WITH ACUTE
        0xd2: u"O", # � LATIN CAPITAL LETTER O WITH GRAVE
        0xd3: u"O", # � LATIN CAPITAL LETTER O WITH ACUTE
        0xd5: u"O", # � LATIN CAPITAL LETTER O WITH TILDE
        0xd9: u"U", # � LATIN CAPITAL LETTER U WITH GRAVE
        0xda: u"U", # � LATIN CAPITAL LETTER U WITH ACUTE
 
        0xdf: u"ss", # � LATIN SMALL LETTER SHARP S
        0xe6: u"ae", # � LATIN SMALL LETTER AE
        0xf0: u"d",  # � LATIN SMALL LETTER ETH
        0xf8: u"oe", # � LATIN SMALL LETTER O WITH STROKE
        0xfe: u"th", # � LATIN SMALL LETTER THORN,
        0xe4: u'ae', # � LATIN SMALL LETTER A WITH DIAERESIS
        0xf6: u'oe', # � LATIN SMALL LETTER O WITH DIAERESIS
        0xfc: u'ue', # � LATIN SMALL LETTER U WITH DIAERESIS
 
        0xe0: u"a", # � LATIN SMALL LETTER A WITH GRAVE
        0xe1: u"a", # � LATIN SMALL LETTER A WITH ACUTE
        0xe3: u"a", # � LATIN SMALL LETTER A WITH TILDE
        0xe7: u"c", # � LATIN SMALL LETTER C WITH CEDILLA
        0xe8: u"e", # � LATIN SMALL LETTER E WITH GRAVE
        0xe9: u"e", # � LATIN SMALL LETTER E WITH ACUTE
        0xea: u"e", # � LATIN SMALL LETTER E WITH CIRCUMFLEX
        0xec: u"i", # � LATIN SMALL LETTER I WITH GRAVE
        0xed: u"i", # � LATIN SMALL LETTER I WITH ACUTE
        0xf2: u"o", # � LATIN SMALL LETTER O WITH GRAVE
        0xf3: u"o", # � LATIN SMALL LETTER O WITH ACUTE
        0xf5: u"o", # � LATIN SMALL LETTER O WITH TILDE
        0xf9: u"u", # � LATIN SMALL LETTER U WITH GRAVE
        0xfa: u"u", # � LATIN SMALL LETTER U WITH ACUTE
 
        0x2018: u"'", # � LEFT SINGLE QUOTATION MARK
        0x2019: u"'", # � RIGHT SINGLE QUOTATION MARK
        0x201c: u'"', # � LEFT DOUBLE QUOTATION MARK
        0x201d: u'"', # � RIGHT DOUBLE QUOTATION MARK
 
        }
 
    # Maps a unicode character code (the key) to a replacement code
    # (either a character code or a unicode string).
    def mapchar(self, key):
        ch = self.get(key)
        if ch is not None:
            return ch
        try:
            de = unicodedata.decomposition(unichr(key))
            p1, p2 = [int(x, 16) for x in de.split(None, 1)]
            if p2 == 0x308:
		ch = self.CHAR_REPLACEMENT.get(key)
            else:
                ch = int(p1)
 
        except (IndexError, ValueError):
            ch = self.CHAR_REPLACEMENT.get(key, key)
        self[key] = ch
        return ch
 
    if sys.version >= "2.5":
        # use __missing__ where available
        __missing__ = mapchar
    else:
        # otherwise, use standard __getitem__ hook (this is slower,
        # since it's called for each character)
        __getitem__ = mapchar
 
map = unaccented_map()
 
def asciify(input):
	try:
		return input.encode('ascii')
	except AttributeError:
		return str(input).encode('ascii')
	except UnicodeEncodeError:
	        return unicodedata.normalize('NFKD', input.translate(map)).encode('ascii', 'replace')
  
if __name__ == "__main__":
    for i, line in enumerate(text.splitlines()):
        line = line.strip()
        print line
        if line and not line.startswith('#'):
            print '\tTrans: ', asciify(line).strip()
	
