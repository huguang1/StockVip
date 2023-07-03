
from django.utils import timezone
from apps.system.models import Logs

import logging
logger = logging.getLogger(__name__)


def add_log(name, content, username):
    time_now = timezone.now()
    try:
        logs = Logs(act_name=name, act_content=content, act_user=username, add_time=time_now)
        logs.save()
    except Exception as e:
        logger.error(e)
