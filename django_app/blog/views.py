from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from django.contrib.auth import get_user_model

from .models import Post
from .forms import PostCreateForm

User = get_user_model()


def post_list(request):
    # posts변수에 ORM을 이용해서 전체 Post의 리스트(쿼리셋)를 대입
    # posts = Post.objects.all()

    # posts변수에 전체 Post를 최신내림차순으로 정렬한 쿼리셋을 대입
    posts = Post.objects.order_by('-created_date')

    # posts변수에 ORM을 사용해서 전달할 쿼리셋이
    # Post의 published_date가 timezone.now()보다
    # 작은 값을 가질때만 해당하도록 필터를 사용한다
    # posts = Post.objects.filter(
    #     published_date__lte=timezone.now()
    # )
    context = {
        'title': 'PostList from post_list view',
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context=context)


def post_detail(request, pk):
    print('post_detail pk:', pk)
    # post라는 키값으로 pk또는 id값이 매개변수로 주어진 pk변수와 같은 Post객체를 전달
    # objects.get을 쓰세요
    context = {
        'post': Post.objects.get(pk=pk),
    }
    return render(request, 'blog/post_detail.html', context)


def post_create(request):
    if request.method == 'GET':
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/post_create.html', context)
    elif request.method == 'POST':
        # Form클래스의 생성자에 POST데이터를 전달하여 Form 인스턴스를 생성
        form = PostCreateForm(request.POST)
        # Form인스턴스의 유효성을 검사하는 is_valid메서드
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            user = User.objects.first()
            post = Post.objects.create(
                title=title,
                text=text,
                author=user
            )
            return redirect('post_detail', pk=post.pk)
        # 유효성 검사를 통과하지 못했을경우 error가 담긴 form을 이용해 기존페이지를 보여줌
        else:
            context = {
                'form': form,
            }
            return render(request, 'blog/post_create.html', context)


def post_modify(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        # POST요청(request)가 올 경우, 전달받은 데이터의 title, text값을 사용해서
        # 해당하는 Post인스턴스 (post)의 title, text속성값에 덮어씌우고
        # DB에 업데이트하는 save()메서드 실행
        form = PostCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            post.title = title
            post.text = text
            post.save()
            # 기존 post인스턴스를 업데이트 한 후, 다시 글 상세화면으로 이동
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostCreateForm()

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'blog/post_modify.html', context)


def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('post_list')
    else:
        return HttpResponse('Method "GET" is not allowed')
