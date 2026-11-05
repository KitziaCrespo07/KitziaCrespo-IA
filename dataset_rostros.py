"""
Tarea #6. Dataset propio de rostros
Materia: Inteligencia Artificial
Profesor: José Mario Ríos Félix
Instituto Tecnológico de Culiacán

Integrantes:
    - Kitzia Marisol Crespo Hernández
    - Emir Gabino Pérez Villarreal
    - Oscar Antonio Sánchez Lara
    - Jonathan Daniel Valencia

Descripción:
    Programa en Python que arma un dataset de rostros con OpenCV y el
    algoritmo Haar Cascade.

    Captura imágenes desde la cámara, detecta el rostro, lo recorta y lo
    guarda. También recorta fotografías de famosos descargadas de Kaggle.
    Se generan 100 imágenes por persona, cada una en su carpeta.

    El dataset servirá más adelante para entrenar un modelo de
    reconocimiento facial.

Instalación:
    pip install -r requirements.txt

Ejecución:
    python dataset_rostros.py
"""


import os
import sys
import time
import unicodedata

import cv2
import numpy as np


# Carpeta donde está este archivo. Las demás rutas parten de ella
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))

# El dataset se divide en dos grupos para distinguir al equipo de los famosos
CARPETA_DATASET = os.path.join(CARPETA_BASE, "dataset")
CARPETA_INTEGRANTES = os.path.join(CARPETA_DATASET, "integrantes_equipo")
CARPETA_FAMOSOS = os.path.join(CARPETA_DATASET, "famosos")

# Fotos de los famosos sin recortar, una subcarpeta por cada uno.
# Si están en otro disco se escribe aquí la ruta completa entre comillas.
# Dejándolo vacío, el programa pregunta la ruta al momento de recortar
CARPETA_DE_FOTOS_FAMOSOS = r""
CARPETA_FOTOS_SIN_RECORTAR = (CARPETA_DE_FOTOS_FAMOSOS or
                              os.path.join(CARPETA_BASE, "fotos_famosos_sin_recortar"))

# Cuántas imágenes se guardan de cada persona
IMAGENES_POR_PERSONA = 100

# Medida en pixeles de cada recorte guardado
TAMANO_RECORTE = 160

# Espacio alrededor de la cara detectada. En cero el recorte queda
# ajustado al rostro, sin cuello ni hombros
MARGEN = 0.0

# Tiempo de espera entre una captura y la siguiente
SEGUNDOS_ENTRE_CAPTURAS = 0.15

# Los recortes por debajo de este valor se consideran borrosos.
# Con cero no se descarta ninguno
NITIDEZ_MINIMA = 25.0

# Con True las imágenes se guardan en blanco y negro
GUARDAR_EN_GRIS = False

# Con True la cámara se ve en espejo, como en una videollamada.
# Solo cambia lo que se ve en pantalla, no lo que se guarda
MODO_ESPEJO = True

# Grados que se gira la imagen de la cámara. Algunas laptops la entregan
# de cabeza. Durante la captura se gira con la tecla R y el valor que
# funcione se anota aquí
ROTACION = 0

# Cámara con la que se intenta primero. Si no entrega imagen se prueban
# las siguientes
INDICE_CAMARA = 0

ARCHIVO_HAAR = "haarcascade_frontalface_default.xml"
EXTENSIONES_IMAGEN = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

# La fuente que trae OpenCV se ve tosca y no admite acentos.
# Si Pillow está instalado se usa una fuente del sistema
try:
    from PIL import Image, ImageDraw, ImageFont
    HAY_PILLOW = True
except ImportError:
    HAY_PILLOW = False

RUTAS_DE_FUENTE = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\calibri.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]

# Las mismas fuentes en negrita, para los títulos
RUTAS_DE_FUENTE_NEGRITA = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\calibrib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]

FUENTES_CARGADAS = {}

# Colores de la ventana en orden rojo, verde, azul.
# OpenCV los usa al revés, por eso existe la función a_bgr
COLOR_PANEL = (14, 16, 22)
COLOR_TITULO = (255, 255, 255)
COLOR_ACENTO = (215, 222, 235)
COLOR_CAPTURANDO = (125, 230, 145)
COLOR_PAUSA = (255, 200, 95)
COLOR_AVISO = (255, 125, 125)
COLOR_FONDO_AVISO = (74, 28, 34)
COLOR_TEXTO_SUAVE = (186, 193, 209)
COLOR_CHIP = (48, 53, 66)

