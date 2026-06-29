# Sistema Integrato di Storage Transazionale, Graph Analytics ed Enterprise Search

## 🎓 Progetto d'Esame: Analisi dei Dati e Big Data
**Università del Salento (UniSalento)**  
**Corso di Laurea Magistrale in Data Science per le Scienze Umane e Sociali**  

### 👥 Il Team
**Angelica Carrieri** &
**Marika Meraglia**  

---

## 📌 Visione d'Insieme del Progetto
Il progetto simula un'infrastruttura dati aziendale di livello Enterprise basata sul paradigma della **Polyglot Persistence**. Invece di forzare un singolo database a rispondere a requisiti di business eterogenei, l'architettura integra tre tecnologie complementari (SQL, NoSQL a Grafi, NoSQL Documentale), orchestrate e interrogate tramite moduli **Python**.

                                 │   PIPELINE DATA SCIENCE   │
                             └─────────────┬─────────────┘
                                               │(Python Drivers)
     ┌───────────────────────────────┼──────────────────────────────┐
     ▼                               ▼                              ▼
┌─────────────────┐             ┌─────────────────┐            ┌───────────────────┐
│ MySQL / DBeaver │             │      Neo4j      │            │   Elasticsearch   │
├─────────────────┤             ├─────────────────┤            ├───────────────────┤
│ OLTP Core       │             │ Graph Analytics │            │ Enterprise Search │
│ Transazioni &   │             │ Raccomandazioni │            │ Full-Text Fuzzy   │
│ Logistica ACID  │             │ & Affinità      │            │ & Aggregations    │
└─────────────────┘             └─────────────────┘            └───────────────────┘

## 🛠️ Architettura Dati e Casi d'Uso

### 1. Database Relazionale (MySQL / DBeaver) — Traccia: *Magazzino e Spedizioni*
Gestisce lo strato operazionale e transazionale core (**OLTP**) per la logistica aziendale, garantendo l'integrità referenziale assoluta e il rispetto formale delle proprietà **ACID**.
* **Modellazione:** Schema concettuale E-R e schema logico rigorosamente normalizzato in **Terza Forma Normale (3NF)** per eliminare anomalie di inserimento e ridondanze.
* **Funzionalità:** Monitoraggio dello stato delle spedizioni, controllo in tempo reale delle giacenze di magazzino e auditing dei tempi di consegna dei corrieri.
* **Query Core (SQL):** * Estrazione e conteggio analitico degli ordini evasi e associati a uno specifico vettore logistico.
  * Individuazione e ranking dei prodotti con la massima frequenza di inserimento nelle righe d'ordine (*analisi di densità di vendita*).

### 2. Database NoSQL a Grafo (Neo4j) — Traccia: *Rete di Biblioteche e Libri*
Sfrutta il modello **Labeled Property Graph (LPG)** e l'architettura nativa *Index-free Adjacency* per esplorare in tempo reale relazioni e cammini complessi sul territorio del Salento, azzerando il costo computazionale delle JOIN relazionali su grandi volumi.
* **Modellazione:** Separazione a grana fine tra l'entità concettuale (`Libro`, contenente proprietà immutabili) e l'entità fisica e locale (`Copia`, dotata di attributi dinamici e di stato).
* **Ottimizzazione:** Configurazione di asserzioni di unicità (`CONSTRAINT`), indici di intervallo (`RANGE INDEX`) e popolamento massivo idempotente tramite clausole `MERGE`.
* **Query Core (Cypher):**
  * **Recommendation Engine:** Calcolo di uno *Score di Somiglianza* pesato tra opere, basato sull'intersezione di tassonomie tematiche e paternità dell'autore.
  * **Collaborative Filtering:** Analisi della rete di lettura finalizzata a mappare l'affinità psicografica tra lettori per anticipare i comportamenti di prestito.
  * **Routing Geo-Logistico:** Interrogazione accoppiata a vincoli di stato per instradare gli utenti verso le biblioteche reali del Salento più vicine aventi volumi contrassegnati come `'Disponibile'`.

