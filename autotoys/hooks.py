from distutils.command import install
import os
from easy2use.common import msgfmt


def setup_hook(config):
    # Tell distutils not to put the data_files in platform-specific
    # installation locations.
    # Refer to the instructions in the openstack/horizon project
    for scheme in install.INSTALL_SCHEMES.values():
        scheme['data'] = scheme['purelib']

    msgfmt.make_i18n('autotoys', 'i18n')
