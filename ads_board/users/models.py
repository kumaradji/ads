from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    A model representing user profiles.
    Each profile is associated with a User instance using a one-to-one relationship.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Boolean field indicating whether the user is an author.
    is_author = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the user profile.
        Returns the username of the associated User instance.
        """
        return self.user.username
