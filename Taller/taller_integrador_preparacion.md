# UNAM - ENES Juriquilla
## Licenciatura en Tecnología | Ciencia de Datos I
### Tema 1, Clase 9: Taller Integrador de Preparación de Datos con pandas

**Mensaje pedagógico central:** *Un dataset preparado es evidencia de decisiones trazables, no una tabla que simplemente ya no contiene celdas vacías o valores faltantes.*

---



### Contexto del Caso Práctico: Registro de Movilidad Estudiantil
En este taller integrador, trabajaremos con un conjunto de datos sintéticos de **movilidad estudiantil de la ENES Juriquilla**. El objetivo es consolidar y preparar un único DataFrame final (`df_preparado`) que servirá como base para los análisis probabilísticos del Tema 2.

Disponemos de cuatro fuentes de datos en formato CSV en nuestro directorio de trabajo:
1. `traslados_semana_1.csv`: Registros de traslados diarios de los estudiantes durante la semana 1.
2. `traslados_semana_2.csv`: Registros de traslados diarios de los estudiantes durante la semana 2.
3. `rutas.csv`: Catálogo de rutas de transporte público y alternativo con sus respectivas zonas asociadas.
4. `zonas.csv`: Catálogo de zonas geográficas de Querétaro.

---



### Diccionario de Datos Oficial

#### 1. Archivos de Traslados (`traslados_semana_1.csv` y `traslados_semana_2.csv`)
Cada fila representa una **observación individual de viaje** de un estudiante.
*   `id_registro`: Identificador único del registro de traslado.
*   `fecha`: Fecha del traslado en formato YYYY-MM-DD.
*   `id_ruta`: Código de la ruta utilizada (llave de relación hacia el catálogo de rutas).
*   `duracion_min`: Duración del viaje en minutos (puede contener ausencias por fallas del GPS móvil).
*   `costo_mxn`: Gasto reportado en pesos por el viaje. Contiene el caracter `"-"` si el alumno no reportó gasto.
*   `medio`: Medio de transporte utilizado. Contiene el centinela `"ND"` si no fue registrado al capturar el formulario.

#### 2. Catálogo de Rutas (`rutas.csv`)
Cada fila representa una **entidad única de ruta de transporte**.
*   `id_ruta`: Identificador único de la ruta.
*   `nombre_ruta`: Nombre común o comercial de la ruta de transporte.
*   `id_zona`: Identificador de la zona geográfica principal donde opera (llave hacia el catálogo de zonas).

#### 3. Catálogo de Zonas (`zonas.csv`)
Cada fila representa una **entidad única de zona de referencia geográfica**.
*   `id_zona`: Identificador único de la zona.
*   `nombre_zona`: Nombre descriptivo de la zona geográfica de la ciudad.



---
## Fase 1: Importación de Librerías e Ingesta Trazable

**Instrucciones:** 
1. Importa `pandas` y `numpy`.
2. Realiza la lectura de los 4 archivos de forma trazable. Es decir, utiliza los parámetros adecuados de `pd.read_csv()` para declarar explícitamente los marcadores de ausencia según el diccionario (`na_values`) y realizar la interpretación de fechas en las columnas correspondientes (`parse_dates`).
3. No modifiques los archivos CSV originales bajo ninguna circunstancia.



```python
import pandas as pd
import numpy as np

# Completa las rutas correspondientes a los archivos en tu espacio de trabajo
semana1_path = "traslados_semana_1.csv"
semana2_path = "traslados_semana_2.csv"
rutas_path = "rutas.csv"
zonas_path = "zonas.csv"

# 1. Ingesta trazable (declara na_values para 'ND' y '-' según corresponda)
df_sem1 = pd.read_csv(semana1_path, na_values=["ND", "-"], parse_dates=["fecha"])
df_sem2 = pd.read_csv(semana2_path, na_values=["ND", "-"], parse_dates=["fecha"])
df_rutas_raw = pd.read_csv(rutas_path)
df_zonas = pd.read_csv(zonas_path)

print("Carga de datos completada exitosamente.")
```



---
## Fase 2: Auditoría Estructural Inicial de las Fuentes

Antes de modificar cualquier celda, es una **regla de oro** realizar un diagnóstico de calidad e integridad de cada DataFrame original.

