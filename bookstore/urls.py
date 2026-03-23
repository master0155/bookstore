"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import debug_toolbar
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from bookstore.views import hello_world, update
from bookstore.frontend_views import (
    login_view, register_view, logout_view,
    feed_view, profile_view, like_tweet, comment_tweet,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    re_path(
        r'^(?P<version>v1)/bookstore/',
        include('product.urls')
    ),

    path('bookstore/', include('product.urls')),
    path('bookstore/', include('order.urls')),
    path('bookstore/', include('tweet.urls')),
    path('bookstore/', include('user_profile.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('bookstore/hello/', hello_world, name='hello_world'),
    path('bookstore/update_server/', update, name='update_server'),

    # Frontend HTML
    path('', feed_view, name='feed'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/<str:username>/', profile_view, name='profile_user'),
    path('tweet/<int:tweet_id>/like/', like_tweet, name='like_tweet'),
    path('tweet/<int:tweet_id>/comment/', comment_tweet, name='comment_tweet'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)