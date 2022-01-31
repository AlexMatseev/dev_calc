from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import DetailView

from .forms import DeviceFormSet, CalcDeviceForm, RegistrationForm, LoginForm
from .models import CalcDevice, Device, ComponentDevice


class DeviceList(ListView):
    model = Device


class DeviceCreate(LoginRequiredMixin, CreateView):
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


class DeviceUpdate(LoginRequiredMixin, UpdateView):
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


class DeviceDelete(LoginRequiredMixin, DeleteView):
    model = Device
    success_url = reverse_lazy('device-list')


class CalcDeviceList(LoginRequiredMixin, ListView):
    model = CalcDevice
    template_name = 'devices/calc_device_list.html'


class CalcDeviceCreate(LoginRequiredMixin, CreateView):
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


class CalcDeviceDetail(LoginRequiredMixin, DetailView):
    model = CalcDevice
    template_name = 'devices/calc_device_detail.html'
    context_object_name = 'calculation'

    def get_context_data(self, **kwargs):
        context = super(CalcDeviceDetail, self).get_context_data(**kwargs)
        context['components'] = ComponentDevice.objects.filter(device_id=self.object.device_id.id)

        return context


class LoginView(View):

    @classmethod
    def get(cls, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'users/login.html', context)

    @classmethod
    def post(cls, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'users/login.html', context)


class RegistrationView(View):

    @classmethod
    def get(cls, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'users/registration.html', context)

    @classmethod
    def post(cls, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = form.cleaned_data['email']
            new_user.username = new_user.email.split('@')[0]
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.set_password(form.cleaned_data['password'])
            user_group = (form.cleaned_data['group'])
            new_user.save()
            user = authenticate(username=new_user.username, password=form.cleaned_data['password'])
            user.save()
            if user_group:
                try:
                    group = Group.objects.get(name=user_group)
                except Group.DoewNotExists:
                    group = None

                if group:
                    group.user_set.add(user)
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'app_users/registration.html', context)


class UserLogoutView(LogoutView):
    next_page = "/"
