from operator import itemgetter

from zope.traversing.api import getParents
from zope.traversing.interfaces import IPhysicallyLocatable
from zope.publisher.browser import BrowserView
from zope.traversing.browser import absoluteURL
#from zope.formlib.form import AddForm, EditForm, Fields, applyChanges
from zope.formlib import form
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget
from zope.app.file.image import Image
from zope.schema import TextLine
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import notify

from z3c.widget.tiny.widget import TinyWidget

from sgs.entry.interfaces import IEntryNav, IEntry
from sgs.entry.entry import Entry

class MyTinyWidget(TinyWidget):
    mce_theme_advanced_toolbar_location="top"
    mce_theme_advanced_toolbar_align="left"
    mce_theme_advanced_statusbar_location="bottom"
    mce_theme_advanced_buttons1 = "bold,italic,separator,link,unlink,separator,undo,redo,separator,cleanup,code"
    mce_theme_advanced_buttons2 = ""
    #mce_theme_advanced_resizing = "true"
    mce_entity_encoding="raw"
    mce_width = "330"
    mce_height = "260"

#entry formlib add form
largeImage_widget = CustomWidgetFactory(ObjectWidget, Image) #Object widget needs constructor
class EntryAddForm(form.AddForm):
    form_fields = form.Fields(TextLine(__name__='urlname', title=u'Name in URL', required=False),IEntryNav, IEntry)
    form_fields['largeImage'].custom_widget = largeImage_widget
    label = u"Add Entry"

    def create(self, data):
        entry = Entry()
        self.context.contentName = data['urlname']
        del data['urlname']
        form.applyChanges(entry, self.form_fields, data)
        return entry
    
#entry formlib edit form
class EntryEditForm(form.EditForm):
    form_fields = form.Fields(IEntryNav, IEntry)
    form_fields['largeImage'].custom_widget = largeImage_widget
    label = u"Edit Entry"

    form_fields['description'].custom_widget = MyTinyWidget

    actions = form.Actions(
        form.Action('Apply', success='handle_edit_action'),
        )
    
    def handle_edit_action(self, action, data): #XXX can this be done better?
        
        if data['data'] == '': #to prevent emty image overwrite
            del data['data']
            del data['contentType']
        if data['largeImage'].getSize() == 0: #to prevent emptry large image overwrite
            del data['largeImage']

        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            notify(ObjectModifiedEvent(self.context)) #TODO notify
            self.status = "Updated."

#the navigation view
class EntryNavigation(BrowserView):

    def __call__(self):
        root = IPhysicallyLocatable(self.context).getNearestSite()
        parents = getParents(self.context)

        # remove all parents below the first found site
        while parents[-1] != root:
            parents.pop()

        parents.pop() #remove Site from parents
        parents.reverse()

        parentSiblings = [ sorted( [
            {'name':IEntryNav(sibling).name,
             'order':IEntryNav(sibling).order,
             'url':absoluteURL(sibling, self.request),
             'class':((sibling in parents) and 'parent') or 'none'}
            for sibling in IEntryNav(item).getSiblings() if IEntryNav(sibling).name != None] , #only if the entry has a name
                                key=itemgetter('order')) for item in parents ]

        mySiblings = sorted( [
            {'name':IEntryNav(sibling).name,
             'order':IEntryNav(sibling).order,
             'url':absoluteURL(sibling, self.request),
             'class':((sibling == self.context) and 'self') or 'none'} \
            for sibling in IEntryNav(self.context).getSiblings() if IEntryNav(sibling).name != None] ,
                             key=itemgetter('order')) 

        
        children = sorted( [
            {'name':IEntryNav(child).name,
             'order':IEntryNav(child).order,
             'url':absoluteURL(child, self.request) }
            for child in IEntryNav(self.context).getChildren() if IEntryNav(child).name != None],
                           key=itemgetter('order'))
        
        parentSiblings.append(mySiblings)
        
        if len(children):
            parentSiblings.append(children)

        return parentSiblings
