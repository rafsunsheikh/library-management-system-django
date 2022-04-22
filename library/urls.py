from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView



app_name = 'library'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('info-register/', InformationView.as_view(), name='info-register'),


    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='library:login'), name='logout'),

    path('books/', BookView.as_view(), name='book-list'),
    path('book/create/', BookCreate.as_view(), name='book-create'),
    path('book/<slug:pk>/', BookDetail.as_view(), name= 'book'),
    path('book/<slug:pk>/update/', BookUpdate.as_view(), name='book-update'),
    path('book/<slug:pk>/delete/', BookDelete.as_view(), name='book-delete'),



    path('officers/', officerView.as_view(), name='officer-list'),
    path('officer/create/', officerCreate.as_view(), name='officer-create'),
    path('officer/<slug:pk>/', officerDetail.as_view(), name='officer-detail'),
    path('officer/<slug:pk>/update/', officerUpdate.as_view(), name='officer-update'),
    path('officer/<slug:pk>/delete/', officerDelete.as_view(), name='officer-delete'),



    path('borrowers/', BorrowerView.as_view(), name='borrower-list'),
    path('borrower/create/', BorrowerCreate.as_view(), name='borrower-create'),
    path('borrower/<slug:pk>/', BorrowerDetail.as_view(), name= 'borrower'),
    path('borrower/<slug:pk>/update/', BorrowerUpdate.as_view(), name='borrower-update'),
    path('borrower/<slug:pk>/delete/', BorrowerDelete.as_view(), name='borrower-delete'),



]
