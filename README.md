# Sistema Integrato di Storage Transazionale, Graph Analytics ed Enterprise Search

## 🎓 Progetto d'Esame: Analisi dei Dati e Big Data
**Università del Salento (UniSalento)** **Corso di Laurea Magistrale in Data Science per le Scienze Umane e Sociali** ### 👥 Il Team
**Angelica Carrieri** & **Marika Meraglia** ---

## 📌 Visione d'Insieme del Progetto

Il progetto simula l'infrastruttura dati di un'azienda moderna basata sulla **Polyglot Persistence**: l'idea di far cooperare database diversi tra loro a seconda del lavoro da svolgere. Invece di usare un solo database per fare tutto, questa architettura ne integra tre (uno relazionale e due NoSQL), collegati e gestiti insieme tramite script **Python**.

```text
                                            │   PIPELINE DATA SCIENCE   │
                                        └─────────────┬─────────────┘
                                                          │ (Python Drivers)
    ┌─────────────────────────────────────────┼─────────────────────────────────────────┐
    ▼                                         ▼                                         ▼
┌───────────────────────┐             ┌───────────────────────┐             ┌───────────────────────┐
│    MySQL / DBeaver    │             │         Neo4j         │             │     Elasticsearch     │
├───────────────────────┤             ├───────────────────────┤             ├───────────────────────┤
│ OLTP Core             │             │ Graph Analytics       │             │ Enterprise Search     │
│ Transazioni &         │             │ Raccomandazioni       │             │ Ricerca di Testo      │
│ Logistica             │             │ & Affinità            │             │ & Statistiche         │
└───────────────────────┘             └───────────────────────┘             └───────────────────────┘

```text

## 🛠️ Architettura Dati e Casi d'Uso

### 1. Database Relazionale (MySQL / DBeaver) — *Traccia: Magazzino e Spedizioni*
Gestisce i dati aziendali più delicati relativi alla logistica (ordini e clienti), dove non sono ammessi errori o perdite di dati.
* **Modellazione:** Progettato tramite Schema E-R e organizzato in **Terza Forma Normale (3NF)** per eliminare dati duplicati e prevenire errori di inserimento.
* **Cosa fa:** Monitora lo stato delle spedizioni, controlla le quantità di prodotti in magazzino e calcola i tempi di consegna dei corrieri.
* **Query Principali (SQL):** * Conteggio degli ordini spediti da un preciso corriere.
  * Classifica dei prodotti più venduti per capire quali sono i più richiesti.

### 2. Database NoSQL a Grafo (Neo4j) — *Traccia: Rete di Biblioteche e Libri*
Utilizza il modello a grafi per collegare i dati in modo nativo. Trova relazioni e collegamenti tra i dati del Salento in tempo reale, senza rallentare il sistema come succederebbe in SQL con troppe tabelle collegate.
* **Modellazione:** Separazione netta tra il `Libro` come opera astratta (titolo, autore) e la `Copia` come oggetto fisico (il volume cartaceo che si trova in una specifica biblioteca).
* **Ottimizzazione:** Inserimento di blocchi per evitare duplicati, creazione di indici velocizzanti e popolamento rapido dei dati.
* **Query Principali (Cypher):**
  * **Motore di Raccomandazione:** Calcola il punteggio di somiglianza tra libri in base ai temi comuni e all'autore.
  * **Filtraggio Collaborativo:** Analizza i gusti dei lettori per consigliare libri simili scelti da utenti con abitudini simili.
  * **Geolocalizzazione:** Trova la biblioteca reale del Salento più vicina che ha la copia fisica di un libro sbloccata come "Disponibile".

### 3. Database NoSQL Documentale (Elasticsearch & Kibana) — *Traccia Libera*
Un motore di ricerca super veloce basato su file JSON, specializzato nel trovare parole chiave all'interno di testi lunghi e nel calcolare statistiche al volo.
* **Modellazione:** Configurazione dei campi di ricerca distinguendo i testi liberi (es. le recensioni degli hotel), le parole esatte (es. i nomi delle città) e le coordinate geografiche (latitudine e longitudine).
* **Query Principali (Query DSL):**
  * **Ricerca Testuale Intelligente (Fuzzy Search):** Trova concetti simili nelle recensioni (es. *"camere silenziose"* o *"vista mare"*) calcolando il punteggio di rilevanza anche in presenza di errori di battitura.
  * **Filtri Combinati:** Ricerche veloci che incrociano la posizione geografica dell'utente e le fasce di prezzo dell'hotel.
  * **Statistiche in Tempo Reale (Aggregations):** Calcola istantaneamente medie e metriche (es. il prezzo medio degli hotel per ogni città) sui dati trovati.

---

## 📊 I Numeri del Progetto
I database sono stati popolati con molti dati per testare la velocità e la tenuta del sistema:
* **Dati in SQL:** `624` righe totali distribuite tra le varie tabelle.
* **Nodi nel Grafo (Neo4j):** `1.137` elementi creati.
* **Collegamenti nel Grafo (Neo4j):** `2.314` relazioni inserite tra i nodi.

---

## 🛠️ Guida all'Installazione e Uso

### Prerequisiti
* **Python** (versione 3.8 o superiore)
* Server **MySQL** attivo
* Istanza **Neo4j** attiva (in locale o su Cloud)
* **Elasticsearch** e **Kibana** attivi

### 1. Scaricare il Progetto
Apri il terminale del computer e digita:
```bash
git clone [https://github.com/](https://github.com/)[TuoUsername]/[NomeRepo].git
cd [NomeRepo]