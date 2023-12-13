
# Kirjalistasovellus

MyBooks on sovellus, johon käyttäjä voi lisätä ja arvostella lukemiaan kirjoja. Sovellus on alustavasti omaan käyttöön ja toimii ns digitaalisena "kirjapäiväkirjana". Tulevaisuudessa sovellusta voisi laajentaa niin että profiili voisi olla julkinen ja käyttäjät voisivat nähdä toistensa arvosteluja. Tällä hetkellä kaverukset voivat nähdä toistensa arvostelut.

# Toiminnallisuusideoita

- Tulevaisuudessa sovellusta voisi laajentaa niin että profiili voisi olla julkinen ja käyttäjät voisivat nähdä toistensa julkisia arvosteluja. 
- Kirjalla olisi oma sivusto, jossa näkyy kaikki siitä kirjoitetut arvostelut.
- Voisi myös kirjata ylös kirjan genren tai muita tietoja.
- Näistä tiedoista voisi tehdä kiinnostavia tilastoja esim. lukijan keskiarvo-arvosana fantasiakirjoille tai montako prosenttia lukijan lukemista kirjoist ovat olleet trillereitä

- Kuva
- Käyttäjä voi poistaa oman arvostelunsa.
- käyttäjä voi nähdä montako arvostelua on

# Nykyinen toiminnallisuus

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä voi antaa kirjalle arvion 1-10 asteelta, valita statuksen ja kirjoittaa arvioinnin kirjasta.
- Käyttäjän "omat arvostelut" -sivulta löytyvat hänen arvostelunsa.
- Käyttäjä voi etsiä kirjaa tietokannasta,
- Käyttäjä voi itse lisätä lukemiaan kirjoja tietokantaan.
- Käyttäjät voivat hakea ja lisätä kavereita
- Käyttäjistä tulee kaveruksia kun molemmat ovat 'connectanneet'.
- Kaverukset voivat nähdä toistensa arvostelut. 
- Käyttäjä voi valita lempikirjoja ja nähdä ne etusivullaan.
- Saman kirjan voi arvostella uudestaan (tai esim. muuttaa statusta) ja uusi arvostelu päivittyy vanhentuneen tilalle.
- Käyttäjä voi nähdä arvostelunsa julkaisupäivän. 
- Käyttäjä voi poistaa kirjan lempikirjoistaan.
- Etusivulla on kuva.
- Käyttäjä voi nähdä arvosteluidensa keskiarvo-arvosanan.

# Käynnistysohjeet

HUOM Ohjeet kurssin materiaaleista

1. Kloonaa repositorio koneellesi
2. Siirry juurikansioon
3. Luo tiedosto: 
```
.env
```
4. Lisää tiedostoon:
```
DATABASE_URL = < tietokannan-paikallinen-osoite >
SECRET_KEY = < salainen-avain >
```
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