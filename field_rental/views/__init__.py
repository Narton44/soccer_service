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
)