# Generated by Django 4.0 on 2022-02-17 07:15

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('authapp', '0001_initial'),
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
                ('status', models.CharField(choices=[('D', 'Черновик'), ('A', 'Активная'), ('H', 'Архивная')], default='D', max_length=1, verbose_name='Статус')),
                ('blocked', models.BooleanField(default=False)),
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
            name='ArticleComment',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.basemodel')),
                ('text', models.TextField(max_length=300, verbose_name='Comment text')),
                ('article_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_comment', to='mainapp.article', verbose_name='Article for comment')),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comment_author', to='authapp.user', verbose_name='Comment Author')),
            ],
            options={
                'db_table': 'article_comments',
                'ordering': ['-created_timestamp'],
            },
            bases=('mainapp.basemodel',),
        ),
        migrations.CreateModel(
            name='UUIDTaggedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(db_index=True, verbose_name='object ID')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uuid_tagged_items', to='taggit.tag')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='ModeratorNotification',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.basemodel')),
                ('status', models.CharField(choices=[('N', 'Новая'), ('A', 'Назначена'), ('U', 'На рассмотрении'), ('R', 'Рассмотрена')], default='N', max_length=1, verbose_name='Статус')),
                ('comment_initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_initiator', to='mainapp.articlecomment', verbose_name='Comment initiator')),
                ('responsible_moderator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='responsible_moderator', to='authapp.user', verbose_name='Responsible moderator')),
            ],
            options={
                'db_table': 'moderator_notification',
                'ordering': ['-created_timestamp'],
            },
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
                'ordering': ['rating'],
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
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='mainapp.UUIDTaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_author', to='authapp.user', verbose_name='Author article'),
        ),
    ]
