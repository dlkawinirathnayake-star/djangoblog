
from django.db import models
from django.utils.text import slugify
from PIL import Image
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    cover_image = models.ImageField(
        upload_to="post_covers/",
        blank=True,
        null=True
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    content = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        # Automatically create a unique slug
        if not self.slug:
            base_slug = slugify(self.title) or "post"
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # Save the post first
        super().save(*args, **kwargs)

        # Resize the cover image if necessary
        if self.cover_image:
            img_path = self.cover_image.path

            with Image.open(img_path) as img:
                if img.height > 800 or img.width > 800:
                    img.thumbnail((800, 800))
                    img.save(img_path)

    def __str__(self):
        return self.title



# Create your models here.
