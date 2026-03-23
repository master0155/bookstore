from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST

from tweet.models import Tweet, Like, Comment
from user_profile.models import UserProfile


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'twitter/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('feed')
    return render(request, 'twitter/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def feed_view(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Tweet.objects.create(author=request.user, content=content)
        return redirect('feed')

    following_users = request.user.profile.following.all()
    tweets = Tweet.objects.filter(author__in=following_users).order_by('-created_at')
    all_tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'twitter/feed.html', {
        'tweets': tweets,
        'all_tweets': all_tweets,
    })


@login_required
def profile_view(request, username=None):
    if username is None:
        profile_user = request.user
    else:
        profile_user = get_object_or_404(User, username=username)

    profile = profile_user.profile
    tweets = Tweet.objects.filter(author=profile_user).order_by('-created_at')
    is_following = request.user.profile.following.filter(id=profile_user.id).exists()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'follow':
            request.user.profile.following.add(profile_user)
        elif action == 'unfollow':
            request.user.profile.following.remove(profile_user)
        elif action == 'update_profile' and profile_user == request.user:
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            bio = request.POST.get('bio', '').strip()
            new_password = request.POST.get('new_password', '').strip()
            if first_name:
                request.user.first_name = first_name
            if last_name:
                request.user.last_name = last_name
            if bio:
                profile.bio = bio
            if new_password:
                request.user.set_password(new_password)
                login(request, request.user)
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            request.user.save()
            profile.save()
            messages.success(request, 'Perfil atualizado!')
        return redirect('profile_user', username=profile_user.username)

    return render(request, 'twitter/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'tweets': tweets,
        'is_following': is_following,
        'followers_count': profile_user.followers.count(),
        'following_count': profile.following.count(),
    })


@login_required
@require_POST
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        like.delete()
    next_url = request.POST.get('next', 'feed')
    return redirect(next_url)


@login_required
@require_POST
def comment_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    content = request.POST.get('content', '').strip()
    if content:
        Comment.objects.create(author=request.user, tweet=tweet, content=content)
    next_url = request.POST.get('next', 'feed')
    return redirect(next_url)
