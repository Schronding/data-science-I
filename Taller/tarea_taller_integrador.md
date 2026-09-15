# UNAM — ENES Unidad Juriquilla
## Licenciatura en Tecnología | Ciencia de Datos I
### **Especificación de Tarea Extraclase: Taller Integrador de Preparación de Datos con pandas**

---

### **1. Información General de la Tarea**
*   **Asignatura:** Ciencia de Datos I (Temas Selectos de Ciencia de Datos I)
*   **Tema correspondiente:** Tema 1 — Introducción a la Ciencia de Datos y Manipulación en Python (Subtema 1.5)
*   **Ponderación:** Tarea de Entrega Extraclase (Aporta al 30% asignado a esta categoría en la Planeación Didáctica)
*   **Modalidad de trabajo:** En parejas académicas (fomenta la co-evaluación y el diseño colaborativo de código)
*   **Formato de entrega obligatorio:** Archivo de cuaderno de Jupyter resuelto (`.ipynb`) con código reproducible y respuestas redactadas en las celdas Markdown designadas.

---

### **2. Objetivos de Aprendizaje**
Al completar esta tarea, el estudiante será capaz de:
1.  **Diseñar e implementar pipelines de ingesta trazable** configurando explícitamente tipos de datos y centinelas de nulos personalizados en pandas.
2.  **Auditar la integridad estructural** de fuentes tabulares identificando anomalías críticas (duplicados de llaves candidatas y registros sin correspondencia).
3.  **Realizar integraciones complejas de datos** en ejes temporales (concatenaciones con marcas de origen) y relaciones de bases de datos (uniones validadas con cardinalidad estricta y trazadores lógicos).
4.  **Redactar un reporte técnico justificado** que analice el impacto metodológico de sus decisiones de curación y declare formalmente los límites explicativos (epistémicos) del conjunto preparado.

---

### **3. Archivos y Materiales del Proyecto**
Para realizar esta actividad, asegúrate de tener descargados y colocados en el mismo directorio de tu Jupyter Notebook los siguientes archivos (disponibles en tu entorno de trabajo):
*   **`taller_integrador_preparacion.ipynb`**: Cuaderno interactivo inicial con la estructura de celdas y espacios para el código del estudiante.
*   **`traslados_semana_1.csv`**: Registros de viajes diarios de movilidad de la semana 1.
*   **`traslados_semana_2.csv`**: Registros de viajes diarios de movilidad de la semana 2.
*   **`rutas.csv`**: Catálogo de rutas de transporte de la ENES Juriquilla.
*   **`zonas.csv`**: Catálogo de zonas geográficas de referencia de Querétaro.

---

### **4. Desglose Detallado de Fases y Requisitos del Entregable**

#### **Fase 1: Importación de Librerías e Ingesta Trazable**
*   **Requisito:** Cargar los 4 archivos CSV en DataFrames independientes.
*   **Restricción Estricta:** No debes editar manualmente los archivos CSV con Excel o editores de texto. Toda la limpieza debe ser declarativa. Debes usar los parámetros `na_values` para mapear los centinelas `"ND"` y `"-"` a nulos reales (`NaN`) y `parse_dates=["fecha"]` para interpretar temporalmente la columna cronológica.

#### **Fase 2: Auditoría Estructural Inicial**
*   **Requisito:** Implementar rutinas ordenadas que impriman en consola para cada DataFrame: sus dimensiones físicas (`shape`), tipos de variables inferidas (`dtypes`), conteo exacto de nulos (`isna().sum()`) y pruebas de unicidad en las llaves primarias (`.duplicated().any()`).
*   **Pregunta de Reflexión (Obligatoria):** Responder detalladamente en la celda designada qué anomalía crítica presenta el catálogo de rutas (`rutas.csv`) para la ruta `R-02` y qué efectos graves causaría realizar una unión relacional sin corregirla.

