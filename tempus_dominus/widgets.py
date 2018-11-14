from datetime import datetime
import json

from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.formats import get_format
from django.utils.translation import get_language
from django.conf import settings
from django.template.loader import render_to_string


def cdn_media():
    css = {
        'all': (
            '//cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.0.1/css/tempusdominus-bootstrap-4.min.css',
        ),
    }

    if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
        moment = "moment-with-locales"
    else:
        moment = "moment"

    js = (
        ('//cdnjs.cloudflare.com/ajax/libs/moment.js/2.22.2/'
         '{moment}.min.js'.format(moment=moment)),
        ('//cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/'
         '5.0.1/js/tempusdominus-bootstrap-4.min.js'),
    )

    return forms.Media(css=css, js=js)


class TempusDominusMixin:

    def __init__(self, attrs=None, options=None):
        super().__init__()

        # Set default options to include a clock item, otherwise datetimepicker shows no icon to switch intto time mode
        self.js_options = {'format': self.get_js_format(),
                           'icons': {'time': 'fa fa-clock'}
                           }
        # If a dictionary of options is passed, combine it with our pre-set js_options.
        if isinstance(options, dict):
            self.js_options = {**self.js_options, **options}
        # save any additional attributes that the user defined in self
        self.attrs = attrs or {}

    @property
    def media(self):
        if getattr(settings, 'TEMPUS_DOMINUS_INCLUDE_ASSESTS', True):
            return cdn_media()

    def render(self, name, value, attrs=None, renderer=None):
        context = super().get_context(name, value, attrs)

        # self.attrs = user-defined attributes from __init__
        # attrs = attributes added for rendering.
        # context['attrs'] contains a merge of self.attrs and attrs
        # NB If crispy forms is used, it will already contain 'class': 'datepicker form-control' for DatePicker widget

        all_attrs = context['widget']['attrs']
        cls = all_attrs.get('class', '')
        if 'form-control' not in cls:
            cls = 'form-control ' + cls
        # Add the attribute that makes datepicker popup close when focus is lost
        cls += ' datetimepicker-input'
        all_attrs['class'] = cls

        # defaults for our widget attributes
        input_toggle = True
        icon_toggle = True
        append = ''
        prepend = ''
        size = ''

        attr_html = ''
        for attr_key, attr_value in all_attrs.items():
            if attr_key == 'prepend':
                prepend = attr_value
            elif attr_key == 'append':
                append = attr_value
            elif attr_key == 'input_toggle':
                input_toggle = attr_value
            elif attr_key == 'icon_toggle':
                icon_toggle = attr_value
            elif attr_key == 'size':
                size = attr_value
            elif attr_key == 'icon_toggle':
                icon_toggle = attr_value
            else:
                attr_html += ' {key}="{value}"'.format(
                    key=attr_key,
                    value=attr_value,
                )

        if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False) and 'locale' not in self.js_options:
            self.js_options['locale'] = get_language()

        options = {}
        options.update(self.js_options)
        if context['widget']['value'] is not None:
            # Append an option to set the datepicker's value using a Javascript moment object
            options.update(self.moment_option(value))

        field_html = render_to_string('tempus_dominus/widget.html', {
            'type': context['widget']['type'],
            'picker_id': context['widget']['attrs']['id'],
            'name': context['widget']['name'],
            'attrs': mark_safe(attr_html),
            'js_options': mark_safe(json.dumps(options)),
            'prepend': prepend,
            'append': append,
            'icon_toggle': icon_toggle,
            'input_toggle': input_toggle,
            'size': size,
        })
        return mark_safe(force_text(field_html))

    def moment_option(self, value):
        """
        Returns an option dict to set the default date and/or time using a Javascript moment object.
        When a form is first instantiated, value is a date, time or datetime object,
        but after a form has been submitted with an error and re-rendered, value contains a formatted string that
        we need to parse back to a date, time or datetime object.

        """
        if isinstance(value, str):
            if isinstance(self, DatePicker):
                formats = 'DATE_INPUT_FORMATS'
            elif isinstance(self, TimePicker):
                formats = 'TIME_INPUT_FORMATS'
            else:
                formats = 'DATETIME_INPUT_FORMATS'
            for fmt in get_format(formats):
                try:
                    value = datetime.strptime(value, fmt)
                    break
                except (ValueError, TypeError):
                    continue
            else:
                return {}
        # Append an option to set the datepicker's value
        # This only works for Date or DateTime, not Time alone.
        # NB returning defaultDate causes a javascript error
        return {'date': value.isoformat()}

    def get_js_format(self):
        raise NotImplementedError


class DatePicker(TempusDominusMixin, forms.widgets.DateInput):
    def get_js_format(self):
        if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
            js_format = 'L'
        else:
            js_format = 'YYYY-MM-DD'
        return js_format


class DateTimePicker(TempusDominusMixin, forms.widgets.DateTimeInput):
    def get_js_format(self):
        if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
            js_format = 'L LTS'
        else:
            js_format = 'YYYY-MM-DD HH:mm:ss'
        return js_format


class TimePicker(TempusDominusMixin, forms.widgets.TimeInput):
    def get_js_format(self):
        if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
            js_format = 'LTS'
        else:
            js_format = 'HH:mm:ss'
        return js_format
