from django.conf import settings

TEMPUS_DOMINUS_VERSION = getattr(settings, "TEMPUS_DOMINUS_VERSION", "6.7.16")

TEMPUS_DOMINUS_INCLUDE_ASSETS = getattr(settings, "TEMPUS_DOMINUS_INCLUDE_ASSETS", True)

TEMPUS_DOMINUS_LOCALIZE = getattr(settings, "TEMPUS_DOMINUS_LOCALIZE", False)

TEMPUS_DOMINUS_DATE_FORMAT = getattr(
    settings, "TEMPUS_DOMINUS_DATE_FORMAT", "yyyy-MM-dd"
)

TEMPUS_DOMINUS_DATETIME_FORMAT = getattr(
    settings, "TEMPUS_DOMINUS_DATETIME_FORMAT", "yyyy-MM-dd HH:mm:ss"
)

TEMPUS_DOMINUS_TIME_FORMAT = getattr(settings, "TEMPUS_DOMINUS_TIME_FORMAT", "HH:mm:ss")

TEMPUS_DOMINUS_CSS_CLASS = getattr(settings, "TEMPUS_DOMINUS_CSS_CLASS", "form-control")

TEMPUS_DOMINUS_ICON_PACK = getattr(settings, "TEMPUS_DOMINUS_ICON_PACK", "fa_five")
