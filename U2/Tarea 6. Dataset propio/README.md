# Tarea #6. Dataset propio de rostros

**Materia:** Inteligencia Artificial  
**Profesor:** José Mario Ríos Félix  
**Instituto Tecnológico de Culiacán**

Programa desarrollado en Python para crear un dataset de rostros utilizando OpenCV y el algoritmo Haar Cascade. Permite detectar, recortar y guardar 100 imágenes faciales por persona.

El dataset estará formado por **900 imágenes**: 400 de los cuatro integrantes del equipo y 500 de cinco celebridades.

En esta primera etapa se realiza la recopilación y el preprocesamiento de las imágenes. Posteriormente, el dataset se utilizará para entrenar un modelo de reconocimiento facial.

## Integrantes del equipo

| Integrante | Carpeta |
| --- | --- |
| Kitzia Marisol Crespo Hernández | `Kitzia_Crespo` |
| Emir Gabino Pérez Villarreal | `Emir_Perez` |
| Oscar Antonio Sánchez Lara | `Oscar_Sanchez` |
| Jonathan Daniel Valencia | `Jonathan_Valencia` |

## Famosos seleccionados

| Famoso | Carpeta |
| --- | --- |
| Robert Downey Jr. | `Robert_Downey_Jr` |
| Emma Watson | `Emma_Watson` |
| Elizabeth Olsen | `Elizabeth_Olsen` |
| Alexandra Daddario | `Alexandra_Daddario` |
| Dwayne Johnson | `Dwayne_Johnson` |

Las fotografías se obtuvieron del **105 Classes Pins Dataset**, disponible en Kaggle. Se seleccionaron celebridades con más de 130 imágenes para disponer de fotografías adicionales en caso de que algunas no sean adecuadas para el dataset.

## Instalación

Instalar las dependencias desde la terminal:

```bash
pip install -r requirements.txt
```

## Ejecución

Ejecutar el programa con el siguiente comando:

```bash
python dataset_rostros.py
```

Al iniciar, se muestra el siguiente menú:

```text
DATASET DE ROSTROS
1. Capturar rostros con la cámara
2. Recortar las fotos de los famosos
3. Salir
```

### Opción 1. Capturar rostros con la cámara

Se ingresa el nombre del integrante y se abre una ventana con la cámara en tiempo real.

Durante la captura, se recomienda mover ligeramente la cabeza hacia ambos lados, mirar hacia arriba y abajo, y variar las expresiones faciales para obtener fotografías diferentes.

La ventana muestra el nombre de la persona, la cantidad de imágenes guardadas y el estado de la captura. También señala el rostro detectado y muestra un aviso cuando no logra identificarlo.

| Tecla | Función |
| --- | --- |
| ESPACIO | Iniciar o pausar la captura |
| R | Girar la imagen 90° |
| Q | Finalizar la captura |

Si la imagen aparece girada, se puede corregir presionando **R**. Para conservar esa orientación en futuras ejecuciones, se modifica el valor de `ROTACION` dentro del código.

### Opción 2. Procesar las fotografías de los famosos

Las fotografías originales deben organizarse dentro de `fotos_famosos_sin_recortar/`, utilizando una carpeta para cada celebridad.

Si las imágenes se encuentran en otra ubicación, el programa permite ingresar su ruta. También se puede establecer directamente en `CARPETA_DE_FOTOS_FAMOSOS`.

El procesamiento se realiza en tres etapas:

1. **Detección inicial:** se utiliza Haar Cascade con parámetros más estrictos para localizar y recortar los rostros.
2. **Detección adicional:** si faltan imágenes, se prueban otros parámetros, clasificadores Haar Cascade y diferentes orientaciones. Los resultados se revisan nuevamente para reducir detecciones incorrectas.
3. **Revisión de imágenes borrosas:** si todavía no se completan las 100 fotografías, se consideran algunos recortes descartados anteriormente, comenzando por los de mayor nitidez.

El procesamiento termina cuando se alcanzan las 100 imágenes o se agotan las fotografías disponibles.

Al finalizar, el programa muestra la cantidad de rostros guardados por celebridad y los resultados de las etapas adicionales, cuando se utilizaron.

## Estructura de carpetas

