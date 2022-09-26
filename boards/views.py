from django.http import HttpResponse
from django.shortcuts import render
from .models import Board
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import NewTopicForm,PostForm
from .models import Board, Post,Topic
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})  

def about(request):
    return render(request, 'about.html')

def about_company(request):
    return render(request, 'about_company.html', {'company_name': 'Simple Complex'})  

def about_author(request):
    return render(request, 'author.html')

def about_vitor(request):
    return render(request, 'vitor.html')

def about_erica(request):
    return render(request, 'erica.html')

def privacy_policy(request):
    return render(request, 'policy.html')  

def myaccounts(request):
    return render(request, 'myaccounts.html')      

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user  # <- here
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user  # <- and here
            )
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})          

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})    

def topic_posts(request, pk,topic_pk):
    topic = get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'topics.html', {'board': board, 'topics': queryset})


 
    
                