from django.apps import AppConfig

from utils.ai_helper import warm_ai_cache
# from ai_service import warm_ai_cache


class EmployeeClientStudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee_Client_student'


class YourAppConfig(AppConfig):
    def ready(self):
        warm_ai_cache()   # server start hote hi site fetch ho jaayegi