**Instrucciones:**
Para cada DataFrame cargado (`df_sem1`, `df_sem2`, `df_rutas_raw`, `df_zonas`), genera una rutina de inspección que responda las siguientes preguntas en celdas de código de forma ordenada:
1. ¿Cuáles son las dimensiones físicas del DataFrame (`shape`)?
2. ¿Qué tipos de datos infirió pandas para cada columna (`dtypes`)?
3. ¿Cuántos valores faltantes (`isna().sum()`) existen en cada columna?
4. ¿Existen duplicados en las llaves primarias candidatas (`id_ruta` en `rutas.csv`, `id_zona` en `zonas.csv`)?



```python
# === Código del Estudiante: Auditoría Semana 1 ===
print("--- SEMANA 1 ---")
print("Dimensiones:", df_sem1.shape)
print("Tipos de datos:\n", df_sem1.dtypes)
print("Valores faltantes por columna:\n", df_sem1.isna().sum())

```



```python
# === Código del Estudiante: Auditoría Semana 2 ===
print("--- SEMANA 2 ---")
print("Dimensiones:", df_sem2.shape)
print("Valores faltantes:\n", df_sem2.isna().sum())

```



```python
# === Código del Estudiante: Auditoría de Catálogos (Rutas y Zonas) ===
print("--- CATÁLOGO DE RUTAS ---")
print("Rutas shape:", df_rutas_raw.shape)
print("¿id_ruta duplicados en rutas?:", df_rutas_raw["id_ruta"].duplicated().any())

print("\n--- CATÁLOGO DE ZONAS ---")
print("Zonas shape:", df_zonas.shape)
print("¿id_zona duplicados en zonas?:", df_zonas["id_zona"].duplicated().any())
```



### Pregunta de reflexión del estudiante:
¿Qué anomalía crítica detectaste en el catálogo de rutas (`df_rutas_raw`) al ejecutar la validación de duplicidad? ¿Qué consecuencias graves traería si unimos esta tabla a ciegas con el DataFrame de traslados mediante `pd.merge()`?



*Escribe tu respuesta aquí:*



---
## Fase 3: Limpieza y Curación de Datos

**Instrucciones:**
1. **Preserva la evidencia original:** Trabaja siempre sobre copias explícitas de tus DataFrames (`.copy()`), manteniendo los originales intactos.
2. **Tratamiento del Catálogo de Rutas:** Corrige el problema de duplicación de llaves detectado en la Fase 2 en tu DataFrame de rutas. Justifica tu decisión (¿cuál fila eliminar? ¿`drop_duplicates`?).
3. **Tipos de Datos:** Asegúrate de corregir los tipos de datos si fuera necesario (por ejemplo, si `costo_mxn` se infirió como texto debido a los caracteres `"-"`, conviértelo formalmente a tipo numérico flotante después de haber mapeado la ausencia).



```python
# === Código del Estudiante: Curación de Datos ===

# 1. Curación del catálogo de rutas (mantener solo el registro válido único)
df_rutas = df_rutas_raw.drop_duplicates(subset=["id_ruta"], keep="first").copy()

# 2. Conversión formal de tipos de datos en los traslados de semanas
df_sem1_clean = df_sem1.copy()
df_sem2_clean = df_sem2.copy()

df_sem1_clean["costo_mxn"] = df_sem1_clean["costo_mxn"].astype(float)
df_sem2_clean["costo_mxn"] = df_sem2_clean["costo_mxn"].astype(float)

print("Tipos de datos convertidos correctamente:")
print("Semana 1 costo_mxn dtype:", df_sem1_clean["costo_mxn"].dtype)
print("¿Duplicados en df_rutas final?:", df_rutas["id_ruta"].duplicated().any())
```



---
## Fase 4: Integración Temporal (pd.concat)

**Instrucciones:**
Queremos apilar verticalmente los registros de la `Semana 1` y la `Semana 2`. 
1. Utiliza `pd.concat()` justificando el uso de `axis=0`.
2. Emplea el parámetro `keys=["semana_1", "semana_2"]` para construir un MultiIndex que preserve explícitamente el bloque de procedencia de cada registro para futuras auditorías de integridad.
3. Restablece el índice usando `.reset_index()` para que el origen quede guardado como una columna estructurada llamada `'origen_bloque'` y el índice final sea plano y ordenado.



```python
# === Código del Estudiante: Concatenación Temporal ===

df_traslados_all = pd.concat(
    [df_sem1_clean, df_sem2_clean],
    axis=0,
    keys=["semana_1", "semana_2"]
)

# Transformamos el MultiIndex para guardar la procedencia en una columna clara
df_traslados_all = df_traslados_all.reset_index(level=0).rename(columns={"level_0": "origen_bloque"})
df_traslados_all = df_traslados_all.reset_index(drop=True)

print("Estructura unificada de traslados:")
print("Dimensiones totales:", df_traslados_all.shape)
print(df_traslados_all.head())
```



