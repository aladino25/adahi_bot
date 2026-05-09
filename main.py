import requests
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "8715583562:AARHrfJi6UMDRBaDt0Rca1pcN0BTJP0-5Arw"
CHAT_ID = "1743632394"

last_wilayas = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print("خطأ في الإرسال:", e)

def check_adahi():
    global last_wilayas
    try:
        print(f"[{time.strftime('%H:%M:%S')}] جاري الفحص...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get("https://www.adahi.dz/wilayas", headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        available = set()
        for line in soup.get_text().split('\n'):
            if '–' in line:
                parts = line.split('–')
                if len(parts) >= 2 and 'متوفر' in parts[1] and 'غير' not in parts[1]:
                    available.add(parts[0].strip())
        
        new_wilayas = available - last_wilayas
        if new_wilayas:
            msg = "🚨 ولايات جديدة متوفرة! 🚨\n\n"
            for w in new_wilayas:
                msg += f"✅ {w}\n"
            send_telegram(msg)
            print(f"📨 تم الإرسال: {new_wilayas}")
        
        last_wilayas = available
        print(f"[{time.strftime('%H:%M:%S')}] اكتمل الفحص")
        
    except Exception as e:
        print("خطأ:", e)

print("🚀 تشغيل بوت مراقبة أضاحي...")
while True:
    check_adahi()
    time.sleep(30)
Rédiger
