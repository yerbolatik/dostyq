# Generated by Django 5.0.3 on 2024-03-24 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0007_rename_verifield_profile_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='following',
            new_name='followings',
        ),
        migrations.AddField(
            model_name='profile',
            name='friends_visibility',
            field=models.CharField(blank=True, choices=[('Only Me', 'Only Me'), ('Everyone', 'Everyone')], default='Everyone', max_length=100, null=True),
        ),
    ]