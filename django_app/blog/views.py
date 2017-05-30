from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Post

from .forms import PostCreateForm

def post_list(request):
    # posts 변수에 ORM을 이용해서 전 Post의 리스트(쿼리셋)를 대입
    #post 정렬하기
    posts = Post.objects.order_by('-created_date')

    # posts 변수에 ORM을 사용해서 전달할 쿼리셋이
    # posts의 published_date가 timezone.now()보다
    # 작은 갓을 가질 때만 해당하도록 필터를 사용한다.
    # posts =Post.objects.filter(
    #     published_date__lte = timezone.now()
    # )
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
    # with open('templates/blog/post_detail.html') as opentemplate:
    #     f = opentemplate.read()
    # return HttpResponse(f)
    return render(request, 'blog/post_detail.html', context = context)

def post_create(request):
    if request.method == 'GET':
        form = PostCreateForm()
        context = {
            'form':form,
        }
        return render(request, 'blog/post_create.html',context)
    elif request.method == 'POST':
        # Form클래스의 생성자에 POST데이터를 전달하여 Form 인스턴스를 생성
        form = PostCreateForm(request.POST)
        # Form인스턴스의 유효성을 검사하는 is_valid메서드
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            user = User.objects.first()
            post = Post.objects.create(
                author=user,
                title = title,
                text = text
            )
            # return HttpResponse(post)
            return redirect('post_detail', pk=post.pk)

        else:
            context = {
                'form':form,
            }
            return render(request, 'blog/post_create.html', context)


def post_modify(request, pk):
    post = Post.objects.get(pk = pk)
    if request.method == 'POST':
        # POST요청(request)가 올 경우, 전달받은 데이터의 title, text값을 사용해서
        # 해당하는 Post 인스턴스 (post)의 title, text속성값에 더ㅠ어씌우고
        # DB에 업데이트하는 save()메서드 실행
        data = request.POST
        # extra) 장고폼을 사용하는 형태로 업데이트
        title = data['title']
        text = data['text']
        post.title = title
        post.text = text
        post.save()
        # 기존 post인스턴스를 업데이트 한 후, 다시 글 상세화면으로 이동
        return redirect('post-detail', pk=post.pk)
    elif request.method == 'GET':
        # pk에 해당하는 Post인스턴스를 전달
        # extra) 장고폼을 'form'키로 전달해서 구현
        context = {
            'post': post,
        }
        return render(request, 'blog/post_modify.html', context)