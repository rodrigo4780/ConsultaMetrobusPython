# Generated by Django 3.2.4 on 2021-06-30 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alcaldia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='MetrobusData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_data', models.IntegerField(blank=True)),
                ('date_updated', models.DateTimeField(blank=True)),
                ('vehicle_id', models.IntegerField(blank=True)),
                ('vehicle_label', models.IntegerField(blank=True)),
                ('vehicle_current_status', models.IntegerField(blank=True)),
                ('position_latitude', models.FloatField(blank=True)),
                ('position_longitude', models.FloatField(blank=True)),
                ('geographic_point', models.CharField(blank=True, max_length=300)),
                ('position_speed', models.IntegerField(blank=True)),
                ('position_odometer', models.IntegerField(blank=True)),
                ('trip_schedule_relationship', models.IntegerField(blank=True)),
                ('trip_id', models.IntegerField(blank=True)),
                ('trip_start_date', models.DateTimeField(blank=True)),
                ('trip_route_id', models.IntegerField(blank=True)),
                ('id_alcaldia', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='consulta_metrobus.alcaldia')),
            ],
        ),
    ]
