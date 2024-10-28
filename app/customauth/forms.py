from django import forms
from django.contrib.auth.forms import UserCreationForm
from customauth.models import MyUser, Profile


class CustomUserCreationForm(UserCreationForm):
    usable_password = None

    gender = forms.ChoiceField(
        # 선택하지 않으면 빈값이 들어갑니다. 그후 MyUser에서 gender에 해당하는 선택지를 가져옵니다.
        choices=[('', 'Choose your gender')] + MyUser._meta.get_field('gender').choices,  # 기본 선택지 추가
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Date of Birth'
    )
    class Meta:
        model = MyUser
        fields = ["email", "password1", "password2", "nick_name", "date_of_birth", "gender"]

class UserUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(
        # 선택하지 않으면 빈값이 들어갑니다. 그후 MyUser에서 gender에 해당하는 선택지를 가져옵니다.
        choices=[('', 'Choose your gender')] + MyUser._meta.get_field('gender').choices,  # 기본 선택지 추가
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Date of Birth'
    )

    class Meta:
        model = MyUser
        fields = ['email', 'nick_name', 'gender', 'date_of_birth',]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image", "description"]

