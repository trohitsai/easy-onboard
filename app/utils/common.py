import logging
from threading import Thread
import threading

def get_logger(level: int = logging.INFO) -> logging:
    """
    Create and return logger object.

    :param level: Log level to be set
    :return: logging
    """
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s {%(pathname)s:%(lineno)d} %(message)s"
    )

    return logging.getLogger("MyApp")

# executes a func asynchronously
def push_to_async(function, params):
    threads = []
    thread = Thread(
        target = function,
        kwargs = params
    )
    thread.start()
    threads.append(thread)

    if threading.active_count()>1:
        return {}, 200