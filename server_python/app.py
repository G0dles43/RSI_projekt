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
    @rpc(Unicode, Unicode, _returns=Unicode)
    def test_connection(ctx, name, date):
        return f"Serwer RSI dziala! Witaj {name}. Dzisiejsza data to {date}."

application = Application(
    [BialystokInfoService],
    tns='pl.bialystok.info',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    # TU RÓWNIEŻ ZMIANA (usunięte Py)
    wsgi_app = WsgiApplication(application) 
    server = make_server('0.0.0.0', 8000, wsgi_app)
    
    print("\n" + "="*42)
    print("SERWER RSI URUCHOMIONY POPRAWNIE!")
    print("Adres: http://localhost:8000")
    print("WSDL:  http://localhost:8000/?wsdl")
    print("="*42 + "\n")
    
    server.serve_forever()
