import os
import json
from datetime import datetime
from fastapi import Request, HTTPException, Depends, Response
from fastapi.templating import Jinja2Templates
from core import config
from core.app.auth.user.service import UserQueryService

from core.fastapi.dependencies import PermissionDependency, RoleDependency, IsAuthenticated, ScopeDependency
from core.exceptions import RequiresLoginException
from core.utils import menu_to_html

root_path = os.getcwd()


def global_context():
    return {
        "app_name": config.APP_NAME,
        "app_version": config.APP_VERSION,
    }


# async def depend_user(request: Request):
#     return await UserQueryService().get_user_by(username=request.user.username)


class PageResponse:
    def __init__(self, path_template: str, prefix_url: str, depend_roles: list[str] = []):
        self.templates = Jinja2Templates(directory="./")
        self.templates.env.globals.update(global_context=global_context)
        self.path = path_template.replace(root_path, "")
        self.context = {}
        self.user = None
        self.prefix_url = "/page" + prefix_url
        self.depend_roles = depend_roles

    async def request(self, request: Request, response: Response, PathCheck: str = None):
        # self.initContext(request, request.user.client_id, "-")
        # return request

        if PathCheck is not None:
            path_check = PathCheck.split(".")
            if len(path_check) == 3:
                if path_check[2] != config.APP_VERSION:
                    raise HTTPException(status_code=404)
                if path_check[0] != request.user.client_id:
                    raise HTTPException(status_code=404)

            self.initContext(request, path_check[0], path_check[1])
        else:

            # if not config.SESSION_DISABLE:
            #     thread = threading.Thread(target=SessionRepository().updateEndTime, args=(req.state.sessionId, req.scope["path"]))
            #     thread.start()
            self.initContext(request, request.user.client_id, request.user.session_id)


        if request.user.username is not None:
            user_path = ".db/cache/user/{}.json".format(request.user.username)
            if os.path.isfile(user_path):
                with open(user_path, "r") as file:
                    user_json = json.load(file)
                    user_json["created_at"] = datetime.strptime(user_json["created_at"], '%Y-%m-%dT%H:%M:%S')
                    self.addContext("userloggedin", user_json)
            menu_sidebar_path = ".db/cache/menu/{}_{}.json".format(request.user.username, "sidebar")
            if os.path.isfile(menu_sidebar_path):
                with open(menu_sidebar_path, "r") as file:
                    menu_sidebar_json = json.load(file)
                    menu_sidebar = menu_to_html(menus=menu_sidebar_json, segmen=request.scope["route"].name)
                    self.addContext("menu_sidebar", menu_sidebar)

        return request

    def addContext(self, key, value):
        self.context[key] = value

    def initContext(self, request: Request, client_id, session_id):
        self.context = {}
        self.addContext("prefix_url", self.prefix_url)
        self.addContext("prefix_url_js", self.prefix_url + "/" + client_id + "." + session_id + "." + config.APP_VERSION)
        self.addContext("prefix_url_post", self.prefix_url + "/" + client_id + "." + session_id)
        self.addContext("TOKEN_KEY", config.COOKIES_KEY)
        self.addContext("segment", request.scope["route"].name)
        # self.addContext("userloggedin", request.user)
        # self.addData("sidemenu", self.sidemenu)
        self.addContext("TOKEN_EXPIRED", (config.COOKIES_EXPIRED * 60 * 1000) - 2000)

    def media_type(self, path: str):
        if path.find(".js") > 0:
            return "application/javascript"
        else:
            return "text/html"

    def response(self, request: Request, path: str):
        return self.templates.TemplateResponse(
            request=request,
            name=self.path + path,
            media_type=self.media_type(path),
            context=self.context,
        )

    def dependencies(self, scopes: list[str] = None):
        if scopes is None:
            return [Depends(PermissionDependency(permissions=[IsAuthenticated], exception=RequiresLoginException))]
        else:
            return [
                Depends(PermissionDependency(permissions=[IsAuthenticated], exception=RequiresLoginException)),
                Depends(RoleDependency(self.depend_roles, exception=RequiresLoginException(self.prefix_url))),
                Depends(ScopeDependency(scopes, exception=RequiresLoginException(self.prefix_url))),
            ]

    def depend_r(self, scopes: list[str] = ["read"]):
        return self.dependencies(scopes)

    def depend_w(self, scopes: list[str] = ["read", "write"]):
        return self.dependencies(scopes)

    def depend_d(self, scopes: list[str] = ["read", "write", "delete"]):
        return self.dependencies(scopes)
