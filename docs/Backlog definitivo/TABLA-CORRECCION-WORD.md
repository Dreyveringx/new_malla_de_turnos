# Tabla para corrección de Word (GST-FM-04)

Fuente: backlog definitivo. Usar junto con `docs/Backlog definitivo/EP-XX-*.md`.

Estado 05/09/2026: las 81 GST activas ya están regeneradas en markdown y Word (`.docx`) desde el backlog. Esta tabla queda como historial de la ronda de corrección.

Leyenda acción Word (histórica):

| Acción | Qué hacer en Word |
| ------ | ----------------- |
| ACTUALIZAR | Abrir el .docx/.md existente y reemplazar contenido desde el backlog definitivo |
| CREAR | Crear documento nuevo (no existía) |
| ARCHIVAR | No actualizar: absorber criterios en otras HU y marcar el Word como obsoleto |
| DIVIDIR | El Word actual se parte en 2+ documentos |

---

## A. HUs nuevas (CREAR Word)

| ID final | Título corto | Épica | Alcance | Nace de |
| -------- | ------------ | ----- | --------- | ------- |
| HU09 | Frentes operativos (catálogo) | EP-01 | Incluida | Nueva |
| HU10 | Capacidades / estrategia / publicación del frente | EP-01 | Incluida | Split HU26 |
| HU25 | Motor de reglas de validación | EP-01 | Incluida | Split HU45 |
| HU46 | Patrón de rotación genérico | EP-03 | Incluida | Split HU47 |
| HU03 | Alcance de frentes a usuarios/roles | EP-00 | Incluida | Split HU02 |
| HU07 | Event types notificación + timeline | EP-00 | Incluida | Nueva |
| HU08 | Listado empleados filtrado/paginado | EP-00 | Incluida | Nueva |
| HU48 | Simular rotación (dry-run) | EP-03 | Incluida | Nueva |
| HU49 | Exclusiones de rotación | EP-03 | Incluida | Nueva |
| HU77 | Configurar intercambio | EP-09 | Incluida | Nueva |
| HU78 | Solicitar intercambio | EP-09 | Incluida | Nueva |
| HU79 | Validar solicitud intercambio | EP-09 | Incluida | Nueva |
| HU80 | Aprobar/rechazar intercambio | EP-09 | Incluida | Nueva |
| HU81 | Aplicar intercambio + auditar + notificar | EP-09 | Incluida | Nueva |
| HU39 | Concurrencia (optimistic lock) | EP-02 | Incluida | Nueva |
| HU40 | Carga parcial de grilla | EP-02 | Incluida | Nueva |
| HU61 | Ownership MVP novedades | EP-05 | Incluida | Nueva (desde HU60) |
| HU74 | Plantilla import novedades TH | EP-08 | Incluida | Nueva (desde HU75) |
| HU27 | Import asistida desde Excel | EP-01 | Incluida | Nueva |
| HU41 | Copiar semana / asignación masiva | EP-02 | Incluida | Nueva (desde alcance previo HU36) |
| HU42 | Fijar atributo de celda por periodo | EP-02 | Incluida | Nueva (desde alcance previo HU38) |

Total nuevas: **21**

---

## B. HUs existentes a ACTUALIZAR en Word

