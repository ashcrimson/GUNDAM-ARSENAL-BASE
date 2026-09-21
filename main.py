import os
import pygame

pygame.init()
pygame.mixer.init()

ANCHO = 1600
ALTO = 900

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Gundam Arsenal Base")

CARPETA_CARTAS = "assets/cartas"
SONIDO_GIRO = pygame.mixer.Sound("assets/sound/flip.mp3")
FUENTE = "C:/Windows/Fonts/arial.ttf"


# --------------------------------------------------
# Buscar cartas
# --------------------------------------------------

def buscar_cartas():

    archivos = os.listdir(CARPETA_CARTAS)
    archivos.sort()

    cartas = []

    for archivo in archivos:

        if not archivo.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp")):
            continue

        nombre, extension = os.path.splitext(archivo)

        if nombre.endswith("_b"):
            continue

        if nombre.endswith("_back"):
            continue

        cartas.append(archivo)

    return cartas


def filtrar_cartas_temporada(temporada):

    resultado = []

    for carta in cartas:

        if carta.startswith(temporada + "-"):
            resultado.append(carta)

    return resultado


cartas = buscar_cartas()

print("Cartas encontradas:", len(cartas))

temporada_seleccionada = "AB01"

cartas_mostradas = filtrar_cartas_temporada(
    temporada_seleccionada
)

print("Cartas de la temporada:", len(cartas_mostradas))


temporadas = [
    ("AB01", "SEASON 01"),
    ("AB02", "SEASON 02"),
    ("AB03", "SEASON 03"),
    ("AB04", "SEASON 04"),

    ("AR01", "ARSENAL RARE 1st SERIES"),
    ("AR02", "ARSENAL RARE 2nd SERIES"),
    ("AR03", "ARSENAL RARE 3rd SERIES"),
    ("AR04", "ARSENAL RARE 4th SERIES"),

    ("BP01", "BOOSTER PACK SEED SERIES"),
    ("BP02", "BOOSTER PACK GQUUUUUUX"),
    ("BP03", "BOOSTER PACK SEED SERIES VOL.2"),
    ("BP04", "3.5th ANNIVERSARY MEMORIAL BOOSTER PACK"),
    ("BP05", "BOOSTER PACK IBO"),
    ("BP06", "BOOSTER PACK DCD 20th"),
    ("BP07", "BOOSTER PACK SEED SERIES VOL.3"),
    ("BP08", "BOOSTER PACK GUNDAM TRY AGE VOL.2"),
    ("BP09", "BOOSTER PACK 4.5th ANNIVERSARY NEXT SELECTION"),

    ("FQ01", "FORSQUAD SEASON 01")
]


# --------------------------------------------------
# Buscar reverso
# --------------------------------------------------

def buscar_reverso(nombre):

    base, extension = os.path.splitext(nombre)

    if base.endswith("_front"):

        reverso = (
            base[:-6]
            + "_back"
            + extension
        )

    else:

        reverso = (
            base
            + "_b"
            + extension
        )

    ruta = os.path.join(
        CARPETA_CARTAS,
        reverso
    )

    if os.path.exists(ruta):
        return reverso

    return None


# --------------------------------------------------
# Cargar carta
# --------------------------------------------------

def cargar_carta(nombre, tamaño):

    ruta = os.path.join(
        CARPETA_CARTAS,
        nombre
    )

    imagen = pygame.image.load(ruta).convert()

    return pygame.transform.smoothscale(
        imagen,
        tamaño
    )


# --------------------------------------------------
# Variables del álbum
# --------------------------------------------------

CARTAS_POR_PAGINA = 10
COLUMNAS = 5

pagina = 0

# Carta que está abierta en el modal
carta_seleccionada = 0

# Estado del modal
modal_abierto = False
mostrando_reverso = False

# Estado de la animación de giro
animando_flip = False
progreso_flip = 0

# Estado de la entrada del modal
animando_entrada = False
progreso_entrada = 0

# Menús
menu_seasons = False
menu_rare = False
menu_booster = False
menu_forsquad = False


# --------------------------------------------------
# Bucle principal
# --------------------------------------------------

