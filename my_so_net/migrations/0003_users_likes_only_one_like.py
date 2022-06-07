# Generated by Django 4.0.4 on 2022-06-07 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_so_net', '0002_rename_post_posts_rename_post_users_likes_posts'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='users_likes',
            constraint=models.UniqueConstraint(fields=('posts', 'user'), name='only_one_like'),
        ),
    ]