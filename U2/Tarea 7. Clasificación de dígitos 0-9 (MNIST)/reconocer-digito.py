"""
Reconocimiento de dígitos escritos a mano con MNIST

Materia: Inteligencia Artificial
Docente: José Mario Ríos Félix
Horario: 6:00 a 7:00 p. m.
Alumna: Kitzia Marisol Crespo Hernández
Número de control: C23171148

Descripción:
    Este programa permite dibujar números en tiempo real y obtener una
    predicción del número dibujado utilizando una red neuronal multicapa
    (MLP) previamente entrenada con el dataset MNIST.

    El modelo se carga desde el archivo mlp_model.keras, generado por la
    notebook entrenar-mlp-mnist.ipynb, sin necesidad de repetir el entrenamiento.

Ejecución:
    python reconocer-digito.py
"""

import logging
import os
import sys

# Reduce los mensajes de avisos de TensorFlow en la consola
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

# Desactiva las optimizaciones oneDNN para evitar sus avisos al iniciar TensorFlow
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

# Oculta los mensajes informativos y advertencias del registro de TensorFlow
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import cv2
import numpy as np


# Obtiene la ubicación del programa para localizar el modelo entrenado
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))

# Ruta del archivo que contiene el modelo entrenado
ARCHIVO_MODELO = os.path.join(CARPETA_BASE, "mlp_model.keras")

# Medidas de la ventana
LADO_LIENZO = 336
ANCHO_VENTANA = 664
ALTO_VENTANA = 470

# Grosor del trazo de 20 píxeles, equivalente a aproximadamente 2 píxeles al reducir la imagen a 28 × 28, similar al grosor de los dígitos de MNIST
GROSOR_TRAZO = 20

# Colores de la interfaz definidos en formato RGB
COLOR_FONDO = (244, 246, 250)
COLOR_PANEL = (255, 255, 255)
COLOR_BORDE = (213, 219, 229)
COLOR_TITULO = (26, 31, 42)
COLOR_ACENTO = (62, 70, 88)
COLOR_SUAVE = (124, 133, 150)
COLOR_BARRA = (64, 136, 236)
COLOR_GANADORA = (26, 150, 84)
COLOR_BOTON = (228, 232, 240)
COLOR_PRIMARIO = (45, 108, 223)

# Pillow permite escribir con acentos y con una tipografía del sistema
try:
    from PIL import Image, ImageDraw, ImageFont
    HAY_PILLOW = True
except ImportError:
    HAY_PILLOW = False

RUTAS_DE_FUENTE = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
RUTAS_DE_FUENTE_NEGRITA = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FUENTES_CARGADAS = {}

# Zonas donde se puede hacer clic, cada una con su nombre
BOTONES = {
    "predecir": (16, 404, 122, 448),
    "borrar": (130, 404, 236, 448),
    "salir": (244, 404, 352, 448),
}


def a_bgr(color):
    """Cambia un color de rojo, verde, azul al orden que usa OpenCV."""
    return (color[2], color[1], color[0])


def obtener_fuente(tamano, negrita=False):
    """Carga una fuente del sistema y la guarda para no volver a leerla."""
    if not HAY_PILLOW:
        return None
    clave = (tamano, negrita)
    if clave not in FUENTES_CARGADAS:
        FUENTES_CARGADAS[clave] = None
        if negrita:
            rutas = RUTAS_DE_FUENTE_NEGRITA + RUTAS_DE_FUENTE
        else:
            rutas = RUTAS_DE_FUENTE
        for ruta in rutas:
            if os.path.isfile(ruta):
                try:
                    FUENTES_CARGADAS[clave] = ImageFont.truetype(ruta, tamano)
                    break
                except OSError:
                    continue
    return FUENTES_CARGADAS[clave]


def quitar_acentos(texto):
    import unicodedata
    normal = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in normal if not unicodedata.combining(c))


