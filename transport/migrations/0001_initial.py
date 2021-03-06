# Generated by Django 3.1.2 on 2020-10-20 21:17

from django.conf import settings
import django.contrib.postgres.constraints
import django.contrib.postgres.fields.ranges
from django.contrib.postgres.operations import BtreeGistExtension
from django.db import migrations, models
import django.db.models.deletion
import django.utils.datetime_safe


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        BtreeGistExtension(),
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=128)),
                ('reserved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BikeStations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='CarParking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('comments', models.TextField()),
                ('date_created', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('bike', models.ManyToManyField(to='transport.Bike')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarParkingReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates_range', django.contrib.postgres.fields.ranges.DateTimeRangeField()),
                ('disabled_space', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.carparking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BikeReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.bike')),
                ('start_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.bikestations')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bike',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.bikestations'),
        ),
        migrations.AddConstraint(
            model_name='carparkingreservation',
            constraint=django.contrib.postgres.constraints.ExclusionConstraint(expressions=[('dates_range', '&&'), ('place', '=')], name='exclude_overlapping_reservations'),
        ),
    ]
