from django.forms import ModelForm

from ..models import Fields



class FieldForm(ModelForm):
   class Meta:
      model = Fields
      fields = '__all__'
      exclude = [
         "owner",
      ]