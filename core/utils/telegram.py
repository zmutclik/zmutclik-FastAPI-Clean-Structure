from ..config import config
import requests
from core.app.message.service import MessageService

list_message = {
    "register_alert": """<b>AKUN SUKSES TERDAFTAR</b>
<code>app   : {app}</code>
<code>user  : {user}</code>
<code>email : {email}</code>
    """
}


async def telegram_bot_sendtext(message_key, data: dict):
    message = list_message[message_key].format(**data)
    token_telegram = config.REPOSITORY["TOKEN_TELEGRAM"]
    bot_token = token_telegram.datalink
    bot_chatID = token_telegram.user
    url_param_1 = "sendMessage"
    url_param_2 = ""
    url_param_3 = ""
    send_url = "https://api.telegram.org/bot{}/{}?chat_id={}&parse_mode=html{}&text={}{}"
    send_text = send_url.format(bot_token, url_param_1, bot_chatID, url_param_2, message, url_param_3)

    data_message = await MessageService().create_message(device="telegram", text=message, sender=token_telegram.user, target=token_telegram.name)
    try:
        response = requests.get(send_text)
        response_json = response.json()
        await MessageService().update_message(data_message.id, status=response_json["ok"])
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        await MessageService().update_message(data_message.id, status="Error")
