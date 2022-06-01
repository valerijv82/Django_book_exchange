from django.contrib.auth.models import User
from django.db import models
from accounts.models import MyUser
from django.conf import settings
from django.urls import reverse


def upload_to(instance, filename):
    get_user_object = MyUser.objects.filter(email=instance.owner)
    user = get_user_object.get(email=instance.owner)
    # image = ProcessedImageField(upload_to=upload_location,
    #     null=True,
    #     blank=False,
    #     processors=[Transpose(), ResizeToFit(1000, 1000, False)],
    #     format='JPEG',
    #     options={'quality': 50},
    #     width_field="width_field",
    #     height_field="height_field")

    return '{username}/{filename}'.format(username=user.username, filename=filename)


class Book(models.Model):
    GENRE_CHOICES = [
        ('biografija', 'Biografija'),
        ('gamta', 'Gamta'),
        ('grozine literatura', 'Grožinė literatūra'),
        ('humoras ir pramogos', 'Humoras & Pramogos'),
        ('inzinerija ir transportas', 'Inžinerija & Transportas'),
        ('istorija', 'Istorija'),
        ('keliones', 'Kelionės'),
        ('komiksai', 'Komiksai'),
        ('kompiuteriai ir it technologijos', 'Kompiuteriai ir IT technologijos'),
        ('kulinarija', 'Kulinarija'),
        ('medicina', 'Medicina'),
        ('menas', 'Menas'),
        ('mokslas', 'Mokslas'),
        ('moksline fantastika', 'Mokslinė fantastika'),
        ('politika ir socialiniai mokslai', 'Politika ir socialiniai mokslai'),
        ('pomegiai', 'Pomėgiai'),
        ('religija', 'Religija'),
        ('sportas ir aktyvus poilsis', 'Sportas ir aktyvus poilsis'),
        ('sveikata ir dieta', 'Sveikata ir dieta'),
        ('seima', 'Šeima'),
        ('teise', 'Teisė'),
        ('vaikams ir jaunimui', 'Vaikams ir jaunimui'),
        ('verslas', 'Verslas'),
        ('NOT_INCLUDED', 'Kita'),
    ]
    LANGUAGE_CHOICES = [
        ('LT', 'Lietuvių'),
        ('EN', 'Anglų'),
        ('PL', 'Lenkų'),
        ('RU', 'Rusų'),
        ('XX', 'Kita'),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    summary = models.TextField(blank=True, max_length=1000, help_text="Įveskite trumpą knygos aprašymą")
    isbn = models.PositiveBigIntegerField(null=True, blank=True)
    genre = models.CharField(max_length=255, blank=True, choices=GENRE_CHOICES)
    upload = models.ImageField(upload_to=upload_to, max_length=150,
                               blank=True, null=True, default='no_book_image.png')
    language = models.CharField(max_length=150, choices=LANGUAGE_CHOICES, default='LT')
    for_sale = models.BooleanField(help_text="Pardavimas")
    price = models.PositiveIntegerField(blank=True, null=True)
    for_exchange = models.BooleanField(help_text="Apsikeitimas")
    for_donation = models.BooleanField(help_text="Dovana")
    publish = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} | Owner: {self.owner.username}'


    @property
    def user(self):
        return User.objects.get(pk=self.user_id)


    def save(self, *args, **kwargs):
        if not self.upload:
            self.upload = 'media/no_book_image.png'
        super().save(*args, **kwargs)


class Comment(models.Model):
    commented_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    commented_username = models.CharField(max_length=100)
    comment_name = models.CharField(max_length=50, help_text='Komentaro pavadinimas')
    comment_text = models.TextField(max_length=1000, help_text='Komentaro tekstas')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment by {}'.format(self.commented_book)

    # def get_absolute_url(self):
    #     return reverse('home')


# class StarRatingsRating(models.Model):
#     count = models.IntegerField()
#     total = models.IntegerField()
#     average = models.DecimalField(max_digits=6, decimal_places=3)
#     object_id = models.IntegerField(blank=True, null=True)
#     content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'star_ratings_rating'
#         unique_together = (('content_type', 'object_id'),)
#
#
# class StarRatingsUserrating(models.Model):
#     created = models.DateTimeField()
#     modified = models.DateTimeField()
#     ip = models.GenericIPAddressField(blank=True, null=True)
#     score = models.SmallIntegerField()
#     rating = models.ForeignKey(StarRatingsRating, models.DO_NOTHING)
#     user = models.ForeignKey(AccountsMyuser, models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'star_ratings_userrating'
#         unique_together = (('user', 'rating'),)
