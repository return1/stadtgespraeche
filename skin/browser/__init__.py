from operator import attrgetter, itemgetter
from zope.publisher.browser import BrowserView
from zope.traversing.browser import absoluteURL
from zope.app.catalog.interfaces import ICatalog
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from z3c.batching.batch import Batch

from sgs.entry.interfaces import IEntryNav

class BaseView(BrowserView):
    def is_true(self, condition, true_result, false_result):
        if condition == True:
            return true_result
        else:
            return false_result

class EntryView(BaseView):
    
    def has_largeimage(self):
        if self.context.largeImage.getSize() != 0:
            return True
        else:
            return False

    def get_children(self):
        if IEntryNav(self.context).name: #depends on, of the entry is visible in the navigation or not
            return self.context.children
        else:
            return self.context.__parent__.children

    def get_batching(self):
        request = self.request
        
        if IEntryNav(self.context).name: #depends on, of the entry is visible in the navigation or not
            entries = self.context.values()
        else:
            entries = self.context.__parent__.values()

        filtered_and_sorted_entries = sorted([x for x in entries if not IEntryNav(x).name],
                                             key=attrgetter('order'))
            
        sequence = [{'url': absoluteURL(x, request),
                           'order': IEntryNav(x).order,
                           'class': x != self.context or 'hl'}
                          for x in filtered_and_sorted_entries]


        size = 17 #batch size
        prev_url = False
        next_url = False
        start = 0
        if self.context in filtered_and_sorted_entries: #get index of actual object
            current_index = filtered_and_sorted_entries.index(self.context)
            if current_index > 0:
                prev_url = "%s/entry.html?bs=%s" % (sequence[current_index-1]['url'], start)
            if current_index < len(sequence)-1:
                next_url = "%s/entry.html?bs=%s" % (sequence[current_index+1]['url'], start)
            start = (current_index/size)*size #where should the batching start?
        else:
            current_index = -1

        batch = Batch(sequence, start=start, size=size)
                    
        return {'batch': batch, 'prev_url': prev_url, 'next_url':next_url}

class OrientationView(BaseView):

    def __init__(self, context, request):
        super(OrientationView, self).__init__(context, request)
        self.alphabet = ['A',u'\xc4','B','C','D','E','F','G','H','I','J','K','L','M','N','O',u'\xd6','P','Q','R','S','T','U',u'\xdc','V','W','X','Y','Z']
        try:
            self.key = request['key']
            if self.key not in self.alphabet:
                self.key = 'A'
        except (KeyError):
            self.key = 'A'
            
        
    def get_entries(self):
        request = self.request
        key = self.key
        catalog = getUtility(ICatalog)
        entries = list(catalog.searchResults(menuNames=(key, key)))
        sequence = sorted([{'url': '%s/entry.html' % absoluteURL(x, request),
                            'name': IEntryNav(x).name}
                           for x in entries], key=itemgetter('name'))
        return sequence


class NewEntriesView(BaseView):
    """ """
    def get_history(self):
        intids = getUtility(IIntIds)
        catalog = getUtility(ICatalog)

        try:
            start = int(self.request['start'])
        except (KeyError, ValueError, TypeError):
            start = 0

        len_all = catalog['created'].documentCount()
        all = sorted(list(catalog['created']._rev_index.items()), key=itemgetter(1), reverse=True)

        batch = Batch(all, start=start, size=21)
        entries = [ intids.getObject(x[0]) for x in list(batch) ]

        return {'entries': entries, 'batch':batch}

        
