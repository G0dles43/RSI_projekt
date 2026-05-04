from zeep import Client

client = Client('http://localhost:8000/?wsdl')

# 1. Dodawanie wydarzenia (z symulowanym obrazkiem)
fake_image = b"TO_JEST_PLIK_BINARNY_ZDJECIA" 
res = client.service.add_event("Dni Bialegostoku", "Koncert", "2026-06-24", "Wielka feta", fake_image)
print(res)

# 2. Pobieranie raportu PDF
pdf_data = client.service.get_pdf_report()
with open("raport.pdf", "wb") as f:
    f.write(pdf_data)
print("Raport PDF został zapisany jako raport.pdf")