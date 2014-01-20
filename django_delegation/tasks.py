from celery.decorators import task
from .utils import execute_delegated_view
from .models import DelegatedView


@task
def handle_delegated_view(dg_id):
    dg = DelegatedView.objects.get(pk=dg_id)

    # Try to encapsulate the task inside a Django Progress watcher.
    # This way, we can take advantage of its exception reporter.
    # If this does not work, we just proceed without it.
    try:
        from djprogress import with_progress, progress_error_reporter
    except ImportError:
        execute_delegated_view(dg)
    else:
        with progress_error_reporter():
            for i in with_progress([None], name='Loading delegated view %s' % dg.url):
                execute_delegated_view(dg)
