from celery.decorators import task
from djprogress import with_progress, progress_error_reporter
from django_delegation.utils import execute_delegated_view
from .models import DelegatedView


@task
def handle_delegated_view(dg_id):
    dg = DelegatedView.objects.get(pk=dg_id)
    with progress_error_reporter():
        for i in with_progress([None], name='Loading delegated view %s' % dg.url):
            execute_delegated_view(dg)
