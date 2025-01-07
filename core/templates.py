from fastapi.templating import Jinja2Templates
from core import config
import os

root_path = os.getcwd()


def global_context():
    return {
        "app_name": config.APP_NAME,
        "app_version": config.APP_VERSION,
    }


templates_html = Jinja2Templates(directory="./")
templates_html.env.globals.update(global_context=global_context)
