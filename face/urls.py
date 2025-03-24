from django.urls import path
from .views import (
    FaceRecognitionView,
    FaceListView,
    FaceCreateView,
    FaceUpdateView,
    FaceDeleteView,
    FaceDetailView,
)

urlpatterns = [
    # API endpoint for face detection and recognition
    path("detect/", FaceRecognitionView.as_view(), name="detect"),
    # Face management views (CRUD operations)
    # List all faces in the system
    path("faces/", FaceListView.as_view(), name="face_list"),
    # Add a new face to the system
    path("faces/add/", FaceCreateView.as_view(), name="face_add"),
    # View details of a specific face
    path("faces/<int:pk>/", FaceDetailView.as_view(), name="face_detail"),
    # Update an existing face's information
    path("faces/<int:pk>/update/", FaceUpdateView.as_view(), name="face_update"),
    # Delete a face from the system
    path("faces/<int:pk>/delete/", FaceDeleteView.as_view(), name="face_delete"),
]
