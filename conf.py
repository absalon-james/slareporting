import os
import ConfigParser

config = ConfigParser.SafeConfigParser()
config.read(['.raxrc', os.path.expanduser('~/.raxrc')])


def get_raxrc():
    """Get instance of raxrc config.

    :returns: Raxrc config
    :rtype: ConfigParser.SafeConfigParser
    """
    return config
