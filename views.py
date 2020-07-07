from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, PostForm, EPostForm
from django.core.mail import send_mail

# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #Trzy posty na każdej stronie.
    page = request.GET.get('page')        #Wskazuje nr bieżącej strony.
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #Jeżeli zmienna page nie jest liczbą całkowitą,
        #wówczas pobierana jest pierwsza strona wyników.
        posts = paginator.page(1)
    except EmptyPage:
        #Jeżeli zmienna page ma wartość większą niż numer ostatniej strony
        #wyników, wtedy pobierana jest ostatnia strona wyników.
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page' : page,
                   'posts' : posts})
                     

def post_detail(request, year, month, day, minute, second, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day,
                                   publish__minute=minute,
                                   publish__second=second)
    return render(request,
                  'blog/post/detail.html',
                  {'post' : post}) 

@login_required
def post_share(request, post_id):
    #Pobranie posta na podstawie jego identyfikatora.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        #Formularz został wysłany.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Weryfikacja pól formularza zakończyła się powodzeniem...
            cd = form.cleaned_data
            #...więc można wysłać wiadomość.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject ='{} ({}) zachęca do przeczytania "{}"'.format(cd['Podpis'], cd['Email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {} : {}'.format(post.title, post_url, cd['Podpis'], cd['Komentarz'])
            send_mail(subject, message, 'ankietydajazarobek@gmail.com', [cd['Odbiorca']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post' : post,
                                                    'form' : form,
                                                    'sent' : sent})    
def post_suma(request):
    object_list = Post.published.all()
    all=0
    ob = ''
    for ob in object_list:
        ob = ob.title
        all += ob 
    return render(request, 'blog/suma.html', {'ob' : ob,
                                              'all' : all})     
@login_required
def new_post(request):
    """Dodaj nową kwotę."""
    if request.method != 'POST':
        form = PostForm(request.POST)
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('blog:post_list'))
    return render(request, 'blog/post/new_post.html', {'form' : form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    
    if request.method != 'POST':
        form = EPostForm(instance=post)
    else:
        form = EPostForm(instance=post, data=request.POST)
        if form.is_valid():
            #edit_post.author = request.user
            form.save()
            return HttpResponseRedirect(reverse('blog:post_list'))
    return render(request, 'blog/post/edit_post.html', {'post':post,
                                                        'form':form })



			
       