# Alto de las dos franjas oscuras de la ventana
ALTO_PANEL_ARRIBA = 80
ALTO_PANEL_ABAJO = 44


def cargar_detector():
    """
    Carga el clasificador Haar Cascade de rostros frontales.
    Primero se busca el que trae OpenCV y si no está se usa la copia
    incluida junto a este programa.
    """
    rutas = []
    carpeta_opencv = getattr(getattr(cv2, "data", None), "haarcascades", None)
    if carpeta_opencv:
        rutas.append(os.path.join(carpeta_opencv, ARCHIVO_HAAR))
    rutas.append(os.path.join(CARPETA_BASE, ARCHIVO_HAAR))

    for ruta in rutas:
        if os.path.isfile(ruta):
            detector = cv2.CascadeClassifier(ruta)
            if not detector.empty():
                return detector

    sys.exit("No se encontró el archivo " + ARCHIVO_HAAR +
             ". Debe estar en la misma carpeta que este programa.")


def nombre_de_carpeta(nombre):
    """
    Convierte un nombre en un texto que sirva como nombre de carpeta.
    Juan Pérez García queda como Juan_Perez_Garcia.
    Se quitan los acentos porque en Windows dan problemas al guardar.
    """
    sin_acentos = unicodedata.normalize("NFKD", nombre)
    sin_acentos = "".join(c for c in sin_acentos if not unicodedata.combining(c))
    palabras = "".join(c if c.isalnum() else " " for c in sin_acentos).split()
    return "_".join(palabras)


def leer_imagen(ruta):
    """
    Lee una imagen del disco.
    No se usa cv2.imread porque en Windows falla cuando la ruta tiene
    acentos, y la carpeta del proyecto los lleva.
    """
    try:
        datos = np.fromfile(ruta, dtype=np.uint8)
    except OSError:
        return None
    if datos.size == 0:
        return None
    return cv2.imdecode(datos, cv2.IMREAD_COLOR)


def guardar_imagen(ruta, imagen):
    """Guarda una imagen. No se usa cv2.imwrite por el mismo motivo que arriba."""
    extension = os.path.splitext(ruta)[1]
    correcto, memoria = cv2.imencode(extension, imagen, [cv2.IMWRITE_JPEG_QUALITY, 92])
    if not correcto:
        return False

    try:
        memoria.tofile(ruta)
    except OSError as problema:
        # Suele pasar cuando se acaba el espacio en disco. Se avisa y se
        # devuelve False en lugar de cortar el programa
        print("No se pudo guardar " + os.path.basename(ruta) + ". " + str(problema))
        try:
            # Para no dejar un archivo vacío a medio escribir
            if os.path.isfile(ruta) and os.path.getsize(ruta) == 0:
                os.remove(ruta)
        except OSError:
            pass
        return False
    return True


def buscar_rostro(imagen, detector, lado_minimo):
    """
    Busca rostros y devuelve el más grande como (x, y, ancho, alto).
    Se toma el más grande porque es el que está frente a la cámara.
    Haar Cascade a veces marca zonas del fondo, y esas detecciones
    incorrectas suelen ser más pequeñas.
    Devuelve None si no encuentra ninguno.
    """
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Empareja el contraste, lo que ayuda cuando hay poca luz
    gris = cv2.equalizeHist(gris)

    rostros = detector.detectMultiScale(
        gris,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(lado_minimo, lado_minimo),
    )
    if len(rostros) == 0:
        return None

    mas_grande = max(rostros, key=lambda caja: caja[2] * caja[3])
    return tuple(int(valor) for valor in mas_grande)


def cargar_cascada_extra(archivo):
    """
    Carga otra de las cascadas incluidas en OpenCV.
    Devuelve None si esa instalación no la trae, para que el programa
    pueda seguir sin ella.
    """
    rutas = []
    carpeta_opencv = getattr(getattr(cv2, "data", None), "haarcascades", None)
    if carpeta_opencv:
        rutas.append(os.path.join(carpeta_opencv, archivo))
    rutas.append(os.path.join(CARPETA_BASE, archivo))

    for ruta in rutas:
        if os.path.isfile(ruta):
            cascada = cv2.CascadeClassifier(ruta)
            if not cascada.empty():
                return cascada
    return None


def rostro_mas_grande(cascada, gris, escala, vecinos, lado_minimo):
    """Aplica una cascada con los parámetros dados y devuelve el rostro más grande."""
    rostros = cascada.detectMultiScale(gris, scaleFactor=escala, minNeighbors=vecinos,
                                       minSize=(lado_minimo, lado_minimo))
    if len(rostros) == 0:
        return None
    return tuple(int(valor) for valor in max(rostros, key=lambda caja: caja[2] * caja[3]))