---
## Fase 5: Integración Relacional Auditada (pd.merge)

**Instrucciones:**
1. **Enriquecimiento del Traslado:** Une el DataFrame de traslados unificados (`df_traslados_all`) con el catálogo de rutas curado (`df_rutas`) mediante una unión izquierda (`how='left'`) sobre la llave `id_ruta`.
2. **Contrato de Cardinalidad:** Agrega obligatoriamente el parámetro de validación de integridad `validate='many_to_one'` (muchos traslados se dirigen a una sola ruta).
3. **Evidencia de Correspondencia:** Activa el parámetro `indicator=True` para generar la columna automática `_merge` que auditará qué registros no tuvieron coincidencia en el catálogo de referencia.
4. **Enlace Secuencial con Zonas:** Realiza un segundo `merge` con el catálogo de zonas (`df_zonas`) sobre `id_zona` con su validación `many_to_one` correspondiente.



```python
# === Código del Estudiante: Combinación Auditada ===

# 1. Primer Merge (Traslados + Rutas)
df_enriquecido = pd.merge(
    df_traslados_all,
    df_rutas,
    on="id_ruta",
    how="left",
    validate="many_to_one",
    indicator=True
)

# Auditoría rápida con la columna _merge
print("Resultado del cruce de Rutas:")
print(df_enriquecido["_merge"].value_counts())

# 2. Segundo Merge (Resultado anterior + Zonas)
# Primero eliminamos o renombramos la columna '_merge' para evitar colisiones
df_enriquecido = df_enriquecido.rename(columns={"_merge": "origen_cruce_ruta"})

df_preparado = pd.merge(
    df_enriquecido,
    df_zonas,
    on="id_zona",
    how="left",
    validate="many_to_one"
)

print("\nCruces completados exitosamente. Dimensiones finales:", df_preparado.shape)
```



### Pregunta de reflexión del estudiante:
Observa el resultado de la columna de auditoría `origen_cruce_ruta`. 
1. ¿Existe algún registro clasificado como `left_only`?
2. De acuerdo con el diccionario de datos, ¿cuál es el código de ruta de ese registro y qué representa?
3. ¿Por qué es metodológicamente incorrecto eliminar esa fila del DataFrame o imputarle un valor calculado (como promedios) a sus características de forma automática?



*Escribe tu respuesta aquí:*



---
## Fase 6: Ficha de Auditoría y Verificación del Producto Final

**Instrucciones:**
Para garantizar que tu DataFrame preparado (`df_preparado`) cumple con las pautas de calidad rigurosas de la UNAM ENES Juriquilla antes de entrar a la fase estadística, despliega en una celda:
1. Las dimensiones físicas finales (`shape`).
2. El estado limpio de tipos de datos (`dtypes`).
3. Un recuento exacto de valores nulos finales por columna (`isna().sum()`).
4. Una muestra representativa de las primeras 5 filas del DataFrame resultante (`head()`).



```python
# === Código del Estudiante: Verificación Final ===
print("=== FICHA DE AUDITORÍA FINAL DEL DATASET ===")
print("Dimensiones del dataset preparado:", df_preparado.shape)
print("\nTipos de datos del dataset final:\n", df_preparado.dtypes)
print("\nConteo final de nulos por variable:\n", df_preparado.isna().sum())

```



---
## Fase 7: Reporte Técnico de Decisiones (Entregable)

Escribe un breve reporte analítico de **200 a 300 palabras** estructurado de la siguiente forma:
1. **Procedencia y Origen:** Describe la fuente de datos declarando explícitamente que son de origen sintético institucional de la ENES Juriquilla, UNAM.
2. **Hallazgos Críticos:** Menciona el problema de duplicados en el catálogo de rutas, el identificador `R-99` sin catálogo, y los caracteres especiales mapeados.
3. **Decisiones de Curación:** Justifica qué hiciste con las ausencias (¿por qué es correcto conservar la ausencia de correspondencia del identificador `R-99` en lugar de borrarlo o imputarlo?).
4. **Límites Epistémicos:** Explica con claridad para qué tipo de preguntas sí es apto este DataFrame (análisis descriptivo y probabilidad básica) y para cuáles queda estrictamente prohibido su uso directo debido a la naturaleza sintética e incompleta de algunas columnas (ej. inferencias causales de impacto social).



*Escribe tu Reporte Técnico aquí (Doble clic para editar)*


