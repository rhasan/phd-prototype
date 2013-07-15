import cgi
from HTMLParser import HTMLParser
import urllib

def escape_html(s):
    return cgi.escape(s, quote = True)

def unescape_html(s):
    return HTMLParser.unescape.__func__(HTMLParser, s)

def url_decode(s):
	return urllib.unquote(s)