def escribir(vista, textos):
    """
    Añade textos a la ventana del programa, utilizando las posiciones,
    tamaños, colores y estilos definidos.

    Utiliza Pillow para mostrar los textos con acentos y, si no está
    disponible, utiliza OpenCV como alternativa.
    """
    if obtener_fuente(14) is None:
        for texto, posicion, tamano, negrita, color in textos:
            escala = tamano / 32.0
            grosor = 2 if negrita else 1
            plano = quitar_acentos(texto)
            alto = cv2.getTextSize(plano, cv2.FONT_HERSHEY_SIMPLEX, escala, grosor)[0][1]
            cv2.putText(vista, plano, (posicion[0], posicion[1] + alto),
                        cv2.FONT_HERSHEY_SIMPLEX, escala, a_bgr(color), grosor, cv2.LINE_AA)
        return vista

    lienzo = Image.fromarray(cv2.cvtColor(vista, cv2.COLOR_BGR2RGB))
    pincel = ImageDraw.Draw(lienzo)
    for texto, posicion, tamano, negrita, color in textos:
        pincel.text(posicion, texto, font=obtener_fuente(tamano, negrita),
                    fill=color, anchor="la")
    return cv2.cvtColor(np.array(lienzo), cv2.COLOR_RGB2BGR)


def cargar_modelo():
    """
    Carga el modelo previamente entrenado desde el archivo .keras.
    Verifica que el archivo exista antes de importar TensorFlow y,
    si no se encuentra, muestra un mensaje indicando cómo generarlo.
    """
    if not os.path.isfile(ARCHIVO_MODELO):
        sys.exit("No se encontró " + os.path.basename(ARCHIVO_MODELO) + ".\n"
                 "Primero hay que ejecutar la notebook entrenar-mlp-mnist.ipynb,\n"
                 "que entrena la red y guarda ese archivo.")

    print("Cargando el modelo entrenado, tarda unos segundos...")
    import tensorflow as tf
    modelo = tf.keras.models.load_model(ARCHIVO_MODELO)
    print("Listo.\n")
    return modelo


def preparar_para_mnist(trazo):
    """
    Convierte el dibujo en una imagen similar a las utilizadas para entrenar
    la red neuronal con MNIST. Los dígitos son blancos sobre fondo negro, se recortan a su contorno, se escalan para caber en un espacio de 20 × 20 píxeles y se centran en una imagen de 28 × 28 según su centro de masa.

    Este proceso facilita el reconocimiento al mantener un formato similar
    al de las imágenes de entrenamiento.
    Devuelve None si el lienzo está vacío.
    """
    columnas = np.where(trazo.max(axis=0) > 0)[0]
    filas = np.where(trazo.max(axis=1) > 0)[0]
    if len(columnas) == 0 or len(filas) == 0:
        return None

    # Se recorta al rectángulo que contiene el trazo
    recorte = trazo[filas[0]:filas[-1] + 1, columnas[0]:columnas[-1] + 1]

    # Se escala conservando la proporción, con el lado mayor en 20 píxeles
    alto, ancho = recorte.shape
    if alto > ancho:
        nuevo_alto = 20
        nuevo_ancho = max(1, int(round(ancho * 20.0 / alto)))
    else:
        nuevo_ancho = 20
        nuevo_alto = max(1, int(round(alto * 20.0 / ancho)))
    recorte = cv2.resize(recorte, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)

    # Centra el dígito en una imagen negra de 28 × 28 píxeles
    imagen = np.zeros((28, 28), dtype=np.float32)
    inicio_y = (28 - nuevo_alto) // 2
    inicio_x = (28 - nuevo_ancho) // 2
    imagen[inicio_y:inicio_y + nuevo_alto, inicio_x:inicio_x + nuevo_ancho] = recorte

    # Ajusta la posición del dígito para centrarlo según su centro de masa
    peso = imagen.sum()
    if peso > 0:
        rejilla_y, rejilla_x = np.mgrid[0:28, 0:28]
        centro_y = (imagen * rejilla_y).sum() / peso
        centro_x = (imagen * rejilla_x).sum() / peso
        corrimiento = np.float32([[1, 0, round(13.5 - centro_x)],
                                  [0, 1, round(13.5 - centro_y)]])
        imagen = cv2.warpAffine(imagen, corrimiento, (28, 28))

    # La red se entrenó con valores entre 0 y 1
    return imagen / 255.0


