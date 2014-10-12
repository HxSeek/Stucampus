from django.conf.urls import url, patterns

from .views import PApplyView, MApplyView, p_success, m_success
from .views import loading, manage_list, app_view

urlpatterns = patterns(
    '',
    url(r'^join/$', loading, name='loading'),
    url(r'^pc/$', PApplyView.as_view(), name='index'),
    url(r'^pc/success/$', p_success, name='p_success'),
    url(r'^mobile/$', MApplyView.as_view(), name='mobile_index'),
    url(r'^mobile/success/$', m_success, name='m_success'),
    url(r'^list/$', manage_list, name='list'),
    url(r'^view/$', app_view, name='view'),
)
