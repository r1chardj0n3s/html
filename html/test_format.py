# -*- encoding: utf8 -*-
import sys
import unittest

from .format import HTML, XHTML, XML

class TestCase(unittest.TestCase):
    def test_empty_tag(self):
        'generation of an empty HTML tag'
        self.assertEquals(str(HTML().br), '<br>')

    def test_empty_tag_xml(self):
        'generation of an empty XHTML tag'
        self.assertEquals(str(XHTML().br), '<br />')

    def test_tag_add(self):
        'test top-level tag creation'
        self.assertEquals(str(HTML('html', 'text')), '<html>\ntext\n</html>')

    def test_tag_add_no_newline(self):
        'test top-level tag creation'
        self.assertEquals(str(HTML('html', 'text', newlines=False)),
            '<html>text</html>')

    def test_iadd_tag(self):
        "test iadd'ing a tag"
        h = XML('xml')
        h += XML('some-tag', 'spam', newlines=False)
        h += XML('text', 'spam', newlines=False)
        self.assertEquals(str(h),
            '<xml>\n<some-tag>spam</some-tag>\n<text>spam</text>\n</xml>')

    def test_iadd_text(self):
        "test iadd'ing text"
        h = HTML('html', newlines=False)
        h += 'text'
        h += 'text'
        self.assertEquals(str(h), '<html>texttext</html>')

    def test_xhtml_match_tag(self):
        'check forced generation of matching tag when empty'
        self.assertEquals(str(XHTML().p), '<p></p>')

    if sys.version_info[0] == 2:
        def test_empty_tag_unicode(self):
            'generation of an empty HTML tag'
            self.assertEquals(unicode(HTML().br), unicode('<br>'))

        def test_empty_tag_xml_unicode(self):
            'generation of an empty XHTML tag'
            self.assertEquals(unicode(XHTML().br), unicode('<br />'))

        def test_xhtml_match_tag_unicode(self):
            'check forced generation of matching tag when empty'
            self.assertEquals(unicode(XHTML().p), unicode('<p></p>'))

    def test_just_tag(self):
        'generate HTML for just one tag'
        self.assertEquals(str(HTML().br), '<br>')

    def test_just_tag_xhtml(self):
        'generate XHTML for just one tag'
        self.assertEquals(str(XHTML().br), '<br />')

    def test_xml(self):
        'generate XML'
        self.assertEquals(str(XML().br), '<br />')
        self.assertEquals(str(XML().p), '<p />')
        self.assertEquals(str(XML().br('text')), '<br>text</br>')

    def test_para_tag(self):
        'generation of a tag with contents'
        h = HTML()
        h.p('hello')
        self.assertEquals(str(h), '<p>hello</p>')

    def test_escape(self):
        'escaping of special HTML characters in text'
        h = HTML()
        h.text('<>&')
        self.assertEquals(str(h), '&lt;&gt;&amp;')

    def test_no_escape(self):
        'no escaping of special HTML characters in text'
        h = HTML()
        h.text('<>&', False)
        self.assertEquals(str(h), '<>&')

    def test_escape_attr(self):
        'escaping of special HTML characters in attributes'
        h = HTML()
        h.br(id='<>&"')
        self.assertEquals(str(h), '<br id="&lt;&gt;&amp;&quot;">')

    def test_subtag_context(self):
        'generation of sub-tags using "with" context'
        h = HTML()
        with h.ol:
            h.li('foo')
            h.li('bar')
        self.assertEquals(str(h), '<ol>\n<li>foo</li>\n<li>bar</li>\n</ol>')

    def test_subtag_direct(self):
        'generation of sub-tags directly on the parent tag'
        h = HTML()
        l = h.ol
        l.li('foo')
        l.li.b('bar')
        self.assertEquals(str(h),
            '<ol>\n<li>foo</li>\n<li><b>bar</b></li>\n</ol>')

    def test_subtag_direct_context(self):
        'generation of sub-tags directly on the parent tag in "with" context'
        h = HTML()
        with h.ol as l:
            l.li('foo')
            l.li.b('bar')
        self.assertEquals(str(h),
            '<ol>\n<li>foo</li>\n<li><b>bar</b></li>\n</ol>')

    def test_subtag_no_newlines(self):
        'prevent generation of newlines against default'
        h = HTML()
        l = h.ol(newlines=False)
        l.li('foo')
        l.li('bar')
        self.assertEquals(str(h), '<ol><li>foo</li><li>bar</li></ol>')

    def test_add_text(self):
        'add text to a tag'
        h = HTML()
        p = h.p('hello, world!\n')
        p.text('more text')
        self.assertEquals(str(h), '<p>hello, world!\nmore text</p>')

    def test_add_text_newlines(self):
        'add text to a tag with newlines for prettiness'
        h = HTML()
        p = h.p('hello, world!', newlines=True)
        p.text('more text')
        self.assertEquals(str(h), '<p>\nhello, world!\nmore text\n</p>')

    def test_doc_newlines(self):
        'default document adding newlines between tags'
        h = HTML()
        h.br
        h.br
        self.assertEquals(str(h), '<br>\n<br>')

    def test_doc_no_newlines(self):
        'prevent document adding newlines between tags'
        h = HTML(newlines=False)
        h.br
        h.br
        self.assertEquals(str(h), '<br><br>')

    def test_unicode(self):
        'make sure unicode input works and results in unicode output'
        h = HTML(newlines=False)
        # Python 3 compat
        try:
            unicode = unicode
            TEST = 'euro \xe2\x82\xac'.decode('utf8')
        except:
            unicode = str
            TEST = 'euro €'
        h.p(TEST)
        self.assertEquals(unicode(h), '<p>%s</p>' % TEST)

    def test_table(self):
        'multiple "with" context blocks'
        h = HTML()
        with h.table(border='1'):
            for i in range(2):
                with h.tr:
                    h.td('column 1')
                    h.td('column 2')
        self.assertEquals(str(h), '''<table border="1">
<tr><td>column 1</td><td>column 2</td></tr>
<tr><td>column 1</td><td>column 2</td></tr>
</table>''')

if __name__ == '__main__':
    unittest.main()


# Copyright (c) 2012 eKit.com Inc (http://www.ekit.com/)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# vim: set filetype=python ts=4 sw=4 et si
