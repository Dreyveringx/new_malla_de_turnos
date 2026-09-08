# Prompt Figma Make — Alineación 100% al backlog HU01…HU81

Prototipo: [Módulo Malla de Turnos](https://www.figma.com/make/6JW2Cr9xieMOYNaekfFKvb)

Copia desde `ALINEACIÓN…` hasta el final y pégalo en Figma Make (mismo archivo).

---

```text
ALINEACIÓN 100% del prototipo existente “Módulo Malla de Turnos” (file 6JW2Cr9xieMOYNaekfFKvb)
al backlog definitivo GRH — HU01…HU81 (orden lógico EP-00→EP-09).

NO rediseñes el design system ni la paleta GRH (#4A628A / #78D1D7 / #F4F7FB / Roboto).
NO conviertas esto en un producto standalone: sigue siendo un MÓDULO DENTRO del shell GRH.
SÍ actualiza pantallas, menú, datos demo y flujos para que coincidan con las HU.
Idioma: español Colombia. Desktop 1440. 1 CTA primario. Labels permanentes. Color de turno/estado SIEMPRE con código+texto.

Fuente de verdad funcional (respétala; no inventes reglas de negocio):
- Épicas EP-00…EP-09, HU01…HU81 continuas
- Máxima parametrización por empresa + frente operativo (catálogo)
- Cero hardcoding de frentes, umbrales (42 h, 3 domingos), ni “Elemento” como concepto especial
- Malla operativa ≠ jornada contractual
- El módulo NO crea empleados (usa listado GRH)
- Entrega HORAS a nómina, no pesos
- Intercambio de turnos SÍ está en alcance (EP-09); por defecto OFF por frente

════════════════════════════════════════
0. PRINCIPIOS QUE EL PROTOTIPO AÚN VIOLA (corrige ya)
════════════════════════════════════════
1) Frentes NO son enum fijo CC/Sitio/Mesa/Lab. Son catálogo de la empresa (HU09).
   Demo puede mostrar 4 frentes de ejemplo, pero S11 y listados deben sentir “catálogo CRUD”, no hardcode.
2) Reglas de validación NO viven como textos fijos “42 h” / “3 domingos”.
   Son ítems del motor de reglas (HU25) con severidad info/advertencia/bloqueo y parámetros editables.
3) “Elemento” es SOLO un sitio del catálogo (HU18), no una entidad especial.
4) CAP (capacitación): asignable a casos = NO (igual que ACT). Corrige S03 y cualquier card que diga lo contrario.
5) Sitio (frente ejemplo “Soporte en sitio”): malla publicada editable = SÍ. Quién arma/publica = Coordinador de sitio (NO Supervisora CC).
6) Mesa y Laboratorio: responsables propios (coordinador de mesa / laboratorio). Nunca “Supervisora CC”.
7) Quita la pantalla S23 como HU propia de “actividad no asignable”.
   Esa capacidad = flag del estado (HU14) + filtro en consulta (HU65). Integra el badge en S21.
8) El strip de navegación NO puede truncar a 3 ítems. Todas las pantallas del grupo a 1 click (Menú “Más ▾” o submenú completo).
9) Agrega selector “Ver como” en topbar (roles de demo) con disabled+tooltip “Sin permiso”.

════════════════════════════════════════
1. MAPA DE PANTALLAS ↔ HU (obligatorio)
════════════════════════════════════════
Mantén stickers Sxx. Reorganiza / agrega / renombra así:

SHELL / EP-00 (contexto, no pantallas de negocio largas)
- Empresa activa en topbar (HU04)
- Ítem menú “Malla de turnos” (HU01)
- Permisos: botones disabled por rol (HU02)
- Alcance por frente: selectores de frente filtrados por usuario (HU03)
- Empleados solo vía buscador GRH (HU05/HU08)
- No mezclar con “jornada / horario laboral” (HU06)
- Campana usa event types de malla (HU07) — solo UX de notificación

A — PARAMETRIZACIÓN (EP-01)
S00 Hub (igual estructura A–E)
S01 Frentes operativos (NUEVA — HU09)  ← antes no existía; era hardcode
S02 Configuración del frente (ex-S11 — HU10): capacidades, estrategia de armado, publicación, flags de atributo, intercambio on/off
S03 Plantillas de turno (ex-S01 — HU11)
S04 Horario por día + break/almuerzo (ex-S02 — HU12/HU13)
S05 Estados de celda + flags (ex-S03 — HU14)  [suma horas, asignable a casos, etc.]
S06 Campañas/tareas (ex-S04 — HU15)
S07 Territorio niveles configurables (ex-S05 — HU16)  ← niveles NO fijos Regional/Zona/SPT; demo puede usar 3 niveles
S08 Modalidades (ex-S06 — HU17) + flag requiere sitio
S09 Sitios de asistencia (ex-S07 — HU18)
S10 Restricciones de persona (ex-S08 — HU19) — tipos de catálogo, no solo estudio/salud
S11 Festivos (solo lectura calendario empresa — HU20) + Cortes de nómina (HU21) + Tipos de hora (HU22)
S12 Reglas de cobertura (HU24) + Compensatorio (HU23) — umbrales PARAMETRIZABLES (quitar “3 domingos” fijo)
S13 Motor de reglas de validación (NUEVA — HU25): listado de reglas con código, alcance (empresa/frente), parámetros, prioridad, severidad (info/advertencia/bloqueo), activo
S14 Flags de atributos de celda del frente (puede ser sección de S02 — HU26)
S15 Importación asistida desde Excel (NUEVA — HU27): wizard descubrimiento → sugiere catálogos

B — CONSTRUCCIÓN (EP-02) + VALIDACIÓN/ROTACIÓN (EP-03) + PUBLICACIÓN (EP-04)
S16 Lista de mallas (ex-S13 — HU28)
S17 Crear malla wizard (ex-S14 — HU28/HU29)
S18 Grilla operativa CORE (ex-S15 — HU30…HU40):
    - asignar turno/estado, segundo turno, territorio, modalidad/sitio, nota, campaña
    - filtros/búsqueda (HU38)
    - badge modo Manual/Asistido/Automático
    - indicador de concurrencia / conflicto de edición (HU39) — toast “otro usuario modificó esta celda”
    - carga parcial: selector de ventana temporal + paginación de personas (HU40)
    - acciones: Copiar semana / asignación masiva (HU41), Fijar atributo por periodo (HU42)
S19 Drawer de celda (ex-S16)
S20 Panel cobertura/contadores + equilibrio + conflictos desde motor HU25 (ex-S17 — HU43/HU44/HU45)
    Conflictos leen reglas del motor; NO hardcodear 42 h
S21 Patrones de rotación genéricos (ex-S12 — HU46): secuencia + duraciones (NO enums 15/15 como único tipo)
S22 Vincular patrón / Simular (dry-run) / Exclusiones / Aplicar (HU47–HU50)
S23 Construcción asistida + breaks + rotar sitios + reequilibrio + restricciones + ajuste manual (HU51–HU56)
    Puede ser modal(es) desde S18; no hace falta 6 pantallas si están conectadas
S24 Publicación: Borrador → En revisión → Publicada / Rechazada (HU57–HU59)
    Separación constructor/publicador según S02

C — NOVEDADES / HISTORIAL (EP-05) + CONSULTA (EP-06)
S25 Novedad en celda = aplicar estado del catálogo + motivo (HU60/HU61). Badge “no suma horas” según flag
S26 Historial inmutable de celda (ex-S20 — HU62) + notificación informativa sin aceptación (HU63)
S27 Historial por funcionario (HU64)
S28 Quién está / disponible (ex-S21 — HU65) — incluye filtro “no asignable a casos” (flag estado)
S29 Cobertura del día por dimensiones habilitadas del frente (ex-S22 — HU66)

D — EMPLEADO (EP-07)
S30 Programación del grupo (solo lectura según política) (HU67)
S31 Mi programación día/semana/mes (HU68)
S32 Historial de mis turnos/cambios (HU69)

E — REPORTES (EP-08)
S33 Horas del periodo por tipos (HU70) — sin pesos
S34 Export Excel/PDF (HU71)
S35 Horas novedad vs operativas (HU72)
S36 Export cobertura terceros (HU73)
S37 Plantilla import novedades TH (HU74) + Cruce malla vs TH (HU75) + Compensatorio en reporte (HU76) con umbrales de S12

F — INTERCAMBIO (EP-09) — NUEVO BLOQUE (antes estaba prohibido; ahora SÍ)
S38 Configurar intercambio del frente (HU77) — switch default OFF
S39 Solicitar intercambio (HU78)
S40 Validación con motor de reglas (HU79)
S41 Aprobar/rechazar (HU80)
S42 Aplicar, auditar, notificar (HU81)
Si el frente tiene intercambio OFF: ocultar S39–S42 o disabled con tooltip “Intercambio deshabilitado en este frente”.

Si necesitas compactar numeración Sxx por espacio, mantén los IDs anteriores donde existan y agrega las NUEVAS con sticker claro (S01 Frentes, S13 Motor reglas, S15 Import Excel, S38–S42 Intercambio). Lo importante es cobertura funcional HU, no el número S exacto.

════════════════════════════════════════
2. DATOS DEMO (corrige data.ts / equivalentes)
════════════════════════════════════════
Empresa: Data Center S.A.

Frentes (catálogo demo, no enum de producto):
- Contact Center: periodo mes; modo asistido; publicada editable SÍ; arma Supervisora CC; publica Coordinador CC; campañas SÍ; territorio NO; modalidad/sitio SÍ; intercambio OFF
- Soporte en sitio: periodo semana; modo automático; publicada editable SÍ; arma y publica Coordinador de sitio; territorio SÍ; campañas NO; modalidad/sitio SÍ; intercambio OFF
- Mesa de servicio: modo manual; publicada editable SÍ; arma/publica Coordinador de mesa; intercambio OFF
- Laboratorio: modo manual; arma/publica Coordinador de laboratorio

Estados: DES, INC, VAC, PER, CAP, ACT, COM
- CAP y ACT: asignable=false
- INC/VAC/PER/DES/COM: sumaHoras=false (según flags)

Reglas motor (ejemplos editables, NO constantes de UI):
- MAX_HORAS_PERIODO (parámetro N, severidad advertencia/bloqueo según config)
- MIN_COBERTURA_FRANJA
- NO_SOLAPE (bloqueo invariante)
- COMPENSATORIO_DIAS_TIPO (parámetro N días tipo domingo — editable)

Sitios demo: Elemento, Sede Calle 26, SPT Restrepo, Laboratorio Bogotá (todos iguales en jerarquía de catálogo).

════════════════════════════════════════
3. NAVEGACIÓN Y PERMISOS
════════════════════════════════════════
- Hub S00: 6 bloques A–F (agrega F Intercambio) O 5 bloques + Intercambio dentro de Construcción/Empleado según config.
  Preferido: bloque F visible solo si algún frente tiene intercambio ON; si todos OFF, mostrar el bloque en Parametrización/Config frente como “próximamente habilitado”.
- Menú interno: sin truncar a 3. “Más ▾” por grupo o sidebar de módulo completo.
- Topbar “Ver como”:
  Coordinadora CC | Coordinador | Analista mesa (solo lectura consulta) | Operador (aterriza en Mi programación) | TH/Nómina (reportes)
- Tooltips reales “Sin permiso”.

════════════════════════════════════════
4. FLUJOS FELICES A DEMOSTRAR (conectar clicks)
════════════════════════════════════════
1) Parametrizar: Frente → Config frente → Turno → Estado → Motor de reglas → (opcional) Import Excel
2) CC mensual: Crear malla → Grilla → conflictos del motor → Enviar revisión → Publicar → Novedad INC → Historial + campana
3) Sitio semanal: Modo automático → Simular patrón → Excluir 1 persona → Aplicar → Ajuste manual 1 celda → Quién está en SPT Restrepo
4) Modalidad: Presencial+sitio / Virtual sin sitio / Híbrido+sede
5) Reportes: horas sin $ → export → plantilla TH → cruce
6) Intercambio (activar en un frente demo): solicitar → validar reglas → aprobar → celda actualizada + auditoría

════════════════════════════════════════
5. QUÉ NO HACER
════════════════════════════════════════
- No liquidación en pesos
- No login / otros módulos GRH (solo shell)
- No dashboard de desempeño
- No hardcodear frentes como único modelo de producto
- No dejar S23 “Actividad” como historia separada
- No decir que el empleado “acepta” el turno
- No versionar malla completa al publicar (cambio puntual + historial)

════════════════════════════════════════
6. CRITERIO DE ACEPTACIÓN DEL PROTOTIPO
════════════════════════════════════════
Al terminar, un revisor debe poder marcar:
[ ] Existe catálogo de frentes (no solo 4 fijos en código visual)
[ ] Config por frente incluye modo armado + publicada editable + capacidades + intercambio on/off
[ ] Motor de reglas visible (no solo textos 42h/3 domingos)
[ ] Grilla cubre asignación, filtros, copia/fijar, concurrencia o su UX, carga parcial
[ ] Rotación: patrón → simular → exclusiones → aplicar → ajuste manual
[ ] Publicación con rechazada
[ ] Novedad = estado + historial + notify informativa
[ ] Consulta sin pantalla huérfana de “actividad”
[ ] Reportes sin pesos + import/cruce TH
[ ] Intercambio EP-09 presente y default off
[ ] Navegación completa sin items ocultos
[ ] Roles “Ver como” con permisos disabled

Entrega: mismo prototipo actualizado, sin romper paleta GRH, con stickers Sxx y flujos clickeables.
```
