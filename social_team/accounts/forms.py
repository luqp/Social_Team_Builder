from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm
)
from django import forms

from .models import UserAccount, Skill


class UserCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = UserAccount
        fields = ['first_name', 'email', 'about_me', 'avatar']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'circle--input--h1',
                    'placeholder': 'Full Name'}),
            'email': forms.TextInput(
                attrs={'placeholder': 'example@example.com'}),
            'about_me': forms.Textarea(
                attrs={'placeholder': 'Tell us about yourself...'}),
            'avatar': forms.FileInput(
                attrs={
                    'style': 'background-color: white;'
                }
            )
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']

    def save(self, commit=True):
        instance = super().save(commit=False)
        skill, created = Skill.objects.get_or_create(
            name=instance.name)
        return skill


SkillFormSet = forms.modelformset_factory(
    Skill,
    form=SkillForm,
    extra=5,
    min_num=1,
    can_delete=True,
    can_order=True
)
