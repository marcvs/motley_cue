import os
from configparser import ConfigParser
from pathlib import Path
import logging

CONFIG = ConfigParser()


def reload():
    """Reload configuration from disk.

    Config locations, by priority:
    /etc/motley/motley.conf
    $MOTLEY_CUE_CONFIG
    ./motley.conf
    ~/.config/motley/motley.conf

    processing is stopped, once a give file is found
    """

    logging.basicConfig(
        level=os.environ.get("LOG", "INFO")
    )
    logger = logging.getLogger(__name__)
    files = []

    # FIXME: hardcoded path for config file
    files += [Path("/etc/motley/motley.conf")]
    filename = os.environ.get("MOTLEY_CUE_CONFIG")
    if filename:
        files += [Path(filename)]

    files += [
        Path('motley.conf'),
        Path.home()/'.config'/'motley'/'motley.conf'
    ]

    for f in files:
        if f.exists():
            files_read = CONFIG.read(f)
            logger.debug(F"Read config from {files_read}")
            break


def to_list(list_str):
    """Convert a string to a list.
    """
    return [
        v.strip('"').strip("'") for v in list_str
        .replace("\n", "").replace(" ", "").replace("\t", "")
        .strip("]").strip("[")
        .rstrip(",").split(",")
    ]


def to_bool(bool_str):
    """Convert a string to bool.
    """
    return True if bool_str.lower() == 'true' else False


# Load config on import
reload()
