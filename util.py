import cgi
from HTMLParser import HTMLParser
import urllib

"""
escapes an HTML string
"""
def escape_html(s):
    return cgi.escape(s, quote = True)

"""
unescapes an HTML string
"""
def unescape_html(s):
    return HTMLParser.unescape.__func__(HTMLParser, s)

"""
decodes a URI
"""
def url_decode(s):
    return urllib.unquote(s.encode('ascii'))


def main():
    print url_decode(u'http://dbpedia.org/resource/Moli%C3%A8re_%281978_film%29')

if __name__ == "__main__":
    main()