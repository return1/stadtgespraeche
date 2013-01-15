import unittest
from doctest import DocFileSuite, ELLIPSIS

#import zope.component.testing
import zope.app.testing.setup 
#from zope.annotation.attribute import AttributeAnnotations
from zope.app.folder import rootFolder

from sgs.entry.interfaces import IEntryNav
from sgs.entry.entry import EntryNav
from sgs.entry.entry import Entry

def setupEntryStructure():
    """ Set up a reasonably complex folder structure

     ____________ rootFolder ________________________
    /                                                \
 folder1 _______________________________	   folder2
   |				        \             |     
 folder1_1 ________________	      folder1_2    folder2_1
   |           \           \             |            |
 folder1_1_1 folder1_1_2 folder1_1_3  folder1_2_1  folder2_1_1
    """
    root = rootFolder()
    entry = root[u'entry1'] = Entry()
    IEntryNav(entry).name = u'Pictorial'
    IEntryNav(entry).order = 2
    entry = root[u'entry1'][u'entry1_1'] = Entry()
    IEntryNav(entry).name = u'Menschen'
    IEntryNav(entry).order = 12
    entry = root[u'entry1'][u'entry1_1'][u'entry1_1_1'] = Entry()
    IEntryNav(entry).name = u'Frauen'
    IEntryNav(entry).order = 113
    entry = root[u'entry1'][u'entry1_1'][u'entry1_1_2'] = Entry()
    IEntryNav(entry).name = u'Gruppen'
    IEntryNav(entry).order = 111
    entry = root[u'entry1'][u'entry1_1'][u'entry1_1_3'] = Entry()
    IEntryNav(entry).name = u'Ausrutschen'
    IEntryNav(entry).order = 112
    entry = root[u'entry1'][u'entry1_2'] = Entry()
    IEntryNav(entry).name = u'Verkehr'
    IEntryNav(entry).order = 11
    entry = root[u'entry1'][u'entry1_2'][u'entry1_2_1'] = Entry()
    IEntryNav(entry).name = u'Pferd'
    entry = root[u'entry2'] = Entry()
    IEntryNav(entry).name = u'Sozial'
    IEntryNav(entry).order = 1
    entry = root[u'entry2'][u'entry2_1'] = Entry()
    IEntryNav(entry).name = u'Hilfestellungen'
    IEntryNav(entry).order = 21
    entry = root[u'entry2'][u'entry2_1'][u'entry2_1_1'] = Entry()
    IEntryNav(entry).name = u'Offiziell'
    IEntryNav(entry).order = 22
    entry = root[u'entry3'] = Entry() #test if entries without name are ignored
    IEntryNav(entry).name = None
    return root


def setUp(test):
    zope.app.testing.setup.placefulSetUp(site=True)
    zope.component.provideAdapter(EntryNav)
    
def tearDown(self):
    zope.app.testing.setup.placefulTearDown()

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('entry.txt',
                     package='sgs.entry',
                     setUp=setUp,
                     tearDown=tearDown,
                     optionflags=ELLIPSIS,
                     globs={'testEntryStructure': setupEntryStructure}),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
