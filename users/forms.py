from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount

GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
class RegistrationForm(UserCreationForm):
    profile_image = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','profile_image','gender','password1', 'password2' ]
    
    def save(self, commit=True):
        account_user = super().save(commit=False)
        if commit == True:
            account_user.save()
            profile_image = self.cleaned_data.get('profile_image')
            gender = self.cleaned_data.get('gender')
        
        UserAccount.objects.create(
            user = account_user,
            profile_image = profile_image,
            gender = gender,
        )
    
        return account_user


class EditProfile(forms.ModelForm):
    profile_image = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices=GENDER_TYPE)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance:
            try:
                user_account = self.instance.account
            except UserAccount.DoesNotExist:
                user_account = None

            if user_account:
                self.fields['profile_image'].initial = user_account.profile_image
                self.fields['gender'].initial = user_account.gender

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserAccount.objects.get_or_create(user=user)

            user_account.profile_image = self.cleaned_data['profile_image']
            user_account.gender = self.cleaned_data['gender']
            
            user_account.save()

        return user

