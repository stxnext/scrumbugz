import logging

from celery import task

from bugzilla.api import bugzilla
from scrum.models import Bug, store_bugs, Sprint
from scrum.utils import chunked

try:
    import newrelic.agent
except ImportError:
    newrelic = False

from scrum.models import BZProduct

log = logging.getLogger(__name__)


@task(name='fetch_new_bugs')
def fetch_new_bugs():
    bug_ids = bugzilla.get_bug_ids()
    bug_ids = set(bug_ids)
    already_fetched_bugs = Bug.objects.only('id')
    already_fetched_bugs = [ b.id for b in already_fetched_bugs ]
    already_fetched_bugs = set(already_fetched_bugs)
    diff = bug_ids.difference(already_fetched_bugs)
    for bids in chunked(diff, 100):
        update_bugs.delay(bids)

@task(name='update_products')
def update_products():
    products = BZProduct.objects.all()
    for product in products:
        update_product.delay(product.name)

@task(name='update_product')
def update_product(product, component=None):
    kwargs = {'product': product, 'scrum_only': False}
    if component:
        kwargs['component'] = component
    bug_ids = bugzilla.get_bug_ids(**kwargs)
    log.debug('Updating %d bugs from %s', len(bug_ids), kwargs)
    for bids in chunked(bug_ids, 100):
        update_bugs.delay(bids)


@task(name='update_bugs')
def update_bugs(bug_ids):
    bugs = bugzilla.get_bugs(ids=bug_ids, scrum_only=False)
    for fault in bugs['faults']:
        if fault['faultCode'] == 102:  # unauthorized
            try:
                Bug.objects.get(id=fault['id']).delete()
                log.warning("DELETED unauthorized bug #%d", fault['id'])
            except Bug.DoesNotExist:
                pass
    store_bugs(bugs)


@task(name='update_sprint_data')
def update_sprint_data(sprint_ids):
    for sprint in Sprint.objects.filter(id__in=sprint_ids):
        sprint.bugs_data_cache = sprint.get_bugs().get_aggregate_data()
        sprint.save()


def update_bug_chunks(bugs, chunk_size=100):
    """
    Update bugs in chunks of `chunk_size`.
    :param bugs: Iterable of bug objects.
    """
    numbugs = 0
    for bchunk in chunked(bugs, chunk_size):
        numbugs += len(bugs)
        log.debug("Updating %d bugs", len(bugs))
        update_bugs.delay([b.id for b in bchunk])
    log.debug("Total bugs updated: %d", numbugs)
