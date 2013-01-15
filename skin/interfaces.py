from zope.interface import Interface
from zope.schema import Text

#it seems to be, that it is not possible to subclass interaces of adapters with formlib
#take a look at http://mail.zope.org/pipermail/zope3-users/2007-May/006167.html

class IHomeAdapter(Interface):
    content = Text(title=u"Content", required=False)    
class IInfoAdapter(Interface):
    content = Text(title=u"Content", required=False)
class ILinksAdapter(Interface):
    content = Text(title=u"Content", required=False)
class IContributorsAdapter(Interface):
    content = Text(title=u"Content", required=False)
class IImprintAdapter(Interface):
    content = Text(title=u"Content", required=False)
class ITechnicsAdapter(Interface):
    content = Text(title=u"Content", required=False)


