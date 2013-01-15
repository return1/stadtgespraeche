from zope.app.container.interfaces import IContainer
from zope.app.container.constraints import contains
from zope.app.component.interfaces import IPossibleSite
from zope.annotation.interfaces import IAttributeAnnotatable

from sgs.entry.interfaces import IEntry

class ISGSHome(IPossibleSite, IContainer, IAttributeAnnotatable):
    """ """
    contains(IEntry)
