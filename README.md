# SparkWeather

**SparkWeather** je aplikacija koja je razvijena da se pokaže kako se vremenski podaci mogu analizirati i obrađivati pomoću distribuiranog sustava temeljenog na FastAPI-ju i PySparku. Projekt se sastoji od tri mikroservisa – `analytics`, `filter` i `trend` – a svaki od njih ima specifičnu ulogu. Za povezivanje i usmjeravanje prometa koristi se NGINX kao reverse proxy.

Cilj je bio učitati podatke iz CSV datoteke i omogućiti njihovu analizu kroz REST API-je, uz podršku za Docker i jednostavno pokretanje svih servisa.

---

## Ključne značajke

- Modularna mikroservisna arhitektura (analytics, filter, trend)
- Brza obrada podataka pomoću **Apache Spark** (PySpark)
- Analitika: prosjek, medijan, sažeci, mjesečne agregacije, trendovi
- Filtriranje vremenskih podataka po godini, gradu, vremenskom rasponu i ekstremima
- Detekcija vremenskih trendova po tjednima, mjesecima i varijablama
- Potpuna podrška za **Docker** i **Docker Compose**
- Reverse proxy pomoću **NGINX** s fallback mehanizmima

---

## Mikroservisi

| Mikroservis | Opis funkcionalnosti                               |
| ----------- | -------------------------------------------------- |
| `analytics` | Agregacije i sažeci vremenskih podataka            |
| `filter`    | Filtriranje po godini, gradu, rasponu i ekstremima |
| `trend`     | Detekcija trendova za vremenske varijable          |

---

## Tehnologije

- Python 3.11
- FastAPI
- Apache Spark (PySpark)
- Docker & Docker Compose
- NGINX (reverse proxy)

---

## CSV datoteka

Svi podaci dolaze iz `weather_data.csv` datoteke. Svaki mikroservis ima vlastitu kopiju datoteke. Očekuje se da CSV sadrži sljedeće stupce:

- datum
- država
- grad
- temperatura
- vjetar
- tlak
- vlaga
- UV_index
- oborine
- vidljivost
- oblacnost
- smjer_vjetra
- kategorija
- opis

---

## Kako pokrenuti projekt?

1. Kloniraj repozitorij:

   ```bash
   git clone https://github.com/imarkovic2002/SparkWeather-RS.git
   ```

   ```bash
   cd SparkWeather-RS

   ```

2. Pokreni sve servise odjednom (potrebno je imati instaliran Docker i Docker Compose):

   ```bash
   docker-compose up --build

   ```

3. Kad je sve spremno, dokumentaciji svakog servisa možeš pristupiti putem preglednika:

- http://localhost/analytics/docs
- http://localhost/filter/docs
- http://localhost/trend/docs

---
