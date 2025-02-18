from django.urls import path
from .views import employee_crud

urlpatterns = [
    path('', employee_crud, name='employee_crud'),
]
