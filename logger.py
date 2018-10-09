"""Logging facilities for the qgraf_parser module"""
import logging
from sys import stdout

class LevelFilter(logging.Filter):
    """A filter to select messages only within a certain level range

    Notes
    -----
    Usage:
        `my_logging_handler.addFilter(LevelFilter(low,high))`
        ensures that my_logging_handler will only consider messages whose levels are contained in the range [low,high],
        *including the boundaries* (low <= level <= high)
    """
    def __init__(self, low, high):
        self._low = low
        self._high = high
        logging.Filter.__init__(self)
    def filter(self, record):
        if self._low <= record.levelno <= self._high:
            return True
        return False

def init_logger(name, *,stderr_output=False,stderr_level=logging.ERROR,stdout_output=False,stdout_min_level=logging.INFO,stdout_max_level=logging.WARNING,logfile_output=False,logfile_path=None,logfile_level=logging.INFO):
    """Create a logger object with a specific name

    This method creates a logger file. Its main purpose is to be called in the root __init__ file of the module when
    the package or any submodule is imported. The basic options allow to have a StreamHandler outputting to stderr with
    a specific level, another outputting  and to have a FileHandler outputting to a chosen logfile.

    Parameters
    ----------
    name : str
        name of the logger. For practical purposes this is just the main package's __name__
    stderr_output : bool, optional
        Should some output be redirected to stderr? Defaults to False
    stderr_level : int, optional
        Minimum level reported to stderr. Defaults to logging.ERROR
    stdout_output : bool, optional
        Should some output be redirected to stdout? Defaults to False
    stdout_min_level : int, optional
        Minimum level reported to stdout. Defaults to logging.INFO
    stdout_max_level : int, optional
        Minimum level reported to stdout. Defaults to logging.WARNING
    logfile_output : bool, optional
        Should some output be redirected to a logfile? Defaults to False
    logfile_path : str, optional
        Path of the logfile. Defaults to None. If None is given, override logfile_output to False
    logfile_level : int, optional
        Minimum level reported to file. Defaults to logging.INFO

    Returns
    -------
    logging.Logger
        A logger setup according to specifications
    """
    logger = logging.getLogger(name)

    # Common format for all msg
    my_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # stderr output handler
    if stderr_output:
        stderr_handler = logging.StreamHandler()
        stderr_handler.setLevel(stderr_level)
        stderr_handler.setFormatter(my_formatter)
        logger.addHandler(my_screen_handler)

    # stderr output handler
    if stdout_output:
        if stdout_min_level > stdout_max_level:
            stdout_level_conflict = True
        else:
            stdout_level_conflict = False
            stdout_handler = logging.StreamHandler(stdout)
            stdout_handler.setLevel(stdout_min_level)
            stdout_handler.addFilter(LevelFilter(stdout_min_level,stdout_max_level))
            stdout_handler.setFormatter(my_formatter)
            logger.addHandler(my_screen_handler)

    # File output handler
    if logfile_path is None:
        true_logfile_output = False
    else:
        true_logfile_output = logfile_output
    if true_logfile_output:
        my_file_handler = logging.FileHandler(logfile_path)
        my_file_handler.setLevel(logfile_level)
        my_file_handler.setFormatter(my_formatter)
        logger.addHandler(my_file_handler)
    # The logger lets all message filter through to the handlers, which are responsible for the triage.
    logger.setLevel(logging.DEBUG)

    # Use the logger to produce a report on itself.
    if stderr_output:
        logger.info("The logger {logger_str} was setup with stderr output".format(logger_str=str(logger)))
        if stderr_level < logging.WARNING:
            logger.warning("The stderr output was setup to include non-error related messages.")
    if stdout_output:
        if stdout_level_conflict:
            logger.warning("The logger {logger_str} was not setup for stdout output due to a min>max level conflict".format(logger_str=str(logger)))
        else:
            logger.info("The logger {logger_str} was setup with stdout output".format(logger_str=str(logger)))
            if stdout_max_level > logging.WARNING:
                logger.warning("The stdout output was setup to include error related messages.")
    if true_logfile_output:
            logger.info("The logger {logger_str} was setup with logfile output at {log_path}".format(logger_str=str(logger),log_path=logfile_path))
    # If the logfile was not used because the path was missing
    elif logfile_output:
        logger.warning("The logger {logger_str} was not setup with logfile output due to a missing logfile path".format(logger_str=str(logger),
                                                                                                 log_path=logfile_path))
    return logger