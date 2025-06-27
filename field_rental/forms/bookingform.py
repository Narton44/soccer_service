from django.forms import ModelForm

from ..models import Booking



class BookingForm(ModelForm):
   class Meta:
      model = Booking
      Booking = '__all__'
      exclude = [
         
      ]
