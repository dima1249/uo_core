from django.apps import AppConfig


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales'
    verbose_name = 'Бараа бүтээгдэхүүн борлуулалт'

    def ready(self):
        from sales.receiver import listen_charge_payment
