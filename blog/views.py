from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from random import randint, choice
from .models import Post
from .forms import PostForm, CommentForm
from .dicts import *
from django.http import HttpResponse

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts' : posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def generator_page(request):
    race = choice(list(race_dict.keys()))
    subrace = choice(race_dict[race])
    gender = choice(gender_list)
    first_class = choice(list(class_dict.keys()))
    first_subclass = choice(class_dict[first_class])
    culture = choice(culture_list)
    background_list_full = background_list
    if culture == "Aedyr":
        background_list_full.extend(("Aristocrat", "Clergy", "Colonist", "Dissident", "Mercenary", "Slave"))
    elif culture == "The Deadfire Archipelago":
        background_list_full.extend(("Aristocrat", "Clergy", "Explorer", "Mercenary", "Raider", "Slave"))
    elif culture == "Ixamitl Plains":
        background_list_full.extend(("Aristocrat", "Dissident", "Mercenary", "Philosopher", "Scholar"))
    elif culture == "Old Vailia":
        background_list_full.extend(("Aristocrat", "Artist", "Colonist", "Dissident", "Mercenary", "Slave"))
    elif culture == "Rauatai":
        background_list_full.extend(("Aristocrat", "Dissident", "Mercenary", "Scholar", "Slave"))
    elif culture == "The Living Lands":
        background_list_full.extend(("Colonist", "Explorer", "Mercenary", "Scientist"))
    elif culture == "The White That Wends":
        background_list_full.extend(("Aristocrat", "Explorer", "Mystic"))
    background = choice(background_list_full)
    second_class = choice(list(class_dict.keys()))
    while second_class == first_class:
        second_class = choice(list(class_dict.keys()))
    multiclass = sorted([first_class, second_class])
    for key, value in multiclass_dict.items():
        if multiclass == value:
          multiclass = key
    multi_subclass = first_subclass + "/" + choice(class_dict[second_class])
    race_link = None
    for key, value in race_link_dict.items():
        if race == key:
            race_link = value
    class_link = None
    for key, value in class_link_dict.items():
        if first_class == key:
            class_link = value
        elif multiclass == key:
            class_link = value

    singleormulti = randint(1,2)
    return render(request, 'blog/generator.html', {'gender' : gender, 'race' : race, 'subrace' : subrace, 'singleormulti' : singleormulti,
     'first_class' : first_class, 'first_subclass' : first_subclass, 'second_class' : second_class, 'multiclass' : multiclass,
     'multi_subclass' : multi_subclass, 'background' : background, 'culture' : culture, 'race_link' : race_link, 'class_link' : class_link})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def logout_view(request):
    logout(request)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
