from functools import wraps
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

try:
    from django.utils.timezone import now
except:
    import datetime
    now = datetime.datetime.now


from .utils import SimpleHTTPRequest, store_delegated_view, execute_delegated_view
from .tasks import handle_delegated_view


def delegate(view_func):
    """
    Decorator for views that became too slow for normal round-trip web requests.
    The view will be executed behind the scenes, and the result will be stored inside
    of a DelegatedView model instance.
    """
    @wraps(view_func)
    def delegated_view(request, *args, **kwargs):
        # Prevent endless recursion
        if isinstance(request, SimpleHTTPRequest):
            return view_func(request, *args, **kwargs)

        simple_request = SimpleHTTPRequest(request)

        dg_obj = store_delegated_view(view_func, simple_request, args, kwargs)
        handle_delegated_view.delay(dg_obj.pk)

        dg_url = reverse('django_delegation_result', kwargs={'dg_id': dg_obj.pk})

        messages.success(request, mark_safe(u'Your page is being loaded in the background. You will get an email when it has finished loading. It will be available <a href="%s">here</a>.' % dg_url))
        return redirect(request.META['HTTP_REFERER'])

    return delegated_view