def medir_texto(texto, tamano, negrita=False):
    """Devuelve el ancho en píxeles que va a ocupar un texto."""
    fuente = obtener_fuente(tamano, negrita)
    if fuente is None:
        escala = tamano / 32.0
        grosor = 2 if negrita else 1
        medida = cv2.getTextSize(quitar_acentos(texto), cv2.FONT_HERSHEY_SIMPLEX,
                                 escala, grosor)
        return medida[0][0]
    return int(fuente.getlength(texto))


def predecir(modelo, entrada):
    """Devuelve las probabilidades de las 10 clases (dígitos del 0 al 9) mediante el modelo entrenado."""
    lote = entrada.reshape(1, 28, 28)
    return modelo.predict(lote, verbose=0)[0]


def panel_relleno(vista, caja, color, radio=8):
    """Dibuja un rectángulo relleno con las esquinas redondeadas."""
    x1, y1, x2, y2 = caja
    radio = max(0, min(radio, (x2 - x1) // 2, (y2 - y1) // 2))
    color_bgr = a_bgr(color)
    cv2.rectangle(vista, (x1 + radio, y1), (x2 - radio, y2), color_bgr, -1)
    cv2.rectangle(vista, (x1, y1 + radio), (x2, y2 - radio), color_bgr, -1)
    for centro in ((x1 + radio, y1 + radio), (x2 - radio, y1 + radio),
                   (x1 + radio, y2 - radio), (x2 - radio, y2 - radio)):
        cv2.circle(vista, centro, radio, color_bgr, -1, cv2.LINE_AA)


def dibujar_ventana(trazo, probabilidades):
    """Arma la imagen completa de la ventana y la devuelve."""
    vista = np.full((ALTO_VENTANA, ANCHO_VENTANA, 3), a_bgr(COLOR_FONDO), dtype=np.uint8)
    textos = [("RECONOCIMIENTO DE DÍGITOS ESCRITOS A MANO",
               (16, 14), 13, True, COLOR_ACENTO),
              ("Dibuja un número del 0 al 9", (16, 32), 15, False, COLOR_SUAVE)]

    # El trazo se guarda en blanco sobre negro, como en MNIST, pero se muestra
    # invertido para simular tinta oscura sobre papel blanco
    vista[56:56 + LADO_LIENZO, 16:16 + LADO_LIENZO] = cv2.cvtColor(255 - trazo,
                                                                   cv2.COLOR_GRAY2BGR)
    cv2.rectangle(vista, (16, 56), (16 + LADO_LIENZO, 56 + LADO_LIENZO),
                  a_bgr(COLOR_BORDE), 2)

    # Los botones
    etiquetas = {"predecir": "PREDECIR", "borrar": "BORRAR", "salir": "SALIR"}
    for nombre, caja in BOTONES.items():
        if nombre == "predecir":
            color, letra = COLOR_PRIMARIO, (255, 255, 255)
        else:
            color, letra = COLOR_BOTON, COLOR_TITULO
        panel_relleno(vista, caja, color)
        centro_x = (caja[0] + caja[2]) // 2 - medir_texto(etiquetas[nombre], 13, True) // 2
        textos.append((etiquetas[nombre], (centro_x, caja[1] + 13), 13, True, letra))

    # Panel derecho donde se muestra el resultado de la predicción
    izquierda = 368
    panel_relleno(vista, (izquierda, 56, ANCHO_VENTANA - 16, 448), COLOR_PANEL, 10)
    cv2.rectangle(vista, (izquierda, 56), (ANCHO_VENTANA - 16, 448),
                  a_bgr(COLOR_BORDE), 1, cv2.LINE_AA)

    if probabilidades is None:
        textos.append(("Presiona PREDECIR", (izquierda + 20, 240), 16, False, COLOR_SUAVE))
        textos.append(("cuando termines de dibujar", (izquierda + 20, 262), 14,
                       False, COLOR_SUAVE))
        return escribir(vista, textos)

    ganadora = int(np.argmax(probabilidades))
    confianza = probabilidades[ganadora] * 100

    textos.append(("El modelo predice un", (izquierda + 20, 150), 13, False, COLOR_SUAVE))
    textos.append((str(ganadora), (izquierda + 20, 164), 56, True, COLOR_GANADORA))
    textos.append(("con una confianza del %.1f %%" % confianza,
                   (izquierda + 20, 226), 14, False, COLOR_ACENTO))

    # Muestra las tres clases con mayor probabilidad, ordenadas de mayor a menor
    # La red devuelve diez valores, pero los restantes suelen ser muy bajos
    # o cercanos a cero, por lo que se muestran solo los tres más altos
    textos.append(("Las tres más probables", (izquierda + 20, 264), 13, True, COLOR_SUAVE))
    inicio_barra = izquierda + 44
    largo = ANCHO_VENTANA - 80 - inicio_barra
    for lugar, digito in enumerate(np.argsort(probabilidades)[::-1][:3]):
        y = 288 + lugar * 26
        cv2.rectangle(vista, (inicio_barra, y), (inicio_barra + largo, y + 14),
                      a_bgr(COLOR_BOTON), -1)
        ancho = int(largo * float(probabilidades[digito]))
        if ancho > 0:
            color = COLOR_GANADORA if lugar == 0 else COLOR_BARRA
            cv2.rectangle(vista, (inicio_barra, y), (inicio_barra + ancho, y + 14),
                          a_bgr(color), -1)
        textos.append((str(int(digito)), (izquierda + 20, y - 1), 15, True, COLOR_ACENTO))
        textos.append(("%4.1f%%" % (probabilidades[digito] * 100),
                       (ANCHO_VENTANA - 74, y - 1), 12, False, COLOR_SUAVE))

    return escribir(vista, textos)


def main():
    modelo = cargar_modelo()

    print("Controles de la ventana:")
    print("   Dibuja un número del 0 al 9")
    print("   PREDECIR o la tecla ESPACIO    realiza la predicción")
    print("   BORRAR o la tecla C            limpia el lienzo")
    print("   SALIR o la tecla Q             cierra el programa\n")

    trazo = np.zeros((LADO_LIENZO, LADO_LIENZO), dtype=np.uint8)
    estado = {"dibujando": False, "anterior": None,
              "probabilidades": None, "salir": False}

    def reconocer():
        """Prepara lo que haya en el lienzo y lo manda a la red."""
        entrada = preparar_para_mnist(trazo)
        if entrada is None:
            print("El lienzo está vacío, dibuja un número primero.")
            return
        estado["probabilidades"] = predecir(modelo, entrada)
        print("Predicción " + str(int(np.argmax(estado["probabilidades"]))))

    def limpiar():
        """Limpia el lienzo y elimina la predicción anterior."""
        trazo[:] = 0
        estado["probabilidades"] = None

    def al_usar_el_mouse(evento, x, y, banderas, parametros):
        dentro = 16 <= x < 16 + LADO_LIENZO and 56 <= y < 56 + LADO_LIENZO
        punto = (x - 16, y - 56)

        if evento == cv2.EVENT_LBUTTONDOWN:
            for nombre, (x1, y1, x2, y2) in BOTONES.items():
                if x1 <= x <= x2 and y1 <= y <= y2:
                    if nombre == "predecir":
                        reconocer()
                    elif nombre == "borrar":
                        limpiar()
                    else:
                        estado["salir"] = True
                    return
            if dentro:
                estado["dibujando"] = True
                estado["anterior"] = punto
                cv2.circle(trazo, punto, GROSOR_TRAZO // 2, 255, -1, cv2.LINE_AA)

        elif evento == cv2.EVENT_MOUSEMOVE and estado["dibujando"] and dentro:
            # Se une con una línea para que el trazo no salga punteado
            cv2.line(trazo, estado["anterior"], punto, 255, GROSOR_TRAZO, cv2.LINE_AA)
            estado["anterior"] = punto

        elif evento == cv2.EVENT_LBUTTONUP:
            estado["dibujando"] = False

    ventana = "Reconocimiento de digitos escritos a mano con MLP y MNIST"
    cv2.namedWindow(ventana)
    cv2.setMouseCallback(ventana, al_usar_el_mouse)

    while not estado["salir"]:
        cv2.imshow(ventana, dibujar_ventana(trazo, estado["probabilidades"]))
        tecla = cv2.waitKey(16) & 0xFF
        if tecla in (ord("q"), ord("Q"), 27):
            break
        if tecla == ord(" "):
            reconocer()
        if tecla in (ord("c"), ord("C")):
            limpiar()
        if cv2.getWindowProperty(ventana, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
