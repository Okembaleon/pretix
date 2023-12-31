# Generated by Django 3.2.18 on 2023-03-22 13:10

from django.db import migrations, models
from django.db.models import Q
from django_scopes import scopes_disabled

from pretix.base.models import Event


@scopes_disabled()
def set_currency(apps, schema_editor):
    BankTransaction = apps.get_model('banktransfer', 'BankTransaction')

    for row in BankTransaction.objects.order_by('organizer', 'event').values('organizer', 'event',
                                                                             'order__event').distinct():
        if row['event'] or row['order__event']:
            currency = Event.objects.get(pk=row['event'] or row['order__event']).currency
            BankTransaction.objects.filter(
                Q(event_id=row['event'] or row['order__event']) | Q(
                    order__event_id=row['event'] or row['order__event']),
                organizer_id=row['organizer'],
            ).update(
                currency=currency
            )
        else:
            currencies = list(
                Event.objects.filter(organizer_id=row['organizer']).order_by('currency').values_list('currency',
                                                                                                     flat=True).distinct())
            if len(currencies) == 1:
                BankTransaction.objects.filter(
                    organizer_id=row['organizer'],
                ).update(
                    currency=currencies[0]
                )

    RefundExport = apps.get_model('banktransfer', 'RefundExport')

    for row in RefundExport.objects.order_by('organizer', 'event').values('organizer', 'event').distinct():
        if row['event']:
            currency = Event.objects.get(pk=row['event']).currency
            RefundExport.objects.filter(
                event_id=row['event'],
                organizer_id=row['organizer'],
            ).update(
                currency=currency
            )
        else:
            currencies = list(
                Event.objects.filter(organizer_id=row['organizer']).order_by('currency').values_list('currency', flat=True).distinct()
            )
            if len(currencies) == 1:
                RefundExport.objects.filter(
                    organizer_id=row['organizer'],
                ).update(
                    currency=currencies[0]
                )


class Migration(migrations.Migration):
    dependencies = [
        ('banktransfer', '0008_alter_banktransaction_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransaction',
            name='currency',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='bankimportjob',
            name='currency',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='refundexport',
            name='currency',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.RunPython(set_currency, migrations.RunPython.noop),
    ]
