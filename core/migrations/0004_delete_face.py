# Generated by Django 5.1.7 on 2025-03-20 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_face_created_at_alter_face_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Face',
        ),
    ]
