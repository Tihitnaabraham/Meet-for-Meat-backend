from django.apps import AppConfig

class KirchagroupsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kirchagroups'

    def ready(self):
        import kirchagroups.signals
