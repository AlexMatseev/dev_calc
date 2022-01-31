# Generated by Django 2.2.10 on 2021-12-15 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('components', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='components.ComponentDict', verbose_name='Устройсво')),
            ],
        ),
        migrations.CreateModel(
            name='ComponentDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Количество компонентов в устройстве')),
                ('component_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='components.ComponentDict', verbose_name='Компонент')),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='device', to='devices.Device', verbose_name='Устройство')),
            ],
        ),
        migrations.CreateModel(
            name='CalcDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_calc', models.CharField(max_length=100, verbose_name='Название сборки')),
                ('price_calc', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True, verbose_name='Стоимость')),
                ('calc_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Lots', verbose_name='Партия')),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Device', verbose_name='Устройство')),
            ],
        ),
    ]
