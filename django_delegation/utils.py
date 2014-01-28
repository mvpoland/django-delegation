import pickle
from cStringIO import StringIO
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

try:
    from django.utils.timezone import now
except:
    import datetime
    now = datetime.datetime.now

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

from .models import DelegatedView


def remove_keys_with_prefix(dictionary, prefix):
    keys_to_remove = [key for key in dictionary.keys() if key[:len(prefix)] == prefix]
    for k in keys_to_remove:
        del dictionary[k]


class SimpleHTTPRequest(object):
    """
    A pickle-able class which will resemble the Django HTTPRequest
    """

    def __init__(self, request, omitted_keys=None):
        """
        Constructor for SimpleHTTPRequest.
        :param request: A real Django HTTPRequest
        """

        self.path = request.path
        self.path_info = request.path_info
        self.method = request.method
        self.body = request.body if hasattr(request, 'body') else request.raw_post_data
        self.raw_post_data = self.body
        self.GET = request.GET
        self.POST = request.POST
        self.REQUEST = request.REQUEST
        self.META = request.META
        remove_keys_with_prefix(self.META, 'wsgi.')
        self.user = request.user
        self.session = request.session
        self.encoding = request.encoding
        if hasattr(request, 'urlconf'):
            self.urlconf = request.urlconf

        omitted_keys = omitted_keys or []

        for k in request.__dict__:
            if k[:1] != '_' and not hasattr(self, k) and not k in omitted_keys:
                setattr(self, k, request.__dict__[k])

        self._is_secure = request.is_secure()

    def is_secure(self):
        return self._is_secure



def store_delegated_view(view_func, request, args, kwargs):
    pickled_request = pickle.dumps((request, args, kwargs, view_func.__module__, view_func.__name__))
    user = request.user if request.user.is_authenticated() else None
    return DelegatedView.objects.create(url=request.path, owner=user, pickled_request=pickled_request)


def execute_delegated_view(dg_obj):
    request, args, kwargs, view_module, view_name = pickle.loads(str(dg_obj.pickled_request))
    view_func = getattr(__import__(view_module, {}, {}, ['']), view_name)
    response = view_func(request, *args, **kwargs)

    if response:
        if hasattr(response, 'render'):
            response.render()

        file_name = 'content.html'
        if 'Content-Disposition' in response:
            import re
            match = re.search(r'filename=(.*)$', response['Content-Disposition'])
            if match:
                file_name = match.groups()[0].replace('"', '').replace("'", '')

        content = response.content.encode('utf-8') if isinstance(response.content, unicode) else response.content
        content_size = len(content)
        dg_obj.status_code = response.status_code
        dg_obj.content_type = response['Content-Type']
        dg_obj.data_size = content_size

        file_data = InMemoryUploadedFile(StringIO(content), 'data', file_name, dg_obj.content_type, content_size, charset=None)
        dg_obj.data.save(file_name, file_data, save=False)
        
        if dg_obj.owner:
            domain = Site.objects.get_current().domain
            mail_message = u'''Hello.
The page %s has finished loading. You can download it on the following link:
http://%s%s

Have a nice day.
-- The happy Django Delegation mailer bot
''' % (dg_obj.url, domain, reverse('django_delegation_result', kwargs={'dg_id': dg_obj.pk}))
            send_mail('Your page has finished loading', mail_message, settings.DEFAULT_FROM_EMAIL,
                [dg_obj.owner.email], fail_silently=False)

    dg_obj.finished = now()
    dg_obj.save()

