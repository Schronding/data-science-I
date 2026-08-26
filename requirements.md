# Guía de Ejercicios Prácticos: Fundamentos de Ciencia de Datos

**Asignatura:** Temas Selectos de Ciencia de Datos I
**Módulo I:** De la pregunta a la descripción (Clases 1 a 3)

## Caso Transversal: La Cafetería Universitaria

La administración de la ENES ha recibido quejas informales sobre el servicio de la cafetería principal. Se menciona que "el servicio es lento" y que "hay mucha gente". La administración te entrega un archivo de Excel extraído del sistema de cobro para que "analices los datos y digas qué está pasando".

---

## Ejercicio 1: La trampa de la pregunta vaga (Ref. Clase 1)

La petición de la administración ("analizar qué está pasando con la lentitud") es una intención amplia, pero no guía el análisis de datos.

1. **Identifica el riesgo:** ¿Por qué empezar a calcular promedios directamente con esta instrucción es un "Anti-Patrón" en ciencia de datos?
2. **Transformación:** Utilizando la anatomía de una pregunta investigable, transforma la queja en una pregunta estructurada. Debes definir explícitamente:
   - **La decisión:** (p. ej., ¿cambiar horarios, contratar personal, rediseñar el menú?)
   - **La población:** (p. ej., ¿todos los estudiantes o solo los del turno vespertino?)
   - **El criterio de éxito / Meta:** (ej. Reducir tiempos en horas pico)
   - **La restricción / cuidado:** (ej. Sin aumentar los precios de los menús)

---

## Ejercicio 2: El significado antes que el formato (Ref. Clase 2)

El sistema de cobro exporta la siguiente tabla rectangular.

| Ticket_ID | Hora_Cobro | Codigo_Menu | Num_Articulos | Total_Pagado | Satisfaccion_App |
|-----------|------------|-------------|----------------|--------------|-------------------|
| 10452     | 13:15:02   | 3           | 2              | $ 45.50      | 4                 |
| 10453     | 13:15:40   | 1           | 1              | $ 60.00      | 2                 |
| 10454     | 13:18:10   | 3           | 4              | $ 110.00     | 5                 |

1. **Unidad de observación:** ¿Qué evento físico representa exactamente una fila en esta tabla? ¿Representa a un estudiante, a un producto o a una transacción?
2. **Clasificación semántica:** Clasifica las siguientes variables indicando si son cualitativas (Nominales/Ordinales) o cuantitativas (Discretas/Continuas) y justifica tu respuesta:
   - `Codigo_Menu` (Donde 1=Vegano, 2=Ejecutivo, 3=Rápido).
   - `Num_Articulos`
   - `Satisfaccion_App` (Estrellas del 1 al 5 dadas en la app).
3. **El error de la etiqueta:** Un analista de la administración calcula que el promedio de la columna `Ticket_ID` es 10453 y el promedio de la columna `Codigo_Menu` es 2.33. ¿Por qué estos cálculos carecen de sentido analítico, aunque Excel los permita?

---

## Ejercicio 3: El punto ciego del centro (Ref. Clase 3)

Para entender los tiempos de espera, mides manualmente en minutos a 7 estudiantes desde que se forman hasta que reciben su comida en el turno de las 14:00 hrs. Los datos obtenidos son: **4, 5, 5, 6, 7, 8, 42**.

1. **Cálculo de localización:** Calcula la media y la mediana de este conjunto de datos.
2. **Evaluación de sensibilidad:** ¿Cuál de las dos métricas representa mejor el tiempo de espera "típico" y por qué? Utiliza el concepto de robustez frente a valores atípicos.
3. **Protocolo de exclusión:** El valor de "42 minutos" resulta claramente inusual. De acuerdo con el protocolo visto en clase, menciona dos posibles hipótesis sobre qué pudo haber causado este valor antes de decidir simplemente borrarlo del registro.

---

## Ejercicio 4: Variabilidad y consistencia (Ref. Clase 3)

El administrador afirma: "Si la mediana de espera es de 6 minutos, el servicio es excelente y predecible". Sin embargo, tú sabes que el centro no cuenta toda la historia.

1. **Medición de dispersión:** Para acompañar a tu Mediana (que es una medida robusta), ¿qué métrica de variabilidad elegirías para reportar: la Desviación Estándar, el Rango o el Rango Intercuartílico (IQR)? Justifica tu decisión basándote en la trampa geométrica de los cuadrados.
2. **Traducción visual:** Si quisieras mostrar a la administración la distribución de estos tiempos continuos, indicando dónde se concentra la mayoría y dejando en evidencia el valor atípico de 42 minutos, ¿qué gráfico utilizarías: una gráfica de barras o un histograma/boxplot? Explica la diferencia fundamental entre ellos.

---

## Ejercicio 5: Los límites de la evidencia (Ref. Clases 1, 2 y 3)

Al presentar tu Resumen Responsable (con tu centro robusto, tu dispersión y tu Boxplot), el administrador decide abrir una caja de cobro adicional con base en tus datos.

Sin embargo, recuerdas que el registro no es la totalidad del fenómeno.

1. **La zona de sombras:** Nombra al menos un fenómeno o "experiencia no registrada" relacionado con la lentitud de la cafetería que no queda capturado en la tabla de transacciones de la caja (p. ej., piensa en lo que ocurre antes de llegar a la caja).
2. **Síntesis del ciclo:** Explica brevemente por qué el descubrimiento de este "punto ciego" nos obliga a realizar un retorno en el ciclo de datos (volver de la Etapa 4 a la Etapa 1 o 2).
