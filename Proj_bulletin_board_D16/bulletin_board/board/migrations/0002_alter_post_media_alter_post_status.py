# Generated by Django 4.2.17 on 2025-01-05 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='media',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
