"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Custom Fields --

@author: Informed Solutions
"""


from django import forms
from django.forms import widgets
from django.utils.timezone import now
from django.utils.translation import gettext, gettext_lazy as _
from govuk_forms.widgets import SplitHiddenDateWidget


#Extremely hacky disgusting workaround for expiry date
#Creating a widget class
class Widget(widgets.Widget):
    input_classes = 'form-control'
    input_error_classes = 'form-control-error'

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        css_classes = self.input_classes() if callable(self.input_classes) else self.input_classes
        attrs['class'] = ('%s %s' % (attrs.get('class', ''), css_classes)).strip()
        return attrs

#Creating a base multiwidget class
class MultiWidget(widgets.MultiWidget, Widget):
    subwidget_group_classes = ()
    subwidget_label_classes = ()
    subwidget_labels = ()

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        iterator = zip(context['widget']['subwidgets'],
                       self.subwidget_group_classes,
                       self.subwidget_label_classes,
                       self.subwidget_labels)
        for subwidget, group_classes, label_classes, label in iterator:
            subwidget.update(
                group_classes=group_classes,
                label_classes=label_classes,
                label=label,
            )
        return context

    def decompress(self, value):
        raise NotImplementedError


class ExpirySplitDateWidget(MultiWidget):
    template_name = 'govuk_forms/widgets/split-date.html'
    subwidget_group_classes = ('form-group form-group-month',
                               'form-group form-group-year')
    subwidget_label_classes = ('form-label', 'form-label')  # or form-label-bold
    subwidget_labels = (_('Month'), _('Year'))

    def __init__(self, attrs=None):
        date_widgets = (widgets.NumberInput(attrs=attrs),
                        widgets.NumberInput(attrs=attrs),)
        super().__init__(date_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.month, value.year]
        return [None, None]
    
class YearField(forms.IntegerField):
    """
    In integer field that accepts years between 1900 and now
    Allows 2-digit year entry which is converted depending on the `era_boundary`
    """

    def __init__(self, era_boundary=None, **kwargs):
        self.current_year = now().year
        self.century = 100 * (self.current_year // 100)
        if era_boundary is None:
            # 2-digit dates are a minimum of 10 years ago by default
            era_boundary = self.current_year - self.century - 10
        self.era_boundary = era_boundary
        bounds_error = gettext('The year cannot be in the past') % {
            'current_year': self.current_year
        }
        options = {
            'min_value': self.current_year,
            'error_messages': {
                'min_value': bounds_error,
                'invalid': gettext('Enter year as a number.'),
            }
        }
        options.update(kwargs)
        super().__init__(**options)

    def clean(self, value):
        value = self.to_python(value)
        if isinstance(value, int) and value < 100:
            if value > self.era_boundary:
                value += self.century - 100
            else:
                value += self.century
        return super().clean(value)    




class ExpirySplitDateField(forms.MultiValueField):
    widget = ExpirySplitDateWidget
    hidden_widget = SplitHiddenDateWidget
    default_error_messages = {
        'invalid': _('Enter a valid date.')
    }

    def __init__(self, *args, **kwargs):
        month_bounds_error = gettext('Month should be between 1 and 12.')

        self.fields = [
            forms.IntegerField(min_value=1, max_value=12, error_messages={
                'min_value': month_bounds_error,
                'max_value': month_bounds_error,
                'invalid': gettext('Enter month as a number.')
            }),
            YearField(),
        ]

        super().__init__(self.fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            try:
                if any(item in self.empty_values for item in data_list):
                    raise ValueError
                return (data_list[1], data_list[0])
            except ValueError:
                raise forms.ValidationError(self.error_messages['invalid'], code='invalid')
        return None

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if not isinstance(widget, ExpirySplitDateWidget):
            return attrs
        for subfield, subwidget in zip(self.fields, widget.widgets):
            if subfield.min_value is not None:
                subwidget.attrs['min'] = subfield.min_value
            if subfield.max_value is not None:
                subwidget.attrs['max'] = subfield.max_value
        return attrs