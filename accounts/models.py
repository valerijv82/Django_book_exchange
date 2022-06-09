from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Vartotojai turi turėti el. pašto adresą')
        if not username:
            raise ValueError('Vartotojai turi turėti vartotojo vardą')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):

        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(unique=True, max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    datetime = models.DateField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def user_id(self):
        return self.id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class StarRatingsRating(models.Model):
    id = models.BigAutoField(primary_key=True)
    count = models.IntegerField()
    total = models.IntegerField()
    average = models.DecimalField(max_digits=6, decimal_places=3)
    object_id = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'star_ratings_rating'
        unique_together = (('content_type', 'object_id'),)


class StarRatingsUserrating(models.Model):
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    ip = models.GenericIPAddressField(blank=True, null=True)
    score = models.SmallIntegerField()
    rating = models.ForeignKey(StarRatingsRating, models.DO_NOTHING)
    user = models.ForeignKey(MyUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'star_ratings_userrating'
        unique_together = (('user', 'rating'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
