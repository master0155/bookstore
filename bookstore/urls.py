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
from rest_framework.authtoken.views import obtain_auth_token
from bookstore.views import update

urlpatterns = [
    path("admin/", admin.site.urls),

    re_path(
        r'^(?P<version>v1)/bookstore/',
        include('product.urls')
    ),

    path('bookstore/', include('product.urls')),
    path('bookstore/', include('order.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('bookstore/update_server/', update, name='update_server'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]