# Generated by Django 4.0 on 2022-02-04 09:22

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.basemodel')),
                ('title', models.CharField(max_length=60, verbose_name='title')),
                ('subtitle', models.CharField(max_length=100, verbose_name='subtitle')),
                ('main_img', models.ImageField(upload_to='article_images', verbose_name='img')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
            options={
                'db_table': 'article',
                'ordering': ['-created_timestamp'],
            },
            bases=('mainapp.basemodel',),
        ),
        migrations.CreateModel(
            name='ArticleCategories',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.basemodel')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='name categories')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            bases=('mainapp.basemodel',),
        ),
        migrations.CreateModel(
            name='ArticleRating',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.basemodel')),
                ('rating', models.PositiveSmallIntegerField(default=0, verbose_name='rating')),
                ('article_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.user', verbose_name='article_author')),
                ('article_rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_rating', to='mainapp.article', verbose_name='article_for_rating')),
            ],
            options={
                'db_table': 'article_rating',
                'ordering': ['-created_timestamp'],
            },
            bases=('mainapp.basemodel',),
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.basemodel')),
                ('text', models.TextField(max_length=300, verbose_name='Comment text')),
                ('article_comment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_comment', to='mainapp.article', verbose_name='Article for comment')),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comment_author', to='authapp.user', verbose_name='Comment Author')),
            ],
            options={
                'db_table': 'article_comments',
                'ordering': ['-created_timestamp'],
            },
            bases=('mainapp.basemodel',),
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.articlecategories', verbose_name='categories'),
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_author', to='authapp.user', verbose_name='Author article'),
        ),
    ]
