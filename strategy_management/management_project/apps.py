from django.apps import AppConfig


class PayrollManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'management_project'



    def ready(self):
        import management_project.signals  # adjust this path accordingly
