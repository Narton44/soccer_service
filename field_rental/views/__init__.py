from .fields import (
    FieldsCreateView,
    FieldsListView,
    FieldsUpdateView,
    FieldsDeleteView,
    FieldsManagerListView,
    FieldsCategoryListView
)
from .bookings import (
#     # BookingsCreateView,
#     # BookingsUpdateView,
#     # BookingsDetailView,
#     # BookingsDeleteView,
      BookingsListView,
      UserBookingListView,
      UserBookingConfirmManagerView,
)

from .search import SearchView


__all__ = (
    "FieldsCreateView",
    "FieldsListView",
    "FieldsUpdateView",
    "FieldsDeleteView",
    "FieldsManagerListView",
    "FieldsCategoryListView",
    # "BookingsCreateView",
    # "BookingsUpdateView",
    # "BookingsDetailView",
    # "BookingsDeleteView",
    "BookingsListView",
    "UserBookingListView",
    "UserBookingConfirmManagerView",
    "SearchView",
)