| ID | Acción Word | Cambio principal al corregir | Archivo backlog |
| -- | ----------- | ---------------------------- | --------------- |
| HU01 | ACTUALIZAR | Completar módulo existente (id 13); no crear módulo duplicado | EP-00 |
| HU02 | DIVIDIR → ACTUALIZAR | Solo RBAC CREAR/LEER/ACTUALIZAR/ELIMINAR por sección; sacar alcance frente → HU03 | EP-00 |
| HU04 | ACTUALIZAR | companyId del contexto autenticado; aislamiento total | EP-00 |
| HU05 | ACTUALIZAR | Sin sedes GRH; sitios = Malla; no padrón paralelo | EP-00 |
| HU06 | ACTUALIZAR (leve) | Mantener separación jornada vs malla; reforzar no escribir jornada | EP-00 |
| HU11 | ACTUALIZAR | Sin frentes/turnos fijos; catálogo | EP-01 |
| HU12 | ACTUALIZAR | Horarios por día genéricos | EP-01 |
| HU13 | ACTUALIZAR | Pausas como datos; no “CC suele…” | EP-01 |
| HU14 | ACTUALIZAR | Ampliar flags; absorbe ex-HU50 y ex-HU54 | EP-01 |
| HU15 | ACTUALIZAR | Campañas catálogo; ejemplos solo seed | EP-01 |
| HU16 | ACTUALIZAR | Niveles territoriales configurables (no Regional/Zona/SPT fijos) | EP-01 |
| HU17 | ACTUALIZAR | Modalidades + flag requiereSitio | EP-01 |
| HU18 | ACTUALIZAR | Sitios catálogo; quitar “Elemento” especial | EP-01 |
| HU19 | ACTUALIZAR | Tipos de restricción catálogo; quitar estudio/salud quemados | EP-01 |
| HU20 | ACTUALIZAR | Solo lectura calendario empresa | EP-01 |
| HU21 | ACTUALIZAR | Cortes sin dinero | EP-01 |
| HU22 | ACTUALIZAR | Tipos de hora catálogo | EP-01 |
| HU23 | ACTUALIZAR | Compensatorio parametrizable; quitar “3 domingos” | EP-01 |
| HU24 | ACTUALIZAR | Cobertura dimensional min/max + severidad | EP-01 |
| HU26 | DIVIDIR → ACTUALIZAR | Solo flags de atributos de celda; estrategia/publicación → HU10 | EP-01 |
| HU28 | ACTUALIZAR | Malla por frente/periodo genérico | EP-02 |
| HU29 | ACTUALIZAR | Grupo + paginación/filtros | EP-02 |
| HU30 | ACTUALIZAR | Celda + motor de reglas | EP-02 |
| HU31 | ACTUALIZAR | Segundo turno solo si capacidad on | EP-02 |
| HU32 | ACTUALIZAR | Territorio opcional por capacidad | EP-02 |
| HU33 | ACTUALIZAR | Modalidad/sitio opcionales | EP-02 |
| HU34 | ACTUALIZAR | Observación por capacidad | EP-02 |
| HU35 | ACTUALIZAR | Grilla + dependencia HU40 | EP-02 |
| HU36 | ACTUALIZAR | Revisar título: en backlog definitivo es campaña/tarea en celda (el Word viejo podía decir “copiar semana”) | EP-02 |
| HU37 | ACTUALIZAR | Cruce entre frentes; sin hardcoding área | EP-02 |
| HU38 | ACTUALIZAR | Filtros dinámicos (Word viejo podía ser “fijar sitio periodo”) | EP-02 |
| HU43 | ACTUALIZAR | Contadores desde reglas, no fórmulas Excel | EP-03 |
| HU44 | ACTUALIZAR | Equilibrio parametrizable | EP-03 |
| HU45 | DIVIDIR → ACTUALIZAR | Solo panel de conflictos; sin “42 h”; motor → HU25 | EP-03 |
| HU47 | DIVIDIR → ACTUALIZAR | Solo vincular patrón a grupo/periodo; definición patrón → HU46 | EP-03 |
| HU50 | ACTUALIZAR | Aplicar solo post simulación; origen automático | EP-03 |
| HU51 | ACTUALIZAR | Asistida según estrategia del frente | EP-03 |
| HU52 | ACTUALIZAR | Breaks desde plantillas/reglas | EP-03 |
| HU53 | ACTUALIZAR | Rotación sitios genérica | EP-03 |
| HU54 | ACTUALIZAR | Reequilibrio post novedad | EP-03 |
| HU55 | ACTUALIZAR | Sin listar estudio/salud | EP-03 |
| HU56 | ACTUALIZAR | Ajuste manual + origen | EP-03 |
| HU57 | ACTUALIZAR | Ciclo vida; absorbe constructor/publicador de ex-HU46 | EP-04 |
| HU58 | ACTUALIZAR | Rechazo en revisión | EP-04 |
| HU59 | ACTUALIZAR | Edición post-publicación por config | EP-04 |
| HU60 | ACTUALIZAR | Estado de catálogo; ownership en HU61 | EP-05 |
| HU62 | ACTUALIZAR | Historial dominio vs timeline | EP-05 |
| HU63 | ACTUALIZAR | notification-service; sin aceptación | EP-05 |
| HU64 | ACTUALIZAR | Historial por funcionario | EP-05 |
| HU65 | ACTUALIZAR | Disponibilidad por flags (absorbe ex-HU54) | EP-06 |
| HU66 | ACTUALIZAR | Cobertura dimensional | EP-06 |
| HU67 | ACTUALIZAR | Visibilidad grupo configurable | EP-07 |
| HU68 | ACTUALIZAR | Mi programación solo lectura | EP-07 |
| HU69 | ACTUALIZAR | Historial propio | EP-07 |
| HU70 | ACTUALIZAR | Horas sin dinero ni 42h | EP-08 |
| HU71 | ACTUALIZAR | Export Excel/PDF | EP-08 |
| HU72 | ACTUALIZAR | Novedad vs operativa por flags | EP-08 |
| HU73 | ACTUALIZAR | Export terceros | EP-08 |
| HU75 | ACTUALIZAR | Cruce TH; plantilla en HU74 | EP-08 |
| HU76 | ACTUALIZAR | Compensatorio desde HU23 | EP-08 |

