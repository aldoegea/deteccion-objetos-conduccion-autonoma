# Detección de Objetos para Conducción Autónoma

Proyecto de Computer Vision centrado en el entrenamiento, ajuste y evaluación de un modelo **YOLOv8n** para detección de objetos en escenarios de conducción autónoma. El trabajo cubre desde el análisis exploratorio del dataset y la preparación de anotaciones hasta el entrenamiento de varios modelos, su comparación cuantitativa, tracking y análisis de errores.

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)](https://docs.ultralytics.com/models/yolov8/#overview)
[![OpenCV](https://img.shields.io/badge/YOLOv8-Object%20Detection-red.svg)](https://opencv.org/)

<br>

## Descripción del proyecto

El objetivo del proyecto es construir un sistema de detección de objetos orientado a conducción autónoma capaz de identificar clases relevantes del tráfico como `car`, `truck`, `bus`, `human`, `motorcycle`, `bicycle` y `trafficcone`. Para ello se parte de un dataset anotado en formato COCO, se realiza un análisis detallado de su calidad, se enriquece con metadatos de visibilidad y posteriormente se convierte a formato YOLO para entrenar distintos modelos.

Además del entrenamiento, el proyecto incluye una fase de **fine-tuning**, evaluación comparativa entre configuraciones, integración de tracking y clustering de errores para entender mejor las limitaciones del sistema y proponer mejoras futuras.

<br>

## Objetivos

| Paso | Tarea | Comentarios |
|------|-------|-------------|
| 1 | Seleccionar el modelo base | Se elige YOLOv8n por su equilibrio entre velocidad, estabilidad y precisión para escenarios en tiempo real. |
| 2 | Analizar el dataset | Se estudian clases, resoluciones, aspect ratio, tamaños de objetos, correlación RGB y calidad del etiquetado. |
| 3 | Enriquecer y preparar los datos | Se añade el metadato `pic_visibility`, se realiza un split estratificado multietiqueta y se convierte COCO a YOLO. |
| 4 | Entrenar varios modelos | Se entrena un modelo from scratch, otro pretrained y una versión finetuned del mejor candidato. |
| 5 | Comparar resultados | Se evalúan métricas como precisión, recall, mAP50 y mAP50-95 por modelo y por clase. |
| 6 | Extender el sistema | Se añaden tracking y clustering de errores para análisis avanzado del comportamiento del modelo. |
| 7 | Visualización de detecciones | Se aplica el modelo de detección sobre un vídeo captado por la cámara de un coche, utilizando el tracking por defecto de Ultralytics y un tracking customizado |

<br>

## Tecnologías principales empleadas

- Python
- YOLOv8 / Ultralytics
- Jupyter Notebook
- OpenCV
- Pandas y NumPy
- scikit-learn
- iterative-stratification
- Albumentations
- FilterPy
- UMAP
- HDBSCAN

<br>

## Dataset

El dataset contiene **52.851 imágenes** procesadas en formato COCO, de las cuales **46.243** están etiquetadas y **6.608** actúan como background. Las 7 clases incluidas son: `bicycle`, `bus`, `car`, `human`, `motorcycle`, `trafficcone` y `truck`.

El preprocesado de estos datos pasa por varias fases clave:

- Visualización manual y análisis exploratorio (EDA) del dataset.
- Estudio analítico de resoluciones, aspect ratio y distribución de tamaños de los objetos.
- Análisis de correlación entre canales RGB para valorar la consistencia cromática del conjunto de imágenes.
- Clasificación de visibilidad (`day`, `night`, `shadow`) a partir de brillo en escala de grises y canal Value en HSV.
- Split estratificado multietiqueta teniendo en cuenta las 7 clases y el metadato `pic_visibility` de visibilidad.
- Por último, conversión de anotaciones desde formato COCO a formato YOLO para proceder con el entrenamiento.

Durante el EDA se detectan varios problemas de calidad en las anotaciones, como etiquetas erróneas, reflejos etiquetados como objetos reales, confusiones entre clases similares y dificultades en condiciones nocturnas o meteorológicas adversas.

<br>

## Entrenamiento

Se entrenan tres configuraciones principales:

### 1. Modelo desde cero (from scratch)

Entrenado desde cero usando `yolov8n.yaml`, con especial atención a hiperparámetros como `imgsz=960`, `optimizer=AdamW`, `batch=8`, fuertes ajustes de data augmentation y una configuración orientada a mejorar robustez ante objetos pequeños, oclusiones y condiciones variables de iluminación.

### 2. Modelo preentrenado (pretrained)

Entrenado a partir de `yolov8n.pt`, congelando parte del backbone y utilizando una tasa de aprendizaje más baja para adaptar con cuidado los pesos preentrenados al dominio específico del tráfico.

### 3. Modelo finetuned

Partiendo del modelo pretrained, se realiza un ajuste fino con cambios en `batch`, `dropout`, `conf`, `iou`, `weight_decay`, `box`, `cls`, y reduciendo `mosaic` y `mixup`. También se incorporan transformaciones de **Albumentations** para reforzar la detección en escenas complejas y visibilidad reducida.

<br>

## Resultados

El mejor rendimiento se obtiene con el modelo **finetuned**, que alcanza en validación global:

| Modelo | mAP50-95 | Precisión | Recall |
|--------|----------|-----------|--------|
| From scratch | 0.167 | 0.500 | 0.327 |
| Pretrained | 0.388 | 0.764 | 0.546 |
| Finetuned | **0.402** | **0.775** | **0.566** |

Estas métricas muestran una mejora clara respecto al entrenamiento desde cero, y una ganancia moderada pero consistente del fine-tuning frente al modelo pretrained base.

<br>

## Métricas por clase

El modelo finetuned obtiene sus mejores resultados en clases como `car`, `motorcycle`, `bicycle` y `truck`, mientras que `human` y `bus` siguen siendo categorías más exigentes. En validación, por ejemplo, la clase `car` alcanza un **mAP50-95 de 0.496**, mientras que `human` se queda en **0.322**.

Esto sugiere que el sistema todavía tiene margen de mejora en detección de peatones y en escenarios urbanos complejos, especialmente cuando hay oclusiones, cruces entre objetos o baja iluminación.

<br>

## Tracking y análisis de errores

Además de la detección, el proyecto incorpora tracking de objetos tanto con el algoritmo por defecto de Ultralytics como con un algoritmo customizado, apoyándose en filtros de Kalman y ajustes específicos sobre la configuración del tracker para mejorar la persistencia temporal en escenas de tráfico.

<iframe width="560" height="315" src="https://www.youtube.com/embed/RBj91L7Pr08?si=y4eC9sHi1OPpKGG2" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<br>


## Conclusiones

El proyecto demuestra que partir de pesos preentrenados y realizar un fine-tuning específico sobre el dominio mejora de forma sustancial el rendimiento respecto a entrenar desde cero. También evidencia que el análisis del dataset, la estratificación adecuada y el estudio de errores son tan importantes como la propia arquitectura del modelo.

Tanto es así, que como un punto adicional se aplica clustering sobre **imágenes con errores** utilizando extracción de características, normalización, reducción dimensional con **UMAP** y agrupación con **HDBSCAN**. Esto permite identificar patrones de fallo asociados a escenas nocturnas, alta complejidad urbana o condiciones visuales extremas. Este análisis es imprescindible para considerar el ajuste de los parámetros de entrenamiento o incluso la incorporación de nuevos datasets.

En conjunto, el sistema desarrollado ofrece una base sólida para aplicaciones de percepción en conducción autónoma y deja abiertas líneas de mejora como la incorporación de nuevos datasets, refuerzo de clases difíciles y optimización del tracking en escenarios más complejos.
