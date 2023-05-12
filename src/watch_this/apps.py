from django.apps import AppConfig


class App(AppConfig):
    name = __package__

    def ready(self):
        # Ensure Django registers signals
        import watch_this.signals