Total a actualizar: **57** (incluye las que se dividen y siguen existiendo)

---

## C. HUs a ARCHIVAR (no corregir Word; absorber)

| ID original | Word | Absorber en | Nota |
| ----------- | ---- | ----------- | ---- |
| ex-HU46 | Separar constructor/publicador | HU10 + HU57 | Marcar obsoleto |
| ex-HU50 | Dejar de sumar horas novedad | HU14 + HU70 | Es un flag de estado |
| ex-HU54 | Actividad no asignable a casos | HU14 + HU65 | Es un flag de estado |

---

## D. Orden sugerido para corregir Word

### Ronda 1 — EP-00 (base)

1. HU01 → HU02 → **CREAR HU03** → HU04 → HU05 → HU06 → **CREAR HU07** → **CREAR HU08**

### Ronda 2 — EP-01 núcleo

2. **CREAR HU09** → **CREAR HU10** → HU11–HU22 → HU24 → **CREAR HU25** → HU26 (solo flags) → HU14 (ampliar)

### Ronda 3 — EP-02 + técnicas

3. HU28–HU35 → HU36–HU38 → **CREAR HU39** → **CREAR HU40**

### Ronda 4 — Publicar / novedades / empleado / horas

4. HU45 (sin 42h) → HU55–HU56 → HU57–HU59 → HU60 + **CREAR HU61** → HU62–HU63 → HU64 → HU65–HU66 → HU67–HU69 → HU70–HU71

### Ronda 5 — Rotación, reportes TH e intercambio

5. HU23, HU44, HU46, HU47, HU48, HU49, HU50–HU54, HU37, HU72–HU76, **CREAR HU74**, EP-09 HU77–HU81, **CREAR HU27**

### Archivar en paralelo

- ex-HU46, ex-HU50, ex-HU54 → carpeta “Obsoletas” o nota en portada del Word

---

## E. Resumen numérico

| Categoría | Cantidad |
| --------- | -------- |
| ACTUALIZAR (existentes) | 57 |
| CREAR (nuevas) | 19 |
| ARCHIVAR (absorbidas) | 3 |
| Total IDs activos finales | 79 (57 + 19 + 3 absorbidas fuera = 76… wait) |

Cálculo correcto de IDs activos:

- Originales que siguen: 63 − 3 absorbidas = 60  
  Pero HU02/20/34/35 se dividen y el “tronco” sigue + HU60/62 generan hijas nuevas.
- Activos en backlog: **79 HUs** (ver índice maestro).

Para Word: **57 actualizar + 19 crear + 3 archivar = 79 piezas de trabajo** (57+19=76 documentos activos; 3 archivados; las divisiones ya están contadas en actualizar+crear).