```text
Tarea 6. Dataset propio/
├── dataset_rostros.py
├── requirements.txt
├── README.md
├── haarcascade_frontalface_default.xml
│
├── fotos_famosos_sin_recortar/
│   ├── Robert Downey Jr/
│   ├── Emma Watson/
│   ├── Elizabeth Olsen/
│   ├── Alexandra Daddario/
│   └── Dwayne Johnson/
│
└── dataset/
    ├── integrantes_equipo/
    │   ├── Kitzia_Crespo/
    │   │   ├── Kitzia_Crespo_001.jpg
    │   │   └── ... hasta Kitzia_Crespo_100.jpg
    │   ├── Emir_Perez/
    │   │   ├── Emir_Perez_001.jpg
    │   │   └── ... hasta Emir_Perez_100.jpg
    │   ├── Oscar_Sanchez/
    │   │   ├── Oscar_Sanchez_001.jpg
    │   │   └── ... hasta Oscar_Sanchez_100.jpg
    │   └── Jonathan_Valencia/
    │       ├── Jonathan_Valencia_001.jpg
    │       └── ... hasta Jonathan_Valencia_100.jpg
    │
    └── famosos/
        ├── Robert_Downey_Jr/
        ├── Emma_Watson/
        ├── Elizabeth_Olsen/
        ├── Alexandra_Daddario/
        └── Dwayne_Johnson/
```

Las imágenes se organizan en carpetas individuales, que posteriormente permitirán identificar las clases utilizadas durante el entrenamiento del modelo.

La carpeta `fotos_famosos_sin_recortar/` no se incluye en el repositorio debido al tamaño de las fotografías originales descargadas de Kaggle. Solo se incorporan las imágenes procesadas que forman parte del dataset final.

## Recomendaciones para la captura

- **Iluminación:** utilizar luz uniforme y evitar sombras intensas sobre el rostro. También conviene incluir pequeñas variaciones para obtener imágenes más diversas.
- **Posiciones:** mirar al centro, girar ligeramente hacia ambos lados y variar la inclinación de la cabeza, procurando que el detector siga identificando el rostro.
- **Apariencia:** incluir fotografías con y sin lentes, o con diferentes peinados, cuando corresponda.
- **Encuadre:** mantener el mismo valor de `MARGEN` para conservar un tamaño de recorte uniforme.
- **Revisión:** comprobar las fotografías guardadas y eliminar aquellas que no correspondan a un rostro o presenten errores importantes.

## Parámetros de configuración

Los siguientes valores se pueden modificar al inicio de `dataset_rostros.py`:

| Parámetro | Valor | Descripción |
| --- | --- | --- |
| `CARPETA_DE_FOTOS_FAMOSOS` | `""` | Ruta alternativa de las fotografías originales |
| `IMAGENES_POR_PERSONA` | `100` | Cantidad máxima de imágenes por persona |
| `TAMANO_RECORTE` | `160` | Resolución de salida de 160 × 160 píxeles |
| `MARGEN` | `0.0` | Espacio adicional alrededor del rostro |
| `NITIDEZ_MINIMA` | `25.0` | Umbral para filtrar imágenes borrosas |
| `GUARDAR_EN_GRIS` | `False` | Permite guardar imágenes en escala de grises |
| `MODO_ESPEJO` | `True` | Invierte horizontalmente la vista de la cámara |
| `ROTACION` | `0` | Orientación de la cámara en grados |
| `INDICE_CAMARA` | `0` | Cámara que se intenta utilizar inicialmente |

## Notas técnicas

- Se utilizan `imdecode` e `imencode` para leer y guardar imágenes, evitando posibles problemas con rutas que contienen acentos.
- Si se detectan varios rostros, se selecciona el de mayor tamaño.
- Se incluye `haarcascade_frontalface_default.xml` como respaldo del clasificador disponible en OpenCV.
- La vista de la cámara puede mostrarse en espejo, pero las fotografías se guardan sin invertir horizontalmente.
- El programa comprueba diferentes índices de cámara cuando no consigue obtener una imagen válida.
- Se utiliza Pillow para mostrar los textos de la interfaz. Si no está disponible, se emplean las fuentes de OpenCV.