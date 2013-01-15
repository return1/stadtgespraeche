import unittest
from zope.testing import doctest
from zope.publisher.browser import TestRequest
import zope.app.testing.setup
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.dublincore.annotatableadapter import ZDCAnnotatableAdapter
import zope.component.eventtesting

from sgs.entry.entry import EntryNav
from sgs.entry.browser import EntryNavigation
from sgs.entry.tests.test_entryNav import setupEntryStructure

def setUp(test):
    zope.app.testing.setup.placefulSetUp(site=True)
    zope.component.eventtesting.setUp(test)
    zope.component.provideAdapter(ZDCAnnotatableAdapter, provides=IWriteZopeDublinCore)
    zope.component.provideAdapter(EntryNav)

def tearDown(test):
    zope.app.testing.setup.placefulTearDown()


class EntryNavigationTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def test_navigation_firstlevel(self):
        request = TestRequest()
        root = setupEntryStructure()
        
        view = EntryNavigation(root[u'entry1'], request)
        
        self.assertEqual(view(), [[{'url': 'http://127.0.0.1/entry2', \
'class': 'none', 'name': u'Sozial', 'order': 1}, {'url': \
'http://127.0.0.1/entry1', 'class': 'self', 'name': u'Pictorial',
'order': 2}], [{'url': 'http://127.0.0.1/entry1/entry1_2', 'name': \
u'Verkehr', 'order': 11}, {'url': 'http://127.0.0.1/entry1/entry1_1', \
'name': u'Menschen', 'order': 12}]])

#    def test_navigation_midlevel(self):
#        request = TestRequest()
#        root = setupEntryStructure()
#        
#        view = EntryNavigation(root[u'entry1'][u'entry1_1'], request)
#        
#        self.assertEqual(view(), [[{'url': 'http://127.0.0.1/entry2', \
#'class': 'none', 'name': u'Sozial', 'order': 1}, {'url': \
#'http://127.0.0.1/entry1', 'class': 'parent', 'name': u'Pictorial', \
#'order': 2}], [{'url': 'http://127.0.0.1/entry1/entry1_2', 'class': 'none', \
#'name': u'Verkehr', 'order': 11}, {'url': 'http://127.0.0.1/entry1/entry1_1'\
#,'class': 'self', 'name': u'Menschen', 'order': 12}], [{'url': \
#'http://127.0.0.1/entry1/entry1_1/entry1_1_2', 'name': u'Gruppen', \
#'order': 111}, {'url': 'http://127.0.0.1/entry1/entry1_1/entry1_1_3', \
#'name': u'Ausrutschen', 'order': 112}, {'url': \
#'http://127.0.0.1/entry1/entry1_1/entry1_1_1', 'name': u'Frauen', \
#'order': 113}]])

#    def test_navigation_lastlevel(self):
#        request = TestRequest()
#        root = setupEntryStructure()
#
#        view = EntryNavigation(root[u'entry1'][u'entry1_1'][u'entry1_1_1'],
#                               request)
#
#        self.assertEqual(view(), [[{'url': 'http://127.0.0.1/entry2', \
#'class': 'none', 'name': u'Sozial', 'order': 1}, {'url': \
#'http://127.0.0.1/entry1', 'class': 'parent', 'name': u'Pictorial', \
#'order': 2}], [{'url': 'http://127.0.0.1/entry1/entry1_2', \
#'class': 'none', 'name': u'Verkehr', 'order': 11}, {'url': \
#'http://127.0.0.1/entry1/entry1_1', 'class': 'parent', 'name': \
#u'Menschen', 'order': 12}], [{'url': \
#'http://127.0.0.1/entry1/entry1_1/entry1_1_2', 'class': 'none', \
#'name': u'Gruppen', 'order': 111}, {'url': \
#'http://127.0.0.1/entry1/entry1_1/entry1_1_3', \
#'class': 'none', 'name': u'Ausrutschen', 'order': 112}, {'url': \
#'http://127.0.0.1/entry1/entry1_1/entry1_1_1', 'class': 'self', \
#'name': u'Frauen', 'order': 113}]])
    

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EntryNavigationTestCase))
    suite.addTest(doctest.DocFileSuite(
        'catalog.txt',
        setUp=setUp,
        tearDown=tearDown,
        globs={'testEntryStructure': setupEntryStructure}))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
