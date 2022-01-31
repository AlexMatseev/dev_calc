from django.db import models
from django.urls import reverse
from components.models import ComponentDict, Lots


class Device(models.Model):
    device_name = models.OneToOneField(ComponentDict, on_delete=models.PROTECT, verbose_name='Устройсво')

    def get_absolute_url(self):
        return reverse('device-update', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.device_name}"


class ComponentDevice(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.PROTECT, related_name='device', verbose_name='Устройство')
    component_id = models.ForeignKey(ComponentDict, on_delete=models.PROTECT, verbose_name='Компонент')
    quantity = models.IntegerField(verbose_name='Количество компонентов в устройстве')

    def __str__(self):
        return f'{self.component_id}'


class CalcDevice(models.Model):
    name_calc = models.CharField(max_length=100, verbose_name='Название сборки')
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
    calc_lot = models.ForeignKey(Lots, on_delete=models.CASCADE, verbose_name='Партия')
    price_calc = models.DecimalField(max_digits=9, decimal_places=3, default=0, null=True, verbose_name='Стоимость')

    def __str__(self) -> str:
        return f'{self.name_calc}'