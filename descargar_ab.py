import requests
import os

TEMPORADA = "FORSQUAD Booster B Series 05"
PREFIJO = "FQB05"

INICIO = 0
MAX_CARTAS = 80

CARPETA = "assets/cartas"

os.makedirs(CARPETA, exist_ok=True)

descargadas = 0
encontradas = 0

for numero in range(INICIO, MAX_CARTAS + 1):

    codigo = f"{PREFIJO}-{numero:03d}"

    carta_encontrada = False

    for lado in ["front", "back"]:

        nombre_archivo = f"{codigo}_{lado}.jpg"

        url = (
            "https://gdt.jediblockz.org/images/"
            "ArsenalBase/"
            f"{TEMPORADA.replace(' ', '%20')}/"
            f"{nombre_archivo}"
        )

        archivo = os.path.join(CARPETA, nombre_archivo)

        if os.path.exists(archivo):
            print(f"{nombre_archivo}: ya existe.")
            carta_encontrada = True
            continue

        try:
            respuesta = requests.get(url, timeout=5)

            if respuesta.status_code == 200:

                with open(archivo, "wb") as f:
                    f.write(respuesta.content)

                print(f"{nombre_archivo}: ¡ENCONTRADA!")
                descargadas += 1
                carta_encontrada = True

            else:
                print(f"{nombre_archivo}: no existe.")

        except requests.RequestException:
            print(f"{nombre_archivo}: error de conexión")

    if carta_encontrada:
        encontradas += 1

print()
print("==============================")
print("RECONOCIMIENTO TERMINADO")
print("==============================")
print(f"Cartas encontradas: {encontradas}")
print(f"Imágenes nuevas:    {descargadas}")
print("==============================")