# Generated by Django 2.2.1 on 2019-05-22 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='current_city',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='friend',
            name='hometown',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='friend',
            name='moved_here',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
