from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('add/addrecord/', views.addrecord, name='addrecord'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('pop/', views.pop, name='pop'),
    path('modify/<int:id>', views.modify, name='modify'),
    path('modify/modifyRecord/<int:id>', views.modifyRecord, name='modifyRecord'),
    ]
    
