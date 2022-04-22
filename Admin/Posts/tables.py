import django_tables2 as tables
from core.Posts.models import Posts


class PostsTable(tables.Table):
    is_active = tables.BooleanColumn(orderable=False)
    actions = tables.TemplateColumn(template_name='Admin/Posts/posts_actions.html', orderable=False)

    class Meta:
        model = Posts
        fields = ('title', 'heading', 'is_active', 'actions')
        attrs = {'class': 'dataTable-table'}
        template_name = "django_tables2/bootstrap4.html"
