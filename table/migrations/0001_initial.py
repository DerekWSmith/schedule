# Generated by Django 4.1 on 2022-09-05 07:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', models.TextField(blank=True, default='', null=True)),
                ('render_type', models.IntegerField(blank=True, choices=[(10, 'date'), (30, 'public holiday'), (50, 'all day'), (70, 'default')], null=True)),
                ('start', models.DateTimeField(default=datetime.datetime(2022, 9, 5, 7, 11, 38, 737132, tzinfo=datetime.timezone.utc))),
                ('week', models.CharField(blank=True, max_length=2, null=True)),
                ('end', models.DateTimeField(default=datetime.datetime(2022, 9, 5, 7, 11, 38, 737160, tzinfo=datetime.timezone.utc))),
                ('location', models.CharField(blank=True, default='none', max_length=100, null=True)),
                ('address', models.CharField(blank=True, default='none', max_length=100, null=True)),
                ('resource', models.CharField(blank=True, default='none', max_length=100, null=True)),
                ('repeat_every', models.IntegerField(blank=True, default=0, null=True)),
                ('alert_options', models.CharField(blank=True, default='none', max_length=100, null=True)),
                ('dependant_upon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventdependson', to='table.event')),
                ('required_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventrequiredby', to='table.event')),
            ],
            options={
                'db_table': 'event',
                'ordering': ['start', 'render_type'],
            },
        ),
    ]
