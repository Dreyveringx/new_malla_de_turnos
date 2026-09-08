# Plan de trabajo — Aprendiz · Módulo Malla de Turnos

| Campo | Valor |
| ----- | ----- |
| **Rol** | Aprendiz de apoyo al módulo (aún no diseña ni estima) |
| **Tutor** | Jair Uribe |
| **Duración inicial** | 4 semanas (1 sep – 26 sep 2026) |
| **Regla de oro** | No inventa reglas de negocio, tablas ni pantallas. Documenta lo que ya está dicho o lo que ve en los Excel / GRH. Toda duda se anota; no se “resuelve” solo. |

---

## Qué **no** hace (todavía)

| No hacer | Por qué |
| -------- | ------- |
| Diseñar el modelo de base de datos | Aún no hay catálogos cerrados ni Excel inventariados. Un esquema ahora se tira. |
| Redactar las 63 HU “de una” | Primero aprende el formato con **una** historia, revisada. |
| Decidir alcance con las áreas | Eso lo hace el tutor en las sesiones de negocio. |
| Revivir el prototipo de aprendices anterior | Fue disparador de conversación, no diseño aprobado. |
| Inventar rotación automática | Es configuración de frente; no un algoritmo a inventar. |

---

## Qué **sí** hace (y sí sirve)

Tres frentes, en este orden:

1. **Entender** el problema (lectura + glosario + mapa de GRH).
2. **Inventariar** los Excel cuando lleguen (el insumo que más desbloquea diseño).
3. **Redactar** HU de catálogo, una por una, con el formato GST-FM-04, después de que la primera quede bien.

---

## Semana 1 — Entender el módulo (sin código de diseño)

**Objetivo:** que pueda explicar la malla en 5 minutos, con las palabras del negocio.

### Lectura obligatoria (en este orden)

1. `turnos.html` o `LEVANTAMIENTO-MALLA-TURNOS-FASE1.md`
2. `Propuesta-HU-Malla-Turnos.md` (solo el listado y la decisión de solución)
3. `README.md` de `gestionrrhh` (qué microservicios hay)
4. Formato `docs/GST-FM-04  FORMATO HISTORIA DE USUARIO.docx`
5. Ejemplo ya empezado: `docs/GST-FM-04-MT-EP01-HU01-Parametrizar-plantillas-turno.docx`

### Entregables de la semana

| # | Entregable | Cómo se acepta |
| - | ---------- | -------------- |
| 1 | **Glosario propio** (1 página): malla, turno, estado, celda, SPT, modalidad, sitio, publicar, corte de nómina, modo manual/asistido/automático | Lo explica en voz alta el viernes, sin leer. Si usa “Elemento” como si fuera el módulo, no pasa. |
| 2 | **Mapa de actores** (tabla): rol → qué hace hoy en Excel → qué debería poder en GRH | Contrasta con la sección 5 del levantamiento. |
| 3 | **Qué ya existe en GRH** (media página): empleados, áreas, cargos, calendario/festivos, `work_schedule`, notificaciones, roles. Una frase: *¿se reutiliza o es dominio nuevo?* | No pega código. Lista pantallas o tablas que encontró y la fuente (archivo o ruta). |
| 4 | **Lista de dudas** (máx. 15). Cada una: qué no entiende + dónde lo leyó. | No “investiga hasta inventar la respuesta”. |

**Check de viernes (30 min con el tutor):** cuenta el flujo de Contact Center y el de Sitio. Si no distingue “jornada contractual” de “malla operativa”, se repite la lectura.

---

## Semana 2 — Inventario de Excel + primera HU

**Objetivo:** pasar de “lo dijeron en la reunión” a “esto es lo que hay en las hojas”.

Cuando lleguen los Excel (CC septiembre + Sitio + Mesa):

### Entregable 5 — Inventario por archivo

Una hoja (o markdown) **por Excel**, con:

- Nombre del archivo y frente (CC / Sitio / Mesa / Lab)
- Hojas que trae
- Columnas de cada hoja (nombre exacto)
- Qué parece ser: turno, estado, persona, día, zona, campaña, horas, novedad
- Colores o letras usadas (DES, INC, T1…)
- Fórmulas que vea (aunque no las entienda: copia la celda y anota “esto calcula X”)
- Lo que **no** aparece en el levantamiento
- Lo que el levantamiento menciona y **el Excel no tiene**

Eso alimenta EP-01 (catálogos) y evita diseñar pantallas a ciegas.

### Entregable 6 — Primera historia de usuario (la única de esta semana)

Copia el formato GST-FM-04 y redacta **solo**:

