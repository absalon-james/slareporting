import conf

from rackspace_monitoring.providers import get_driver
from rackspace_monitoring.types import Provider

_DRIVER_INSTANCE = None


def get_instance():
    """Get instance of the rackspace cloud monitoring driver.

    :returns: Driver instance
    :rtype: rackspace_monitoring.drivers.rackspace.RackspaceMonitoringDriver
    """
    global _DRIVER_INSTANCE

    if _DRIVER_INSTANCE is None:
        driver = get_driver(Provider.RACKSPACE)
        rax_conf = conf.get_raxrc()
        _DRIVER_INSTANCE = driver(
            rax_conf.get('credentials', 'username'),
            rax_conf.get('credentials', 'api_key'),
            ex_force_auth_url=rax_conf.get('auth_api', 'url')
        )
    return _DRIVER_INSTANCE
