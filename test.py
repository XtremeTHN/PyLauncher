from minecraft_launcher_lib.utils import get_available_versions
import json
def main():
    lista_diccionarios = get_available_versions("/home/axel/.minecraft")

    fechas = [diccionario["releaseTime"] for diccionario in lista_diccionarios]
    sorted_dates = sorted(fechas, reverse=True)
    lista_ordenada = list(zip(sorted_dates, lista_diccionarios))
    return lista_ordenada

# list(map(lambda x: print(x["id"], x["type"]), get_available_versions("/home/axel/.minecraft")))
