from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from .models import Book, Comment, Message
from .forms import CommentForm, NewMessageForm
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib import messages
import xlwt
import csv

User = get_user_model()

getting_owner_id = 0


def answer_message(request, pk):
    form = NewMessageForm
    messaga = Message.objects.get(id=pk)  # get instance of this message
    get_this_message_sender_id = messaga.author_id  # this message owner_id number int
    message_content = messaga.content  # get content
    get_sender_id = User.objects.get(id=get_this_message_sender_id)  # user instance of this message
    if request.method == 'POST':
        form = NewMessageForm(data=request.POST)
        if form.is_valid():
            form.instance.author_id = request.user.id  # assign authenticated user.username to new comment (to know who commented)
            form.instance.recipient = get_sender_id.id  # assign this book.id , can't be Null, and for filter in future
            form.save()
            form = NewMessageForm()
            messages.add_message(request, messages.SUCCESS, "Atsakymas išsiųstas")
        else:
            form = NewMessageForm()
    context = {
        'form': form,
        'sender_username': get_sender_id,
        'content': message_content
    }
    return render(request, 'answer_message.html', context)


def new_message(request):

    form = NewMessageForm
    if request.method == 'POST':
        form = NewMessageForm(data=request.POST)
        get_book_owner_id = User.objects.get(id=getting_owner_id)
        if form.is_valid():
            form.instance.author_id = request.user.id
            form.instance.recipient = get_book_owner_id.id
            form.save()
            form = NewMessageForm
            messages.add_message(request, messages.SUCCESS, "Žinutė išsiųsta")
        else:
            form = NewMessageForm
    context = {
        'form': form,
    }
    return render(request, 'new_message.html', context)


def show_detail_view(request, pk):
    new_comment = None
    global getting_owner_id
    comment_form = CommentForm()
    book = Book.objects.get(id=pk)  # instance of this book
    getting_owner_id = book.owner_id  # this book owner_id number int
    all_this_book_comments = Comment.objects.filter(commented_book=pk).order_by(
        '-created')  # getting all comments of this book
    username = request.user.username  # authenticated user
    getting_owner_user = User.objects.get(id=getting_owner_id)  # user instance of this book
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.commented_username = username  # assign authenticated user.username to new comment (to know who commented)
            comment_form.instance.commented_book_id = book.id  # assign this book.id , can't be Null, and for filter in future
            comment_form.save()
            comment_form = CommentForm()
        else:
            comment_form = CommentForm()
    context = {
        'book': book,
        'user_owner': getting_owner_user,
        'commented_username': username,
        'comment_form': comment_form,
        'all_this_book_comments': all_this_book_comments,
        'new_comment': new_comment
    }
    return render(request, 'book_details.html', context)


def homepage_books_display(request):
    data = Book.objects.all()
    if request.method == 'GET':
        query = request.GET.get('q', None)
        if query:
            data = Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(isbn__icontains=query) |
                Q(genre__icontains=query)
            ).order_by('-publish')
    context = {
        'data': data
    }
    return render(request, 'home.html', context)


class BookEditView(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'upload', 'language',
              'for_sale', 'price', 'for_exchange', 'for_donation']
    template_name = 'book_edit.html'
    success_url = reverse_lazy('mylibrary')


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('mylibrary')


class BookDetailView(DetailView):
    model = Book
    fields = ('title', 'author', 'summary', 'isbn', 'genre', 'upload', 'language',
              'for_sale', 'price', 'for_exchange', 'for_donation',)
    template_name = 'book_details.html'


class BookCreationView(CreateView):
    model = Book
    fields = ('title', 'author', 'summary', 'isbn', 'genre', 'upload', 'language',
              'for_sale', 'price', 'for_exchange', 'for_donation',)
    success_url = reverse_lazy('success_upload')
    template_name = "book_register.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def get_my_books(request):
    user = request.user.id
    data = Book.objects.filter(owner_id=user)
    return render(request, 'mylibrary.html', {'data': data})


def export_books_csv(request):
    user = request.user.id
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Author', 'Summary', 'ISBN', 'Genre',
                     'Language', 'For sale', 'Price', 'For exchange', 'For donation'])

    books = Book.objects.filter(owner_id=user).values_list('title', 'author', 'summary',
                                                           'isbn', 'genre', 'language',
                                                           'for_sale', 'price', 'for_exchange',
                                                           'for_donation')
    for book in books:
        writer.writerow(book)
    return response


def get_my_books_exel_file(request):
    user = request.user.id
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="books.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Books')
    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Title', 'Author', 'Summary', 'ISBN', 'Genre',
               'Language', 'For sale', 'Price', 'For exchange', 'For donation', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Book.objects.filter(owner_id=user).values_list('title', 'author', 'summary',
                                                          'isbn', 'genre', 'language',
                                                          'for_sale', 'price', 'for_exchange',
                                                          'for_donation')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


class BookUploadSuccess(TemplateView):
    template_name = 'book_upload_success.html'


class HomePageView(TemplateView):
    template_name = 'home.html'


class MyLibraryPageView(TemplateView):
    template_name = 'mylibrary.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class HowItWorksView(TemplateView):
    template_name = 'how_it_works.html'


class FeedbackView(TemplateView):
    template_name = 'feedback.html'
