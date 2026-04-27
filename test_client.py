from zeep import Client
import sys

url = 'http://localhost:8000/?wsdl'

print(f"--- Próba połączenia z: {url} ---")

try:
    # 1. Inicjalizacja klienta
    client = Client(url)
    print("--- Klient zainicjalizowany poprawnie ---")

    # 2. Wywołanie metody
    # Upewnij się, że nazwa metody to test_connection (tak jak w app.py)
    print("--- Wywołuję metodę test_connection... ---")
    response = client.service.test_connection("Bartek", "2026-04-27")

    # 3. Wyświetlenie wyniku
    print("\n" + "="*40)
    print("SUKCES! Odpowiedź z serwera:")
    print(f">>> {response} <<<")
    print("="*40 + "\n")

except Exception as e:
    print("\n" + "!"*40)
    print(f"WYSTĄPIŁ BŁĄD: {e}")
    print("!"*40 + "\n")