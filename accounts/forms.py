from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from .models import *

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("No User")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        return user

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    username = forms.CharField(label='User Name', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "User Name"
    }))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "First Name"
    }))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Last Name"
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm Password"
    }))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use. Please choose a different one.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Please use a different email.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don`t match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.admin = False
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any additional customization for the form fields here

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']  # Include the fields you want to edit

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email",
        })
    )
    username = forms.CharField(
        label='User Name',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "User Name",
        })
    )
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First Name",
        })
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Last Name",
        })
    )
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm Password"
    }))

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already in use. Please choose a different one.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already in use. Please use a different email.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don`t match")
        return password2

    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user
