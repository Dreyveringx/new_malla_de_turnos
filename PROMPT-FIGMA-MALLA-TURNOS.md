# Prompt Figma Make — Módulo Malla de Turnos (GRH)

Copia desde la línea `PROTOTIPO…` hasta el final y pégalo en Figma Make.

---

```text
PROTOTIPO NUEVO. Módulo “Malla de Turnos” dentro de la plataforma GRH (Gestión RRHH) ya existente.
NO es un producto standalone. NO es un Excel. NO es un rediseño de GRH.
Es un módulo NUEVO que vive DENTRO del shell actual de GRH, con el mismo lenguaje visual.

Idioma: español Colombia. Desktop 1440×900. Tipografía: Roboto.
WCAG 2.2 AA. Labels permanentes (nunca placeholder como único label). 1 CTA primario por pantalla.
Cada color de turno/estado SIEMPRE lleva código o texto; nunca semántica solo por color.

════════════════════════════════════════
DESIGN SYSTEM = GRH ACTUAL (obligatorio)
════════════════════════════════════════
NO uses la paleta del prototipo de Candidatos (#1B4F8A / #F6F7F9).
USA esta paleta, que es la de producción GRH:

- Primario / títulos / botones primarios: #4A628A
- Primario hover: #415880
- Secundario / acento / bordes activos / switch: #78D1D7
- Primario suave: mix 35% #4A628A + 65% blanco
- Fondo app: #F4F7FB
- Superficie card / tabla / sidebar: #FFFFFF
- Texto fuerte: #484848
- Texto cuerpo: #686868
- Texto muted: #A4A4A4
- Bordes: #E9EEF3 / #D4D4D4
- Filas tabla borde: #D7E2EE
- Éxito / activo: #28A745 y #68BC87
- Error / peligro: #DA1F31
- Advertencia: #DB3910
- Fondo filtros suave: #EFF6FF
- Blanco botones secundarios: #FFFFFF con borde #D4D4D4 y texto #484848

Componentes (imitar PrimeNG de GRH, no Material, no Tailwind “saas genérico”):
- Sidebar izquierda blanca, colapsada 60 px / expandida 194 px, logo arriba, ítems con icono + texto.
- Header de página: título H1 color #4A628A, acciones a la derecha (botón primario 36 px alto, radius 4 px, texto blanco).
- Cards blancas radius 10 px, sombra suave.
- Tablas: thead 13 px #686868, celdas 12 px, padding 12×16, sin zebra fuerte.
- Dialogs modales ~900 px, header con título y línea decorativa #78D7D7 bajo el título.
- Inputs con label arriba, radius 8 px, focus ring mix del primario.
- Tabs, Select, DatePicker, Toast, chips/tags, paginator.
- Botón secundario: blanco, borde gris, radius 8 px.
- Botón icono de tabla: lápiz / ojo / basura en color primario.

SHELL GRH (todas las pantallas lo llevan):
- Sidebar con ítems existentes (Mi organización, Funcionarios, etc.) + ítem activo “Malla de turnos”.
- Top bar mínima: campana de notificaciones (la de GRH), avatar, nombre de empresa.
- Breadcrumb: GRH / Malla de turnos / [pantalla].
- Contenido sobre fondo #F4F7FB.

════════════════════════════════════════
REGLAS QUE NO SE NEGOCIAN
════════════════════════════════════════
1. Multi-tenant: toda pantalla muestra la empresa activa. Los catálogos son por empresa y, cuando aplique, por área/frente. NUNCA un catálogo único global.
2. El módulo NO crea empleados. El selector de personas busca funcionarios ya existentes en GRH.
3. Jornada contractual (horario laboral GRH) ≠ malla operativa. No mezcles esas pantallas. Este módulo es programación de turnos.
4. “Elemento” NO es una pantalla ni un concepto rígido. Es UN sitio del catálogo de sitios de asistencia. Debe poder haber otros (Sede Norte, SPT Restrepo, Laboratorio…).
5. Modalidad del día es catálogo: Presencial, Virtual, Híbrido + las que parametrice el admin. Si la modalidad requiere sitio, el campo Sitio se habilita.
6. Rotación HÍBRIDA. Cada frente configura un modo:
   - Manual: el coordinador asigna celda a celda.
   - Asistido: el sistema muestra contadores, equilibrio y advertencias; NO asigna solo.
   - Automático: el sistema aplica el patrón; el humano SIEMPRE puede ajustar a mano.
   El modo se ve en la config del frente y en un badge en la grilla (“Modo: automático”).
7. Publicar NO versiona la malla completa. El cambio posterior es puntual, con historial (antes / después / quién / cuándo / motivo).
8. El empleado NO acepta el turno. La notificación es informativa (campana + correo).
9. El módulo entrega HORAS a nómina, no pesos. No diseñes liquidación ni “valor a pagar”.
10. Permisos por rol (muéstralos en cada pantalla con estados disabled + tooltip “Sin permiso”):
    - Supervisora CC: crea/edita borrador, novedad puntual.
    - Coordinador: revisar, publicar, conflictos, reportes, rotación.
    - Analista de mesa: SOLO lectura de consulta en vivo.
    - Operador/técnico: malla del grupo + su programación.
    - TH/Nómina: exportar horas, no opera la grilla.
11. Flujo de malla: Borrador → En revisión → Publicada. Rechazo vuelve a Borrador. En frentes con “publicada editable”, la grilla publicada sigue permitiendo cambio de celda.
12. Nav del prototipo: bloques A–E + S00. Cada pantalla tiene ID visible en un sticker discreto (S00, S01…). Conecta los flujos (click de lista → detalle → modal → toast → vuelve).

════════════════════════════════════════
DATOS DE DEMO (usa estos, no lorem)
════════════════════════════════════════
Empresa: Data Center S.A.
Frentes: Contact Center · Soporte en sitio · Mesa de servicio · Laboratorio
Personas CC: Laura Méndez, Camilo Restrepo, Diana López, Andrés Peña, Natalia Cruz
Personas Sitio: Jennifer Ruiz (zona Norte), Héctor Molina (SPT Restrepo), Luis Suárez
Turnos CC ejemplo: T1 06:00–14:00, T5 14:00–22:00, T8 07:00–15:30 (lun–jue) / 07:00–16:00 (vie)
Estados: DES, INC, VAC, PER, CAP, ACT, COM
Campañas: Data Service, Pagos de gobierno, Canguro
Sitios: Elemento, Sede Calle 26, SPT Restrepo, Laboratorio Bogotá
Modalidades: Presencial, Virtual, Híbrido
Periodo demo: septiembre 2026 (malla mensual CC) y semana 31 ago–6 sep 2026 (sitio)

════════════════════════════════════════
S00 — Hub del módulo
════════════════════════════════════════
Pantalla de entrada “Malla de turnos”. 5 bloques grandes (como el hub de Candidatos), cada uno entra a su sección:

A  Parametrización     catálogos del módulo (turnos, estados, modalidades, sitios, reglas, frente)
B  Construcción        mallas, grilla, rotación, publicación
C  Consulta operativa  quién está ahora / cobertura del día
D  Mi programación     vista del empleado
E  Reportes            horas, Excel, cobertura para terceros

Bajo los bloques: leyenda de estados de malla (Borrador / En revisión / Publicada) y una línea “La rotación es híbrida: cada frente elige manual, asistido o automático”.
Muestra 3 chips de mallas recientes (CC septiembre Publicada · Sitio semana En revisión · Lab sábado Borrador).

════════════════════════════════════════
A — PARAMETRIZACIÓN (S01–S12)
════════════════════════════════════════
Patrón de todas las pantallas A: header título + botón “Nuevo …”, card de filtros (buscar + estado activo/inactivo + área), tabla PrimeNG, acciones ver/editar. Click Nueva o Editar abre modal 900 px. Empty state si el catálogo está vacío: “Crea el primer … para poder armar mallas”.

S01 Plantillas de turno
Lista por área. Columnas: código, nombre, horario, días de aplicación, color (chip + código), nocturno sí/no, activo. Modal: código, nombre, tipo (mañana/tarde/noche/transversal), hora inicio/fin, cruza medianoche, color, área, empresa (readonly), activo. Link “Horario por día, break y almuerzo” → S02.

S02 Detalle de un turno
Tabs: Horario por día | Break y almuerzo.
Horario por día: tabla lun–dom con hora inicio/fin distintas (ejemplo Turno 8: lun–jue 07:00–15:30, vie 07:00–16:00, sáb 08:00–12:00).
Break/almuerzo: inicio, fin, opcional, “no dejar franja descubierta” como nota de regla.
CTA Guardar.

S03 Estados de celda
Columnas: código (DES, INC…), nombre, color+texto, ¿suma horas?, ¿asignable a casos?, activo.
Modal con esos campos. Explica en helper: “Actividad (ACT) = ocupado, no recibe casos aunque no tenga turno”.

S04 Campañas / tareas
Etiquetas de celda que NO son un turno. Data Service, Canguro, etc. Color + código. Activo. Área opcional.

S05 Territorio operativo
Árbol o tabla anidada: Regional → Zona → SPT. CRUD. Helper: “Solo aplica a los frentes que lo activen. Contact Center puede no usarlo”.

S06 Modalidades de jornada
Catálogo. Presencial / Virtual / Híbrido. Campo “requiere sitio de asistencia” (sí/no). Virtual = no requiere sitio.

S07 Sitios de asistencia
Catálogo de sitios (Elemento, Sede Calle 26, SPT Restrepo…). Relación N:N con modalidades que requieren sitio. NO hay una pantalla llamada Elemento.

S08 Restricciones de persona
Tipos: Estudio (solo diurno), Salud (no sede física), otras. Asignación de restricción a un funcionario existente (buscador GRH). Vigencia. Efecto: bloquear o advertir (parametrizable).

S09 Cortes de nómina y tipos de hora
Dos tabs.
Cortes: nombre, fecha inicio, fecha fin (ej. 7–21).
Tipos de hora: ordinaria, extra, festiva diurna, festiva nocturna, recargo nocturno. Solo catálogo de tipos; no hay campo “valor $”.

S10 Compensatorios y cobertura mínima
Regla ejemplo: “3 domingos trabajados en el mes → sugerir compensatorio”. Cobertura mínima: 1 técnico por regional en domingo/festivo, N personas por franja. Tratamiento: advertir o bloquear (select).

S11 Configuración del frente (clave de la solución)
Una card por frente (CC, Sitio, Mesa, Lab) con:
- Periodo por defecto: semana | mes
- Quién arma / quién publica (mismo rol o separados)
- ¿Malla publicada sigue editable? sí/no
- Modo de armado: Manual | Asistido | Automático (radio, uno solo)
- ¿Usa territorio (zona/SPT)? sí/no
- ¿Usa campañas? sí/no
- ¿Usa modalidad y sitio? sí/no
Helper visible: “Automático aplica los patrones de S12; el coordinador puede corregir cada celda y queda en historial”.

S12 Patrones de rotación
Lista de patrones del área: “15 días mañana / 15 tarde”, “2 trabajan / 1 descansa”, “no repetir el mismo tipo semana a semana”.
Modal: nombre, secuencia de turnos, duración, excepciones (respetar restricciones S08).
Solo se “aplica” desde la grilla si el frente está en modo Automático o el usuario pulsa “Aplicar patrón” en asistido (como propuesta, no commit silencioso).

════════════════════════════════════════
B — CONSTRUCCIÓN, ROTACIÓN Y PUBLICACIÓN (S13–S20)
════════════════════════════════════════
S13 Lista de mallas
Tabla: nombre, frente, periodo, responsable, estado (chip Borrador/En revisión/Publicada), modo de armado, actualizado.
Filtros: frente, estado, periodo.
CTA “Nueva malla”. Click fila → S15. Click Nueva → S14.

S14 Crear malla (wizard 3 pasos)
1. Datos: nombre, frente (trae config S11), periodo (rango; semanal o mensual según frente), responsable = usuario en sesión (readonly).
2. Personas: multi-select de funcionarios existentes del área. No hay “crear empleado”. Muestra cargo y área.
3. Turnos aplicables: checkboxes de plantillas S01 de ese frente.
Resumen final: N personas, N turnos, fechas, horas estimadas. Alerta si hay cruce. CTA “Crear borrador” → S15.

S15 Grilla de malla (PANTALLA CORE)
Excel-like, no calendario de citas.
Filas = personas. Columnas = días del periodo. Festivos tomados del calendario GRH (columna con marca “F” + nombre del festivo).
Celda muestra: código de turno o estado, chip de color, icono de modalidad (edificio / casa / mixto), puntito si tiene zona/campaña/nota.
Toolbar:
- Filtros frente/semana/mes (ya viene de la malla)
- Leyenda de colores (código + nombre)
- Contadores vivos a la derecha: personas por franja mañana / intermedio / tarde, total del día (S16 panel)
- Badge modo: Manual | Asistido | Automático
- Botones según estado y permiso: Enviar a revisión, Publicar, Rechazar, Aplicar rotación, Exportar
Click celda → S16.
Si modo asistido o automático: toasts/banners de advertencia no bloquean salvo reglas “bloquear” (solape horario real).

S16 Panel / drawer de celda
Campos:
- Turno (select plantillas) y/o Estado (select S03). Si estado de novedad, el turno se limpia o queda tachado.
- Segundo turno (opcional) con flag “extra”.
- Modalidad (S06) → si requiere sitio, Sitio (S07).
- Zona / SPT (si el frente usa territorio).
- Campaña/tarea (si el frente las usa).
- Nota / observación (textarea).
- Motivo (obligatorio si la malla ya está publicada).
Footer: Guardar cambio. Texto: “Quedará en historial. El empleado recibe aviso informativo, no acepta”.
Link “Ver historial de esta celda” → S20.

S17 Panel de cobertura (puede ser columna derecha de S15 o pantalla split)
Contadores por franja y por turno. Equilibrio: cuántas veces cada persona tuvo cada turno en el periodo.
Lista de conflictos: solape, celda vacía, breaks pegados, cobertura bajo mínimo, 42 h no cierra, repetir turno, restricción estudio/salud.
Cada ítem dice Advertencia o Bloqueo según S10/S11.

S18 Aplicar rotación
Modal desde S15.
Si modo Manual: el botón está disabled con tooltip “Este frente está en modo manual. Cambia el modo en Configuración del frente”.
Si Asistido: “Proponer patrón” llena la grilla en preview, el usuario acepta o descarta. No guarda solo.
Si Automático: aplica patrón S12 + opciones check: rotar campañas, distribuir breaks, rotar sitios, respetar excepciones de sitio (reforzamiento), respetar restricciones.
Preview de N celdas que cambiarán. CTA “Aplicar”. Luego se puede editar a mano (S16) y el historial distingue “automático” vs “ajuste manual”.

S19 Publicación
Desde S15:
- Enviar a revisión (si el frente separa constructor/publicador).
- Publicar: confirm dialog con resumen (personas, periodo, conflictos abiertos). Si hay solo advertencias, permite publicar con checkbox “Publicar con advertencias”. Si hay bloqueos, no deja.
- Rechazar: motivo, vuelve a Borrador.
Al publicar: toast “Malla publicada. Se notificó a N funcionarios (campana + correo)”.

S20 Historial de celda
Timeline: fecha/hora, usuario, valor anterior, valor nuevo, motivo, origen (manual / automático / novedad).
Inmutable. Filtro por persona o tipo de cambio. Exportar.
Si se abre por novedad (incapacidad hoy): formulario corto “cambiar a INC + motivo + cobertura sugerida” y el registro aparece aquí. La celda deja de sumar horas (badge “No suma horas”).

════════════════════════════════════════
C — CONSULTA OPERATIVA (S21–S23)
════════════════════════════════════════
S21 Quién está ahora
Pantalla de mesa. Buscador: nombre, zona, SPT, sitio.
Resultado en tiempo real (helper: “se actualiza al guardar un cambio de celda, no espera al viernes”).
Card por persona: turno actual, horario, zona/SPT, modalidad+sitio, disponible SÍ/NO.
No disponible si DES / INC / VAC / PER / ACT.
Analista de mesa: sin botones de editar.

S22 Cobertura del día
Vista “quién hay hoy en SPT Restrepo / Elemento / Zona Norte”. Lista + conteo. Filtro fecha (default hoy). CTA Exportar (para directores SPT) → genera Excel, copy “para terceros sin acceso a la plataforma”.

S23 Actividad / no asignable
Muestra personas en estado ACT (capacitación, examen, mantenimiento). Badge “No asignable a casos”. Link a la celda origen.

════════════════════════════════════════
D — VISTA DEL EMPLEADO (S24–S26)
════════════════════════════════════════
S24 Malla del grupo
Misma grilla que S15 pero solo lectura. Pública para el grupo del frente. Sin panel de edición. Leyenda visible.

S25 Mi programación
Calendario/lista personal: día, semana, mes. Próximo turno, horario, modalidad, sitio, descansos.
Toggle semana/mes.

S26 Historial de mis turnos
Solo cambios que afectan al usuario logueado. “Te cambiaron T5 → INC el 3 sep por incapacidad. Notificación informativa”.

════════════════════════════════════════
E — REPORTES (S27–S30)
════════════════════════════════════════
S27 Horas para nómina
Filtro: corte de nómina (S09), frente, persona.
Tabla: persona, ordinarias, extra, festiva diurna, festiva nocturna, recargo nocturno. TOTALES.
NO hay columnas de pesos. CTA Exportar Excel.
Chip del corte activo (“7–21 sep 2026”).

S28 Exportar malla
Preview de la grilla a Excel y PDF. Conserva códigos y leyenda, no solo color.

S29 Incapacidad y vacaciones vs horas operativas
Dos bloques: total del periodo e individual. Impacto de capacidad (horas no cubiertas por vacaciones).

S30 Cruce vs novedades TH + compensatorios
Tabla: persona, horas malla, horas novedad TH, resultado OK / inconsistencia.
Columna compensatorio: “3 domingos trabajados → sugerido”.
Nota: “Integración bidireccional con el Excel de TH es evaluable; esta pantalla es el cruce”.

════════════════════════════════════════
ESTADOS, VACÍOS Y CONEXIONES (obligatorio)
════════════════════════════════════════
Empty states:
- S13 sin mallas: “Crea la primera malla del frente. Antes parametriza turnos en A”.
- S01 sin turnos: bloquea S14 paso 3.
- S21 sin coincidencias: “Nadie cubre ese SPT en este momento”.
- S11 frente sin modo: no se puede aplicar rotación.

Permisos: en S15 un analista ve la grilla y S21, botones de editar/publicar disabled.
Toasts: éxito verde, error #DA1F31, advertencia naranja.
Loading de grilla: skeleton de filas, no spinner a pantalla completa.

Conecta TODO:
S00 → A/B/C/D/E
S01 → S02
S11 ↔ S15 badge modo
S12 → S18 → S15
S13 → S14 → S15 → S16 → S20
S15 → S17, S18, S19, S28
S16 modalidad → filtra sitios S07
S19 publicar → toast + S24 visible para el grupo + campana
S21 lee el vigente de S15 (publicada editable)
S25/S26 leen las celdas del usuario
S27 usa cortes S09 y tipos S09 y deja de sumar si estado S03 “no suma horas”

NO diseñes:
- flujo empleado solicita cambio / intercambio
- liquidación de nómina
- dashboard de indicadores de desempeño
- onboarding de fábrica
- pantallas de login o de otros módulos GRH (solo el shell)

Al final entrega:
1) S00 con los 5 bloques navegables
2) Todas las pantallas S01–S30
3) Un flujo feliz CC mensual: parametrizar turno → crear malla septiembre → armar grilla → publicar → novedad INC el día 3 → historial + aviso
4) Un flujo Sitio semanal: modo automático 15/15 → aplicar → ajustar a mano una celda → consulta “quién está ahora en SPT Restrepo”
5) Un flujo modalidad: celda con Presencial + sitio Elemento, otra Virtual sin sitio, otra Híbrido + sede
```
