import json
import os
from datetime import datetime
json_saldo = "modules/wydatki/saldo.json"

# Funkcja do wczytywania użytkowników z pliku
def wczytaj_baze(plik):
    if not os.path.exists(plik):
        with open(plik, "w") as f:
            json.dump({}, f)  # tworzy pusty plik JSON
    with open(plik, "r") as f:
        return json.load(f)

# Funkcja do zapisywania użytkowników do pliku
def zapisz_baze(plik, item):
    with open(plik, "w") as f:
        json.dump(item, f, indent=4)

# Funkcja podająca aktualną datę
def podaj_date():
    teraz = datetime.now()
    return teraz.strftime("%d-%m-%Y %H:%M")

# Funkcja słuząca do wypisywania elementów z listy razem z indexem
def iteracja_z_indexem(lista):
    i = 1
    wynik = ""
    for item in lista:
        wynik += str(i) + " - " + item + "\n"
        i += 1
    return wynik

def podaj_wszystkie_id(baza):
    baza_id = []
    if not baza:
        return 0
    else:
        for item in baza:
            baza_id.append(item["ID"])
        return baza_id

# Funkcja generująca ID w bazie
def podaj_ostatnie_id(baza):
    return max(podaj_wszystkie_id(baza))
    
def podaj_pierwsze_id(baza):
    return min(podaj_wszystkie_id(baza))
    
def oblicz_stan_konta():
    wynik = 0
    for item in saldo["historia_transakcji"]:
        wynik += int(item["KWOTA"])
    return wynik

saldo = wczytaj_baze(json_saldo)

# Funkcja dodająca pieniądze do konta
def dodaj_pieniadze():
    ile = input("\nPodaj kwotę wpłaty pieniędzy: ")
    wybierz_kategoria = input("\n" + iteracja_z_indexem(saldo["kategoria_wplat"]) + "Wybierz kategorię (1-" + str(len(saldo["kategoria_wplat"])) + "): ")
    opis = input("Podaj opis: ")
    saldo["historia_transakcji"].append({"ID":podaj_ostatnie_id(saldo["historia_transakcji"])+1, "TYP": "Dodaj", "KWOTA": ile, "KATEGORIA": saldo["kategoria_wplat"][int(wybierz_kategoria)-1], "OPIS": opis, "DATA": podaj_date()})
    zapisz_baze(json_saldo, saldo)
    return("Wpłacono " + ile + " zł.\n")

# Funkcja odejmująca pieniądze z konta
def odejmij_pieniadze():
    ile = input("\nPodaj kwotę wypłaty pieniędzy: ")
    if int(ile) > oblicz_stan_konta():
        print("\nNie mozesz wypłacić tyle pieniędzy :(")
        print("Spróbuj mniejszą kwotę :)")
        odejmij_pieniadze()
    else:
        wybierz_kategoria = input("\n" + iteracja_z_indexem(saldo["kategoria_wydatkow"]) + "Wybierz kategorię (1-" + str(len(saldo["kategoria_wydatkow"])) + "): ")
        opis = input("Podaj opis: ")
        saldo["historia_transakcji"].append({"ID":podaj_ostatnie_id(saldo["historia_transakcji"])+1, "TYP": "Odejmij", "KWOTA": ile, "KATEGORIA": saldo["kategoria_wydatkow"][int(wybierz_kategoria)-1], "OPIS": opis, "DATA": podaj_date()})
        zapisz_baze(json_saldo, saldo)
        return("Wypłacono " + ile + " zł.\n")

# Funkcja pokazująca stan konta
def stan_konta():
    return("\nObecny stan konta: " + str(oblicz_stan_konta()) + " zł.\n")

# Funkcja pokazująca historię transakcji
def historia_transakcji():
    wplywy = 0
    wydatki = 0
    for item in saldo["historia_transakcji"]:
        if item["TYP"] == "Dodaj":
            wplywy += int(item["KWOTA"])
        if item["TYP"] == "Odejmij":
            wydatki += int(item["KWOTA"])
        print("ID: "+ str(item["ID"]) + " | TYP: "+ item["TYP"] + " | KWOTA: "+ item["KWOTA"] + " | DATA: "+ item["DATA"])
    print("Suma wpływów: " + str(wplywy) + "\nSuma wydatków: " + str(wydatki))
    wybierz_transakcje = input("\nWybierz transakcję (" + str(podaj_pierwsze_id(saldo["historia_transakcji"])) + "-" + str(podaj_ostatnie_id(saldo["historia_transakcji"])) + ")\nlub wyjdź (0): ")
    wybierz_transakcje = int(wybierz_transakcje)
    if wybierz_transakcje == 0:
        return "Wyjście\n"
    elif wybierz_transakcje not in podaj_wszystkie_id(saldo["historia_transakcji"]):
        print("\nWybrano niepoprawne ID!")
        print(historia_transakcji())
    else:
        wyswietl_transakcje(wybierz_transakcje)

def wyswietl_transakcje(id):
    for item in saldo["historia_transakcji"]:
        if item["ID"] == id:
            print("\nID: "+ str(item["ID"]) + "\nTYP: "+ item["TYP"] + "\nKWOTA: "+ item["KWOTA"] + "\nKATEGORIA: "+ item["KATEGORIA"] + "\nOPIS: "+ item["OPIS"] + "\nDATA: "+ item["DATA"])
    wybierz_akcje = input("1. Edytuj transakcję\n2. Usuń transakcję\n0. Wyjdź\nWybierz akcję: ")
    if (wybierz_akcje == "1"):
        edytuj_transakcje(id)
    elif (wybierz_akcje == "2"):
        usun_transakcje(id)
    elif (wybierz_akcje == "0"):
        print(historia_transakcji())

def edytuj_transakcje(id):
    wybierz_pole = input("Które pole chcesz zedytować? (KWOTA, KATEGORIA, OPIS): ")
    wybierz_pole = wybierz_pole.upper()
    if wybierz_pole == "KWOTA" or wybierz_pole == "KATEGORIA" or wybierz_pole == "OPIS":
        zmiana = input("Wprowadź zmianę: ") # Problem do naprawienia w przyszłości: pola można zamienić na każdą wartość
        for item in saldo["historia_transakcji"]:
            if item["ID"] == id:
                item[wybierz_pole] = zmiana
                zapisz_baze(json_saldo, saldo)
    else:
        print("Niepoprawny wybór")
        edytuj_transakcje()

def usun_transakcje(id):
    for item in saldo["historia_transakcji"]:
        if item["ID"] == id:
            saldo["historia_transakcji"].remove(item)
    zapisz_baze(json_saldo, saldo)

def wyswietl_kategorie():
    print("\n1. Kategorie wpłat:\n" + iteracja_z_indexem(saldo["kategoria_wplat"]) +
          "\n2. Kategorie wypłat:\n" + iteracja_z_indexem(saldo["kategoria_wydatkow"]))
    input()

while True:

    print("=================")
    print("1. Dodaj pieniądze")
    print("2. Odejmij pieniądze")
    print("3. Stan konta")
    print("4. Historia transakcji")
    print("5. Wyświetl kategorie")
    print("=================")

    wybierz = input("Wybierz (1-5): ")
    if wybierz == "1":
        print(dodaj_pieniadze())
    elif wybierz == "2":
        print(odejmij_pieniadze())
    elif wybierz == "3":
        print(stan_konta())
    elif wybierz == "4":
        print(historia_transakcji())
    elif wybierz == "5":
        wyswietl_kategorie()
    else:
        print("Niepoprawna wartość")
        
