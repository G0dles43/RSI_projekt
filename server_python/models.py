from spyne import ComplexModel, Unicode, Integer, ByteArray

class Event(ComplexModel):
    id = Integer
    name = Unicode
    event_type = Unicode
    date = Unicode
    description = Unicode
    poster = ByteArray # Do obs³ugi MTOM
