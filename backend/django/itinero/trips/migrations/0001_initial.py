# Generated by Django 4.2.7 on 2023-11-16 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_list', models.TextField()),
                ('hotel', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Trips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeOfTrip', models.CharField(choices=[('upcoming', 'Upcoming'), ('past', 'Past')], max_length=50)),
                ('firstDay', models.DateField()),
                ('lastDay', models.DateField()),
                ('crimeIndex', models.FloatField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=100)),
                ('rating', models.FloatField()),
                ('date', models.DateField()),
                ('time_slot', models.CharField(choices=[(1, 'Breakfast'), (2, 'Mid-Day Activity'), (3, 'Lunch'), (4, 'Evening Activity'), (5, 'Dinner')], max_length=50)),
                ('activity', models.CharField(max_length=100)),
                ('search_keyword', models.CharField(default='', max_length=150)),
                ('place', models.CharField(max_length=200)),
                ('place_list', models.TextField()),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='trips.itinerary')),
            ],
        ),
        migrations.AddField(
            model_name='itinerary',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itinerary', to='trips.trips'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.state'),
        ),
    ]
