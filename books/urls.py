from django.urls import path
from .views import *
from accounts.views import logout, profile

urlpatterns = [
    path('', homepage_books_display, name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('howitworks/', HowItWorksView.as_view(), name='how_it_works'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('mylibrary/', get_my_books, name='mylibrary'),
    path('export_excel', get_my_books_exel_file, name='export-excel'),
    path('export/csv/', export_books_csv, name='export_books_csv'),
    path('communicate/', new_message, name='message'),
    path('communicate/<int:pk>/back', answer_message, name='answer_message'),
    path('mylibrary/<int:pk>/details', show_detail_view, name='book_details'),
    path('mylibrary/<int:pk>/edit', BookEditView.as_view(), name='book_edit'),
    path('mylibrary/<int:pk>/delete', BookDeleteView.as_view(), name='book_delete'),
    path('profile/', profile, name='profile'),
    path('mylibrary/book_register/', BookCreationView.as_view(), name='book_register'),
    path('mylibrary/book_register/success', BookUploadSuccess.as_view(), name='success_upload'),
    path('logout/', logout, name='logout'),
]
