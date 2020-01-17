from django.apps import AppConfig


class MissionsConfig(AppConfig):
    name = 'missions'

    # noinspection PyUnresolvedReferences
    def ready(self):
        import missions.signals  # noqa: F401
