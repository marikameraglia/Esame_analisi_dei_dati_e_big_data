from neo4j import GraphDatabase

# ==============================================================================
# CONFIGURAZIONE CONNESSIONE NEO4J
# ==============================================================================
URI = "neo4j://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "password"  # <-- Inserisci qui la tua password di Neo4j

def esegui_e_stampa_tabella(driver, cypher_query, titoli_colonne, chiavi_record):
    """Esegue la query e stampa i risultati in una tabella formattata senza usare pandas"""
    with driver.session() as session:
        result = session.run(cypher_query)
        records = [dict(record) for record in result]
        
        if not records:
            print("Nessun risultato trovato. Verifica i dati nel database.")
            return

        # Calcola la larghezza massima per ogni colonna per l'allineamento
        larghezze = {k: len(titoli_colonne[k]) for k in chiavi_record}
        for r in records:
            for k in chiavi_record:
                valore_str = str(r.get(k, ''))
                if len(valore_str) > larghezze[k]:
                    larghezze[k] = len(valore_str)

        # Stampa l'intestazione
        riga_header = " | ".join(titoli_colonne[k].ljust(larghezze[k]) for k in chiavi_record)
        print(riga_header)
        print("-" * len(riga_header))

        # Stampa i dati
        for r in records:
            riga_dati = " | ".join(str(r.get(k, '')).ljust(larghezze[k]) for k in chiavi_record)
            print(riga_dati)

# ==============================================================================
# LE 3 QUERY ANALITICHE DEFINITIVE
# ==============================================================================

def mostra_query_1(driver):
    print("\n" + "="*80)
    print(" QUERY 1: RACCOMANDAZIONE DI LIBRI SIMILI (Target: 1984 - L06)")
    print("="*80)
    
    query = """
    MATCH (l_target:Libro {id_libro: 'L06'})
    MATCH (l_target)-[:APPARTIENE_A]->(t:Tema)<-[:APPARTIENE_A]-(l_simile:Libro)
    WHERE l_simile <> l_target

    OPTIONAL MATCH (l_target)<-[:HA_SCRITTO]-(a:Autore)-[:HA_SCRITTO]->(l_simile)

    WITH l_simile, 
         count(DISTINCT t) AS TemiInComune, 
         CASE WHEN a IS NOT NULL THEN 1 ELSE 0 END AS StessoAutore

    RETURN l_simile.id_libro AS ID,
           l_simile.titolo AS Titolo, 
           TemiInComune AS TemiInComune,
           CASE WHEN StessoAutore = 1 THEN 'Sì' ELSE 'No' END AS StessoAutore,
           (TemiInComune * 2) + (StessoAutore * 5) AS ScoreSomiglianza
    ORDER BY ScoreSomiglianza DESC, TemiInComune DESC;
    """
    titoli = {'ID': 'ID', 'Titolo': 'Titolo Libro', 'TemiInComune': 'Temi in Comune', 'StessoAutore': 'Stesso Autore', 'ScoreSomiglianza': 'Score'}
    esegui_e_stampa_tabella(driver, query, titoli, ['ID', 'Titolo', 'TemiInComune', 'StessoAutore', 'ScoreSomiglianza'])

def mostra_query_2(driver):
    print("\n" + "="*80)
    print(" QUERY 2: INDIVIDUARE LETTORI CON INTERESSI SIMILI (Target: Marika)")
    print("="*80)
    
    query = """
    MATCH (target:Lettore {email: 'marika@email.it'})-[:HA_IN_PRESTITO]->(:Copia)-[:COPIA_DI]->(:Libro)-[:APPARTIENE_A]->(t:Tema)
    MATCH (outro:Lettore)-[:HA_IN_PRESTITO]->(:Copia)-[:COPIA_DI]->(:Libro)-[:APPARTIENE_A]->(t)
    WHERE outro <> target

    RETURN outro.nome + ' ' + outro.cognome AS LettoreSimile, 
           outro.email AS Email,
           count(DISTINCT t) AS NumeroTemi, 
           collect(DISTINCT t.nome) AS TemiCondivisi
    ORDER BY NumeroTemi DESC
    LIMIT 10;
    """
    titoli = {'LettoreSimile': 'Lettore Simile', 'Email': 'Email', 'NumeroTemi': 'Temi in Comune', 'TemiCondivisi': 'Temi Condivisi'}
    esegui_e_stampa_tabella(driver, query, titoli, ['LettoreSimile', 'Email', 'NumeroTemi', 'TemiCondivisi'])

def mostra_query_3(driver):
    print("\n" + "="*80)
    print(" QUERY 3: TROVARE LE BIBLIOTECHE PIÙ VICINE AGLI INTERESSI (Target: Marika)")
    print("="*80)
    
    query = """
    MATCH (u:Lettore {email: 'marika@email.it'})-[:HA_IN_PRESTITO]->(:Copia)-[:COPIA_DI]->(:Libro)-[:APPARTIENE_A]->(tema_preferito:Tema)
    WITH DISTINCT tema_preferito

    MATCH (b:Biblioteca)-[:POSSIEDE]->(c:Copia)-[:COPIA_DI]->(l:Libro)-[:APPARTIENE_A]->(tema_preferito)
    WHERE c.stato = 'Disponibile'

    RETURN b.nome AS BibliotecaConsigliata, 
           b.citta AS Citta,
           b.quartiere AS Zona,
           count(c) AS CopieDisponibili
    ORDER BY Citta = 'Lecce' DESC, CopieDisponibili DESC;
    """
    titoli = {'BibliotecaConsigliata': 'Biblioteca Consigliata', 'Citta': 'Città', 'Zona': 'Zona / Quartiere', 'CopieDisponibili': 'Copie Disponibili'}
    esegui_e_stampa_tabella(driver, query, titoli, ['BibliotecaConsigliata', 'Citta', 'Zona', 'CopieDisponibili'])

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        print("Connessione a Neo4j stabilita con successo.")
        
        # Esecuzione delle query e stampa dei report
        mostra_query_1(driver)
        mostra_query_2(driver)
        mostra_query_3(driver)
        
        print("\n" + "="*80)
        print(" ESECUZIONE COMPLETATA CON SUCCESSO! Il grafo è pronto per la presentazione.")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione dello script: {e}")
    
    finally:
        driver.close()