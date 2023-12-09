

HUOM tällä hetkellä käyttäjistä tulee kaveruksia jo kun vain toinen on "connectannut" toisen kanssa. Eli ongelmasta ollaan tietoisia ja työn alla on jo sellainen toiminnallisuus, että he olisivat kaveruksia vain jos Molemmat ovat niin päättäneet.

# Kirjalistasovellus

MyBooks on sovellus, johon käyttäjä voi lisätä ja arvostella lukemiaan kirjoja. Sovellus on alustavasti omaan käyttöön ja toimii ns digitaalisena "kirjapäiväkirjana". Tulevaisuudessa sovellusta voisi laajentaa niin että profiili voisi olla julkinen ja käyttäjät voisivat nähdä toistensa arvosteluja. Tällä hetkellä myös kaverukset voivat lisätä toisensa ja näin nähdä toistensa arvostelut.

# Toiminnallisuusideoita

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä voi antaa kirjalle arvion 1-10 asteelta, valita statuksen ja kirjoittaa arvioinnin kirjasta.
- Käyttäjä voi poistaa oman arvostelunsa.
- Käyttäjän "omat arvostelut" -sivulta löytyvat hänen arvostelunsa.
- Käyttäjät voivat hakea ja lisätä kavereita ja kaverukset voivat nähdä toistensa arvostelut.
- Käyttäjä voi etsiä kirjaa tietokannasta, jos hän ei löydä sitä kirjaa, hän voi itse lisätä sen tietokantaan.
- Käyttäjä voi valita lempikirjansa ja tarkastella lempikirjojaan sekä poistaa kirjan lempikirjoistaan.
- Käyttäjä voi nähdä arvostelunsa julkaisupäivän. 
- Kirjalla olisi oma sivusto, jossa näkyy kaikki siitä kirjoitetut arvostelut.
- Kaverit näkisivät feedillä toistensa uusimmat arvostelut.
- Käyttäjä voisi nähdä mielekkäitä tilastoja lukemistaan kirjoista esim keskiarvo-arvosana hänen lukemilleen kirjoille.
- Saman kirjan voi arvostella uudestaan (tai esim. muuttaa statusta) ja uusi arvostelu päivittyy vanhentuneen tilalle. (ei duplikaatteja)
- Käyttäjälle näkyy päivä jolloin hän on arvostellut minkäkin kirjan.


# Nykyinen toiminnallisuus
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä voi antaa kirjalle arvion 1-10 asteelta, valita statuksen ja kirjoittaa arvioinnin kirjasta.
- Käyttäjän "omat arvostelut" -sivulta löytyvat hänen arvostelunsa.
- Käyttäjä voi etsiä kirjaa tietokannasta, jos hän ei löydä sitä kirjaa, hän voi itse lisätä sen tietokantaan.
- Käyttäjät voivat hakea ja lisätä kavereita ja kaverukset voivat nähdä toistensa arvostelut.
- Käyttäjä voi valita lempikirjansa ja tarkastella lempikirjojaan.
- Saman kirjan voi arvostella uudestaan (tai esim. muuttaa statusta) ja uusi arvostelu päivittyy vanhentuneen tilalle. (ei duplikaatteja)
- Käyttäjälle näkyy päivä jolloin hän on arvostellut minkäkin kirjan.

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