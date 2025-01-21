import os


def check_exits(db_path):
    with open(db_path, "w") as f:
        f.write("")


def check_sizes(db_path):
    if os.path.exists(db_path):
        file_stats = os.stat(db_path)
        return True if file_stats.st_size == 0 else False
