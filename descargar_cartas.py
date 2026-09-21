import requests
import os

CARPETA = "assets/cartas"

os.makedirs(CARPETA, exist_ok=True)

for numero in range(1, 11):
    codigo = f"ST01-{numero:03d}"

    url = (
        "https://gdt.jediblockz.org/images/"
        "ArsenalBase/Starter%20Deck%20(Season%2001)/"
        f"{codigo}_p1_back.jpg"
    )

    archivo = f"{CARPETA}/{codigo}_back.jpg"

    if os.path.exists(archivo):
        print(f"{codigo}: ya existe, saltando.")
        continue

    respuesta = requests.get(url)

    print(f"{codigo}: código {respuesta.status_code}")

    if respuesta.status_code == 200:
        with open(archivo, "wb") as f:
            f.write(respuesta.content)

        print(f"{codigo}: descargada.")
    else:
        print(f"{codigo}: no encontrada.")