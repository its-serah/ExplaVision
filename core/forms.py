from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    """
    Custom user registration form extending Django's UserCreationForm.

    This form includes email validation and custom styling with Tailwind CSS classes.
    It provides a clean, responsive interface for new user registration while ensuring
    data validation and security.
    """

    # Add email field which is required and has Tailwind CSS styling
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            }
        ),
    )

    # Override password field to customize label
    password1 = forms.CharField(
        label=_("Password"),
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta:
        """
        Meta configuration for the registration form.

        Specifies which model to use and which fields to include in the form.
        """

        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and add Tailwind CSS classes to all form fields.

        This ensures consistent styling across the entire form without repeating
        CSS class definitions for each field individually.
        """
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Add Tailwind CSS classes to the form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs[
                "class"
            ] = "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"

    def clean_email(self):
        """
        Custom validation method for the email field.

        Ensures that the email address is not already registered in the system
        to prevent duplicate accounts.

        Returns:
            str: The validated email if it passes the unique check

        Raises:
            ValidationError: If the email is already registered
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
