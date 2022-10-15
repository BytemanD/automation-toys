import logging
import os
from easy2use.globals import i18n as global_i18n

LOG = logging.getLogger(__name__)


def init_i18n():
    project_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    locale_path = os.path.join(project_name, 'locale')
    LOG.info('i18n locale path %s', locale_path)
    global_i18n.init('autotoys', locale_path)


init_i18n()

_ = global_i18n._
