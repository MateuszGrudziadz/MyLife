import json
import os
from datetime import datetime

json_saldo = "modules/wydatki/saldo.json"

# Funkcja do wczytywania użytkowników z pliku
def wczytajBaze(plik):
    if not os.path.exists(plik):
        with open(plik, "w") as f:
            json.dump({}, f)  # tworzy pusty plik JSON
    with open(plik, "r") as f:
        return json.load(f)

# Funkcja do zapisywania użytkowników do pliku
def zapiszBaze(plik, item):
    with open(plik, "w") as f:
        json.dump(item, f, indent=4)

def podajDate():
    teraz = datetime.now()
    return teraz.strftime("%d-%m-%Y %H:%M")

saldo = wczytajBaze(json_saldo)
# Funckja dodająca pieniądze do konta
def dodajPieniadze():
    ile = input("\nPodaj kwotę wpłaty pieniędzy: ")
    saldo["stan_konta"] += int(ile)
    saldo["historia_transakcji"].append({"TYP": "Dodaj", "KWOTA": ile, "DATA": podajDate()})
    zapiszBaze(json_saldo, saldo)
    return("Wpłacono " + ile + " zł.\n")

# Funckja odejmująca pieniądze z konta
def odejmijPieniadze():
    ile = input("\nPodaj kwotę wypłaty pieniędzy: ")
    if int(ile) > saldo["stan_konta"]:
        print("\nNie mozesz wypłacić tyle pieniędzy :(")
        print("Spróbuj mniejszą kwotę :)")
        odejmijPieniadze()
    else:
        saldo["stan_konta"] -= int(ile)
        saldo["historia_transakcji"].append({"TYP": "Odejmij", "KWOTA": ile, "DATA": podajDate()})
        zapiszBaze(json_saldo, saldo)
        return("Wypłacono " + ile + " zł.\n")

# Funkcja pokazująca stan konta
def stanKonta():
    return("\nObecny stan konta: " + str(saldo["stan_konta"]) + " zł.\n")

def historiaTransakcji():
    wplywy = 0
    wydatki = 0
    for item in saldo["historia_transakcji"]:
        if item["TYP"] == "Dodaj":
            wplywy += int(item["KWOTA"])
        if item["TYP"] == "Odejmij":
            wydatki += int(item["KWOTA"])
        print("TYP: "+ item["TYP"] + " | KWOTA: "+ item["KWOTA"] + " | DATA: "+ item["DATA"])
    return "Suma wpływów: " + str(wplywy) + "\nSuma wydatków: " + str(wydatki)

while True:

    print("=============")
    print("1. Dodaj pieniądze")
    print("2. Odejmij pieniądze")
    print("3. Stan konta")
    print("4. Historia transakcji")
    print("=============")

    wybierz = input("Wybierz (1-3): ")
    if wybierz == "1":
        print(dodajPieniadze())
    elif wybierz == "2":
        print(odejmijPieniadze())
    elif wybierz == "3":
        print(stanKonta())
    elif wybierz == "4":
        print(historiaTransakcji())
        
