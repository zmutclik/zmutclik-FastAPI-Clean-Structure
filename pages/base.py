from fastapi.templating import Jinja2Templates
from core import config

templates = Jinja2Templates(directory="pages/templates")
templates.env.globals.update(
    add_global_context={
        "app_name": config.APP_NAME,
    }
)
