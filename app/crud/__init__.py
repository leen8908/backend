from .crud_gr_member import gr_member
from .crud_group import group
from .crud_matching_room import matching_room
from .crud_notification import notification
from .crud_user import user

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
