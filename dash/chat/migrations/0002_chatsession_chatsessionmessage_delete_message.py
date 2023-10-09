# Generated by Django 4.0.5 on 2023-10-06 10:05

import dash.helpers.file
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('members', models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Chat Sessions',
                'ordering': ('-updated',),
            },
        ),
        migrations.CreateModel(
            name='ChatSessionMessage',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to=dash.helpers.file.RandomFileName('chats'))),
                ('is_read', models.BooleanField(default=False)),
                ('chat_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatsession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Chat Session Messages',
            },
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]