### 3. Database NoSQL Documentale (Elasticsearch & Kibana) — *Traccia Libera*
Funge da motore di indicizzazione invertito distribuito, ottimizzato per lo storage denormalizzato di oggetti JSON e per l'esecuzione di interrogazioni semantiche e aggregazioni analitiche in tempo reale.
* **Modellazione:** Definizione esplicita del *Mapping* strutturato, isolando i campi di ricerca testuale (`text` associati ad analizzatori linguistici standard) dalle stringhe di corrispondenza esatta (`keyword`) e dalle coordinate geografiche (`geo_point`).
* **Query Core (Query DSL):**
  * **Full-Text Fuzzy Search:** Ricerca semantica avanzata con calcolo nativo del punteggio di rilevanza (algoritmo *BM25*) per concetti sfumati (es. *"vista panoramica"*, *"camere silenziose"*) nelle recensioni.
  * **Boolean Filter Routing:** Combinazione logica di vincoli strutturati (`must`, `range`) ottimizzata tramite cache a bitset interna per ricerche spaziali e per fasce di prezzo.
  * **Real-time Aggregations:** Computazione di metriche aggregate e statistiche descrittive (es. calcolo della distribuzione del prezzo medio per città) calcolate dinamicamente sui cluster di documenti estratti.

---

## 📊 Analisi Quantitativa del Deployment
I tre database sono stati popolati in modo massivo con dataset speculari, simulando volumi aziendali atti a saggiare la bontà e la scalabilità dei piani di esecuzione:
* **Record Relazionali (SQL):** `624` tuple transazionali distribuite sulle tabelle operazionali.
* **Nodi nel Grafo (Neo4j):** `1.137` nodi logici e fisici istanziati.
* **Relazioni nel Grafo (Neo4j):** `2.314` archi tipizzati, orientati e dotati di proprietà.

---

## 💻 Guida all'Installazione e Deployment

### Prerequisiti
* **Python** versione 3.8 o superiore
* Server **MySQL** attivo (locale o remoto)
* Istanza **Neo4j** attiva (locale o tramite Neo4j AuraDB)
* Cluster **Elasticsearch** (locale o tramite Elastic Cloud) con **Kibana** attivo

### 1. Clonazione del Repository
Aprire il terminale e clonare il codice sorgente:
```bash
git clone [https://github.com/](https://github.com/)[TuoUsername]/[NomeRepo].git
cd [NomeRepo]

2. Configurazione dell'Ambiente Python
Installare i driver e i client SDK ufficiali per consentire a Python l'interazione nativa con i tre motori di database:
pip install mysql-connector-python neo4j elasticsearch

3. Esecuzione dei Moduli di Analisi
I moduli contenuti nella cartella src/ implementano la logica di connessione, inviano le query analitiche e stampano l'output formattato direttamente in console:

Esecuzione Query Relazionali (SQL):
python src/progetto_sql.py

Esegui analisi di Grafo (Neo4j):
python src/progetto_grafo.py

Esegui ricerche Documentali (Elasticsearch):
python src/progetto_search.py

📂 Struttura delle Cartelle
Il repository è strutturato seguendo le migliori pratiche di ingegneria del software per garantire la massima leggibilità, la modularità dei codici e un isolamento netto delle tecnologie utilizzate:

├── README.md               # Questa introduzione di progetto
├── docs/                   # Documentazione ufficiale d'esame
│   └── Presentazione_Esame_BigData.pdf  # Slide in formato PDF per la discussione orale
├── sql_relational/         # Cartella 1: Modello Relazionale (MySQL)
│   ├── schemaand_data_population.sql          # Script DDL (CREATE TABLE, vincoli, indici)
│   └── queries.sql # Script DML (INSERT delle anagrafiche e delle transazioni)
├── graph_neo4j/            # Cartella 2: Modello a Grafi (Neo4j)
│   ├── constraints_and_population.cypher  # Vincoli di unicità (Assertion) e indici grafici
│   └── queries.cypher # Popolamento e query in Cypher
├── nosql_elasticsearch/    # Cartella 3: Modello Documentale (Elasticsearch)
│   ├── mapping_hotel.json  # Definizione esplicita delle proprietà del Mapping JSON
│   └── queries_dsl.json    # Strutture di ricerca Full-Text e Aggregations in Query DSL
├── src/                    # Cartella 4: Core Engine Python
│   ├── progetto_sql.py     # Connessione al DBMS relazionale ed esecuzione query
│   ├── progetto_grafo.py   # Driver di interazione ed estrazione cammini su Neo4j
│   └── progetto_search.py  # Client di invio payload ed estrazione hit da Elasticsearch
└── assets/                 # Cartella 5: Risorse Visive del Progetto
    ├── diagramma_er.png    # Diagramma concettuale Entity-Relationship
    ├── diagramma_strisce   # Diagramma a strisce
    ├── schema_arrows.png   # Schema logico del grafo (progettato su Arrows.app)
    └──  elastic_search_1_2_3_4 # Screenshot delle visualizzazioni analitiche di Kibana
   

