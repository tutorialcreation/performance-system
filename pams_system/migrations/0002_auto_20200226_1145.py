# Generated by Django 2.2.7 on 2020-02-26 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pams_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplist',
            name='state',
            field=models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255),
        ),
        migrations.AddField(
            model_name='maptype',
            name='state',
            field=models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255),
        ),
    ]