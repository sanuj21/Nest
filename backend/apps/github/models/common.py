"""Github app common models."""

from django.db import models


class GenericUserModel(models.Model):
    """Generic user model."""

    class Meta:
        abstract = True

    name = models.CharField(verbose_name="Name", max_length=200)
    login = models.CharField(verbose_name="Key", max_length=100, unique=True)
    email = models.EmailField(verbose_name="Email", max_length=100, default="")

    avatar_url = models.URLField(verbose_name="Avatar URL", max_length=200, default="")
    company = models.CharField(verbose_name="Company", max_length=200, default="")
    location = models.CharField(verbose_name="Location", max_length=200, default="")

    collaborators_count = models.PositiveIntegerField(
        verbose_name="Collaborators count", default=0
    )
    following_count = models.PositiveIntegerField(verbose_name="Following count", default=0)
    followers_count = models.PositiveIntegerField(verbose_name="Followers count", default=0)
    public_gists_count = models.PositiveIntegerField(verbose_name="Public gists count", default=0)
    public_repositories_count = models.PositiveIntegerField(
        verbose_name="Public repositories count", default=0
    )

    original_created_at = models.DateTimeField(verbose_name="Original created_at")
    original_updated_at = models.DateTimeField(verbose_name="Original updated_at")

    def from_github(self, data):
        """Update instance based on GitHub data."""
        field_mapping = {
            "avatar_url": "avatar_url",
            "collaborators_count": "collaborators",
            "company": "company",
            "email": "email",
            "followers_count": "followers",
            "following_count": "following",
            "location": "location",
            "login": "login",
            "name": "name",
            "original_created_at": "created_at",
            "original_updated_at": "updated_at",
            "public_gists_count": "public_gists",
            "public_repositories_count": "public_repos",
        }

        # Direct fields.
        for model_field, response_field in field_mapping.items():
            value = getattr(data, response_field)
            if value is not None:
                setattr(self, model_field, value)
