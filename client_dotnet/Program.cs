using System;
using System.Threading.Tasks;

// Nazwa przestrzeni nazw z wygenerowanego pliku (sprawdź w ServiceReference1.cs)
using ServiceReference; 

class Program
{
    static async Task Main(string[] args)
    {
        Console.WriteLine("Łączenie z serwerem Pythona z C#...");
        
        var client = new BialystokInfoServicePortTypeClient();
        
        try
        {
            // Wywołujemy Twoją metodę testową
            var result = await client.test_connectionAsync("Bartek (z C#)", "2026-04-27");
            
            Console.WriteLine("================================");
            Console.WriteLine("ODPOWIEDŹ Z SERWERA:");
            Console.WriteLine(result);
            Console.WriteLine("================================");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Błąd: {ex.Message}");
        }
        finally
        {
            await client.CloseAsync();
        }
    }
}