#### **Fase 3: Limpieza y Curación de Datos**
*   **Requisito:** 
    1.  Preservar la evidencia original realizando copias explícitas (`.copy()`) antes de cualquier modificación física.
    2.  Remover el registro duplicado erróneo del catálogo de rutas mediante `drop_duplicates(subset=["id_ruta"], keep="first")` justificando la decisión.
    3.  Asegurar que la columna de costo en los traslados es de tipo flotante (`float64`) para cálculos numéricos.

#### **Fase 4: Integración Temporal (`pd.concat`)**
*   **Requisito:** Concatenar verticalmente los DataFrames curados de traslados de la Semana 1 y 2. Debes emplear el parámetro `keys=["semana_1", "semana_2"]` para construir un MultiIndex de trazabilidad y posteriormente aplanar el DataFrame usando `.reset_index()` de modo que la columna resultante de procedencia se llame `'origen_bloque'`.

#### **Fase 5: Integración Relacional Auditada (`pd.merge`)**
*   **Requisito:** 
    1.  Cruzar el DataFrame unificado de traslados con el catálogo curado de rutas mediante una unión izquierda (`how='left'`) sobre la llave `id_ruta`.
    2.  Validar de forma obligatoria la integridad de la relación empleando el contrato `validate='many_to_one'`.
    3.  Activar el parámetro `indicator=True` para auditar la coincidencia de llaves.
    4.  Renombrar el indicador de procedencia para evitar colisiones e integrar un segundo merge (con validación de integridad) hacia el catálogo de zonas geográficas.
*   **Pregunta de Reflexión (Obligatoria):** Responder analíticamente en la celda de Markdown qué registros quedaron sin correspondencia (con etiqueta `left_only` en el indicador), a qué código de ruta pertenecen, y por qué es metodológicamente incorrecto eliminar estas observaciones de movilidad o inventarles datos (imputación automática).

#### **Fase 6: Ficha de Auditoría Final**
*   **Requisito:** Generar e imprimir un reporte de calidad final de tu DataFrame consolidado (`df_preparado`) que muestre de forma limpia sus dimensiones finales, los tipos de datos de sus columnas, el conteo exacto de nulos resultantes y una vista previa de las primeras 5 filas.

#### **Fase 7: Reporte Técnico de Decisiones (Entregable Crítico)**
*   **Requisito:** Redactar un reporte de **200 a 300 palabras** estructurado formalmente en cuatro secciones:
    1.  *Procedencia y Origen:* Declaración del origen institucional sintético de los datos (ENES Juriquilla, UNAM).
    2.  *Hallazgos Críticos:* Resumen técnico de las anomalías de calidad descubiertas durante la auditoría.
    3.  *Justificación de Decisiones:* Defensa lógica y ética de las decisiones de limpieza (tratamiento del duplicado, conservación justificada de nulos geográficos del código `R-99`).
    4.  *Límites Epistémicos:* Definición explícita de qué tipo de análisis estadísticos sí es apto de sostener este DataFrame (descriptivos y probabilidad del Tema 2) y para cuáles está prohibido su uso (inferencia de políticas públicas causales).

---

### **5. Rúbrica Detallada de Evaluación**

La calificación de esta entrega se realizará sobre una escala máxima de **100 puntos**, distribuidos de acuerdo con la siguiente matriz de rigor analítico:

