# SparkWeather

**SparkWeather** je distribuirana aplikacija za analizu i upravljanje vremenskim podacima koristeći **FastAPI**, **PySpark** i **cloud-native DynamoDB** (emuliran pomoću LocalStacka). Aplikacija učitava podatke iz CSV datoteke i omogućuje analizu, filtriranje, brisanje i vizualizaciju vremenskih podataka putem REST API-ja.

---

## Značajke

- REST API razvijen u FastAPI-u
- Obrada podataka pomoću PySparka
- Podrška za cloud-native bazu (DynamoDB preko LocalStacka)
- Učitavanje velikih CSV datoteka
- GET i DELETE rute za dohvat i brisanje
- Docker & Docker Compose podrška

---

## Tehnologije

- Python 3.11
- FastAPI
- PySpark
- DynamoDB (LocalStack)
- Docker, Docker Compose

--- 
## Struktura podataka (CSV)

CSV datoteka mora sadržavati sljedeće stupce:
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

## Pokretanje projekta

1. Kloniraj repozitorij:

```bash
git clone https://github.com/imarkovic2002/SparkWeather-RS
cd SparkWeather
```

2. Pokreni aplikaciju i bazu
```bash
```

3. Učitaj CSV podatke u DynamoDB
```bash
```

## API dokumentacija
Nakon pokretanja, pristupi FastAPI dokumentaciji:
```bash
http://localhost:8000/docs
```
