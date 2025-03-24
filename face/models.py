from django.db import models


class Face(models.Model):
    """
    Model representing a stored face in the face recognition system.

    Each face record consists of a name for identification and an image file
    that will be used for training and recognition. The model also tracks
    when each face was added to the system.
    """

    # Name of the person whose face is stored
    name = models.CharField(max_length=100)

    # Image file of the person's face, stored in the media/faces directory
    # This image will be used by the DeepFace library for face recognition
    image = models.ImageField(upload_to="faces/")

    # Indicates whether the face is allowed to access the system
    is_allowed = models.BooleanField(
        default=True, help_text="Whether this person is allowed access"
    )

    # Automatically set timestamp when a face is first added to the system
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of a Face instance.
        Returns the name of the person for easy identification in admin interface and queries.
        """
        return self.name
