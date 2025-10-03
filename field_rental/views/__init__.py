from .fields import (
    FieldsCreateView,
    FieldsListView,
    FieldsUpdateView,
    FieldsDeleteView,
    FieldsManagerListView
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
    # "BookingsCreateView",
    # "BookingsUpdateView",
    # "BookingsDetailView",
    # "BookingsDeleteView",
    "BookingsListView",
    "UserBookingListView",
    "UserBookingConfirmManagerView",
    "SearchView",
)