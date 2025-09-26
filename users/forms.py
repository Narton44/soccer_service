from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import CustomUser

# Класс формы создания обычного пользователя, без права указания ролей.
class CustomUserForm(UserCreationForm):
   email = forms.EmailField(
      label="Email",
      max_length=30,
      help_text="Используйте только Российские Email",
      widget=forms.TextInput(
         attrs={
            "type": "email", 
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

# Класс формы создания пользователей для админа, с правом указания любой роли.
class CustomUserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.NumberInput):
                field.widget = forms.TextInput(
                    attrs={"type": "text", "class": "formatted-input"}
                )

    class Meta:
        model = CustomUser
        fields = ["role", "email", "username", "phone_number",]
        exclude = ['password',]

class PasswordResetForm(forms.ModelForm):
    new_password = forms.CharField(
        label="Новый пароль",
        help_text="Пароль не должен быть слишком похож на другую вашу личную информацию. Ваш пароль должен содержать как минимум 8 символов. Пароль не должен быть слишком простым и распространенным. Пароль не может состоять только из цифр.",
        widget=forms.PasswordInput,
        min_length=8
    )
    confirm_password = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput,
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз."
    )

    class Meta:
        model = CustomUser
        fields = []


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data
    
class CustomUserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "username", "phone_number",]
        exclude = ['password',]