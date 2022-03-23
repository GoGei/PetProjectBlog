import django_tables2 as tables
from core.Posts.models import Posts


class PostsTable(tables.Table):
    class Meta:
        model = Posts
        fields = ('author__email', 'title', 'heading')
        attrs = {'class': 'dataTable-table'}
