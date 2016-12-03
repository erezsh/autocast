import cgi
import json

from ..autocast import CastError, autoclass, autocast

@autoclass
class HTML:

    def __init__(self, html):
        self.html = html

    def __repr__(self):
        return "HTML(%r)" % self.html

    def from__str(s):
        assert isinstance(s, str), s
        return HTML(cgi.html.escape(s))

    def to__str(self):
        return str(cgi.html.unescape(self.html))

    # def from__list(l):
    #     return '<ol>\n%s\n</ol>' % '\n'.join('<li>%s</li>' % (n >> ).html for n in l)

    # def from__set(s):
    #     return '<ul>\n%s\n</ul>' % '\n'.join('<li>%s</li>' % (n >> cls).html for n in s)

    # def from__dict(cls, d):
    #     return '<dl>\n%s\n</dl>' % '\n'.join('<dt>%s</dt><dd>%s</dd>' % ((k>>cls).html, (v>>cls).html) for k,v in d.items())


@autoclass
class RGB:

    @autocast
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def to__HTML(self):
        return HTML('#%02x%02x%02x' % (self.r, self.g, self.b))


@autoclass
class JSON:

    @autocast
    def __init__(self, json_str: str):
        self.json_str = json_str

    def from__dict(d):
        return JSON(json.dumps(d))
    def to__dict(self):
        return json.loads(self.json_str)

    def to__str(self):
        return self.json_str



