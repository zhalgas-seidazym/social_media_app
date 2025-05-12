from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib
import time
from django.conf import settings

def profile_path(instance, filename: str) -> str:
    """
    Generate a unique path for profile pictures using MinIO storage.
    """
    extension = filename.split(".").pop()
    directory_name = f"profile/{instance.username}_{instance.id}"
    hash = hashlib.md5(str(time.time()).encode()).hexdigest()
    return f"{directory_name}/{hash}.{extension}"


def cover_image_path(instance, filename: str) -> str:
    """
    Generate a unique path for cover images using MinIO storage.
    """
    extension = filename.split(".").pop()
    directory_name = f"profile/cover/{instance.username}_{instance.id}"
    hash = hashlib.md5(str(time.time()).encode()).hexdigest()
    return f"{directory_name}/{hash}.{extension}"


class User(AbstractUser):
    profile_pic = models.ImageField(upload_to=default_storage, null=True, blank=True)
    cover_pic = models.ImageField(storage=default_storage, null=True, blank=True)

    # Two ManyToManyField with custom through models
    following = models.ManyToManyField(
        'self',
        through='UserFollowing',
        related_name='user_following',
        symmetrical=False
    )
    followers = models.ManyToManyField(
        'self',
        through='UserFollower',
        related_name='user_followers',
        symmetrical=False
    )

    @property
    def profile_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        return ""

    @property
    def cover_pic_url(self):
        if self.cover_pic:
            return self.cover_pic.url
        return ""


class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='follower_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'following_user')
        indexes = [
            models.Index(fields=['user', 'following_user']),
        ]


class UserFollower(models.Model):
    user = models.ForeignKey(User, related_name='followers_set', on_delete=models.CASCADE)
    follower_user = models.ForeignKey(User, related_name='followed_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'follower_user')
        indexes = [
            models.Index(fields=['user', 'follower_user']),
        ]
