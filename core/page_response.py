import os
from typing import Annotated
from fastapi import Request, HTTPException, Depends, Response
from fastapi.templating import Jinja2Templates
from core import config

root_path = os.getcwd()


def global_context():
    return {
        "app_name": config.APP_NAME,
        "app_version": config.APP_VERSION,
    }


class PageResponse:
    def __init__(self, path_template: str, prefix_url: str):
        self.templates = Jinja2Templates(directory="./")
        self.templates.env.globals.update(global_context=global_context)
        self.path = path_template.replace(root_path, "")
        self.context = {}
        self.user = None
        self.prefix_url = "/page" + prefix_url

    def request(self, req: Request, res: Response, PathCheck: str = None):
        self.req = req
        # print(req.scope["route"])
        # print("log channel ", self.req.user.channel)
        # print(req.scope["route"].__dict__)
        # self.user = user
        # self.sidemenu = get_menus(1, user.id, req.scope["route"].name)

        print("req_response = ", req.user)

        if PathCheck is not None:
            path_check = PathCheck.split(".")
            if len(path_check) == 3:
                if path_check[2] != config.APP_VERSION:
                    raise HTTPException(status_code=404)
                if path_check[0] != req.user.client_id:
                    raise HTTPException(status_code=404)

            self.initContext(path_check[0], path_check[1])
        else:

            # if not config.SESSION_DISABLE:
            #     thread = threading.Thread(target=SessionRepository().updateEndTime, args=(req.state.sessionId, req.scope["path"]))
            #     thread.start()
            self.initContext(req.user.client_id, req.user.session_id)

        return req

    def addContext(self, key, value):
        self.context[key] = value

    def initContext(self, client_id, session_id):
        pass
        self.context = {}
        self.addContext("prefix_url", self.prefix_url)
        self.addContext("prefix_url_js", self.prefix_url + "/" + client_id + "." + session_id + "." + config.APP_VERSION)
        self.addContext("prefix_url_post", self.prefix_url + "/" + client_id + "." + session_id)
        self.addContext("clientId", self.req.user.client_id)
        self.addContext("sessionId", self.req.user.session_id)
        # self.addData("TOKEN_KEY", config.TOKEN_KEY)
        self.addContext("segment", self.req.scope["route"].name)
        self.addContext("userloggedin", self.req.user.username)
        # self.addData("sidemenu", self.sidemenu)
        self.addContext("TOKEN_EXPIRED", (config.COOKIES_EXPIRED * 60 * 1000) - 2000)

    def media_type(self, path: str):
        if path.find(".js") > 0:
            return "application/javascript"
        else:
            return "text/html"

    def response(self, path: str):
        return self.templates.TemplateResponse(
            request=self.req,
            name=self.path + path,
            media_type=self.media_type(path),
            context=self.context,
        )
