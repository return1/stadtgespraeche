from zope.interface import implements
from zope.app.container.btree import BTreeContainer
from zope.app.component.site import LocalSiteManager, SiteManagerContainer
from zope.component import adapter
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.intid.interfaces import IIntIds
from zope.app.intid import IntIds
from zope.app.catalog.interfaces import ICatalog
from zope.app.catalog.catalog import Catalog
from zope.app.catalog.field import FieldIndex
from zope.app.security.interfaces import IAuthentication
from zope.app.authentication.authentication import PluggableAuthentication
from zope.app.authentication.principalfolder import PrincipalFolder

from interfaces import *
from sgs.entry.interfaces import IEntryNav, IEntry, IEntryCountChildren

class SGSHome(SiteManagerContainer, BTreeContainer):
    """SGS Home Container"""
    implements(ISGSHome, IEntryCountChildren)
    
    __name__ = __parent__ = None

    children = 0

@adapter(ISGSHome, IObjectAddedEvent)
def setupSGSSiteSubscriber(home, event):
    """ set container als Site and register the needed utilities
    """
    home.setSiteManager(LocalSiteManager(home))
    sm = home.getSiteManager()

    intids = IntIds()
    sm['intids'] = intids
    sm.registerUtility(intids, IIntIds)

    catalog = Catalog()
    sm['catalog'] = catalog
    sm.registerUtility(catalog, ICatalog)

    menuNames = FieldIndex(
        interface=IEntryNav,
        field_name='getEntryMenuNameFirstLetter',
        field_callable=True
        )
    catalog[u'menuNames'] = menuNames

    created = FieldIndex(
        interface=IEntry,
        field_name='get_dc_created',
        field_callable=True
        )
    catalog[u'created'] = created

    pas = PluggableAuthentication()

    principalfolder = PrincipalFolder()
    principalfolder.prefix = u"sgs."
    pas['PrincipalFolder'] = principalfolder
    pas.authenticatorPlugins = [u"PrincipalFolder"]
    pas.credentialsPlugins = [u'Zope Realm Basic-Auth'] #predefined utility

    sm['auth'] = pas
    sm.registerUtility(pas, IAuthentication)
