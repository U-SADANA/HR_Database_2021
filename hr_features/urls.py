from django.urls import path
from . import views

urlpatterns = [
    path('add_hr/',views.add_hr,name='add_hr'),
    path('show_hr/',views.show_hr,name='show_hr'),
    path('update_hr/<int:id>',views.update_hr,name='update_hr'),
    path('delete_hr/<int:id>',views.delete_hr,name='delete_hr'), 
    path('validate_email_hr',views.validate_email_hr,name='validate_email_hr'), 
    path('validate_phno',views.validate_phno,name='validate_phno'), 
]
