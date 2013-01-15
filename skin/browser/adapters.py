from zope.formlib import form
from zope.publisher.browser import BrowserView
from zope.app.catalog.interfaces import ICatalog
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
import random

from sgs.skin.interfaces import *
from sgs.skin.browser import BaseView

from z3c.widget.tiny.widget import TinyWidget

def create_tinymce():
    w = TinyWidget
    w.mce_theme_advanced_toolbar_location="top"
    w.mce_theme_advanced_toolbar_align="left"
    w.mce_theme_advanced_statusbar_location="bottom"
    w.mce_theme_advanced_buttons1 = "bold,italic,separator,link,unlink,separator,undo,redo,separator,cleanup,code"
    w.mce_theme_advanced_buttons2 = ""
    #w.mce_theme_advanced_resizing = "true"
    w.mce_entity_encoding="raw"
    w.mce_width = "700"
    w.mce_height = "400"
    return w

class EditHome(form.EditForm):
    form_fields = form.Fields(IHomeAdapter)
    label = u"Edit Home"
    form_fields['content'].custom_widget = create_tinymce()

class EditInfo(form.EditForm):
    form_fields = form.Fields(IInfoAdapter)
    label = u"Edit Info"
    form_fields['content'].custom_widget = create_tinymce()

class EditLinks(form.EditForm):
    form_fields = form.Fields(ILinksAdapter)
    label = u"Edit Links"
    form_fields['content'].custom_widget = create_tinymce()

class EditContributors(form.EditForm):
    form_fields = form.Fields(IContributorsAdapter)
    label = u"Edit Sammler"
    form_fields['content'].custom_widget = create_tinymce()

class EditImprint(form.EditForm):
    form_fields = form.Fields(IImprintAdapter)
    label = u"Edit Impressum"
    form_fields['content'].custom_widget = create_tinymce()

class EditTechnics(form.EditForm):
    form_fields = form.Fields(ITechnicsAdapter)
    label = u"Edit Technik"
    form_fields['content'].custom_widget = create_tinymce()

class ViewContentPages(BaseView):
    def view_home(self):
        return IHomeAdapter(self.context).content
    def view_info(self):
        return IInfoAdapter(self.context).content
    def view_links(self):
        return ILinksAdapter(self.context).content
    def view_contributors(self):
        return IContributorsAdapter(self.context).content
    def view_imprint(self):
        return IImprintAdapter(self.context).content
    def view_technics(self):
        return ITechnicsAdapter(self.context).content

    def random_images(self):
        intids = getUtility(IIntIds)
        catalog = getUtility(ICatalog)

        #see http://mail.zope.org/pipermail/zope3-users/2007-May/006168.html for discussion of that
        #import logging
        #import time
        #t0 = time.time()
        #len_all = len(catalog['created']._rev_index)
        len_all = catalog['created'].documentCount()
        #len_all = len(catalog.apply({'created':(None,None)}))
        all = list(catalog['created']._rev_index.keys())
        #logging.info(time.time()-t0)

        imagelist = []
        for n in range(9):
            try:
                intid = all[random.randint(0,len_all-1)]
            except IndexError:
                intid = all[0] #maybe some item got deleted meanwhile

            imagelist.append(intids.getObject(intid))

        return imagelist

        
