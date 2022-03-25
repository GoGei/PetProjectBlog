from django.utils import timezone

from core.Posts.models import PostClassifier


class PostOrderClass:
    def __init__(self, request, qs):
        self.request = request
        self.qs = qs

    def get_qs(self):
        request = self.request
        order = request.GET.get('order', PostClassifier.DEFAULT_ORDER)
        order_by = PostClassifier.ORDER_BY_MAP.get(order)
        return self.qs.order_by(order_by)


class PostExtraFilterClass:
    def __init__(self, extra_filter, qs):
        self.extra_filter = extra_filter
        self.qs = qs

    def get_qs(self):
        _filter = self.extra_filter
        qs = self.qs
        if _filter:
            if _filter not in PostClassifier.EXTRA_FILTERS:
                raise AttributeError('This posts extra filter is not defined')
            today = timezone.localdate()
            delta = PostClassifier.TIMEDELTA
            target_date = today - delta

            if _filter == PostClassifier.RECENTLY_CHANGED:
                qs = qs.filter(modified_stamp__gte=target_date)
            elif _filter == PostClassifier.THIS_MONTH:
                qs = qs.filter(created_stamp__gte=target_date)

        return qs
