from spyne import ComplexModel, Unicode, Integer, ByteArray

class Event(ComplexModel):
    """Model danych wydarzenia dla serwisu informacyjnego"""
    id = Integer
    name = Unicode
    event_type = Unicode  # np. Koncert, Teatr, Sport
    date = Unicode       # YYYY-MM-DD
    week_number = Integer
    description = Unicod    e
    
    # MTOM: To pole pozwoli nam przesyłać zdjęcia lub PDFy jako dane binarne
    # W SOAP zostanie to wysłane jako zoptymalizowany załącznik
    attachment = ByteArray