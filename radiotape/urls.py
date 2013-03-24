from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'radiotape.views.home', name='home'),
    # url(r'^radiotape/', include('radiotape.foo.urls')),

    url(r'^$', 'rec.views.login_view'),
    url(r'^api/login/$', 'rec.views.login_view'),
    url(r'^api/logout/$', 'rec.views.logout_view'),
    url(r'^api/register/$', 'rec.views.register_view'),

    url(r'^api/mix/$', 'rec.views.mix_view'),
    url(r'^api/mix/(?P<id>\d+)/$', 'rec.views.mix_view'),
    url(r'^api/remix/$', 'rec.views.remix_view'),
    url(r'^api/remixes/(?P<id>\d+)/$', 'rec.views.remix_view'),
    url(r'^api/mix_social/(?P<id>\d+)/$', 'rec.views.mix_social_view'),

    url(r'^api/track/$', 'rec.views.track_view'),
    url(r'^api/track/(?P<id>\d+)/$', 'rec.views.track_view'),
    url(r'^api/upload_track/$', 'rec.views.upload_track_view'),

    url(r'^api/mix_comment/$', 'rec.views.mix_comment_view'),
    url(r'^api/mix_comments/(?P<id>\d+)/$', 'rec.views.mix_comment_view'),

    url(r'^api/favorite_mix/(?P<id>\d+)/$', 'rec.views.favorite_mix_view'),
    url(r'^api/favorite_mixes/$', 'rec.views.favorite_mix_view'),

    url(r'^api/user/(?P<username>\w+)/$', 'rec.views.user_view'),
    url(r'^api/profile_image/$', 'rec.views.profile_image_view'),

    url(r'^api/follow/(?P<username>\w+)/$', 'rec.views.follow_view'),
    url(r'^api/following_mixes/$', 'rec.views.follow_view'),

    url(r'^api/global_mixes/$', 'rec.views.global_view'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