reloj = pygame.time.Clock()

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            ejecutando = False


        # ==================================================
        # CLICK
        # ==================================================

        if evento.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()


            # ==================================================
            # MENÚ
            # ==================================================

            if not modal_abierto:

                y_menu = 100


                # ------------------------------------------
                # SEASONS
                # ------------------------------------------

                rect_seasons = pygame.Rect(
                    20,
                    y_menu,
                    240,
                    40
                )

                if rect_seasons.collidepoint(
                        mouse_x,
                        mouse_y):

                    menu_seasons = not menu_seasons

                y_menu += 45

                if menu_seasons:

                    for codigo, nombre in temporadas:

                        if not codigo.startswith("AB"):
                            continue

                        rect_temporada = pygame.Rect(
                            30,
                            y_menu,
                            450,
                            35
                        )

                        if rect_temporada.collidepoint(
                                mouse_x,
                                mouse_y):

                            temporada_seleccionada = codigo

                            cartas_mostradas = (
                                filtrar_cartas_temporada(
                                    temporada_seleccionada
                                )
                            )

                            pagina = 0



                        y_menu += 38


                # ------------------------------------------
                # ARSENAL RARE
                # ------------------------------------------

                rect_rare = pygame.Rect(
                    20,
                    y_menu,
                    240,
                    40
                )

                if rect_rare.collidepoint(
                        mouse_x,
                        mouse_y):

                    menu_rare = not menu_rare

                y_menu += 45

                if menu_rare:

                    for codigo, nombre in temporadas:

                        if not codigo.startswith("AR"):
                            continue

                        rect_temporada = pygame.Rect(
                            30,
                            y_menu,
                            230,
                            35
                        )

                        if rect_temporada.collidepoint(
                                mouse_x,
                                mouse_y):

                            temporada_seleccionada = codigo

                            cartas_mostradas = (
                                filtrar_cartas_temporada(
                                    temporada_seleccionada
                                )
                            )

                            pagina = 0



                        y_menu += 38


                # ------------------------------------------
                # BOOSTER PACK
                # ------------------------------------------

                rect_booster = pygame.Rect(
                    20,
                    y_menu,
                    460,
                    40
                )

                if rect_booster.collidepoint(
                        mouse_x,
                        mouse_y):

                    menu_booster = not menu_booster

                y_menu += 45

                if menu_booster:

                    for codigo, nombre in temporadas:

                        if not codigo.startswith("BP"):
                            continue

                        if len(nombre) > 25:
                            alto_item = 63
                        else:
                            alto_item = 38

                        rect_temporada = pygame.Rect(
                            30,
                            y_menu,
                            450,
                            alto_item
                        )

                        if rect_temporada.collidepoint(
                                mouse_x,
                                mouse_y):
                            temporada_seleccionada = codigo

                            cartas_mostradas = (
                                filtrar_cartas_temporada(
                                    temporada_seleccionada
                                )
                            )

                            pagina = 0



                        y_menu += alto_item


                # ------------------------------------------
                # FORSQUAD
                # ------------------------------------------

                rect_forsquad = pygame.Rect(
                    20,
                    y_menu,
                    240,
                    40
                )

                if rect_forsquad.collidepoint(
                        mouse_x,
                        mouse_y):

                    menu_forsquad = not menu_forsquad

                y_menu += 45

                if menu_forsquad:

                    for codigo, nombre in temporadas:

                        if not codigo.startswith("FQ"):
                            continue

                        rect_temporada = pygame.Rect(
                            30,
                            y_menu,
                            230,
                            35
                        )

                        if rect_temporada.collidepoint(
                                mouse_x,
                                mouse_y):

                            temporada_seleccionada = codigo

                            cartas_mostradas = (
                                filtrar_cartas_temporada(
                                    temporada_seleccionada
                                )
                            )

                            pagina = 0



                        y_menu += 38


                # ==================================================
                # ÁLBUM
                # ==================================================

                ancho_carta = 180
                alto_carta = 252

                espacio_x = 35
                espacio_y = 35

                inicio_x = 450
                inicio_y = 100

                for i in range(CARTAS_POR_PAGINA):

                    indice = (
                        pagina * CARTAS_POR_PAGINA
                        + i
                    )

                    if indice >= len(cartas_mostradas):
                        break

                    fila = i // COLUMNAS
                    columna = i % COLUMNAS

                    x = (
                        inicio_x
                        + columna * (
                            ancho_carta
                            + espacio_x
                        )
                    )

                    y = (
                        inicio_y
                        + fila * (
                            alto_carta
                            + espacio_y
                        )
                    )

                    rect = pygame.Rect(
                        x,
                        y,
                        ancho_carta,
                        alto_carta
                    )

                    if rect.collidepoint(
                            mouse_x,
                            mouse_y):

                        carta_seleccionada = indice

                        modal_abierto = True

                        mostrando_reverso = False

                        animando_entrada = True
                        progreso_entrada = 0

                       


            # ==================================================
            # MODAL
            # ==================================================

            else:

                ancho_grande = 500
                alto_grande = 700

                x = (
                    ANCHO
                    - ancho_grande
                ) // 2

                y = (
                    ALTO
                    - alto_grande
                ) // 2

                rect_carta = pygame.Rect(
                    x,
                    y,
                    ancho_grande,
                    alto_grande
                )

                if rect_carta.collidepoint(
                        mouse_x,
                        mouse_y):

                    if not animando_flip:

                        animando_flip = True
                        progreso_flip = 0

                        SONIDO_GIRO.play()

                else:

                    modal_abierto = False
                    mostrando_reverso = False


        # ==================================================
        # TECLADO
        # ==================================================

        if evento.type == pygame.KEYDOWN:

            # ESC
            if evento.key == pygame.K_ESCAPE:

                if modal_abierto:

                    modal_abierto = False
                    mostrando_reverso = False

                else:

                    ejecutando = False


            # Página siguiente
            if evento.key == pygame.K_RIGHT:

                if not modal_abierto:

                    ultima_pagina = (
                        len(cartas_mostradas) - 1
                    ) // CARTAS_POR_PAGINA

                    if pagina < ultima_pagina:

                        pagina += 1

                        print(
                            "Página:",
                            pagina + 1,
                            "| Temporada:",
                            temporada_seleccionada,
                            "| Primera carta:",
                            cartas_mostradas[
                                pagina * CARTAS_POR_PAGINA
                            ]
                        )


            # Página anterior
            if evento.key == pygame.K_LEFT:

                if not modal_abierto:

                    if pagina > 0:

                        pagina -= 1

    # ==================================================
    # Animación de entrada del modal
    # ==================================================

    if animando_entrada:

        progreso_entrada += 0.15

        if progreso_entrada >= 1:
            progreso_entrada = 1
            animando_entrada = False
    # ==================================================
    # Animación del flip
    # ==================================================

    if animando_flip:

        progreso_flip += 0.20

        if progreso_flip >= 1:

            progreso_flip = 0
            animando_flip = False

            mostrando_reverso = not mostrando_reverso


    # ==================================================
    # DIBUJAR ÁLBUM
    # ==================================================

    pantalla.fill(
        (235, 235, 235)
    )


    # --------------------------------------------------
    # Panel lateral
    # --------------------------------------------------

    pygame.draw.rect(
        pantalla,
        (245, 245, 245),
        (0, 0, 400, ALTO)
    )


    pygame.draw.line(
        pantalla,
        (30, 30, 30),
        (400, 0),
        (400, ALTO),
        2
    )

    fuente_menu = pygame.font.Font(
        FUENTE,
        24
    )

    titulo_menu = fuente_menu.render(
        "ARSENAL BASE",
        True,
        (30, 30, 30)
    )

    pantalla.blit(
        titulo_menu,
        (30, 30)
    )


    y_menu = 100


    # ------------------------------------------
    # SEASONS
    # ------------------------------------------

    pygame.draw.rect(
        pantalla,
        (30, 30, 30),
        (20, y_menu - 5, 360, 42)
    )

    flecha = "▼" if menu_seasons else "▶"

    texto = fuente_menu.render(
        flecha + " SEASONS",
        True,
        (255, 255, 255)
    )

    pantalla.blit(
        texto,
        (30, y_menu)
    )

    y_menu += 45

    if menu_seasons:

        for codigo, nombre in temporadas:

            if not codigo.startswith("AB"):
                continue

            if len(nombre) > 25:
                alto_item = 63
            else:
                alto_item = 38

            if codigo == temporada_seleccionada:
                pygame.draw.rect(
                    pantalla,
                    (220, 220, 220),
                    (30, y_menu, 450, 35)
                )

                pygame.draw.rect(
                    pantalla,
                    (30, 30, 30),
                    (30, y_menu, 350, 35),
                    1
                )
            texto = fuente_menu.render(
                nombre,
                True,
                (30, 30, 30)
            )

            pantalla.blit(
                texto,
                (45, y_menu)
            )

            y_menu += 38


    # ------------------------------------------
    # ARSENAL RARE
    # ------------------------------------------

    flecha = "▼" if menu_rare else "▶"

    texto = fuente_menu.render(
        flecha + " ARSENAL RARE",
        True,
        (30, 30, 30)
    )

    pantalla.blit(
        texto,
        (30, y_menu)
    )

    y_menu += 45

    if menu_rare:

        for codigo, nombre in temporadas:

            if not codigo.startswith("AR"):
                continue

            if codigo == temporada_seleccionada:
                pygame.draw.rect(
                    pantalla,
                    (220, 220, 220),
                    (30, y_menu, 450, 35)
                )

                pygame.draw.rect(
                    pantalla,
                    (30, 30, 30),
                    (30, y_menu, 450, 35),
                    1
                )

            texto = fuente_menu.render(
                nombre,
                True,
                (30, 30, 30)
            )

            pantalla.blit(
                texto,
                (45, y_menu)
            )

            y_menu += 38


    # ------------------------------------------
    # BOOSTER PACK
    # ------------------------------------------

    flecha = "▼" if menu_booster else "▶"

    texto = fuente_menu.render(
        flecha + " BOOSTER PACK",
        True,
        (30, 30, 30)
    )

    pantalla.blit(
        texto,
        (30, y_menu)
    )

    y_menu += 45

    if menu_booster:

        for codigo, nombre in temporadas:

            if not codigo.startswith("BP"):
                continue

            if codigo == temporada_seleccionada:
                pygame.draw.rect(
                    pantalla,
                    (220, 220, 220),
                    (30, y_menu, 450, 35)
                )

                pygame.draw.rect(
                    pantalla,
                    (30, 30, 30),
                    (30, y_menu, 450, 35),
                    1
                )

            fuente_booster = pygame.font.Font(
                FUENTE,
                16
            )

            if len(nombre) > 25:

                palabras = nombre.split()
                linea1 = ""
                linea2 = ""

                for palabra in palabras:

                    if len(linea1 + " " + palabra) <= 25:
                        linea1 += (" " if linea1 else "") + palabra
                    else:
                        linea2 += (" " if linea2 else "") + palabra

                texto1 = fuente_menu.render(
                    linea1,
                    True,
                    (30, 30, 30)
                )

                texto2 = fuente_menu.render(
                    linea2,
                    True,
                    (30, 30, 30)
                )

                pantalla.blit(
                    texto1,
                    (45, y_menu)
                )

                pantalla.blit(
                    texto2,
                    (45, y_menu + 25)
                )

                y_menu += 63

            else:

                texto = fuente_menu.render(
                    nombre,
                    True,
                    (30, 30, 30)
                )

                pantalla.blit(
                    texto,
                    (45, y_menu)
                )

                y_menu += 38


    # ------------------------------------------
    # FORSQUAD
    # ------------------------------------------

    flecha = "▼" if menu_forsquad else "▶"

    texto = fuente_menu.render(
        flecha + " FORSQUAD",
        True,
        (30, 30, 30)
    )

    pantalla.blit(
        texto,
        (30, y_menu)
    )

    y_menu += 45

    if menu_forsquad:

        for codigo, nombre in temporadas:

            if not codigo.startswith("FQ"):
                continue

            if codigo == temporada_seleccionada:
                pygame.draw.rect(
                    pantalla,
                    (220, 220, 220),
                    (30, y_menu, 450, 35)
                )

                pygame.draw.rect(
                    pantalla,
                    (30, 30, 30),
                    (30, y_menu, 450, 35),
                    1
                )
            texto = fuente_menu.render(
                nombre,
                True,
                (30, 30, 30)
            )

            pantalla.blit(
                texto,
                (45, y_menu)
            )

            y_menu += 38


    # ==================================================
    # TÍTULO
    # ==================================================

    fuente = pygame.font.Font(
        FUENTE,
        38
    )

    titulo = fuente.render(
        "GUNDAM ARSENAL BASE",
        True,
        (30, 30, 30)
    )

    pantalla.blit(
        titulo,
        (
            540 + (ANCHO - 540) // 2
            - titulo.get_width() // 2,
            35
        )
    )

    pygame.draw.line(
        pantalla,
        (30, 30, 30),
        (520, 85),
        (1560, 85),
        2
    )


    # ==================================================
    # CARTAS
    # ==================================================

    ancho_carta = 180
    alto_carta = 252

    espacio_x = 45
    espacio_y = 35

    inicio_x = 450
    inicio_y = 100

    for i in range(CARTAS_POR_PAGINA):

        indice = (
            pagina * CARTAS_POR_PAGINA
            + i
        )

        if indice >= len(cartas_mostradas):
            break

        fila = i // COLUMNAS
        columna = i % COLUMNAS

        x = (
            inicio_x
            + columna * (
                ancho_carta
                + espacio_x
            )
        )

        y = (
            inicio_y
            + fila * (
                alto_carta
                + espacio_y
            )
        )

        imagen = cargar_carta(
            cartas_mostradas[indice],
            (
                ancho_carta,
                alto_carta
            )
        )

        pantalla.blit(
            imagen,
            (x, y)
        )


    # ==================================================
    # PÁGINA
    # ==================================================

    fuente = pygame.font.Font(
        FUENTE,
        24
    )

    total_paginas = (
        len(cartas_mostradas) - 1
    ) // CARTAS_POR_PAGINA + 1

    texto_pagina = fuente.render(
        f"Página {pagina + 1} / {total_paginas}",
        True,
        (30, 30, 30)
    )

    pantalla.blit(
        texto_pagina,
        (
            ANCHO // 2
            - texto_pagina.get_width() // 2,
            670
        )
    )


    # ==================================================
    # MODAL
    # ==================================================

    if modal_abierto:

        # ----------------------------------------------
        # Fondo oscuro transparente
        # ----------------------------------------------

        overlay = pygame.Surface(
            (ANCHO, ALTO),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 180)
        )

        pantalla.blit(
            overlay,
            (0, 0)
        )

        # ----------------------------------------------
        # Panel del modal
        # ----------------------------------------------

        panel_ancho = 560
        panel_alto = 780

        panel_x = (
                          ANCHO - panel_ancho
                  ) // 2

        panel_y = (
                          ALTO - panel_alto
                  ) // 2

        # Sombra

        sombra = pygame.Surface(
            (panel_ancho, panel_alto),
            pygame.SRCALPHA
        )

        sombra.fill(
            (0, 0, 0, 100)
        )

        pantalla.blit(
            sombra,
            (
                panel_x + 12,
                panel_y + 12
            )
        )

        # Panel

        pygame.draw.rect(
            pantalla,
            (245, 245, 245),
            (
                panel_x,
                panel_y,
                panel_ancho,
                panel_alto
            )
        )

        # Borde exterior

        pygame.draw.rect(
            pantalla,
            (30, 30, 30),
            (
                panel_x,
                panel_y,
                panel_ancho,
                panel_alto
            ),
            3
        )


        # ----------------------------------------------
        # Carta grande
        # ----------------------------------------------

        nombre = cartas_mostradas[
            carta_seleccionada
        ]

        reverso = buscar_reverso(
            nombre
        )

        if mostrando_reverso and reverso:

            imagen = cargar_carta(
                reverso,
                (500, 700)
            )

        else:

            imagen = cargar_carta(
                nombre,
                (500, 700)
            )

        # ----------------------------------------------
        # Animación de entrada
        # ----------------------------------------------

        if animando_entrada:
            import math

            escala_modal = (
                    0.90
                    + 0.10 * progreso_entrada
            )

            nuevo_ancho = int(
                500 * escala_modal
            )

            nuevo_alto = int(
                700 * escala_modal
            )

            imagen = pygame.transform.smoothscale(
                imagen,
                (
                    nuevo_ancho,
                    nuevo_alto
                )
            )


        # ----------------------------------------------
        # Efecto de giro
        # ----------------------------------------------

        if animando_flip:

            import math

            escala = abs(
                math.cos(
                    progreso_flip * math.pi
                )
            )

            nuevo_ancho = max(
                1,
                int(500 * escala)
            )


            if progreso_flip < 0.5:

                nombre_animacion = nombre

            else:

                if reverso:

                    nombre_animacion = reverso

                else:

                    nombre_animacion = nombre


            imagen = cargar_carta(
                nombre_animacion,
                (500, 700)
            )

            imagen = pygame.transform.smoothscale(
                imagen,
                (
                    nuevo_ancho,
                    700
                )
            )


        # ----------------------------------------------
        # Dibujar carta
        # ----------------------------------------------

        x = (
            ANCHO
            - imagen.get_width()
        ) // 2

        y = (
            ALTO
            - imagen.get_height()
        ) // 2

        pantalla.blit(
            imagen,
            (x, y)
        )


        # ----------------------------------------------
        # Instrucciones
        # ----------------------------------------------

        fuente = pygame.font.Font(
            FUENTE,
            22
        )

        texto = fuente.render(
            "Click en la carta: dar vuelta    |    "
            "Click afuera: cerrar    |    ESC",
            True,
            (30, 30, 30)
        )

        pantalla.blit(
            texto,
            (
                ANCHO // 2
                - texto.get_width() // 2,
                810
            )
        )


    pygame.display.flip()

    reloj.tick(60)


pygame.quit()