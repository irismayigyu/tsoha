

HUOM tällä hetkellä käyttäjistä tulee kaveruksia jo kun vain toinen on "connectannut" toisen kanssa. Eli ongelmasta ollaan tietoisia ja työn alla on jo sellainen toiminnallisuus, että he olisivat kaveruksia vain jos Molemmat ovat niin päättäneet.

# Kirjalistasovellus

MyBooks on sovellus, jossa arvostellaan kirjoja. 

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä voi antaa kirjalle arvion 1-10 asteelta, valita statuksen ja kirjoittaa arvioinnin kirjasta.
- Käyttäjä voi poistaa oman arvostelunsa.
- Käyttäjän "omat arvostelut" -sivulta löytyvat hänen arvostelunsa.
- Käyttäjät voivat hakea ja lisätä kavereita ja kaverukset voivat nähdä toistensa arvostelut.
- Käyttäjä voi etsiä kirjaa tietokannasta, jos hän ei löydä sitä kirjaa, hän voi itse lisätä sen tietokantaan.
- Käyttäjä voi valita lempikirjansa ja tarkastella lempikirjojaan sekä poistaa kirjan lempikirjoistaan.


# Nykyinen toiminnallisuus
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä voi antaa kirjalle arvion 1-10 asteelta, valita statuksen ja kirjoittaa arvioinnin kirjasta.
- Käyttäjän "omat arvostelut" -sivulta löytyvat hänen arvostelunsa.
- Käyttäjä voi etsiä kirjaa tietokannasta, jos hän ei löydä sitä kirjaa, hän voi itse lisätä sen tietokantaan.
- Käyttäjät voivat hakea ja lisätä kavereita ja kaverukset voivat nähdä toistensa arvostelut.

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


HUOM Sovelluksessa on käytetty chatgpteetä. 