import sqlite3
import sys

# ⚠️ INSERISCI QUI IL PERCORSO ASSOLUTO DEL FILE CHE VEDI SU DBEAVER
# Esempio: "C:/Users/TuoNome/Desktop/negozio.db" 
NOME_DB = r"C:\Users\angel\Desktop\magazzino_finale"  

try:
    conn = sqlite3.connect(NOME_DB)
    cursor = conn.cursor()
    print(f"✅ Connessione al database SQLite '{NOME_DB}' riuscita con successo!\n")
except Exception as e:
    print(f"❌ Errore durante la connessione al database: {e}")
    sys.exit()

print("=========================================================================")

# 🚚 QUERY 1: Elencare gli ordini spediti tramite un determinato corriere
print("\n🔍 QUERY 1: Ordini spediti tramite corriere 'DHL Express'")
query_1 = """
SELECT 
    o.IdOrdine, 
    o.DataOrdine, 
    o.StatoOrdine, 
    s.IdSpedizione, 
    s.StatoSpedizione, 
    c.Nome
FROM ORDINE o
JOIN SPEDIZIONE s ON o.IdSpedizione = s.IdSpedizione
JOIN CORRIERE c ON s.IdCorriere = c.IdCorriere
WHERE c.Nome = 'DHL Express';
"""
cursor.execute(query_1)
results_1 = cursor.fetchall()
if not results_1:
    print("Nessun record trovato. Verifica se hai effettuato il Commit su DBeaver!")
for row in results_1:
    print(f"- Ordine ID: {row[0]} | Data: {row[1]} | Stato Ordine: {row[2]} | Spedizione ID: {row[3]} | Stato Spedizione: {row[4]} | Corriere: {row[5]}")


print("\n=========================================================================")


# 🏆 QUERY 2: Trovare i prodotti presenti nel mayor numero di ordini
print("\n🔍 QUERY 2: Classifica Prodotti presenti nel maggior numero di ordini")
query_2 = """
SELECT 
    p.CodiceProd, 
    p.Nome AS NomeProdotto, 
    COUNT(ro.IdOrdine) AS NumeroDiOrdiniInCuiEPresente
FROM PRODOTTO p
JOIN RIGA_ORDINE ro ON p.CodiceProd = ro.CodiceProd
GROUP BY p.CodiceProd, p.Nome
ORDER BY NumeroDiOrdiniInCuiEPresente DESC;
"""
cursor.execute(query_2)
for row in cursor.fetchall(): # Rimosso [:10], mostra TUTTI i prodotti
    print(f"- Codice: {row[0]} | Prodotto: {row[1][:30]:<30} | Presente in {row[2]} ordini")


print("\n=========================================================================")


# 📦 QUERY 3: Controllare le giacenze
print("\n🔍 QUERY 3: Controllo Giacenze di Magazzino (Tutti i prodotti)")
query_3 = """
SELECT CodiceProd, Nome, QuantitaDisponibile 
FROM PRODOTTO;
"""
cursor.execute(query_3)
for row in cursor.fetchall(): # Rimosso [:10], mostra TUTTI i prodotti
    print(f"- Codice: {row[0]} | Prodotto: {row[1][:35]:<35} | Q.tà Disponibile: {row[2]}")


print("\n=========================================================================")


# ⏱️ QUERY 4: Monitorare le spedizioni
print("\n🔍 QUERY 4: Monitoraggio complessivo delle Spedizioni")
query_4 = """
SELECT o.IdOrdine, s.IdSpedizione, c.Nome, s.StatoSpedizione, s.DataPartenza
FROM ORDINE o
JOIN SPEDIZIONE s ON o.IdSpedizione = s.IdSpedizione
JOIN CORRIERE c ON s.IdCorriere = c.IdCorriere;
"""
cursor.execute(query_4)
for row in cursor.fetchall(): # Rimosso [:10]
    print(f"- Ordine: {row[0]} | Spedizione ID: {row[1]} | Corriere: {row[2]:<12} | Stato Spedizione: {row[3]:<12} | Data Partenza: {row[4]}")


print("\n=========================================================================")


# 📅 QUERY 5: Verificare i tempi di consegna sfruttando la colonna generata nel DDL
print("\n🔍 QUERY 5: Calcolo dei Giorni di Consegna (Verifica Tempi)")
query_5 = """
SELECT IdSpedizione, DataPartenza, DataConsegnaPrevista,
       CAST(julianday(DataConsegnaPrevista) - julianday(DataPartenza) AS INT) AS GiorniDiConsegna
FROM SPEDIZIONE;
"""
cursor.execute(query_5)
for row in cursor.fetchall():
    print(f"- Spedizione ID: {row[0]} | Partenza: {row[1]} | Consegna Prevista: {row[2]} | Giorni Stimati: {row[3]}")


print("\n=========================================================================")


# 💰 QUERY 6: Vedere totale ordine
print("\n🔍 QUERY 6: Calcolo del Valore Economico Totale di ciascun Ordine")
query_6 = """
SELECT o.IdOrdine, o.DataOrdine, SUM(ro.Quantita * ro.PrezzoApplicato) AS Totale_Ordine
FROM ORDINE o
JOIN RIGA_ORDINE ro ON o.IdOrdine = ro.IdOrdine
GROUP BY o.IdOrdine, o.DataOrdine;
"""
cursor.execute(query_6)
for row in cursor.fetchall():
    print(f"- Ordine ID: {row[0]} | Data Ordine: {row[1]} | 💰 VALORE TOTALE: {row[2]:.2f} €")


print("\n=========================================================================")

# Chiusura finale
cursor.close()
conn.close()
print("\n🔌 Connessione chiusa. Script completato.")