`MT-EP01-HU06 — Parametrizar plantillas de turno por empresa y área`

Usando el ejemplo HU01 como plantilla. Debe incluir:

- Como [rol], quiero [acción], para [beneficio]
- Criterios de aceptación (lista numerada, comprobables)
- Qué reutiliza de GRH (empresa, área) y qué es nuevo (la plantilla de turno)
- Qué **no** cubre esta HU (horario por día = HU07; break = HU08)

**El tutor revisa antes de que escriba una segunda.** Si la primera está floja, se reescribe; no se sigue.

---

## Semana 3 — Catálogos (HU fáciles) + diccionario de datos conceptual

**Objetivo:** practicar HU en lo más simple (CRUD de parametría) y nombrar conceptos **sin** pasar a SQL.

### Entregables

| # | Qué | Notas |
| - | --- | ----- |
| 7 | HU GST-FM-04 de **HU09 estados**, **HU12 modalidades**, **HU13 sitios** (una por día, revisión diaria de 20 min) | Mismo molde que HU06. Si una se atasca, para y pregunta. |
| 8 | **Diccionario conceptual** (no es modelo ER): ficha por concepto: nombre de negocio, atributos que ya vimos, de quién es (empresa/área), ejemplo. Conceptos: Turno plantilla, Estado, Modalidad, Sitio, Frente, Malla, Celda, Historial de celda. | Prohibido: tipos SQL, PK/FK, nombres de tabla. Eso lo hace el tutor después. |
| 9 | Matriz **frente × campos de celda**: CC / Sitio / Mesa / Lab vs turno, estado, zona, modalidad, sitio, campaña, nota. Marca obligatorio / opcional / no aplica. | Sale del levantamiento + Excel. Donde falte info: “pendiente”, no adivinar. |

---

## Semana 4 — Apoyo a mockups y sesión de validación

**Objetivo:** que llegue a la sesión del 7–11 sep (o la siguiente) sabiendo contrastar diseño vs levantamiento.

| # | Qué |
| - | --- |
| 10 | Lista de chequeo Figma vs HU: “esta pantalla cubre HU06, esta no cubre HU26”. Usa `PROMPT-FIGMA-MALLA-TURNOS.md` y el prototipo cuando exista. |
| 11 | Preparar 5 preguntas concretas para las áreas (las que siguen abiertas: catálogo de turnos 1–12 y 1–9, letras de estado, bloquear vs advertir). |
| 12 | Minuta de la sesión: decisiones, pendientes, quién debe enviar qué. |

A partir de aquí, si las HU de catálogo salen bien, el tutor le suelta EP-01 completo (HU06–HU20), nunca EP-03 (rotación) ni el esquema de BD.

---

## Ritmo con el tutor

| Cuándo | Para qué |
| ------ | -------- |
| Lunes 20 min | Objetivo de la semana, desbloquear dudas |
| Diario 10 min (chat o stand-up) | “¿Estoy inventando o documentando?” |
| Viernes 30 min | Revisión de entregables. Pasa / se rehace |

El aprendiz **no espera a viernes** si se traba más de una hora. Pregunta.

---

## Cómo aprende a hacer HU (método)

1. Lee **una** HU buena (HU01 del repo).
2. Reescribe HU06 en el mismo formato, con datos del levantamiento.
3. El tutor marca: criterio vago, criterio inventado, criterio que es otra HU.
4. Recién ahí copia el molde a la siguiente.

Criterio de aceptación bueno: *“Al guardar un turno sin hora de inicio, el sistema no persiste y muestra error en el campo.”*  
Criterio malo: *“El sistema debe ser amigable e intuitivo.”*

---

## Cómo se acerca a la BD (más adelante, no ahora)

Cuando existan: Excel inventariado + 4 HU de catálogo aceptadas + diccionario conceptual revisado, el tutor arma **con él** (no él solo) un primer modelo:

Empresa → Frente → Turno plantilla → Malla → Celda.

Hasta ese día, si pregunta “¿qué tablas van?”, la respuesta es: **ninguna todavía**.

---

## Mensaje corto para pegarle al aprendiz (kickoff)

> Vas a apoyar el módulo nuevo de Malla de turnos. Las primeras 4 semanas no diseñas base de datos ni escribes el backlog completo. Vas a: (1) entender cómo programan turnos hoy, (2) inventariar los Excel que nos envíen las áreas, (3) aprender el formato GST-FM-04 redactando una historia de parametrizar turnos, y (4) armar un diccionario de conceptos de negocio. Todo lo que no esté en el levantamiento o en el Excel se anota como duda; no se inventa. El viernes me lo explicas en voz alta.
