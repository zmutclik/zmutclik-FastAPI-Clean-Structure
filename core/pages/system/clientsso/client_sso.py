import os
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from core.pages.response import PageResponse, EnumJS

from core.app.security.clientsso.service import ClientSSOService
from core.app.security.clientsso.exceptions import ClientSSONotFoundException
from .request import ClientSSORequest
from .response import ClientSSOResponse
from fastapi.exceptions import RequestValidationError

router = APIRouter(prefix="/client_sso")
page = PageResponse(path_template=os.path.dirname(__file__), prefix_url="/sys" + router.prefix, depend_roles=["system"])
page_req = Annotated[PageResponse, Depends(page.request)]


@router.get("", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_clientsso(req: page_req):
    return page.response(req, "/html/index.html")


@router.get("/{PathCheck}/form/add", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_clientsso_form_add(req: page_req):
    return page.response(req, "/html/form.html")


@router.get("/{PathCheck}/{pathFile}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_clientsso_js(req: page_req, pathFile: EnumJS):
    return page.response(req, "/html/" + pathFile)


@router.get("/{PathCheck}/form/{clientsso_id}", response_class=HTMLResponse, dependencies=page.depend_w())
async def page_system_clientsso_form_edit(clientsso_id: str, req: page_req):
    page.addContext("data_clientsso", await ClientSSOService().get_clientsso(clientsso_id))
    return page.response(req, "/html/form.html")


#######################################################################################################################
@router.post("/{PathCheck}/datatables", status_code=202, dependencies=page.depend_r())
async def page_system_clientsso_datatables(params: dict[str, Any], req: page_req) -> dict[str, Any]:
    return await ClientSSOService().datatable_clientsso(params=params)


@router.post("/{PathCheck}", status_code=201, response_model=ClientSSOResponse, dependencies=page.depend_w())
async def page_system_clientsso_create(dataIn: ClientSSORequest, req: page_req):
    data_created = await ClientSSOService().create_clientsso(
        created_user=req.user.username,
        nama=dataIn.nama,
        ipaddress=dataIn.ipaddress,
        callback_uri=dataIn.callback_uri,
    )
    return data_created


@router.post("/{PathCheck}/{clientsso_id}", status_code=201, response_model=ClientSSOResponse, dependencies=page.depend_w())
async def page_system_clientsso_update(clientsso_id: str, dataIn: ClientSSORequest, req: page_req):
    data_updated = await ClientSSOService().update_clientsso(
        clientsso_id=clientsso_id,
        nama=dataIn.nama,
        ipaddress=dataIn.ipaddress,
        callback_uri=dataIn.callback_uri,
        disabled=dataIn.disabled,
    )
    return data_updated


@router.post("/{PathCheck}/{clientsso_id}/generate_clientsso_secret", status_code=201, response_model=ClientSSOResponse, dependencies=page.depend_w())
async def page_system_clientsso_clientsso_secret(clientsso_id: str, req: page_req):
    data_updated = await ClientSSOService().update_clientsso(
        clientsso_id=clientsso_id,
        clientsso_secret=True,
    )
    return data_updated


@router.delete("/{PathCheck}/{clientsso_id}", status_code=202, dependencies=page.depend_d())
async def page_system_clientsso_delete(clientsso_id: str, req: page_req):
    clientsso = await ClientSSOService().get_clientsso(clientsso_id)
    if clientsso is None:
        raise ClientSSONotFoundException
    await ClientSSOService().delete_clientsso(clientsso_id, req.user.username)
