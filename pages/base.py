from fastapi.templating import Jinja2Templates
from core import config


def global_context():
    return {"app_name": config.APP_NAME}


templates = Jinja2Templates(directory="pages/templates")
templates.env.globals.update(global_context=global_context)
