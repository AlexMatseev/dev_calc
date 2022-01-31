from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, DetailView

from .forms import ComponentPriceFormSet
from .models import ComponentDict, PriceComponent


class ComponentList(ListView):
    model = ComponentDict
    template_name = 'components/component_list.html'


class ComponentCreate(CreateView):
    model = ComponentDict
    fields = ['component_name', 'sku', 'vendor', 'vendor_pn', 'term_delivery']
    success_url = reverse_lazy('components-list')
    template_name = 'components/component_form.html'

    def get_context_data(self, **kwargs):
        data = super(ComponentCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['component_price'] = ComponentPriceFormSet(self.request.POST)
        else:
            data['component_price'] = ComponentPriceFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        component_price = context['component_price']
        with transaction.atomic():
            self.object = form.save()

            if component_price.is_valid():
                component_price.instance = self.object
                component_price.save()
        return super(ComponentCreate, self).form_valid(form)



class ComponentUpdate(UpdateView):
    model = ComponentDict
    fields = ['component_name', 'sku', 'vendor', 'vendor_pn', 'term_delivery']
    success_url = reverse_lazy('components-list')

    def get_context_data(self, **kwargs):
        data = super(ComponentUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['component_price'] = ComponentPriceFormSet(self.request.POST, instance=self.object)
        else:
            data['component_price'] = ComponentPriceFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        component_price = context['component_price']
        with transaction.atomic():
            self.object = form.save()

            if component_price.is_valid():
                component_price.instance = self.object
                component_price.save()
        return super(ComponentUpdate, self).form_valid(form)


class ComponentDelete(DeleteView):
    model = ComponentDict
    success_url = reverse_lazy('components-list')


class ComponentDetail(DetailView):
    model = ComponentDict
    template_name = 'components/component_detail.html'
    context_object_name = 'component'

    def get_context_data(self, **kwargs):
        context = super(ComponentDetail, self).get_context_data(**kwargs)
        context['component_prices'] = PriceComponent.objects.filter(component=self.object)

        return context