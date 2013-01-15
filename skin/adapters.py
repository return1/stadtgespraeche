from zope.annotation.interfaces import IAnnotations
from interfaces import *

KEY_HOME = "sgs.specialpage.home"
KEY_LINKS = "sgs.specialpage.links"
KEY_INFO = "sgs.specialpage.info"
KEY_CONTRIBUTORS = "sgs.specialpage.contributors"
KEY_IMPRINT = "sgs.specialpage.imprint"
KEY_TECHNICS = "sgs.specialpage.technics"

class HomeAdapter(object):
    #implements and adapts is not working, if i subclass the adapter implementations
    #so this is handled via "provides" and "for" in zcml

    def __init__(self, context):
        self.context = context
        self.KEY = KEY_HOME

    #for formlib admin view
    def content():
        def get(self):
            try:
                return IAnnotations(self.context)[self.KEY]
            except KeyError:
                return None
        def set(self, v):
            IAnnotations(self.context)[self.KEY] = v
        return property(get, set)
    content = content()

class InfoAdapter(HomeAdapter):
    def __init__(self, context):
        self.context = context
        self.KEY = KEY_INFO
        
class LinksAdapter(HomeAdapter):
    def __init__(self, context):
        self.context = context
        self.KEY = KEY_LINKS

class ContributorsAdapter(HomeAdapter):
    def __init__(self, context):
        self.context = context
        self.KEY = KEY_CONTRIBUTORS

class ImprintAdapter(HomeAdapter):
    def __init__(self, context):
        self.context = context
        self.KEY = KEY_IMPRINT

class TechnicsAdapter(HomeAdapter):
    def __init__(self, context):
        self.context = context
        self.KEY = KEY_TECHNICS
