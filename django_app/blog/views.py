from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Post


def post_list(request):
    # posts 변수에 ORM을 이용해서 전체 Post의 리스트(쿼리셋)를 대입
    # posts = Post.objects.all()

    # posts 변수에 ORM을 사용해서 전달할 쿼리셋이
    # posts의 published_date가 timezone.now()보다
    # 작은 갓을 가질 때만 해당하도록 필터를 사용한다.
    posts =Post.objects.filter(
        published_date__lte = timezone.now()
    )
    context = {
        'title' : 'PostList from post_list view',
        'posts' : posts,
    }
    return render(request, 'blog/post_list.html', context = context)

def post_detail(request, pk):
    print('post_detail pk:', pk)
    # post라는 키값으로 pk또는 id값이 매개변수로 주어진 pk변수와 같은 Post객체를 전달
    # objects.get을 쓰세요
    context = {
        'post': Post.objects.get(pk=pk)
    }
    return render(request, 'blog/post_detail.html', context = context)