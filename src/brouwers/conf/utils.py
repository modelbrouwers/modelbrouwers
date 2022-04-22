from decouple import Csv, config as _config, undefined
from sentry_sdk.integrations import DidNotEnable, django


def config(option: str, default=undefined, *args, **kwargs):
    if "split" in kwargs:
        kwargs.pop("split")
        kwargs["cast"] = Csv()

    if default is not undefined and default is not None:
        kwargs.setdefault("cast", type(default))
    return _config(option, default=default, *args, **kwargs)


def get_sentry_integrations() -> list:
    """
    Determine which Sentry SDK integrations to enable.
    """
    default = [
        django.DjangoIntegration(),
        # redis.RedisIntegration(),
    ]
    extra = []

    try:
        from sentry_sdk.integrations import celery
    except DidNotEnable:  # happens if the celery import fails by the integration
        pass
    else:
        extra.append(celery.CeleryIntegration())

    return [*default, *extra]
