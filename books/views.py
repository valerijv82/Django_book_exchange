from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from .models import Book, Comment, Message
from .forms import CommentForm, BookEditForm, NewMessageForm
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib import messages


User = get_user_model()

getting_owner_id = 0


class NewMessageView(CreateView):
    model = Message
    fields = ('content',)
    success_url = reverse_lazy('home')
    template_name = "new_message.html"



def new_message(request):
    message = Message
    content = None

    form = NewMessageForm
    if request.method == 'POST':
        form = NewMessageForm(data=request.POST)
        get_book_owner_id = User.objects.get(id=getting_owner_id)
        print(get_book_owner_id.id)
        if form.is_valid():
            form.instance.author_id = request.user.id
            form.instance.recipient = get_book_owner_id.id
            form.save()
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
    # gl = User.objects.filter(id=getting_owner_id)  # user instance of this book
    # print(gl.instance.id)
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


def fetch_messages(request):
    model = Message


def homepage_books_display(request):
    data = Book.objects.all()
    if request.method == 'GET':
        query = request.GET.get('q', None)
        if query:
            data = Book.objects.filter(
                # genre=Book.GENRE_CHOICES.query |
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
    # form = BookEditForm
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'upload', 'language',
              'for_sale', 'price', 'for_exchange', 'for_donation']
    template_name = 'book_edit.html'
    success_url = reverse_lazy('mylibrary')


# def book_delete(request):
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
        q = self.request.user.username
        return super().form_valid(form)


def get_my_books(request):
    user = request.user.id
    data = Book.objects.filter(owner_id=user)
    return render(request, 'mylibrary.html', {'data': data})


# def get_my_books(request):
#     user = request.user.id
#     # data = Book.objects.filter(owner_id=user)
#     data = Book.objects.all()
#     print(data.values())
#     print(user)
#     return render(request, 'mylibrary.html', {'data': data})


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

# class BookCreationView(LoginRequiredMixin, CreateView):
#     model = Book
#     fields = '__all__'
#     # exclude = ['owner']
#     success_url = reverse_lazy('success_upload')
#     template_name = "book_register.html"
#
#     def get_form_class(self):
#         modelform = super().get_form_class()
#         modelform.base_fields['owner'].limit_choices_to = {'id': self.request.user.id}
#         # modelform.base_fields['owner'] = self.request.user.id
#         return modelform


# def index(request ):
#     # book_objects = Book.objects.all()
#     # instance = MyUser.objects.get(id=request.user.id)
#
#     book = Book()
#     if request.method == 'POST':
#         current_user = request.user
#         # print(user.id)
#         # print(current_user.pk)
#         form = BooksForm(request.POST or None)
#
#         if form.is_valid():
#             form.owner = current_user
#             book.owner = form.owner
#             # print(dir(form.cleaned_data))
#             # book.owner = form.cleaned_data.get(form.owner)
#             book.author = form.cleaned_data.get("author")
#             book.title = form.cleaned_data.get("title")
#             book.summary = form.cleaned_data.get("summary")
#             book.isbn = form.cleaned_data.get("isbn")
#             book.enre = form.cleaned_data.get("genre")
#             book.upload = form.cleaned_data.get("upload")
#             book.language = form.cleaned_data.get("language")
#             book.for_sale = form.cleaned_data.get("for_sale")
#             book.price = form.cleaned_data.get("price")
#             book.for_exchange = form.cleaned_data.get("for_exchange")
#             book.for_donation = form.cleaned_data.get("for_donation")
#
#             book = form.save(commit=False)
#             book.save()
#             return redirect('success_upload')
#     else:
#         form = BooksForm()
#     # context = {'articles': book_objects, 'form': form}
#     # context = {'articles': book_objects, 'form': form}
#     return render(request, 'book_register.html', {'form': form})

# def b_register(request, self):
#     form_class = BooksForm(request.POST)
#     success_url = reverse_lazy('success_upload')
#     template_name = "book_register.html"
#     if form_class.is_valid():
#         form = form_class.save(commit=False)
#         form.owner = # hz=============================================
#         form.author = BooksForm.cleaned_data.get("author")
#         form.title = BooksForm.cleaned_data.get("title")
#         form.summary = BooksForm.cleaned_data.get("summary")
#         form.isbn = BooksForm.cleaned_data.get("isbn")
#         form.enre = BooksForm.cleaned_data.get("genre")
#         form.upload = BooksForm.cleaned_data.get("upload")
#         form.language = BooksForm.cleaned_data.get("language")
#         form.for_sale = BooksForm.cleaned_data.get("for_sale")
#         form.price = BooksForm.cleaned_data.get("price")
#         form.for_exchange = BooksForm.cleaned_data.get("for_exchange")
#         form.for_donation = BooksForm.cleaned_data.get("for_donation")
#         form.save()
#         return redirect(success_url)
#     return render(request, template_name, {'form': form_class})


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Jūsų slaptažodis sėkmingai atnaujintas!')
#             return render(request, 'registration/password_change_success.html')
#         else:
#             messages.error(request, 'Ištaisykite toliau pateiktą klaidą.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'registration/change_password.html', {
#         'form': form
#     })
#
#
# def book_register(self, request,  *args, **kwargs):
#     form = BooksForm()
#     # book_model.title = form.cleaned_data.get("title")
#     # book_model.author = form.cleaned_data.get("author")
#     # book_model.summary = form.cleaned_data.get("summary")
#     # book_model.isbn = form.cleaned_data.get("isbn")
#     # book_model.enre = form.cleaned_data.get("genre")
#     # book_model.upload = form.cleaned_data.get("upload")
#     # book_model.language = form.cleaned_data.get("language")
#     # book_model.for_sale = form.cleaned_data.get("for_sale")
#     # book_model.price = form.cleaned_data.get("price")
#     # book_model.for_exchange = form.cleaned_data.get("for_exchange")
#     # book_model.for_donation = form.cleaned_data.get("for_donation")
#     # book_model.save()
#     success_url = reverse_lazy('success_upload')
#     if request.POST:
#         form = BooksForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return success_url
#     query_results = Book.objects.all()
#
#     return render(request, 'book_register.html', {'book': query_results})


# class BookRegister(CreateView):
#     form_class = BooksForm
#     # form_class.owner = request.HttpRequest.user.id
#     success_url = reverse_lazy('success_upload')
#     template_name = "book_register.html"
