import logging
from django.dispatch import receiver
from django_q.tasks import async_task

logger = logging.getLogger(__name__)
