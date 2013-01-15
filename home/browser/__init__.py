from operator import itemgetter

from zope.publisher.browser import BrowserView
from zope.traversing.browser import absoluteURL

from sgs.entry.interfaces import IEntryNav, IEntry

class HomeEntryNavigation(BrowserView):

    def __call__(self):
        """ we return a list in a list, so we fake the IEntry EntryNavigation View with just one navigation level """

        children = []
        for child in self.context.values():
            if IEntry.providedBy(child):
                children.append(child)
        
        return [sorted( [
            {'name':IEntryNav(child).name,
             'order':IEntryNav(child).order,
             'url':absoluteURL(child, self.request) }
            for child in children if IEntryNav(child).name != None ],
                       key=itemgetter('order'))]

class EntryRecount(BrowserView):
    def __call__(self):
        return str(recursive_count(self.context))

def recursive_count(entry):
    count = len(entry)
    entries = entry.values()
    for item in entries:
        if IEntry.providedBy(item):
            count += recursive_count(item)
    entry.children = count
    return count
