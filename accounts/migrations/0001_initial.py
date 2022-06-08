# Generated by Django 4.0.4 on 2022-06-02 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StarRatingsRating',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('count', models.IntegerField()),
                ('total', models.IntegerField()),
                ('average', models.DecimalField(decimal_places=3, max_digits=6)),
                ('object_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'star_ratings_rating',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StarRatingsUserrating',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('score', models.SmallIntegerField()),
            ],
            options={
                'db_table': 'star_ratings_userrating',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('datetime', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
