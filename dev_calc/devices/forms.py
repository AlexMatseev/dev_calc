from django.forms import ModelForm, inlineformset_factory

from .models import  CalcDevice, Device, ComponentDevice


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        exclude = ()


class FamilyMemberForm(ModelForm):
    class Meta:
        model = ComponentDevice
        exclude = ()


DeviceFormSet = inlineformset_factory(Device, ComponentDevice,
                                            form=FamilyMemberForm, extra=1)


class CalcDeviceForm(ModelForm):
    class Meta:
        model = CalcDevice
        exclude = ('price_calc', )