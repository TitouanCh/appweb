# Generated by Django 5.1.3 on 2025-02-06 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BioDatabase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('blastn_url', models.URLField(blank=True, null=True)),
                ('blastp_url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