| Criterio de Evaluación | Desempeño Sobresaliente (Max Puntos) | Desempeño Suficiente | Desempeño Insuficiente / No Entregado |
| :--- | :--- | :--- | :--- |
| **Fase 1: Ingesta Trazable** <br>*(10 puntos)* | **10 pts:** Importación limpia de librerías. Uso correcto de `na_values=["ND", "-"]` y `parse_dates` en la carga, logrando la interpretación directa de tipos de datos sin tocar los CSV. | **5 pts:** Carga parcial de datos, omisión de la interpretación automática de nulos o fallas al mapear la fecha. | **0 pts:** Carga incorrecta que genera fallas en la lectura de archivos o alteración manual del origen. |
| **Fase 2: Auditoría Inicial** <br>*(15 puntos)* | **15 pts:** Rutina completa de inspección para cada DataFrame. Identificación y documentación explícita de la duplicación en `R-02`. Explicación matemática clara de la explosión cartesiana. | **8 pts:** Auditorías incompletas (no revisa todos los archivos) o responde vagamente la pregunta de reflexión sobre el impacto del duplicado. | **0 pts:** Omisión de la auditoría o respuesta incoherente que demuestra falta de análisis del catálogo. |
| **Fase 3: Limpieza y Curación** <br>*(15 puntos)* | **15 pts:** Aplicación rigurosa de `.copy()`. Limpieza declarativa del duplicado en rutas con `drop_duplicates(..., keep="first")` y conversión impecable de costo a tipo `float64`. | **8 pts:** No realiza copias de seguridad de datos originales, o conserva tipos incorrectos (texto en costo) que impiden operaciones matemáticas. | **0 pts:** No remueve el duplicado o realiza una eliminación destructiva arbitraria sin justificación. |
| **Fase 4: Integración Temporal** <br>*(15 puntos)* | **15 pts:** Concatenación vertical (`axis=0`) exitosa con marcas lógicas mediante `keys=["semana_1", "semana_2"]` y aplanamiento limpio del MultiIndex para obtener la variable de procedencia. | **8 pts:** Concatenación correcta de registros pero sin mantener marcas de procedencia, dificultando la trazabilidad. | **0 pts:** Error técnico en la unión temporal (por ejemplo, unión por columnas equivocadas o falla de alineación). |
| **Fase 5: Integración Relacional** <br>*(20 puntos)* | **20 pts:** Dos uniones izquierdas consecutivas impecables utilizando el contrato de validación `validate='many_to_one'`. Uso del trazador de auditoría `indicator=True`. Respuesta metodológica sobresaliente sobre `R-99` y la censura muestral. | **10 pts:** Realiza los merges pero omite el parámetro de validación formal, o borra las filas de la ruta `R-99` sin justificación científica (incurriendo en sesgo). | **0 pts:** Código de combinación roto, merge incorrecto (por ejemplo `inner` que elimina los registros valiosos) o copia de código sin comprender. |
| **Fase 6: Ficha de Auditoría** <br>*(10 puntos)* | **10 pts:** Despliegue limpio del resumen de control de calidad mostrando que las dimensiones, tipos y conteos de nulos finales son consistentes para la estadística. | **5 pts:** Muestra incompleta o error al formatear los tipos en la impresión de la ficha. | **0 pts:** Omisión total de la ficha de verificación de calidad. |
| **Fase 7: Reporte Técnico** <br>*(15 puntos)* | **15 pts:** Reporte analítico sobresaliente de 200 a 300 palabras. Estructura formal impecable. Justificación impecable del tratamiento de nulos y declaración explícita de límites epistémicos. | **8 pts:** Reporte demasiado breve, superficial o redundante. No aborda con precisión las limitaciones o los hallazgos críticos de calidad. | **0 pts:** Omisión del reporte o copia de texto que no corresponde al análisis metodológico del equipo. |

---

### **6. Políticas de Entrega y Código de Honestidad Académica**

*   **Puntualidad en la entrega:**
    *   La entrega tardía de la tarea penalizará el puntaje final de acuerdo con los criterios establecidos en la planeación didáctica de la materia (penalización acumulativa del **20% de la calificación por cada día de retraso académico**). No se aceptarán entregas después del tercer día natural de retraso.
*   **Código de Honestidad y Rigor Académico:**
    *   Esta actividad se rige bajo el **Código de Ética de la UNAM**. 
    *   **Cero Tolerancia al Plagio:** La compartición directa de código entre parejas o el copiado de repositorios externos será sancionado de manera estricta de acuerdo con las directrices de la UNAM, anulando la calificación de los equipos implicados de forma irrevocable.
    *   La IA y los modelos de lenguaje pueden utilizarse como asistentes de aclaración de conceptos y sintaxis elemental, pero el diseño lógico del flujo, la validación de integridad relacional y la redacción analítica de las conclusiones del reporte técnico deben ser de autoría estrictamente intelectual y humana de los integrantes del equipo.
