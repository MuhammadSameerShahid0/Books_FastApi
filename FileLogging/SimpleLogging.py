import logging
import os
from logging.handlers import TimedRotatingFileHandler

def simplelogging(filename: str):
    log_directory = "Logs"
    log_file_path = os.path.join(log_directory, f"{filename}.txt")
    os.makedirs(log_directory, exist_ok=True)

    logger = logging.getLogger(filename)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        file_handler = TimedRotatingFileHandler(
            log_file_path,
            when="midnight",
            backupCount=7,
            delay=True,
            encoding="utf-8")

        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger


# import logging
# import os
#
# class LazyFileHandler(logging.FileHandler):
#     def __init__(self, filename, mode="a", encoding=None, delay=True):
#         # delay=True means the file is not created/opened until first emit()
#         super().__init__(filename, mode=mode, encoding=encoding, delay=delay)
#
# def simplelogging(filename : str):
#     log_directory = "Logs"
#     log_file_path = os.path.join(log_directory, f"{filename}.txt") #Folder Name
#     os.makedirs(log_directory, exist_ok=True)
#
#     logger = logging.getLogger(filename)  # in file log Name
#
#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#         handlers=[
#             logging.FileHandler(log_file_path),
#             logging.StreamHandler()
#         ],
#         force=True # <-- reconfigures root logger
#     )
#     return logger