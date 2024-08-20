"""Github app Repository model."""

from django.db import models

from apps.common.models import TimestampedModel


class Repository(TimestampedModel):
    """Repository model."""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["key", "owner"], name="unique_key_owner"),
        ]
        db_table = "github_repositories"
        verbose_name_plural = "Repositories"

    name = models.CharField(verbose_name="Name", max_length=100)
    key = models.CharField(verbose_name="Key", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=500, default="")

    default_branch = models.CharField(verbose_name="Default branch", max_length=100, default="")
    homepage = models.CharField(verbose_name="Homepage", max_length=100, default="")
    languages = models.JSONField(verbose_name="Languages", default=dict)
    license = models.CharField(verbose_name="License", max_length=100, default="")
    size = models.PositiveIntegerField(verbose_name="Size in KB", default=0)
    topics = models.JSONField(verbose_name="Topics", default=list)

    is_archived = models.BooleanField(verbose_name="Is archived", default=False)
    is_fork = models.BooleanField(verbose_name="Is fork", default=False)
    is_template = models.BooleanField(verbose_name="Is template", default=False)

    has_downloads = models.BooleanField(verbose_name="Has downloads", default=False)
    has_issues = models.BooleanField(verbose_name="Has issues", default=False)
    has_pages = models.BooleanField(verbose_name="Has pages", default=False)
    has_projects = models.BooleanField(verbose_name="Has projects", default=False)
    has_wiki = models.BooleanField(verbose_name="Has wiki", default=False)

    forks_count = models.PositiveIntegerField(verbose_name="Forks count", default=0)
    open_issues_count = models.PositiveIntegerField(verbose_name="Open issues count", default=0)
    stars_count = models.PositiveIntegerField(verbose_name="Stars count", default=0)
    subscribers_count = models.PositiveIntegerField(verbose_name="Subscribers count", default=0)
    watchers_count = models.PositiveIntegerField(verbose_name="Watchers count", default=0)

    pushed_at = models.DateTimeField(verbose_name="Pushed at")

    original_created_at = models.DateTimeField(verbose_name="Original created_at")
    original_updated_at = models.DateTimeField(verbose_name="Original updated_at")

    # FKs.
    organization = models.ForeignKey(
        "github.Organization",
        verbose_name="Organization",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    owner = models.ForeignKey(
        "github.User",
        verbose_name="Owner",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        """Repository human readable representation."""
        return f"{self.name}"

    @property
    def owasp_url(self):
        """Get OWASP URL for the repository."""
        return f"https://owasp.org/{self.key}"

    def from_github(self, gh_repository, languages=None, organization=None, user=None):
        """Update instance based on GitHub repository data."""
        field_mapping = {
            "default_branch": "default_branch",
            "description": "description",
            "forks_count": "forks_count",
            "has_downloads": "has_downloads",
            "has_issues": "has_issues",
            "has_pages": "has_pages",
            "has_projects": "has_projects",
            "has_wiki": "has_wiki",
            "homepage": "homepage",
            "is_archived": "archived",
            "is_fork": "fork",
            "is_template": "is_template",
            "language": "language",
            "name": "full_name",
            "open_issues_count": "open_issues_count",
            "original_created_at": "created_at",
            "original_updated_at": "updated_at",
            "pushed_at": "pushed_at",
            "size": "size",
            "stars_count": "stargazers_count",
            "subscribers_count": "subscribers_count",
            "topics": "topics",
            "watchers_count": "watchers_count",
        }

        # Direct fields.
        for model_field, response_field in field_mapping.items():
            value = getattr(gh_repository, response_field)
            if value is not None:
                setattr(self, model_field, value)

        # Languages.
        total_size = sum(languages.values())
        self.languages = {
            language: round(size * 100.0 / total_size, 1) for language, size in languages.items()
        }

        # License.
        self.license = gh_repository.license.name

        # Organization.
        self.organization = organization

        # Owner.
        self.owner = user
