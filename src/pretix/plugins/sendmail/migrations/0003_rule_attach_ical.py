# Generated by Django 3.2.18 on 2023-04-13 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendmail', '0002_rule_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='attach_ical',
            field=models.BooleanField(default=False),
        ),
    ]
