# Generated by Django 3.2.11 on 2022-11-24 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_support', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='messgae_text',
            new_name='message_text',
        ),
    ]