from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User,Group
from .models import ConfirmCode


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
    def save(self,commit=True):
        user = super().save()
        common_user = Group.objects.get(name="common user")
        user.groups.add(common_user)

        return user
class loginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

class loginFormConfirmCode(forms.ModelForm):
    class Meta:
        model = ConfirmCode
        fields = (
            "code",
            "user",
        )