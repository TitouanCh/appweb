# Generated by Django 5.1.3 on 2025-02-06 19:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('annotation', '0001_initial'),
        ('genhome', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='sequence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to='genhome.fasequence'),
        ),
        migrations.AddField(
            model_name='feature',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='feature', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feature',
            name='sequence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature', to='genhome.fasequence'),
        ),
    ]
