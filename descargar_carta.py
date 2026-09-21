import requests

url = (
    "https://gdt.jediblockz.org/images/"
    "ArsenalBase/Starter%20Deck%20(Season%2001)/"
    "ST01-001_p1_back.jpg"
)

respuesta = requests.get(url)

print("Código:", respuesta.status_code)

if respuesta.status_code == 200:
    with open("assets/cartas/ST01-001_back.jpg", "wb") as archivo:
        archivo.write(respuesta.content)

    print("Carta descargada.")
else:
    print("No se pudo descargar la carta.")