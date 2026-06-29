import json
from elasticsearch import Elasticsearch

# 1. CONNESSIONE AD ELASTICSEARCH
es = Elasticsearch(["http://localhost:9200"])

if es.ping():
    print("✅ Connessione a Elasticsearch riuscita con successo!\n")
else:
    print("❌ Impossibile connettersi a Elasticsearch. Verifica che sia avviato.")
    exit()

print("=========================================================================")

# 📊 QUERY 1: Ricerca per frase esatta negli Hotel
print("\n🔍 ESECUZIONE QUERY 1 (Hotel): Ricerca 'camere silenziose'")
query_1a = {
    "match_phrase": {
        "descrizione": "camere silenziose"
    }
}
res_1a = es.search(index="hotel", query=query_1a)

for hit in res_1a['hits']['hits']:
    print(f"- Hotel: {hit['_source']['nome']} ({hit['_source']['citta']}) | Descrizione: {hit['_source']['descrizione'][:60]}...")


print("\n=========================================================================")


# 📊 QUERY 1: Ricerca testuale nelle Recensioni
print("\n🔍 ESECUZIONE QUERY 1 (Recensioni): Ricerca 'vista panoramica'")
query_1b = {
    "match": {
        "testo_recensione": "vista panoramica"
    }
}
res_1b = es.search(index="recensioni", query=query_1b)

for hit in res_1b['hits']['hits']:
    print(f"- Utente: {hit['_source']['utente']} | ID Hotel: {hit['_source']['id_hotel']} | Recensione: \"{hit['_source']['testo_recensione']}\"")


print("\n=========================================================================")


# 📊 QUERY 2: Filtro combinato (Roma, Prezzo tra 100€ e 300€)
print("\n🎯 ESECUZIONE QUERY 2: Hotel a Roma con budget 100€ - 300€")
query_2 = {
    "bool": {
        "filter": [
            { "term": { "citta": "Roma" } },
            { "range": { "prezzo_notte": { "gte": 100, "lte": 300 } } }
        ]
    }
}
res_2 = es.search(index="hotel", query=query_2)

for hit in res_2['hits']['hits']:
    print(f"- {hit['_source']['nome']} | Città: {hit['_source']['citta']} | Prezzo/Notte: {hit['_source']['prezzo_notte']}€")


print("\n=========================================================================")


# 📊 QUERY 3: Aggregazione Analitica (Voto medio servizi e pulizia massima per hotel)
print("\n📈 ESECUZIONE QUERY 3: Aggregazioni e Statistiche sulle Recensioni")
aggs_3 = {
    "raggruppamento_per_hotel": {
        "terms": {
            "field": "id_hotel"
        },
        "aggs": {
            "voto_medio_servizi": {
                "avg": { "field": "punteggio_servizi" }
            },
            "voto_massimo_pulizia": {
                "max": { "field": "punteggio_pulizia" }
            }
        }
    }
}

res_3 = es.search(index="recensioni", size=0, aggs=aggs_3)

buckets = res_3['aggregations']['raggruppamento_per_hotel']['buckets']
for bucket in buckets:
    hotel_id = bucket['key']
    media_servizi = bucket['voto_medio_servizi']['value']
    max_pulizia = bucket['voto_massimo_pulizia']['value']
    print(f"- ID Hotel: {hotel_id} | Media Servizi: {media_servizi:.2f} ⭐ | Pulizia Max: {max_pulizia} ⭐")

print("\n=========================================================================")