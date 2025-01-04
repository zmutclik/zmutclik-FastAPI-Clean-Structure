from fastapi.templating import Jinja2Templates
from core import config


def global_context():
    return {"app_name": config.APP_NAME}


templates_html = Jinja2Templates(directory="./")
templates_html.env.globals.update(global_context=global_context)
