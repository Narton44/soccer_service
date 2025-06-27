from django.forms import ModelForm

from .models import Fields
from .models import Booking


class FieldForm(ModelForm):
   class Meta:
      model = Fields
      fields = '__all__'
      exclude = [
         "owner",
      ]

class BookingForm(ModelForm):
   class Meta:
      model = Booking
      Booking = '__all__'
      exclude = [
         
      ]
