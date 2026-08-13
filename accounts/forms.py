from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', )

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'autocomplete': 'email',
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'new-password',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
        })





class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
                "autocomplete": "email",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        )
    )




class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            "image",
            "first_name",
            "last_name",
            "description",
        )

        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tell us about yourself",
                    "rows": 5,
                }
            ),
        }