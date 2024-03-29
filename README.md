# Django Tempus Dominus

Django Tempus Dominus provides Django widgets for the [Tempus Dominus v6](https://getdatepicker.com/ "Tempus Dominus") date and time picker.

## Installation

* From PyPI: `pip install django-tempus-dominus`

Then add `tempus_dominus` to `INSTALLED_APPS` in your Django settings.

## Usage & Django Settings

The following settings are available:

* `TEMPUS_DOMINUS_LOCALIZE` (default: `False`): if `True`, widgets will be translated to the selected browser language and use the localized date and time formats.
* `TEMPUS_DOMINUS_INCLUDE_ASSETS` (default: `True`): if `True`, loads Tempus Dominus and `moment` JS and CSS from Cloudflare's CDN, otherwise loading the JS and CSS is up to you.
* `TEMPUS_DOMINUS_DATE_FORMAT` (default: `yyyy-MM-dd`)
* `TEMPUS_DOMINUS_DATETIME_FORMAT` (default: `yyyy-MM-dd HH:mm:ss`)
* `TEMPUS_DOMINUS_TIME_FORMAT` (default: `HH:mm:ss`)
* `TEMPUS_DOMINUS_CSS_CLASS` (default: `form-control`): this CSS class will be applied to the form input, defaulting to Bootstrap's `form-control`. It can be overridden by passing `attrs` during instantiation.
* `TEMPUS_DOMINUS_ICON_PACK` (default: `fa_five`): the icon pack to use. Accepted values:
    * `fa_five`: FontAwesome 5
    * `bi_one`: Bootstrap Icons 1

Three widgets are provided:

* `DatePicker`
    * Defaults to `L` if `TEMPUS_DOMINUS_LOCALIZE` is `True`, otherwise `TEMPUS_DOMINUS_DATE_FORMAT`
* `DateTimePicker`
    * Defaults to `L LTS` if `TEMPUS_DOMINUS_LOCALIZE` is `True`, otherwise `TEMPUS_DOMINUS_DATETIME_FORMAT`
* `TimePicker`
    * Defaults to `LTS` if `TEMPUS_DOMINUS_LOCALIZE` is `True`, otherwise `TEMPUS_DOMINUS_TIME_FORMAT`

In your Django form, you can use the widgets like this:

```python
from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

class MyForm(forms.Form):
    date_field = forms.DateField(widget=DatePicker())
    date_field_required_with_min_max_date = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                'restrictions': {
                    'minDate': '2009-01-20',
                    'maxDate': '2017-01-20',
                }
            },
        ),
        initial='2013-01-01',
    )
    """
    In this example, the date portion of `defaultDate` is irrelevant;
    only the time portion is used. The reason for this is that it has
    to be passed in a valid MomentJS format. This will default the time
    to be 14:56:00 (or 2:56pm).
    """
    time_field = forms.TimeField(
        widget=TimePicker(
            options={
                'defaultDate': '1970-01-01T14:56:00',
                'restrictions': {
                    'enabledHours': [9, 10, 11, 12, 13, 14, 15, 16]
                }
            },
        ),
    )
    datetime_field = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
            },
        ),
    )
```

Then in your template, include jQuery, `{{ form.media }}`, and render the form:

```HTML+Django
<html>
  <head>
    {# Django Tempus Dominus assets are included in `{{ form.media }}` #}
    {{ form.media }}
  </head>
  
  <body>
    <div class="container">
      <div class="row">
        <div class="col">
          <form method="post" action=".">
            {% csrf_token %}
            {{ form.as_p }}
          </form>
        </div>
      </div>
    </div>
  </body>
</html>
```

## Widget Options

* `options` (dictionary): This dictionary will be passed to Tempus Dominus. [A full list of options is available here](https://getdatepicker.com/6/options/).
* `input_toggle` (boolean, default `True`): Controls whether clicking on the input field toggles the datepicker popup. Typically is set to False when an icon is in use.
* `input_group` (boolean, default `True`): Whether to include a Bootstrap 4 `input-group` around the picker.
* `size` (string): Controls the size of the input group (`small` or `large`). Defaults to the default size.
* `prepend` (string): Name of a Font Awesome icon to prepend to the input field (`fa fa-calendar`).
* `append` (string): Name of a Font Awesome icon to append to the input field (`fa fa-calendar`).
* `icon_toggle` (boolean, default `True`): Controls whether clicking on the icon toggles the datepicker popup. Typically is set to False when an icon is in use.

## Release Notes and Contributors

* [Release notes](https://github.com/flipperpa/django-tempus-dominus/releases)
* [Our wonderful contributors](https://github.com/flipperpa/django-tempus-dominus/graphs/contributors)

## Maintainers

* Timothy Allen (https://github.com/FlipperPA)
* Ian Stewart (https://github.com/ianastewart)

This package is largely maintained by the staff of [Wharton Research Data Services](https://wrds.wharton.upenn.edu/). We are thrilled that [The Wharton School](https://www.wharton.upenn.edu/) allows us a certain amount of time to contribute to open-source projects. We add features as they are necessary for our projects, and try to keep up with Issues and Pull Requests as best we can. Due to time constraints (our full time jobs!), Feature Requests without a Pull Request may not be implemented, but we are always open to new ideas and grateful for contributions and our package users.
