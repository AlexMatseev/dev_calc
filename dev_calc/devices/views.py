from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import DetailView

from .forms import DeviceFormSet, CalcDeviceForm
from .models import CalcDevice, Device, ComponentDevice


class DeviceList(ListView):
    model = Device


class DeviceCreate(CreateView):
    model = Device
    fields = ['device_name']
    success_url = reverse_lazy('device-list')

    def get_context_data(self, **kwargs):
        data = super(DeviceCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['familymembers'] = DeviceFormSet(self.request.POST)
        else:
            data['familymembers'] = DeviceFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(DeviceCreate, self).form_valid(form)


class DeviceUpdate(UpdateView):
    model = Device
    fields = ['first_name']
    success_url = reverse_lazy('device-list')

    def get_context_data(self, **kwargs):
        data = super(DeviceUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['familymembers'] = DeviceFormSet(self.request.POST, instance=self.object)
        else:
            data['familymembers'] = DeviceFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(DeviceUpdate, self).form_valid(form)


class DeviceDelete(DeleteView):
    model = Device
    success_url = reverse_lazy('device-list')


class CalcDeviceList(ListView):
    model = CalcDevice
    template_name = 'devices/calc_device_list.html'


class CalcDeviceCreate(CreateView):
    model = CalcDevice
    form_class = CalcDeviceForm
    template_name = 'devices/calc_device_form.html'
    success_url = reverse_lazy('calc_device-list')

    def form_valid(self, form):
        self.object = form.save()
        all_prices = 0
        device_prices = ComponentDevice.objects.filter(device_id=self.object.device_id.id)
        for component in device_prices.all():
            for i in component.component_id.component_dict.all():
                if i.lot_id.value == self.object.calc_lot.value:
                    all_prices += i.price * component.quantity
        self.object.price_calc = all_prices
        return super(CalcDeviceCreate, self).form_valid(form)


class CalcDeviceDetail(DetailView):
    model = CalcDevice
    template_name = 'devices/calc_device_detail.html'
    context_object_name = 'calculation'

    def get_context_data(self, **kwargs):
        context = super(CalcDeviceDetail, self).get_context_data(**kwargs)
        context['components'] = ComponentDevice.objects.filter(device_id=self.object.device_id.id)

        return context
