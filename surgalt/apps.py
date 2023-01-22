from django.apps import AppConfig
# from surgalt.receiver import *

class SurgaltConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'surgalt'
    verbose_name = 'Сургалт'

    def ready(self):
        from surgalt.receiver import update_course_student

