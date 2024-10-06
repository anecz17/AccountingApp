# Könyvelői Segédprogram Gyűjtemény

## Áttekintés
A projektnek jelenlég két része van:
- App: ebben a mappában található az alkalmazás, aminek két fő része van. 
1. Letölti az ügyfelek adószámláit az adóhivatal adatbázisából
2. Számlázó program exportját főkönyvi adatokkal feltölti. Kontírozza és a költséghely besorolást részlegesen elvégzi.


### Adószámla lekérdezés:
Az alkalmazás a felhasználónév és jelsző megadása után Mozilla Firefoxot használva megnyitja a https://ebev.nav.gov.hu/ honlapot. Bejelentkezik. Majd letölti az összes adószámlát a jelenlegi időszaknak megfelelően. Az ügyfelek neve és felhasználóneve a data.json fájlban vannak tárolva. Az alkalmazás jelszavakat nem tárol, azokat minden egyes alkalommal meg kell adni.

### Excel Makró
Választhatóan feltölti a Liget Hotel és a Liget Cafe számlázó program exportját főkönyvi adatokkal. Törli a csv-t és megnyitja a szerkesztett dokumentumot az alapértelmezett csv megnyitó programban. A kész fájlok a Liget Hotel/Liget Cafe mappákba kerülnek.

## Tartalomjegyzék
- [Áttekintés](#áttekintés)
- [Telepítés](#telepítés)
- [Használat](#használat)
- [Funkciók](#funkciók)
- [Hozzájárulás](#hozzájárulás)
- [Licenc](#licenc)
- [Kapcsolat](#kapcsolat)

## Telepítés
### App
Az appot a zip fájlban érdemes letölteni. A működéshez szükséges, hogy a data.json és a path.json is az exe mappájában legyen.

### Fejlesztés
A requirements.txt tartalmazza a minimális követelményeket.

## Használat
Open Source, ingyenesen használható a licencnek megfelelően.

## Kapcsolat
Necz András
[text](https://www.linkedin.com/in/andras-necz/)







