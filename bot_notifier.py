import sys
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="xgsvnz Order Notifier API")

# Konfigurasi WhatsApp Admin
TARGET_PHONE = "62895622363969"  # Nomor WA Admin (Format internasional tanpa '+')
FONNTE_TOKEN = "YOUR_FONNTE_TOKEN"  # Masukkan Token Fonnte / WhatsApp Gateway Kamu

class OrderSchema(BaseModel):
    name: str
    contact: str
    service: str
    details: str

def send_whatsapp_notification(order: OrderSchema):
    text = (
        f"🚨 *ORDER BARU xgsvnz* 🚨\n\n"
        f"👤 *Nama:* {order.name}\n"
        f"📞 *Kontak:* {order.contact}\n"
        f"💼 *Layanan:* {order.service}\n"
        f"📝 *Detail:* {order.details}"
    )
    
    # Menggunakan Fonnte API
    url = "https://api.fonnte.com/send"
    payload = {
        "target": TARGET_PHONE,
        "message": text,
    }
    headers = {
        "Authorization": FONNTE_TOKEN
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        print("Response WA:", response.json())
    except Exception as e:
        print(f"Gagal mengirim notifikasi WhatsApp: {e}")

@app.post("/api/notify")
async def receive_order(order: OrderSchema):
    # Kirim notifikasi otomatis ke WhatsApp Admin
    if FONNTE_TOKEN != "YOUR_FONNTE_TOKEN":
        send_whatsapp_notification(order)
    else:
        print("Notifikasi WA dilewati: Token belum diisi.")
    
    return {"status": "success", "message": f"Order dari {order.name} berhasil diproses!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
