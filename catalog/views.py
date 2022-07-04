#from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.shortcuts import render
from django.views import generic

from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_authors = Author.objects.count()  # El 'all()' se obvia en este caso.
    # Libros disponibles (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # El 'all()' esta implícito por defecto.
    # Numero de visitas a esta view, como está contado en la variable de sesión.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Carga la plantilla index.html con la información adicional en la variable context.
    return render(request, 'index.html', context=context)



class BookListView(generic.ListView):
    model = Book
    """
    context_object_name = 'my_book_list'  # your own name for the list as a template variable
    queryset = Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    """
    paginate_by = 1
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['some_data'] = Book.objects.all()
        return context

class BookDetailView(generic.DetailView):
        model = Book

        def book_detail_view(request, pk):
            try:
                book_id = Book.objects.get(pk=pk)
            except Book.DoesNotExist:
                raise Http404("Book does not exist")

            # book_id=get_object_or_404(Book, pk=pk)

            return render(
                request,
                'catalog/book_detail.html',
                context={'book': book_id, }
            )

class AuthorListView(generic.ListView):
    model = Author

    context_object_name = 'my_Author_list'  # your own name for the list as a template variable
    queryset = Author.objects.all()  # Get 5 books containing the title war
    template_name = 'catalog/author_list.html'  # Specify your own template name/location

    paginate_by = 1
    """def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['some_data'] = Book.objects.all()
        return context"""

class AuthorDetailView(generic.DetailView):
        model = Author

        def author_detail_view(request, pk):
            try:
                author_id = Author.objects.get(pk=pk)
            except Author.DoesNotExist:
                raise Http404("Book does not exist")

            # book_id=get_object_or_404(Book, pk=pk)

            return render(
                request,
                'catalog/author_detail.html',
                context={'author': author_id, }
            )

