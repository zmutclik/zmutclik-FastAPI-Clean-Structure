from ..config import config
import requests
from core.app.message.service import MessageService

list_message = {
    "otp": """Login pakai kode ini: *{code}*. 
Berlaku sampai 10 menit, dan tetap jangan kasih tahu orang lain ya! 🔒
    """
}


async def fonnte_bot_sendtext(target, message_key, data:dict):
    message = list_message[message_key].format(**data)
    token_fonnte = config.REPOSITORY["TOKEN_FONNTE"]
    headers = {"Authorization": token_fonnte.datalink}
    data = {
        "target": target,
        "message": message,
        "schedule": 0,
        "typing": "true",
        "delay": "2",
        "countryCode": "62",
    }
    send_url = "https://api.fonnte.com/send"
    data_message = await MessageService().create_message(device="fonnte", text=message, sender=token_fonnte.user, target=target)
    try:
        response = requests.post(send_url, headers=headers, data=data)
        response_json = response.json()
        # {"detail":"success! message in queue","id":["80833170"],"process":"pending","requestid":3799937,"status":true,"target":["62812345678"]}
        await MessageService().update_message(data_message.id, status=response_json["detail"])
    except requests.exceptions.RequestException as e:
        await MessageService().update_message(data_message.id, status="Error: {e}")