def buscar_rostro_a_fondo(imagen, detector, alterna, perfil):
    """
    Busca el rostro probando varias configuraciones antes de darse por vencido.
    Se usa solo con las fotografías de los famosos, donde la cara puede estar
    de perfil, inclinada o pequeña dentro de la imagen. En la cámara se sigue
    usando la búsqueda estricta, porque bajar las exigencias en vivo hace que
    se recorten partes del fondo.
    Devuelve la imagen de la que hay que recortar, ya que algunos intentos
    trabajan sobre la foto volteada o girada, la posición del rostro, y si el
    resultado vino del primer intento o de los siguientes.
    """
    gris = cv2.equalizeHist(cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY))
    lado = max(30, min(imagen.shape[:2]) // 8)
    lado_chico = max(24, lado // 2)

    # Primer intento con la configuración estricta, la misma de la cámara
    caja = rostro_mas_grande(detector, gris, 1.1, 5, lado)
    if caja is not None:
        return imagen, caja, True

    # Búsqueda más fina y menos exigente, que acepta caras más pequeñas
    caja = rostro_mas_grande(detector, gris, 1.05, 3, lado_chico)
    if caja is not None:
        return imagen, caja, False

    # Otra cascada Haar, entrenada con imágenes distintas
    if alterna is not None:
        caja = rostro_mas_grande(alterna, gris, 1.05, 3, lado_chico)
        if caja is not None:
            return imagen, caja, False

    # Cascada de perfil. La imagen volteada sirve para el perfil contrario
    if perfil is not None:
        caja = rostro_mas_grande(perfil, gris, 1.05, 3, lado_chico)
        if caja is not None:
            return imagen, caja, False
        caja = rostro_mas_grande(perfil, cv2.flip(gris, 1), 1.05, 3, lado_chico)
        if caja is not None:
            return cv2.flip(imagen, 1), caja, False

    # Caras inclinadas. Se gira la foto unos grados y se recorta de la girada
    medida = (imagen.shape[1], imagen.shape[0])
    centro = (medida[0] / 2.0, medida[1] / 2.0)
    for grados in (-14, 14, -25, 25):
        matriz = cv2.getRotationMatrix2D(centro, grados, 1.0)
        caja = rostro_mas_grande(detector, cv2.warpAffine(gris, matriz, medida),
                                 1.05, 3, lado_chico)
        if caja is not None:
            return cv2.warpAffine(imagen, matriz, medida), caja, False

    return None, None, False


def confirmar_rostro(recorte, detector, alterna, perfil):
    """
    Vuelve a aplicar el detector sobre un recorte ya hecho, probando las tres
    cascadas y la imagen volteada.
    Si en una imagen que se supone que es un rostro ya no se detecta ninguno,
    lo más probable es que el recorte haya tomado otra cosa.
    Esta comprobación se aplica a los recortes que no salieron del primer
    intento, porque con un rostro frontal bien detectado falla de vez en cuando.
    """
    gris = recorte if recorte.ndim == 2 else cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    gris = cv2.equalizeHist(gris)
    lado = max(40, gris.shape[0] // 3)

    for cascada in (detector, alterna, perfil):
        if cascada is None:
            continue
        for version in (gris, cv2.flip(gris, 1)):
            rostros = cascada.detectMultiScale(version, scaleFactor=1.08,
                                               minNeighbors=3, minSize=(lado, lado))
            if len(rostros) > 0:
                return True
    return False


def recortar_rostro(imagen, caja):
    """
    Recorta el rostro en forma cuadrada y lo deja del tamaño de salida,
    para que todas las imágenes del dataset midan lo mismo.
    """
    x, y, ancho, alto = caja
    alto_imagen, ancho_imagen = imagen.shape[:2]

    lado = int(max(ancho, alto) * (1 + 2 * MARGEN))
    lado = min(lado, alto_imagen, ancho_imagen)

    centro_x = x + ancho // 2
    centro_y = y + alto // 2
    x1 = max(0, min(centro_x - lado // 2, ancho_imagen - lado))
    y1 = max(0, min(centro_y - lado // 2, alto_imagen - lado))

    recorte = imagen[y1:y1 + lado, x1:x1 + lado]
    interpolacion = cv2.INTER_AREA if lado >= TAMANO_RECORTE else cv2.INTER_LINEAR
    recorte = cv2.resize(recorte, (TAMANO_RECORTE, TAMANO_RECORTE), interpolation=interpolacion)

    if GUARDAR_EN_GRIS:
        recorte = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    return recorte


def medir_nitidez(recorte):
    """
    Calcula qué tan enfocada está una imagen con la varianza del laplaciano.
    Entre más bajo el resultado, más borrosa está.
    """
    gris = recorte if recorte.ndim == 2 else cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gris, cv2.CV_64F).var()


def subcarpetas(carpeta):
    """Devuelve los nombres de las subcarpetas que contiene una carpeta."""
    return sorted(d for d in os.listdir(carpeta)
                  if os.path.isdir(os.path.join(carpeta, d)))


def listar_imagenes(carpeta):
    return sorted(f for f in os.listdir(carpeta) if f.lower().endswith(EXTENSIONES_IMAGEN))


def siguiente_numero(carpeta):
    """Devuelve el siguiente número libre, para no sobrescribir lo que ya existe."""
    numeros = [0]
    for archivo in listar_imagenes(carpeta):
        partes = os.path.splitext(archivo)[0].split("_")
        if partes[-1].isdigit():
            numeros.append(int(partes[-1]))
    return max(numeros) + 1


def capturar_con_camara(detector):
    """Enciende la cámara y guarda 100 recortes del rostro de una persona."""
    nombre = input("\nNombre de la persona, por ejemplo Juan Pérez: ").strip()
    if not nombre:
        print("Hace falta escribir un nombre.")
        return

    carpeta_persona = nombre_de_carpeta(nombre)
    destino = os.path.join(CARPETA_INTEGRANTES, carpeta_persona)
    os.makedirs(destino, exist_ok=True)

    ya_guardadas = len(listar_imagenes(destino))
    if ya_guardadas >= IMAGENES_POR_PERSONA:
        print("Esa carpeta ya tiene " + str(ya_guardadas) + " imágenes. No se agregó nada.")
        return
    if ya_guardadas > 0:
        print("La carpeta ya tenía " + str(ya_guardadas) + " imágenes. Las nuevas se suman.")

    numero = siguiente_numero(destino)
    faltan = IMAGENES_POR_PERSONA - ya_guardadas

    print("\nControles de la ventana de la cámara")
    print("   ESPACIO   inicia o pausa la captura")
    print("   R         gira la imagen, por si la cámara la entrega de cabeza")
    print("   Q         termina")
    print("Mientras captura, muévete despacio. Gira la cara a los lados, súbela")
    print("y bájala un poco, y cambia de expresión, para que las imágenes varíen.")
    print("Procura tener buena luz de frente, es lo que más afecta al entrenamiento.\n")

    camara = abrir_camara()
    capturando = False
    guardadas = 0
    ultimo_guardado = 0.0
    descartadas_borrosas = 0
    rotacion = ROTACION % 360

    while guardadas < faltan:
        correcto, cuadro = camara.read()
        if not correcto:
            print("Se perdió la señal de la cámara.")
            break

        cuadro = girar(cuadro, rotacion)
        caja = buscar_rostro(cuadro, detector, lado_minimo=100)

        # La vista puede ir en espejo para moverse con comodidad, pero el
        # recorte se toma siempre del cuadro original
        vista = cv2.flip(cuadro, 1) if MODO_ESPEJO else cuadro.copy()

        if caja is not None:
            x, y, ancho, alto = caja
            x_vista = cuadro.shape[1] - x - ancho if MODO_ESPEJO else x
            dibujar_marco(vista, (x_vista, y, ancho, alto),
                          COLOR_CAPTURANDO if capturando else COLOR_PAUSA)

            ahora = time.time()
            if capturando and ahora - ultimo_guardado >= SEGUNDOS_ENTRE_CAPTURAS:
                recorte = recortar_rostro(cuadro, caja)
                if medir_nitidez(recorte) < NITIDEZ_MINIMA:
                    descartadas_borrosas += 1
                else:
                    archivo = carpeta_persona + "_" + format(numero, "03d") + ".jpg"
                    if guardar_imagen(os.path.join(destino, archivo), recorte):
                        numero += 1
                        guardadas += 1
                        ultimo_guardado = ahora

        total = ya_guardadas + guardadas
        vista = escribir_en_pantalla(vista, carpeta_persona, total, capturando,
                                     caja is None, rotacion)
        cv2.imshow("Tarea 6, captura de rostros", vista)

        tecla = cv2.waitKey(1) & 0xFF
        if tecla in (ord("q"), ord("Q"), 27):
            break
        if tecla == ord(" "):
            capturando = not capturando
        if tecla in (ord("r"), ord("R")):
            rotacion = (rotacion + 90) % 360
            print("Imagen girada a " + str(rotacion) + " grados. "
                  "Anota ese valor en ROTACION para no repetirlo cada vez.")

    camara.release()
    cv2.destroyAllWindows()

    # Si se salió sin capturar nada, la carpeta se borra para no dejarla vacía
    if not listar_imagenes(destino):
        os.rmdir(destino)
        print("\nNo se capturó ninguna imagen. La carpeta no se creó.")
        return

    print("\nSe guardaron " + str(guardadas) + " imágenes nuevas en " + destino)
    if descartadas_borrosas:
        print("Se descartaron " + str(descartadas_borrosas) + " recortes por estar borrosos.")


def abrir_camara():
    """
    Abre la cámara y devuelve la primera que entregue imagen.
    Se prueban varios índices porque hay equipos con cámaras virtuales que
    abren sin error pero solo devuelven cuadros en negro.
    En Windows se usa el backend DirectShow porque inicia más rápido.
    """
    indices = [INDICE_CAMARA] + [i for i in range(4) if i != INDICE_CAMARA]

    for indice in indices:
        if os.name == "nt":
            camara = cv2.VideoCapture(indice, cv2.CAP_DSHOW)
        else:
            camara = cv2.VideoCapture(indice)

        if camara.isOpened():
            camara.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            correcto, cuadro = camara.read()
            if correcto and float(np.mean(cuadro)) > 1.0:
                if indice != INDICE_CAMARA:
                    print("Se encontró la cámara en el índice " + str(indice) + ".")
                return camara
        camara.release()

    sys.exit("Ninguna cámara entregó imagen. Revisa que no la esté usando otro programa.")


def girar(imagen, grados):
    """Gira la imagen en múltiplos de 90 grados."""
    if grados == 90:
        return cv2.rotate(imagen, cv2.ROTATE_90_CLOCKWISE)
    if grados == 180:
        return cv2.rotate(imagen, cv2.ROTATE_180)
    if grados == 270:
        return cv2.rotate(imagen, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return imagen


def obtener_fuente(tamano, negrita=False):
    """Carga una fuente del sistema y la guarda para no volver a leerla del disco."""
    if not HAY_PILLOW:
        return None
    clave = (tamano, negrita)
    if clave not in FUENTES_CARGADAS:
        FUENTES_CARGADAS[clave] = None
        # Si no se encuentra la negrita se usa la normal
        rutas = RUTAS_DE_FUENTE_NEGRITA + RUTAS_DE_FUENTE if negrita else RUTAS_DE_FUENTE
        for ruta in rutas:
            if os.path.isfile(ruta):
                try:
                    FUENTES_CARGADAS[clave] = ImageFont.truetype(ruta, tamano)
                    break
                except OSError:
                    continue
    return FUENTES_CARGADAS[clave]


def quitar_acentos(texto):
    normal = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in normal if not unicodedata.combining(c))


def a_bgr(color):
    """Cambia un color de rojo, verde, azul al orden que usa OpenCV."""
    return (color[2], color[1], color[0])


def medir_texto(texto, tamano, negrita=False):
    """Devuelve el ancho en pixeles que va a ocupar un texto."""
    fuente = obtener_fuente(tamano, negrita)
    if fuente is None:
        escala = tamano / 32.0
        grosor = 2 if negrita else 1
        medida = cv2.getTextSize(quitar_acentos(texto), cv2.FONT_HERSHEY_SIMPLEX,
                                 escala, grosor)
        return medida[0][0]
    return int(fuente.getlength(texto))


def panel_oscuro(vista, desde, hasta, opacidad=0.66):
    """Oscurece una franja de la imagen para que el texto se lea sobre ella."""
    desde = max(0, desde)
    hasta = min(vista.shape[0], hasta)
    if hasta <= desde:
        return
    franja = vista[desde:hasta]
    fondo = np.full(franja.shape, a_bgr(COLOR_PANEL), dtype=np.uint8)
    vista[desde:hasta] = cv2.addWeighted(franja, 1 - opacidad, fondo, opacidad, 0)


def rectangulo_redondeado(vista, esquina1, esquina2, color, radio):
    """Dibuja un rectángulo relleno con las esquinas redondeadas."""
    x1, y1 = esquina1
    x2, y2 = esquina2
    radio = max(0, min(radio, (x2 - x1) // 2, (y2 - y1) // 2))
    color_bgr = a_bgr(color)
    cv2.rectangle(vista, (x1 + radio, y1), (x2 - radio, y2), color_bgr, -1)
    cv2.rectangle(vista, (x1, y1 + radio), (x2, y2 - radio), color_bgr, -1)
    for centro in ((x1 + radio, y1 + radio), (x2 - radio, y1 + radio),
                   (x1 + radio, y2 - radio), (x2 - radio, y2 - radio)):
        cv2.circle(vista, centro, radio, color_bgr, -1, cv2.LINE_AA)


def dibujar_marco(vista, caja, color):
    """Marca el rostro detectado con cuatro esquinas, para no taparlo."""
    x, y, ancho, alto = caja
    color_bgr = a_bgr(color)

    capa = vista.copy()
    cv2.rectangle(capa, (x, y), (x + ancho, y + alto), color_bgr, 1, cv2.LINE_AA)
    vista[:] = cv2.addWeighted(capa, 0.38, vista, 0.62, 0)

    largo = max(16, int(min(ancho, alto) * 0.24))
    esquinas = (((x, y), 1, 1), ((x + ancho, y), -1, 1),
                ((x, y + alto), 1, -1), ((x + ancho, y + alto), -1, -1))
    for (punto_x, punto_y), hacia_x, hacia_y in esquinas:
        cv2.line(vista, (punto_x, punto_y), (punto_x + hacia_x * largo, punto_y),
                 color_bgr, 3, cv2.LINE_AA)
        cv2.line(vista, (punto_x, punto_y), (punto_x, punto_y + hacia_y * largo),
                 color_bgr, 3, cv2.LINE_AA)


def dibujar_textos(vista, textos):
    """
    Escribe una lista de textos sobre la imagen. De cada uno se indica el
    contenido, la posición, el tamaño, si va en negrita, el color y si se
    alinea a la derecha.
    Con Pillow se usa una fuente del sistema. Si no está instalado se usa la
    de OpenCV, que no admite acentos y por eso se le quitan.
    """
    if obtener_fuente(13) is None:
        for texto, posicion, tamano, negrita, color, a_la_derecha in textos:
            escala = tamano / 32.0
            grosor = 2 if negrita else 1
            plano = quitar_acentos(texto)
            medida = cv2.getTextSize(plano, cv2.FONT_HERSHEY_SIMPLEX, escala, grosor)[0]
            x = posicion[0] - medida[0] if a_la_derecha else posicion[0]
            cv2.putText(vista, plano, (x, posicion[1] + medida[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, escala, a_bgr(color), grosor, cv2.LINE_AA)
        return vista

    lienzo = Image.fromarray(cv2.cvtColor(vista, cv2.COLOR_BGR2RGB))
    pincel = ImageDraw.Draw(lienzo)
    for texto, posicion, tamano, negrita, color, a_la_derecha in textos:
        pincel.text(posicion, texto, font=obtener_fuente(tamano, negrita), fill=color,
                    anchor="ra" if a_la_derecha else "la")
    return cv2.cvtColor(np.array(lienzo), cv2.COLOR_RGB2BGR)


def escribir_en_pantalla(vista, persona, total, capturando, sin_rostro, rotacion):
    """Dibuja sobre el video el nombre, el contador, el estado y las teclas."""
    alto, ancho = vista.shape[:2]

    panel_oscuro(vista, 0, ALTO_PANEL_ARRIBA)
    panel_oscuro(vista, alto - ALTO_PANEL_ABAJO, alto)
    cv2.line(vista, (0, ALTO_PANEL_ARRIBA), (ancho, ALTO_PANEL_ARRIBA),
             a_bgr(COLOR_ACENTO), 2, cv2.LINE_AA)

    # El punto de color indica si está guardando o en pausa
    color_estado = COLOR_CAPTURANDO if capturando else COLOR_PAUSA
    cv2.circle(vista, (21, 64), 5, a_bgr(color_estado), -1, cv2.LINE_AA)

    textos = [
        ("TAREA 6    DATASET DE ROSTROS", (16, 10), 12, True, COLOR_ACENTO, False),
        (persona.replace("_", " "), (16, 27), 22, True, COLOR_TITULO, False),
        (str(total) + " / " + str(IMAGENES_POR_PERSONA), (ancho - 16, 27), 22, True,
         COLOR_ACENTO, True),
        ("Capturando" if capturando else "En pausa", (34, 56), 15, True, color_estado, False),
    ]

    # Las teclas se dibujan abajo, cada una en su recuadro
    posicion_x = 16
    linea_teclas = alto - 30
    for tecla, que_hace in (("ESPACIO", "inicia o pausa"), ("R", "gira"), ("Q", "termina")):
        ancho_tecla = medir_texto(tecla, 12, True) + 16
        rectangulo_redondeado(vista, (posicion_x, linea_teclas - 6),
                              (posicion_x + ancho_tecla, linea_teclas + 18), COLOR_CHIP, 6)
        textos.append((tecla, (posicion_x + 8, linea_teclas), 12, True, COLOR_TITULO, False))
        posicion_x += ancho_tecla + 7
        textos.append((que_hace, (posicion_x, linea_teclas), 12, False, COLOR_TEXTO_SUAVE, False))
        posicion_x += medir_texto(que_hace, 12) + 16

    if rotacion:
        textos.append(("girada " + str(rotacion) + " grados", (ancho - 16, linea_teclas),
                       12, False, COLOR_PAUSA, True))

    if sin_rostro:
        aviso = "No se detecta ningún rostro"
        ancho_aviso = medir_texto(aviso, 15, True) + 30
        izquierda = (ancho - ancho_aviso) // 2
        arriba = ALTO_PANEL_ARRIBA + 18
        rectangulo_redondeado(vista, (izquierda, arriba),
                              (izquierda + ancho_aviso, arriba + 30), COLOR_FONDO_AVISO, 15)
        textos.append((aviso, (izquierda + 15, arriba + 6), 15, True, COLOR_AVISO, False))

    return dibujar_textos(vista, textos)


def procesar_famosos(detector):
    """
    Recorta el rostro de las fotografías descargadas de los famosos.
    Cada famoso debe tener su propia subcarpeta dentro de la carpeta de fotos.
    """
    carpeta_origen = CARPETA_FOTOS_SIN_RECORTAR
    if not os.path.isdir(carpeta_origen):
        os.makedirs(carpeta_origen, exist_ok=True)

    famosos = subcarpetas(carpeta_origen)
    if not famosos:
        # Si la carpeta de siempre está vacía se pregunta dónde están las fotos,
        # porque pesan mucho y a veces se guardan en otro disco
        print("\nNo hay subcarpetas de famosos en " + carpeta_origen)
        print("Ahí debe ir una carpeta por famoso, con sus fotografías adentro.")
        otra = input("Si están en otra carpeta, pega aquí la ruta y pulsa Enter: ")
        otra = otra.strip().strip('"')
        if not otra:
            return
        if not os.path.isdir(otra):
            print("No existe esa carpeta.")
            return
        carpeta_origen = otra
        famosos = subcarpetas(carpeta_origen)
        if not famosos:
            print("Esa carpeta no tiene subcarpetas de famosos adentro.")
            return

    # Cascadas de apoyo para las fotos donde la primera no encuentra el rostro
    alterna = cargar_cascada_extra("haarcascade_frontalface_alt2.xml")
    perfil = cargar_cascada_extra("haarcascade_profileface.xml")

    print("\nFamosos encontrados: " + str(len(famosos)))

    # Los datasets de Kaggle traen decenas de personas y casi nunca se usan
    # todas. Procesarlas todas tarda mucho y ocupa bastante espacio
    if len(famosos) > 10:
        print("Son bastantes. Recortarlos todos tarda un buen rato y ocupa")
        print("mucho espacio. Lo normal es dejar en la carpeta solo los que se")
        print("van a usar, y borrar o mover los demás.")
        seguir = input("Escribe si para recortarlos todos, o Enter para cancelar: ")
        if seguir.strip().lower() not in ("si", "sí", "s"):
            print("Cancelado. No se recortó nada.")
            return

    for famoso in famosos:
        origen = os.path.join(carpeta_origen, famoso)

        # Las carpetas del dataset de Kaggle empiezan con pins_.
        # Se le quita para que la clase lleve el nombre de la persona
        nombre_limpio = famoso[5:] if famoso.lower().startswith("pins_") else famoso
        carpeta_persona = nombre_de_carpeta(nombre_limpio)
        destino = os.path.join(CARPETA_FAMOSOS, carpeta_persona)
        os.makedirs(destino, exist_ok=True)

        guardadas = len(listar_imagenes(destino))
        numero = siguiente_numero(destino)
        sin_rostro = 0
        no_confirmadas = 0
        con_insistencia = 0

        # Recortes borrosos, por si al final faltan imágenes
        apartadas = []

        # Fotos ya revisadas en la primera vuelta
        usadas = set()

        se_lleno_el_disco = False

        def guardar(recorte):
            """Guarda un recorte y avisa si el disco dejó de aceptar escrituras."""
            nonlocal numero, guardadas, se_lleno_el_disco
            nombre_salida = carpeta_persona + "_" + format(numero, "03d") + ".jpg"
            if guardar_imagen(os.path.join(destino, nombre_salida), recorte):
                numero += 1
                guardadas += 1
                return True
            se_lleno_el_disco = True
            return False

        archivos = listar_imagenes(origen)

        # Primera vuelta con la configuración estricta, que es la que menos
        # detecciones incorrectas produce. Cuando hay fotografías de sobra las
        # cien imágenes salen de aquí y no hacen falta las otras dos vueltas
        for archivo in archivos:
            if guardadas >= IMAGENES_POR_PERSONA or se_lleno_el_disco:
                break
            imagen = leer_imagen(os.path.join(origen, archivo))
            if imagen is None:
                continue

            caja = buscar_rostro(imagen, detector, max(30, min(imagen.shape[:2]) // 8))
            if caja is None:
                continue

            usadas.add(archivo)
            recorte = recortar_rostro(imagen, caja)
            nitidez = medir_nitidez(recorte)
            if nitidez < NITIDEZ_MINIMA:
                apartadas.append((nitidez, recorte))
                continue
            guardar(recorte)

        # Segunda vuelta, solo si faltan imágenes. Aquí se usan las otras
        # cascadas y la foto girada, y cada recorte se comprueba otra vez
        for archivo in archivos:
            if guardadas >= IMAGENES_POR_PERSONA or se_lleno_el_disco:
                break
            if archivo in usadas:
                continue
            imagen = leer_imagen(os.path.join(origen, archivo))
            if imagen is None:
                continue

            base, caja, estricto = buscar_rostro_a_fondo(imagen, detector, alterna, perfil)
            if caja is None:
                sin_rostro += 1
                continue

            recorte = recortar_rostro(base, caja)
            if not estricto and not confirmar_rostro(recorte, detector, alterna, perfil):
                no_confirmadas += 1
                continue

            nitidez = medir_nitidez(recorte)
            if nitidez < NITIDEZ_MINIMA:
                apartadas.append((nitidez, recorte))
                continue
            if guardar(recorte):
                con_insistencia += 1

        # Tercera vuelta, si todavía faltan. Se aprovechan los recortes que se
        # habían apartado por borrosos, del mejor enfocado al peor, y se
        # comprueban antes de guardarlos
        apartadas.sort(key=lambda par: par[0], reverse=True)
        recuperadas = 0
        for nitidez, recorte in apartadas:
            if guardadas >= IMAGENES_POR_PERSONA or se_lleno_el_disco:
                break
            if not confirmar_rostro(recorte, detector, alterna, perfil):
                no_confirmadas += 1
                continue
            if guardar(recorte):
                recuperadas += 1

        if se_lleno_el_disco:
            print("\nNo se están pudiendo guardar las imágenes. Casi siempre es")
            print("porque ya no queda espacio en el disco. Libera espacio y vuelve")
            print("a elegir la opción 2, lo que ya se guardó se conserva.")
            return

        detalles = []
        if sin_rostro:
            detalles.append(str(sin_rostro) + " sin rostro")
        if no_confirmadas:
            detalles.append(str(no_confirmadas) + " descartadas al revisarlas")
        if con_insistencia:
            detalles.append(str(con_insistencia) + " con los intentos extra")
        if recuperadas:
            detalles.append(str(recuperadas) + " borrosas aprovechadas")

        resumen = carpeta_persona.ljust(28) + str(guardadas).rjust(3) + " rostros"
        if detalles:
            resumen += "   (" + ", ".join(detalles) + ")"
        print("   " + resumen)

    print("\nRevisa las carpetas y borra a mano cualquier recorte que no sea una cara.")


def main():
    detector = cargar_detector()
    os.makedirs(CARPETA_DATASET, exist_ok=True)

    opciones = {
        "1": lambda: capturar_con_camara(detector),
        "2": lambda: procesar_famosos(detector),
    }

    while True:
        print("\nDATASET DE ROSTROS")
        print("   1. Capturar rostros con la cámara")
        print("   2. Recortar las fotos de los famosos")
        print("   3. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "3":
            break
        if opcion in opciones:
            opciones[opcion]()
        else:
            print("Esa opción no existe.")


if __name__ == "__main__":
    main()
