# Generated by Django 3.2.4 on 2021-06-26 08:55

from django.db import migrations
import users.models.user_model


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.models.user_model.UserManager()),
            ],
        ),
    ]