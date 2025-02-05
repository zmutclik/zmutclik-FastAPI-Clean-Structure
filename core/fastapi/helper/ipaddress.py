from fastapi import Request


def get_ipaddress(request: Request):
    ipaddress = request.client.host
    ipproxy = None
    try:
        if request.headers.get("X-Real-IP") is not None:
            ipaddress = request.headers.get("X-Real-IP")
            ipproxy = request.client.host
    except:
        pass

    return ipaddress, ipproxy
