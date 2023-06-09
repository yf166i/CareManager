# Generated by Django 4.1.7 on 2023-02-26 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useroffacility',
            name='address',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='useroffacility',
            name='handicap_level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='useroffacility',
            name='handicap_name',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='useroffacility',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]
