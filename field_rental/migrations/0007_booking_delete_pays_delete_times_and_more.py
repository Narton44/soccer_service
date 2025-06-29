# Generated by Django 5.1.7 on 2025-06-23 16:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field_rental', '0006_alter_fields_indoor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Время начала')),
                ('end_time', models.DateTimeField(verbose_name='Время окончания')),
                ('status', models.CharField(choices=[('pending', 'Ожидает подтверждения'), ('confirmed', 'Подтверждено'), ('canceled', 'Отменено'), ('completed', 'Завершено')], default='pending', max_length=10, verbose_name='Статус бронирования')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания брони')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления брони')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='field_rental.fields', verbose_name='Футбольное поле')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
                'ordering': ['-start_time'],
            },
        ),
        migrations.DeleteModel(
            name='Pays',
        ),
        migrations.DeleteModel(
            name='Times',
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.CheckConstraint(condition=models.Q(('end_time__gt', models.F('start_time'))), name='end_time_after_start_time'),
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.UniqueConstraint(condition=models.Q(('status__in', ['pending', 'confirmed'])), fields=('field', 'start_time', 'end_time'), name='unique_booking_slot'),
        ),
    ]
