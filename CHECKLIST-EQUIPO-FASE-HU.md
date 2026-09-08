# Checklist de equipo — Malla de turnos (fase HU / mockups / validación)

**Proyecto GRH:** 677705  
**Fase:** documentación y diseño. Sin modelo de BD ni código del módulo.  
**Hito:** sesión de validación, semana del 7–11 sep 2026.  
**Uso:** marcar `[x]` lo hecho y anotar fecha en el informe.

Leyenda de estado: `Pendiente` · `En curso` · `Hecho` · `Bloqueado`

---

## Jair Uribe — Full stack / visión / HU

Objetivo: cerrar alcance y HU para que diseño mockee y negocio apruebe.

- [ ] Cerrar GST-FM-04 de **MT-EP00-HU01** (módulo en GRH) — Id asociado 677705
- [ ] Redactar **MT-EP00-HU02** (permisos por rol y área)
- [ ] Redactar **MT-EP00-HU03** (multi-tenant)
- [ ] Redactar **MT-EP00-HU04** (reutilizar empleados, áreas, festivos)
- [ ] Redactar **MT-EP00-HU05** (malla ≠ jornada contractual)
- [ ] Redactar paquete **EP-01** mínimo para mockups: HU06 plantillas, HU09 estados, HU12 modalidades, HU13 sitios, HU20 config del frente
- [ ] Redactar paquete **núcleo grilla** para la sesión: HU21 crear malla, HU23 celda, HU28 grilla, HU43/HU45 publicar y editar publicada
- [ ] Entregar a diseño cada paquete cerrado (no esperar las 63 HU)
- [ ] Enviar / hacer seguimiento al correo de **Excel** (CC septiembre + Sitio + Mesa)
- [ ] Ensayo de presentación (viernes previo a la sesión)
- [ ] Presentar en sesión: alcance, HU núcleo, mockups; no comprometer DB ni código
- [ ] Recoger aprobado / ajustes y lista de pendientes de negocio
- [ ] Kickoff interno: reglas de fase (no código, no tablas, HU las escribe Jair)

**No hace en esta fase:** diseñar ER, abrir microservicio, estimar sprints de desarrollo.

---

## Diseñadora

Objetivo: mockups navegables del núcleo, alineados a HU y al shell GRH.

- [ ] Recibir HU01 y paquete EP-00 / EP-01
- [ ] Ajustar Figma Make con el prompt de iteración (Sitio editable, menú A–E, selector de rol)
- [ ] Mockup **S00** Hub
- [ ] Mockups **parametría**: turnos, estados, modalidades, sitios, config del frente (modos manual / asistido / automático)
- [ ] Mockup **S15** grilla + panel de celda (modalidad + sitio, no “pantalla Elemento”)
- [ ] Mockup flujo publicar / novedad (aviso informativo, sin aceptación)
- [ ] Dejar paleta GRH (`#4A628A`, `#78D1D7`, `#F4F7FB`)
- [ ] Entregar prototipo para ensayo y para la sesión

**No hace:** flujos que no estén en HU; liquidación en pesos; alta de empleados.

---

## Aprendiz de documentación

Objetivo: Word, glosario, Excel e informe de sesión. No decide alcance.

### Semana 1 (1–5 sep)

- [ ] Leer levantamiento (`turnos.html` o `LEVANTAMIENTO-MALLA-TURNOS-FASE1.md`) y listado de épicas
- [ ] Pasar al GST-FM-04 la **HU01** que Jair cierre (copia fiel; dudas por escrito)
- [ ] Glosario 1 página: malla, turno, estado, celda, modalidad, sitio, publicar, corte de nómina, modo de armado
- [ ] Armar carpeta de HU (nomenclatura `GST-FM-04-MT-EPxx-HUxx-nombre.docx`)
- [ ] Lista de dudas (máx. 15): qué no entiende + en qué documento lo leyó

### Hasta la sesión

- [ ] Pasar a Word cada HU nueva el mismo día que Jair la cierre
- [ ] Inventariar Excel cuando lleguen (un archivo por frente: hojas, columnas, letras, colores, fórmulas vistas)
- [ ] Checklist HU vs Figma (pantalla Sxx cubre / no cubre / parcial)
- [ ] Apoyar ensayo: imprimir o PDF de HU núcleo + glosario
- [ ] Minuta de la sesión: decisión / pendiente / responsable / fecha

**No hace:** redactar HU desde cero; modelo de datos; negociar con las áreas.

---

## Aprendiz backend (sin acceso al repo ~2 semanas)

Objetivo: dominio y mapa de reutilización. Cero tablas y cero código de Malla.

### Semana 1

- [ ] Leer levantamiento + listado de HU + HU01
- [ ] Entregar 1 página: qué es malla / turno / celda / modalidad / sitio / publicar
- [ ] Entregar tabla *se reutiliza / dominio nuevo / no está claro*: empleados, áreas, cargos, empresa, festivos, notificaciones, `work_schedule`
- [ ] Lista de máx. 10 dudas (con fuente)
- [ ] Explicar el viernes en voz alta Contact Center vs Sitio y por qué malla ≠ horario laboral

### Semana 2 (sigue sin repo o recién entra)

- [ ] Apoyar a docs **interpretando** el Excel (catálogo vs celda vs horas); no arma el inventario solo
- [ ] Estudiar Spring Boot + API REST + PostgreSQL + dato por empresa (curso/tutorial, sin repo GRH)
- [ ] Cuando tenga repo: **solo lectura**. Revisar un CRUD existente y cómo viaja `companyId`
- [ ] Anotar por escrito qué del mockup chocaría con GRH (duplicar empleados, etc.)

**No hace:** ER, migraciones, elegir microservicio, commits.

---

## Aprendiz frontend (esta fase)

Objetivo: conocer el look & feel de GRH para que los mockups sean implementables después. Cero código de Malla.

- [ ] Recorrer GRH (menú, un listado, un formulario, un modal) y anotar patrones: sidebar, título, botón primario, tabla
- [ ] Contrastar Figma vs GRH real: 5 diferencias (íconos, menú inventado, etc.)
- [ ] Confirmar con diseño: labels permanentes, 1 CTA primario, color + código en celdas
- [ ] Lista de dudas de UI (máx. 10)
- [ ] Estar en el ensayo; no presentar alcance

**No hace:** ramas, pantallas nuevas, prototipos “para adelantar” el módulo.

---

## Informe semanal (llenar cada viernes)

| Persona | Hecho esta semana | Bloqueado por | Siguiente semana |
| --- | --- | --- | --- |
| Jair | | | |
| Diseño | | | |
| Docs | | | |
| Back | | | |
| Front | | | |

**Bloqueos típicos a declarar:** Excel no llega · HU no cerrada · Figma sin iterar · repo back pendiente · sesión sin fecha confirmada.

---

## Después del aprobado (no marcar ahora)

- [ ] Jair: modelo de datos + si es MS nuevo o extensión
- [ ] Jair: tarjeta técnica de la primera HU a construir
- [ ] Back: persistencia + API de esa HU
- [ ] Front: pantalla de esa HU
- [ ] Docs: HU “listo para demo” y glosario actualizado
