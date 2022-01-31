from django.db import models
from django.urls import reverse


class ComponentDict(models.Model):
    """
    Модель для компонентов устройства
    """
    component_name = models.CharField(max_length=50, verbose_name='Компонент')
    sku = models.CharField(max_length=50, verbose_name='Артикул')
    vendor = models.CharField(max_length=50, verbose_name='Vendor')
    vendor_pn = models.CharField(max_length=50, verbose_name='Vendop P/N')
    term_delivery = models.CharField(max_length=50, verbose_name='Условие доставки')

    def get_absolute_url(self):
        return reverse('component-update', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.component_name}"


class Lots(models.Model):
    """
    Модель партий компонентов и устройств
    """
    lot_name = models.CharField(max_length=50, verbose_name='Тип партии')
    value = models.IntegerField(verbose_name='Значение')

    def __str__(self) -> str:
        return f'{self.lot_name}'


class PriceComponent(models.Model):
    """
    Модель цен компонентов, устройств и сборок.
    """
    component = models.ForeignKey(ComponentDict, on_delete=models.PROTECT, related_name='component_dict', blank=True, null=True, verbose_name='Компонент')
    lot_id = models.ForeignKey(Lots, on_delete=models.PROTECT, verbose_name='Партия', blank=True, null=True)
    price = models.IntegerField(verbose_name='Цена', blank=True, null=True)

    def __str__(self):
        return f'{self.component}'
