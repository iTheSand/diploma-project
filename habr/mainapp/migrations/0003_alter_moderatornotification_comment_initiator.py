# Generated by Django 4.0 on 2022-02-15 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_moderatornotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderatornotification',
            name='comment_initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_initiator', to='mainapp.articlecomment', verbose_name='Comment initiator'),
        ),
    ]