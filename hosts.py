from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'', 'Blog.urls', name='blog'),
    host(r'admin', 'Admin.urls', name='admin'),
)
