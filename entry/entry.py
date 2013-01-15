from zope.interface import implements
from zope.component import adapts, adapter
from zope.app.container.btree import BTreeContainer
from zope.app.file.image import Image
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation import IAnnotations
from persistent.dict import PersistentDict
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.container.interfaces import IObjectAddedEvent, IObjectRemovedEvent
from zope.traversing.api import getParents

from interfaces import *

class Entry(BTreeContainer, Image):
    implements(IEntry, IEntryContainer, IEntryCountChildren, IAttributeAnnotatable)

    __name__ = __parent__ = None

    def __init__(self, data=''):
        """ we need to call both inits !!! """
        Image.__init__(self, data)
        BTreeContainer.__init__(self)
    
    description = u""
    caption = u""
    largeImage = None
    children = 0

    @property
    def order(self): #needed for attrgetter in batching view
        return IEntryNav(self).order

    def get_dc_created(self): # used for catalog
        dc = IWriteZopeDublinCore(self)
        return dc.created
    
    def set_dc_created(self, create_date): #TODO Test (used for data import)
        dc = IWriteZopeDublinCore(self)
        dc.created = create_date


EntryNavAnnotations_KEY = "sgs.entrynav"

class EntryNav(object):
    implements(IEntryNav)
    adapts(IEntry)

    def __init__(self, context):
        self.context = self.__parent__  = context # see PvWh book site 269
        annotations = IAnnotations(context)
        mapping = annotations.get(EntryNavAnnotations_KEY)
        if mapping is None:
            mapping = annotations[EntryNavAnnotations_KEY] = PersistentDict({'name': '', 'order': 0})
        self.mapping = mapping

    def name():
        def get(self):
            return self.mapping['name']
        def set(self, v):
            self.mapping['name']= v
        return property(get, set)
    name = name()

    def order():
        def get(self):
            return self.mapping['order']
        def set(self, v):
            self.mapping['order'] = v
        return property(get, set)
    order = order()

    def getEntryMenuNameFirstLetter(self):
        if self.mapping['name'] and len(self.mapping['name']):
            return self.mapping['name'][0]

    def setEntryMenuOrder(self, order):
        self.mapping['order'] = order

    def getEntryMenuOrder(self):
        return self.mapping['order']

    def getChildren(self):
        return self.context.values() 

    def getSiblings(self):
        siblings = []
        for sibling in self.context.__parent__.values():
            if IEntry.providedBy(sibling):
                siblings.append(sibling)
        return siblings


@adapter(IEntryCountChildren, IObjectAddedEvent)
def UpdateEntryChildrenOnAddSubscriber(entry, event):
    for obj in getParents(entry):
        if IEntryCountChildren.providedBy(obj):
            obj.children += 1 #add one child-count on all parents

@adapter(IEntryCountChildren, IObjectRemovedEvent)
def UpdateEntryChildrenOnRemoveSubscriber(entry, event):
    for obj in getParents(entry):
        if IEntryCountChildren.providedBy(obj):
            obj.children -= 1 #remove one child-count on all parents
