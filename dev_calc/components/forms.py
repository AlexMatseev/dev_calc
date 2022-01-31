from django.forms import ModelForm, inlineformset_factory

from .models import  ComponentDict, PriceComponent


class ComponentForm(ModelForm):
    class Meta:
        model = ComponentDict
        exclude = ()


class ComponentPriceForm(ModelForm):
    class Meta:
        model = PriceComponent
        exclude = ()


ComponentPriceFormSet = inlineformset_factory(ComponentDict, PriceComponent,
                                            form=ComponentPriceForm, extra=1)