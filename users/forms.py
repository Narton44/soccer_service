from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import CustomUser


class CustomUserForm(UserCreationForm):
   email = forms.EmailField(
      label="Email",
      max_length=30,
      widget=forms.TextInput(
         attrs={
            "type": "text", 
            "class": "formatted-input"
            }
      )
   )

   
   class Meta:
      model = CustomUser
      fields = (
         "email",
         "username",
         "phone_number",
      )
