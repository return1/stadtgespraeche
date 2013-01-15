from zope.interface import Interface
from zope.app.file.interfaces import IImage
from zope.app.container.interfaces import IContainer
from zope.app.container.constraints import contains
from zope.schema import SourceText, TextLine, Object, Int

class IEntryCountChildren(Interface):
    """ Implementation of this interface knows amount if its children
    this is because BTree is to slow to count that much entries on the fly
    entries are now statically counted and updated via Events on Entry Creation or Removal
    """

    children = Int(title=u"Children", required=False)

class IEntry(IImage):
    """ Interface for Entry  """

    description = SourceText(title=u"Image Description", required=False)
    caption = TextLine(title=u"Image Caption", required=False)
    largeImage = Object(description=u"Large Image", schema=IImage, required=False)

    def order():
        """ needed for attrgetter and sorting """

    def get_dc_created():
        """ used for catalog """

    def set_dc_created(create_date):
        """ used for data import """
                                        


class IEntryContainer(IContainer):
    """ Container Interface for an Entry """
    contains(IEntry)

class IEntryNav(Interface):
    """used as Adapter for menu creation
    """

    name = TextLine(title=u"Menuname", required=False)
    order = Int(title=u"Order", required=False)

    def setEntryMenuName(menuname):
        """ set the navigation menu name  """

    def getEntryMenuName():
        """ get the navigation menu name """

    def getEntryMenuNameFirstLetter():
        """ get the navigation menu name first letter """

    def getEntryMenuOrder():
        """ get the navigation menu order """

    def setEntryMenuOrder(order):
        """ set the navigation menu order """
                        
    def getChildren():
        """ get all IEntry children from this location """

    def getSiblings():
        """ get all IEntry Siblings from this location
            (self is included)
        """
        
