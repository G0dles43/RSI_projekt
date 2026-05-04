import sys
import six

# --- UNIWERSALNY PATCH DLA SPYNE V4 ---
# Definiujemy brakującą funkcję, której spyne szuka w bibliotece six
if not hasattr(six, 'get_function_name'):
    def get_function_name(f):
        return f.__name__
    six.get_function_name = get_function_name

# Przekierowujemy moduły
sys.modules['spyne.util.six'] = six
sys.modules['spyne.util.six.moves'] = six.moves
sys.modules['spyne.util.six.moves.collections_abc'] = six.moves.collections_abc
sys.modules['spyne.util.six.moves.http_cookies'] = six.moves.http_cookies
sys.modules['spyne.util.six.moves.urllib'] = six.moves.urllib
sys.modules['spyne.util.six.moves.urllib.parse'] = six.moves.urllib_parse
# --------------------------------------

import json
import os
import io
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Array, ByteArray
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from reportlab.pdfgen import canvas

class BialystokInfoService(ServiceBase):
    DB_FILE = 'events.json'

    def _get_db(self):
        if not os.path.exists(self.DB_FILE):
            return []
        with open(self.DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_db(self, db):
        with open(self.DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)

    @rpc(Unicode, Unicode, Unicode, Unicode, ByteArray, _returns=Unicode)
    def add_event(ctx, name, event_type, date, description, image_data):
        """Dodaje wydarzenie i zapisuje obrazek (MTOM)"""
        svc = BialystokInfoService()
        db = svc._get_db()
        
        event_id = len(db) + 1
        
        # Obsługa obrazka (MTOM / Dane binarne)
        image_path = ""
        if image_data:
            if not os.path.exists('data'): 
                os.makedirs('data')
            image_path = f"data/event_{event_id}.jpg"
            with open(image_path, 'wb') as f:
                # NAPRAWIONE: Sklejamy tuple bajtów w jeden obiekt bytes
                f.write(b''.join(image_data)) 

        new_event = {
            "id": event_id,
            "name": name,
            "type": event_type,
            "date": date,
            "description": description,
            "image": image_path
        }
        
        db.append(new_event)
        svc._save_db(db)
        return f"Dodano wydarzenie: {name} (ID: {event_id})"

    @rpc(Unicode, _returns=Array(Unicode))
    def get_events(ctx, date):
        """Pobiera nazwy wydarzeń dla danej daty"""
        svc = BialystokInfoService()
        db = svc._get_db()
        return [f"{e['name']} [{e['type']}]" for e in db if e['date'] == date]

    @rpc(_returns=ByteArray)
    def get_pdf_report(ctx):
        """Generuje PDF z listą wszystkich wydarzeń"""
        svc = BialystokInfoService()
        db = svc._get_db()
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, "SERWIS INFORMACYJNY BIAŁYSTOK - RAPORT")
        y = 750
        for e in db:
            p.drawString(100, y, f"- {e['date']}: {e['name']} ({e['type']})")
            y -= 20
        p.showPage()
        p.save()
        return buffer.getvalue()

# Logowanie wywołań (Wymóg: Handlers)
def on_method_call(ctx):
    print(f"--- [HANDLER] Wywołano metodę: {ctx.method_name} ---")

BialystokInfoService.event_manager.add_listener('method_call', on_method_call)

application = Application(
    [BialystokInfoService],
    tns='pl.bialystok.info',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    print("\nSERWER BIAŁYSTOK INFO URUCHOMIONY!")
    server.serve_forever()