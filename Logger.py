import logging
from datetime import datetime
from os import listdir, path, remove

BASE_PATH = path.dirname(path.abspath(__file__))

def delete_old_log():
    all_logs = listdir(path.join(BASE_PATH, 'logs'))
    all_logs_strings = [x.split("_log")[0] for x in all_logs]
    all_datetimes = []
    for l in all_logs_strings:
        l = l.replace('_', '-').split('-')
        all_datetimes.append(datetime(int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5])))
    min_date = all_datetimes.index(min(all_datetimes))
    remove(path.join(BASE_PATH, 'logs', all_logs[min_date]))

def get_logger():
    file_name = datetime.now().isoformat().replace("T", "_").replace(":", "-").split(".")[0] + "_log.log"
    logging.basicConfig(filename=path.join(BASE_PATH, "logs", file_name), level=logging.INFO)
    if len(listdir('logs')) > 3:
        delete_old_log()
    logger = logging.getLogger(__name__)
    return logger
