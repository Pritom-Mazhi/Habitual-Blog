from django.db import models
from django.conf import settings

from django.db.models import Q
from django.utils import timezone
# Create your models here.

class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now) #lte->less than or equal | past

    def search(self, query):
        lookup = (
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(user__username__icontains=query)
                    )

        return self.filter(lookup)


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)

# BlogPost.objects.all().filter(publish_date__lte=now) #same below
# self.get_queryset().filter(publish_date__lte=now)

User = settings.AUTH_USER_MODEL
class BlogPost(models.Model): #blogpost_set -> qs to the in 'user'
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)#CASCADE
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BlogPostManager()

    class Meta:
        ordering = ['-publish_date', '-updated', '-timestamp']

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"
        # return f"/blog/{self.slug}/edit" #redundant

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
