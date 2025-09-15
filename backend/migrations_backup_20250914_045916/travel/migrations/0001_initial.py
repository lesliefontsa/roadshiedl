import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('role', models.CharField(default='client', max_length=10)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_number', models.CharField(max_length=20)),
                ('bus_model', models.CharField(max_length=100)),
                ('total_seats', models.PositiveIntegerField()),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(default='disponible', max_length=20)),
                ('mileage', models.PositiveIntegerField(default=0)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_city', models.CharField(max_length=100)),
                ('arrival_city', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('duration', models.CharField(blank=True, max_length=20, null=True)),
                ('available_seats', models.PositiveIntegerField(default=0)),
                ('price_simple', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_return', models.DecimalField(decimal_places=2, max_digits=10)),
                ('notes', models.TextField(blank=True, null=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.bus')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number', models.CharField(max_length=50)),
                ('client_email', models.EmailField(max_length=254)),
                ('seats', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('trip_type', models.CharField(max_length=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_intent_id', models.CharField(blank=True, max_length=100, null=True)),
                ('card_last4', models.CharField(blank=True, max_length=4, null=True)),
                ('card_brand', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(default='confirmed', max_length=20)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='travel.trip')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.customuser')),
            ],
        ),
    ]
