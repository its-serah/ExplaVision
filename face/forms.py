from .models import Face
from django import forms


class FaceForm(forms.ModelForm):
    """
    Form for adding and editing faces in the face recognition system.

    This form handles the creation and updating of Face model instances,
    allowing users to upload face images with associated names.
    The form applies Tailwind CSS styling for a modern, responsive UI.
    """

    class Meta:
        """
        Meta configuration for the face form.

        Specifies which model to use, which fields to include, and custom
        styling for form widgets using Tailwind CSS.
        """

        model = Face
        fields = ["name", "image", "is_allowed"]
        widgets = {
            # Text input for the person's name with Tailwind CSS styling
            "name": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                }
            ),
            # Checkbox input for allowing/disallowing access with appropriate checkbox styling
            "is_allowed": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                }
            ),
            # File input for uploading face images with Tailwind CSS styling
            "image": forms.FileInput(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                }
            ),
        }
