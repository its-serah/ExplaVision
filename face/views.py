from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
from ultralytics import YOLO
from deepface import DeepFace
import os
from django.conf import settings

from .models import Face
from .forms import FaceForm
from .utils import align_face, send_telegram_message_sync


# Define available face detection models
# These are the pre-trained YOLO models that can be selected for face detection
AVAILABLE_MODELS = {
    "yolov8n": "yolov8n.pt",  # YOLOv8 nano - general object detection
    "yolov8m": "yolov8m.pt",  # YOLOv8 medium - general object detection
    "yolov8n-face": "yolov8n-face.pt",  # YOLOv8 nano - specific for face detection
    "yolov8m-face": "yolov8m-face.pt",  # YOLOv8 medium - specific for face detection
    "yolov8l-face": "yolov8l-face.pt",  # YOLOv8 large - specific for face detection
    "yolov10s-face": "yolov10s-face.pt",  # YOLOv10 small - specific for face detection
    "yolov11m-face": "yolov11m-face.pt",  # YOLOv11 medium - specific for face detection
    "yolov11l-face": "yolov11l-face.pt",  # YOLOv11 large - specific for face detection
}


class FaceRecognitionView(LoginRequiredMixin, View):
    """
    Face detection and recognition API endpoint.

    This is the core functionality of the system. It:
    1. Receives an uploaded image
    2. Uses YOLO to detect faces in the image
    3. Uses DeepFace to recognize detected faces
    4. Sends Telegram notifications for recognized faces
    5. Returns recognition results as JSON

    Authentication is required to access this view.
    """

    def post(self, request):
        """
        Process POST requests with image uploads for face recognition.

        Steps:
        1. Validate uploaded image
        2. Load appropriate face detection model
        3. Process image to detect faces
        4. For each detected face, try to recognize using DeepFace
        5. Send Telegram notifications
        6. Return results as JSON

        Args:
            request: The HTTP request with uploaded image

        Returns:
            JsonResponse: Recognition results in JSON format
        """
        # Get uploaded image from request
        file = request.FILES.get("image")
        if not file:
            return JsonResponse({"error": "No image uploaded"}, status=400)

        # Get model selection from request, default to yolov8n.pt
        model_key = request.POST.get("model", "yolov8n")
        model_path = AVAILABLE_MODELS.get(model_key, AVAILABLE_MODELS["yolov8n"])

        # Initialize model for this request
        model = YOLO(model_path)

        # Convert uploaded file to OpenCV format
        np_img = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Run face detection with YOLO
        results = model(img)
        recognized_people = []

        # Save the input image temporarily for Telegram notifications
        temp_image_path = os.path.join(settings.MEDIA_ROOT, "temp_detection.jpg")
        cv2.imwrite(temp_image_path, img)

        # Process each detected face
        for result in results:
            for box in result.boxes:
                # Extract bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Crop the detected face from the image
                face_img = img[y1:y2, x1:x2]

                # Try to recognize the face using DeepFace
                try:
                    # Align the face to improve recognition accuracy
                    aligned_face = align_face(face_img)

                    # Search for the face in the database
                    df_results = DeepFace.find(
                        aligned_face, db_path="media/faces", model_name="Facenet"
                    )

                    # Check if any matches were found
                    if df_results and len(df_results) > 0 and len(df_results[0]) > 0:
                        # Get the most similar face
                        best_match = df_results[0].iloc[0]

                        # Extract the filename from the path
                        face_path = best_match["identity"]
                        filename = os.path.basename(face_path)

                        # Try to find a matching face in the database
                        try:
                            # Find a face object with matching image filename
                            face_obj = Face.objects.filter(
                                image__contains=filename
                            ).first()

                            if face_obj:
                                # Found matching face in database
                                person_data = {
                                    "id": face_obj.id,
                                    "name": face_obj.name,
                                    "filename": f"/media/faces/{filename}",
                                    "confidence": float(best_match["distance"]),
                                    "box": [int(x1), int(y1), int(x2), int(y2)],
                                    "is_allowed": face_obj.is_allowed,  # Include allowed status
                                }
                                recognized_people.append(person_data)

                                # Customize message based on allowed status
                                access_status = (
                                    "✅ ALLOWED" if face_obj.is_allowed else "⛔ DENIED"
                                )
                                message = f"✨ Face Recognized!\nName: {face_obj.name}\nAccess: {access_status}\nConfidence: {100*(1 - float(best_match['distance'])):.2f}%"
                                send_telegram_message_sync(message, temp_image_path)

                            else:
                                # Found similar face but not in our database
                                person_data = {
                                    "name": "Unknown (Match found but not in database)",
                                    "filename": f"/media/faces/{filename}",
                                    "confidence": float(best_match["distance"]),
                                    "box": [int(x1), int(y1), int(x2), int(y2)],
                                    "is_allowed": False,  # Unknown faces are not allowed by default
                                }
                                recognized_people.append(person_data)

                                # Send Telegram notification for unknown face
                                message = "⚠️ Unknown Face Detected\nMatch found but not in database\nAccess: ⛔ DENIED"
                                send_telegram_message_sync(message, temp_image_path)

                        except Exception as e:
                            # Error matching with database
                            error_data = {
                                "name": "Error matching with database",
                                "error": str(e),
                                "box": [int(x1), int(y1), int(x2), int(y2)],
                            }
                            recognized_people.append(error_data)

                            # Send Telegram notification for error
                            message = f"❌ Error in Face Recognition\nError: {str(e)}"
                            send_telegram_message_sync(message)

                except Exception as e:
                    # Error in DeepFace recognition
                    error_data = {
                        "name": "Unknown",
                        "error": str(e),
                        "box": [int(x1), int(y1), int(x2), int(y2)],
                    }
                    recognized_people.append(error_data)

                    # Send Telegram notification for unrecognized face
                    message = f"❓ Unrecognized Face\nError: {str(e)}"
                    send_telegram_message_sync(message, temp_image_path)

        # Clean up temporary image
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

        # Return recognition results as JSON
        return JsonResponse(
            {
                "status": "success",
                "recognized_people": recognized_people,
                "people_count": len(recognized_people),
            }
        )

    def get(self, request):
        """
        Handle GET requests to the face recognition endpoint.

        This endpoint only accepts POST requests with image uploads,
        so GET requests are rejected with an error.

        Args:
            request: The HTTP request

        Returns:
            JsonResponse: Error message in JSON format
        """
        return JsonResponse({"error": "Invalid request"}, status=400)


