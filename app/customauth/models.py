from django.db import models
from photo.models import GifArchive
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from customauth.fields import ThumbnailImageField


class MyUserManager(BaseUserManager):
    def create_user(self, email, nick_name, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            nick_name=nick_name,
            date_of_birth = date_of_birth
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nick_name, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            nick_name=nick_name,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    # choices=[(A, B)] : A는 DB에 들어갈 값, B는 display 용 이름
    gender = models.CharField(max_length=5, choices=[('m', 'Male'), ('f', 'Female')], blank=True)
    date_of_birth = models.DateField()
    nick_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    create_dt = models.DateField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth", "nick_name"]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    # Delete Gif_thumb_path as well when MyUser instance are deleted.
    def delete(self, using=None, keep_parents=False):
        # GIFArchive 인스턴스와 관련된 썸네일 삭제
        gif_archives = GifArchive.objects.filter(owner=self)
        for gif_archive in gif_archives:
            gif_archive.delete()  # 이때 GifArchive 모델의 delete 메서드가 호출됩니다.

        super().delete(using=using, keep_parents=keep_parents)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Profile(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = ThumbnailImageField(upload_to='profile/%Y/%m', default="static/image/default_profile.png")
    description = models.TextField("Profile Description", max_length=100, default='안녕하세요. 반가워요!')

    def __str__(self):
        return str(self.user_id)

class Subscriber(models.Model):
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='following')

    class Meta:
        # One user can only like one gif once
        unique_together = ('current_user', 'following')
    
    def __str__(self):
        return f"{self.current_user} - {self.following}"

# Create a Profile instance automatically when a new MyUser instance is created!
@receiver(post_save, sender=MyUser)
def create_profile_for_myuser(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user_id=instance)

# Update Profile instance if it exists when MyUser is saved
@receiver(post_save, sender=MyUser)
def save_profile_for_myuser(sender, instance, **kwargs):
    instance.profile.save()