"""module for logging"""
# builtin imports
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
#piplib imports
from structlog import get_logger, configure, make_filtering_bound_logger

Log = get_logger()

def init_logger(config:dict)->None:
    """initialize logger"""
    configure(wrapper_class=make_filtering_bound_logger(log_level(config['log_level'])))

def log_level(level:str)->int:
    """map level string to level int"""
    return {
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARN": WARNING,
        "WARNING": WARNING,
        "ERROR": ERROR,
        "CRIT": CRITICAL,
        "CRITICAL": CRITICAL
    }[level.upper()]
