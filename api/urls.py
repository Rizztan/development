from django.urls import path
from .views import HelloWorld 
from .views import Students
from .views import ContactListView
from .exam_views import ChatView
urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('Students/', Students.as_view(), name='list_student'),
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('chat/', ChatView.as_view(), name='chat_view'),
      
]
