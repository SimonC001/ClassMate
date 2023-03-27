from django.apps import AppConfig


class PhotoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photoapp'

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
