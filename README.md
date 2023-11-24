20.11. muokattu niin että sovelluksen testaamisen pitäisi nyt onnistua.
HUOM käytetty chatgpteetä. 

# Kirjalistasovellus

Sovellukseen lisätään itse lukemia kirjoja ja arvioidaan ne. Jokainen käyttäjä on ylläpitäjä tai peruskäyttäjä.

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä voi antaa arvion 1-10 asteelta, valita statuksen ja kirjoittaa arvioinnin kirjasta.
- Käyttäjän "omista arvioinneista" löytyy hänen tallentamansa kirjat.
- Käyttäjät voivat lisätä kavereita ja kaverukset voivat nähdä toistensa arvioimat kirjat.
- Käyttäjä voi etsiä kirjaa tietokannasta, jos ei löydä sitä kirjaa, hän voi itse lisätä sen tietokantaan. 


# Nykyinen toiminnallisuus
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä voi antaa arvion 1-10 asteelta, valita statuksen ja kirjoittaa arvioinnin kirjasta. 
- Käyttäjän "omista kirjoista" löytyy hänen tallentamansa kirjat.

# Käynnistysohjeet

HUOM Ohjeet kurssin materiaaleista

1. Kloonaa repositorio koneellesi
2. Siirry juurikansioon
3. Luo .env -tiedosto
4. Lisää tiedostoon:
DATABASE_URL = < tietokannan-paikallinen-osoite >
SECRET_KEY = < salainen-avain >

Luodaan Pythonin virtuaaliympäristö komennolla:
```
python3 -m venv venv

```

Siirry virtuaaliympäristöön komennolla:
```
source venv/bin/activate

```

Lataa riippuvuudet:
```
pip install -r requirements.txt
```
Luo sovelluksen tietokannat komennolla:
```
psql < schema.sql
```
Käynnistä sovellus:
```
flask run
```

