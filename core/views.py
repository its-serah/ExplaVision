from django.shortcuts import redirect
from django.views.generic import (
    TemplateView,
    FormView,
)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import UserRegistrationForm


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard view for authenticated users.

    This view renders the main application interface where users can
    upload images for face detection and recognition.

    Authentication is required to access this view.
    """

    template_name = "index.html"  # Template to render


class UserLoginView(LoginView):
    """
    User login view.

    Handles authentication of users trying to access the system.
    Uses Django's built-in LoginView with custom template and behavior.
    """

    template_name = "login.html"  # Custom login template
    redirect_authenticated_user = True  # Redirect already logged-in users

    def form_invalid(self, form):
        """
        Handle invalid login attempts.

        Displays an error message when login credentials are invalid.

        Args:
            form: The submitted login form with validation errors

        Returns:
            HttpResponse: The response with error message
        """
        messages.error(self.request, "Invalid username or password")
        return super().form_invalid(form)

    def get_success_url(self):
        """
        Determine where to redirect after successful login.

        Returns:
            str: URL to redirect to after login
        """
        return reverse_lazy("index")  # Redirect to main dashboard


class UserRegistrationView(FormView):
    """
    User registration view.

    Handles creation of new user accounts with the custom registration form.
    """

    template_name = "register.html"  # Template for registration form
    form_class = UserRegistrationForm  # Custom form with email validation
    success_url = reverse_lazy(
        "login"
    )  # Redirect to login after successful registration

    def dispatch(self, request, *args, **kwargs):
        """
        Handle the incoming request.

        Redirects authenticated users to the dashboard, as they don't need to register.

        Args:
            request: The HTTP request

        Returns:
            HttpResponse: Redirect to index for authenticated users, otherwise normal view
        """
        if request.user.is_authenticated:
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Process valid form data.

        Creates a new user account and displays a success message.

        Args:
            form: The validated registration form

        Returns:
            HttpResponse: Response with success message
        """
        user = form.save()  # Create the user
        messages.success(
            self.request, "Account created successfully! You can now log in."
        )
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """
    User logout view.

    Handles logging users out of the system.
    Uses Django's built-in LogoutView with custom behavior.
    """


    def dispatch(self, request, *args, **kwargs):
        """
        Handle the logout request.

        Displays a success message when a user logs out.

        Args:
            request: The HTTP request

        Returns:
            HttpResponse: Response with logout success message
        """
        messages.success(request, "You have been logged out")
        return super().dispatch(request, *args, **kwargs)
    