from django import forms
from .models import Custom_User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


class AddNewUser(forms.ModelForm):
    USER_TYPE = [
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
    ]
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputFirstName', 'placeholder': 'Enter First Name',
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputLastName', 'placeholder': 'Enter Last Name',
    }))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputUsername', 'placeholder': 'Enter username',
    }))
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'id': 'inputEmail', 'placeholder': 'Enter email address',
    }))
    phone_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPhoneNumber', 'placeholder': 'Enter phone number',
    }))
    user_type = forms.CharField(max_length=50, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputUserType'
    }, choices=USER_TYPE))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'id': 'inputPassword', 'placeholder': 'Enter password',
    }))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control', 'id': 'inputProfilePicture'
    }))

    class Meta:
        model = Custom_User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'user_type', 'password', 'profile_picture']


class Login_Form(forms.Form):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'id': 'inputUsername', 'placeholder': 'Enter email address'
    }))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'id': 'inputPassword', 'placeholder': 'Enter password'
    }))

    error_messages = {
        "invalid_login": (
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
    }

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password is not None:
            self.user_cache = authenticate(
                email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()

        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )


User = get_user_model()
class UserProfileForm(forms.ModelForm):
    USER_TYPE = [
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
    ]
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputFirstName', 'placeholder': 'Enter First Name',
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputLastName', 'placeholder': 'Enter Last Name',
    }))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputUsername', 'placeholder': 'Enter username',
    }))
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'id': 'inputEmail', 'placeholder': 'Enter email address',
    }))
    phone_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPhoneNumber', 'placeholder': 'Enter phone number',
    }))
    user_type = forms.CharField(max_length=50, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputUserType'
    }, choices=USER_TYPE))
    
    password = forms.CharField(max_length=50, required=False, label="New Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'id': 'inputPassword', 'placeholder': 'Enter password',
    }))
    
    profile_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control', 'id': 'inputProfilePicture'
    }))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'user_type', 'phone_number', 'profile_picture']
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'].help_text = "Leave blank if you don't want to change the password"
        self.fields['profile_picture'].help_text = "Leave blank if you don't want to change the profile picture"
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return password
        return None
    
    def clean(self):
        cleaned_data = super().clean()
        new_profile_picture = self.cleaned_data.get('profile_picture')
        clear_file = self.data.get('profile_picture-clear')

        if clear_file:
            if self.instance.profile_picture:
                self.instance.profile_picture.delete(save=False)

        elif new_profile_picture and new_profile_picture != self.instance.profile_picture:
            if self.instance.profile_picture:
                self.instance.profile_picture.delete(save=False)
        
        return cleaned_data


