# Generated by Django 3.2.8 on 2021-10-15 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_allocation', '0006_peer_edges_projects_pref'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_created',
            field=models.BooleanField(default=False),
        ),
    ]