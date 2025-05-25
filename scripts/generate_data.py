import csv
import random
from datetime import datetime, timedelta

# Parametri
broj_redaka = 10_000_000
datum_pocetni = datetime(2020, 1, 1)
datum_zavrsni = datetime(2024, 12, 31)

# Prošireni skup država i gradova
drzave_gradovi = {
    'Hrvatska': ['Zagreb', 'Split', 'Rijeka', 'Osijek', 'Zadar'],
    'BiH': ['Sarajevo', 'Mostar', 'Banja Luka', 'Tuzla', 'Zenica'],
    'Srbija': ['Beograd', 'Novi Sad', 'Niš', 'Kragujevac', 'Subotica'],
    'Mađarska': ['Budimpešta', 'Debrecen', 'Szeged', 'Pécs', 'Miskolc'],
    'Slovenija': ['Ljubljana', 'Maribor', 'Celje', 'Koper', 'Nova Gorica'],
    'Austrija': ['Beč', 'Graz', 'Linz', 'Salzburg', 'Innsbruck'],
    'Njemačka': ['Berlin', 'München', 'Hamburg', 'Köln', 'Frankfurt', 'Stuttgart', 'Dresden'],
    'Crna Gora': ['Podgorica', 'Nikšić', 'Bar', 'Herceg Novi', 'Bijelo Polje'],
    'Albanija': ['Tirana', 'Drač', 'Vlorë', 'Shkodër', 'Elbasan'],
    'Sjeverna Makedonija': ['Skoplje', 'Bitola', 'Tetovo', 'Ohrid', 'Kumanovo'],
    'Italija': ['Rim', 'Milano', 'Napulj', 'Torino', 'Firenca', 'Bolonja'],
    'Francuska': ['Pariz', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Strasbourg'],
    'Španjolska': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 'Malaga'],
    'Poljska': ['Varšava', 'Krakov', 'Lodz', 'Wroclaw', 'Poznan', 'Gdanjsk'],
    'Češka': ['Prag', 'Brno', 'Ostrava', 'Plzen', 'Olomouc'],
    'Slovačka': ['Bratislava', 'Košice', 'Prešov', 'Nitra'],
    'Rumunjska': ['Bukurešt', 'Cluj-Napoca', 'Timișoara', 'Iași', 'Constanța'],
    'Grčka': ['Atena', 'Solun', 'Patras', 'Heraklion'],
    'Turska': ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya'],
    'Velika Britanija': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow'],
    'Nizozemska': ['Amsterdam', 'Rotterdam', 'Haag', 'Utrecht', 'Eindhoven'],
    'Belgija': ['Bruxelles', 'Antwerpen', 'Gent', 'Liege', 'Bruges'],
    'Švicarska': ['Zürich', 'Ženeva', 'Bern', 'Lausanne'],
    'Švedska': ['Stockholm', 'Göteborg', 'Malmö', 'Uppsala'],
    'Norveška': ['Oslo', 'Bergen', 'Trondheim', 'Stavanger'],
    'Finska': ['Helsinki', 'Espoo', 'Tampere', 'Turku'],
}

# Kategorije i opisi vremena
vremenske_kategorije = [
    ("sunčano", "Vedro i sunčano bez oblaka."),
    ("djelomično oblačno", "Sunčano uz umjerenu naoblaku."),
    ("oblačno", "Pretežno oblačno, bez padalina."),
    ("kiša", "Umjerena do jaka kiša."),
    ("pljusak", "Kratkotrajni intenzivni pljusak."),
    ("snijeg", "Lagana do umjerena snježna oborina."),
    ("magla", "Smanjena vidljivost zbog magle."),
    ("oluja", "Jaka oluja s vjetrom i mogućim grmljavinama."),
]

# Ime izlazne datoteke
naziv_datoteke = "weather_data.csv"

with open(naziv_datoteke, mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "datum", "država", "grad", "temperatura", "vjetar", "tlak",
        "vlaga", "UV_index", "oborine", "vidljivost", "oblacnost",
        "smjer_vjetra", "kategorija", "opis"
    ])

    for _ in range(broj_redaka):
        drzava = random.choice(list(drzave_gradovi.keys()))
        grad = random.choice(drzave_gradovi[drzava])
        datum = datum_pocetni + timedelta(days=random.randint(0, (datum_zavrsni - datum_pocetni).days))

        temperatura = round(random.uniform(-25, 65 if random.random() < 0.01 else 45), 1)
        vjetar = round(random.uniform(0, 35), 1)
        tlak = random.randint(930, 1060)
        vlaga = random.randint(20, 100)
        uv_index = round(random.uniform(0, 11), 1)
        oborine = round(random.uniform(0, 100), 1)  # mm
        vidljivost = round(random.uniform(0.1, 20), 1)  # km
        oblacnost = random.randint(0, 100)
        smjer_vjetra = random.randint(0, 360)

        kategorija, opis = random.choice(vremenske_kategorije)

        writer.writerow([
            datum.strftime("%Y-%m-%d"),
            drzava,
            grad,
            temperatura,
            vjetar,
            tlak,
            vlaga,
            uv_index,
            oborine,
            vidljivost,
            oblacnost,
            smjer_vjetra,
            kategorija,
            opis
        ])

print(f"Datoteka '{naziv_datoteke}' generirana sa {broj_redaka:,} redaka.")
