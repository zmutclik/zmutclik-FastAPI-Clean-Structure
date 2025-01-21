import os
from ..config import DBCORE_FILE

if os.path.exists(DBCORE_FILE):
    file_stats = os.stat(DBCORE_FILE)
    if file_stats.st_size != 0:
        from .session_core import session_core
        from .session_auth import session_auth
        from .session_menu import session_menu
        from .session_logs import session_logs
        from .session_ import session

        __all__ = [
            "session",
            "session_core",
            "session_auth",
            "session_logs",
            "session_menu",
        ]
