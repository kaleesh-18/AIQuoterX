
from django.contrib import admin
from django.urls import path
from myapp import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.employee_crud, name='employee_crud'),  # Map the root URL to employee_crud view
    path('employee_crud/', views.employee_crud, name='employee_crud'),  # If needed, also keep this for another path
]
