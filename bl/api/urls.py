from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import BucketlistView, BucketlistDetailsView, ItemView, ItemDetailsView, UserView, CreateUserView, UserDetailsView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace="rest_framework")),
    url(r'^bucketlists/$', BucketlistView.as_view(), name="bucketlists"),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$', BucketlistDetailsView.as_view(), name="singlebucket"),
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/$', ItemView.as_view(), name="items"),
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<pk2>[0-9]+)/$', ItemDetailsView.as_view(), name="singleitem"),
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'^users/register/$', CreateUserView.as_view(), name="register"),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetailsView.as_view(), name="user_details"),
    url(r'^login/$', obtain_auth_token)
}

urlpatterns = format_suffix_patterns(urlpatterns)