# Face CRUD Operations
class FaceListView(LoginRequiredMixin, ListView):
    """
    List view for all faces in the database.

    Displays all stored faces that can be recognized by the system.
    Authentication is required to access this view.
    """

    model = Face  # Model to list
    template_name = "faces/face_list.html"  # Template to render
    context_object_name = "faces"  # Variable name in template

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.

        Args:
            **kwargs: Additional keyword arguments

        Returns:
            dict: Context data for the template
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Manage Faces"  # Page title
        return context


class FaceCreateView(LoginRequiredMixin, CreateView):
    """
    View for adding new faces to the system.

    Allows uploading images of new faces with names for recognition.
    Authentication is required to access this view.
    """

    model = Face  # Model to create
    form_class = FaceForm  # Form for creating faces
    template_name = "faces/face_form.html"  # Template to render
    success_url = reverse_lazy("face_list")  # Redirect after success

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.

        Args:
            **kwargs: Additional keyword arguments

        Returns:
            dict: Context data for the template
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Add New Face"  # Page title
        context["button_text"] = "Add Face"  # Submit button text
        return context

    def form_valid(self, form):
        """
        Process valid form data.

        Creates a new face entry and displays a success message.

        Args:
            form: The validated form

        Returns:
            HttpResponse: Response with success message
        """
        messages.success(self.request, "Face added successfully!")
        return super().form_valid(form)


class FaceUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating existing faces.

    Allows editing face information (name, image).
    Authentication is required to access this view.
    """

    model = Face  # Model to update
    form_class = FaceForm  # Form for updating faces
    template_name = "faces/face_form.html"  # Template to render
    success_url = reverse_lazy("face_list")  # Redirect after success

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.

        Args:
            **kwargs: Additional keyword arguments

        Returns:
            dict: Context data for the template
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Face"  # Page title
        context["button_text"] = "Update Face"  # Submit button text
        return context

    def form_valid(self, form):
        """
        Process valid form data.

        Updates the face entry and displays a success message.

        Args:
            form: The validated form

        Returns:
            HttpResponse: Response with success message
        """
        messages.success(self.request, "Face updated successfully!")
        return super().form_valid(form)


class FaceDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting faces from the system.

    Displays a confirmation page before deleting a face.
    Authentication is required to access this view.
    """

    model = Face  # Model to delete
    template_name = "faces/face_confirm_delete.html"  # Template to render
    success_url = reverse_lazy("face_list")  # Redirect after success

    def delete(self, request, *args, **kwargs):
        """
        Process deletion request.

        Deletes the face and displays a success message.

        Args:
            request: The HTTP request

        Returns:
            HttpResponse: Response with success message
        """
        messages.success(self.request, "Face deleted successfully!")
        return super().delete(request, *args, **kwargs)


class FaceDetailView(LoginRequiredMixin, TemplateView):
    """
    View for displaying details of a specific face.

    Shows all information about a stored face.
    Authentication is required to access this view.
    """

    template_name = "faces/face_detail.html"  # Template to render

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.

        Retrieves the face object and adds it to the context.

        Args:
            **kwargs: Additional keyword arguments including the face PK

        Returns:
            dict: Context data for the template
        """
        context = super().get_context_data(**kwargs)
        # Get the face object or return 404 if not found
        face = get_object_or_404(Face, pk=self.kwargs["pk"])
        context["face"] = face  # Add face to context
        context["title"] = f"Face Details: {face.name}"  # Page title
        return context
