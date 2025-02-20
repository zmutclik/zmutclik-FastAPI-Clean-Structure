from ..config import config
import requests
from core.app.message.service import MessageService

list_message = {
    "otp": """Login pakai kode ini: *{code}*. 
Berlaku sampai 5 menit, dan tetap jangan kasih tahu orang lain ya! 🔒
    """,
    "reset_code": """Kami menerima permintaan untuk mereset kode akun Anda. 
Silakan gunakan link berikut untuk mengatur ulang akun Anda: 
_reset url_ : *{link}*
_reset kode_ : *{code}*
link ini berlaku selama 15 menit. 
Jangan bagikan kode ini kepada siapa pun demi keamanan akun Anda. 
Jika Anda tidak meminta reset akun, harap abaikan pesan ini.

Terima kasih,
    """,
    "password_change": """Halo {full_name},

Kami ingin memberitahukan bahwa password akun Anda telah berhasil diperbarui pada {tanggal}. Jika Anda yang melakukan perubahan ini, tidak ada tindakan lebih lanjut yang diperlukan.
Namun, jika Anda tidak mengenali perubahan ini, segera hubungi tim dukungan kami di iT SIMRS untuk mengamankan akun Anda.

Jaga keamanan akun Anda dengan tidak membagikan informasi login kepada siapa pun.

Terima kasih,""",
}


async def fonnte_bot_sendtext(target, message_key, data: dict):
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
