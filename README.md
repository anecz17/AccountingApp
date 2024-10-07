# Könyvelői Segédprogram Gyűjtemény

## Tartalomjegyzék
- [Áttekintés](#áttekintés)
- [Telepítés](#telepítés)
- [Használat](#használat)
- [Funkciók](#funkciók)
- [Hozzájárulás](#hozzájárulás)
- [Licenc](#licenc)
- [Kapcsolat](#kapcsolat)


## Áttekintés
A projektnek jelenlég két része van:
**App**: ebben a mappában található az alkalmazás, aminek két része van. 
1. Letölti az ügyfelek adószámláit az adóhivatal adatbázisából
2. Számlázó program exportját főkönyvi adatokkal feltölti. Kontírozza és a költséghely besorolást részlegesen elvégzi.

**Script**:
Egy rossz formátumban lévő excel fájlt rendez. 

### Adószámla lekérdezés:
Az alkalmazás a felhasználónév és jelsző megadása után Mozilla Firefoxot használva megnyitja a https://ebev.nav.gov.hu/ honlapot. Bejelentkezik. Majd letölti az összes adószámlát a jelenlegi időszaknak megfelelően. Az ügyfelek neve és felhasználóneve a data.json fájlban vannak tárolva. Az alkalmazás jelszavakat nem tárol, azokat minden egyes alkalommal meg kell adni.

### Excel Makró
Választhatóan feltölti a Liget Hotel és a Liget Cafe számlázó program exportját főkönyvi adatokkal. Törli a csv-t és megnyitja a szerkesztett dokumentumot az alapértelmezett csv megnyitó programban. A kész fájlok a *Liget Hotel*/*Liget Cafe* mappákba kerülnek.


## Telepítés
### App
Az appot a zip fájlban érdemes letölteni. A működéshez szükséges, hogy a *data.json* és a *path.json* is az exe mappájában legyen.

### Fejlesztés
*Klónozd a repository-t*
```git clone https://github.com/anecz17/AccountingApp.git```

*Lépj be a projekt könyvtárába*
```cd projekt-név```

*Hozz létre virtuális környezetet (opcionális, de ajánlott)*
```python -m venv venv```
```Windows-on: venv\Scripts\activate``` //MAC ```source venv/bin/activate```

*Függőségek telepítése*
```pip install -r requirements.txt```
*A requirements.txt tartalmazza a minimális követelményeket.*

## Használat
*A script futtatása* ```python könyvelői_Kisprogram1.5.py```

## Funkciók
**v1.5**
- A jelszó már csillagozva van gépelés közben.
- Túllép a ebev honlapon figyelmeztetésen
- A program nem omlik össze, ha nem tudja törölni az eredeti csv fájlt

**v2.0**
- Az adószámla lekérdezés megszűnik az eddigi weboldalon így a 2.0-ás verzió már az új weboldalról fogja lekérni az adatokat.


## Hozzájárulás
1. Forkold a repository-t GitHub-on a **Fork** gombra kattintva.
2. Hozz létre egy új branch-et (```git checkout -b új-funkció-branch```)
3. Végezd el a változtatásokat és commitolj (```git commit -m 'Hozzáadott funkció'```)
4. Pushold a branch-et (```git push origin új-funkció-branch```)
5. Nyiss egy Pull Request-et a változtatásaid beolvasztásához.


## Licenc
Lásd [MIT License](./LICENSE).

## Kapcsolat
Necz András
[LinkedIn](https://www.linkedin.com/in/andras-necz/)
[Github](https://www.github.com/anecz17)