# Prompt Figma Make — Iteración 1 (correcciones)

Pégalo en el **mismo** prototipo: [Módulo Malla de Turnos](https://www.figma.com/make/6JW2Cr9xieMOYNaekfFKvb).

Copia desde `ITERACIÓN…` hasta el final.

---

```text
ITERACIÓN del prototipo existente “Módulo Malla de Turnos” (file 6JW2Cr9xieMOYNaekfFKvb).
NO rediseñes desde cero. NO borres S00–S30 ni el design system.
NO cambies la paleta GRH (#4A628A / #78D1D7 / #F4F7FB / Roboto).
NO inventes pantallas nuevas (salvo el selector de rol y el menú “Más” que indico).
CORRIGE solo lo listado. Mantén español Colombia, desktop 1440, stickers S00–S30, 1 CTA primario.

════════════════════════════════════════
1. DATOS DE FRENTE — Sitio es “en línea”
════════════════════════════════════════
Hoy el demo está AL REVÉS. Déjalo así:

Contact Center (CC)
- Periodo: mes
- Modo: asistido
- Malla publicada editable: SÍ (cambios puntuales por novedad)
- Quién arma: Supervisora CC
- Quién publica: Coordinador CC
- Usa campañas: sí. Usa modalidad/sitio: sí. Usa territorio: no

Soporte en sitio (SITIO)
- Periodo: semana
- Modo: automático
- Malla publicada editable: SÍ  ← crítico. Se envía el viernes y SIGUE editable todos los días
- Quién arma: Coordinador de sitio (Freddy / Luis) — NUNCA “Supervisora CC”
- Quién publica: el mismo coordinador (no hay separación)
- Usa territorio zona/SPT: sí. Usa modalidad/sitio: sí. Usa campañas: no

Mesa de servicio
- Periodo: mes (o semana)
- Modo: manual
- Publicada editable: sí
- Quién arma / publica: Coordinador de mesa — no Supervisora CC

Laboratorio
- Quién arma / publica: Coordinador de laboratorio — no Supervisora CC

S11 debe mostrar estos valores. El badge de S15 Sitio debe decir “Publicada · editable en línea”.

════════════════════════════════════════
2. NAVEGACIÓN A–E — todas las pantallas a 1 click
════════════════════════════════════════
Hoy el strip solo pinta items.slice(0, 3) y S04–S12 / S14 / S20 se esconden.

Reemplaza el strip truncado por:
- Hub sigue siendo S00
- Cada grupo A B C D E: los 3 primeros ítems + un botón “Más ▾” con el resto del grupo
  A Más: Campañas, Territorio, Modalidades, Sitios, Restricciones, Cortes, Compensatorios, Config. frente, Patrones
  B Más: Crear malla, Historial de celda
- O un menú lateral de módulo (debajo del sidebar GRH) con los 5 grupos completos, sin recortar

Quien entre a Parametrización debe llegar a S06, S07 y S11 sin adivinar la URL.

════════════════════════════════════════
3. SELECTOR DE ROL (obligatorio para la demo)
════════════════════════════════════════
En el topbar, junto al avatar, un select “Ver como”:

- Coordinadora CC (Ana Rodríguez) — default. Puede armar, novedad, enviar a revisión. No publica si el frente separa roles.
- Coordinador (Héctor Molina) — publica, rotación, conflictos, reportes.
- Analista de mesa — SOLO lectura. En S15: drawer no abre edición; Publicar / Rotación / Guardar disabled con tooltip “Sin permiso”. S21 y S22 sí. S01–S12 disabled o hidden.
- Operador / técnico (Laura Méndez) — al elegir este rol, aterriza en S24/S25. No ve S13 ni parametría.
- TH / Nómina — S27–S30. Grilla S15 solo lectura, sin editar.

Muestra el tooltip “Sin permiso” de verdad (hover), no solo opacity.

════════════════════════════════════════
4. DATOS QUE MENTÍAN — alinear
════════════════════════════════════════
- CAP (Capacitación) en S03: asignable a casos = NO (igual que ACT). S23 y S03 deben decir lo mismo.
- Quita el card “Laura Méndez (3 sep)” de S21. Laura es UNA persona; el 3 sep está INC, no es otro funcionario.
- Filtro Frente y SPT en S21 deben filtrar de verdad (hoy el select de frente no está cableado). Empty: “Nadie cubre ese SPT en este momento”.
- S14 paso 3, el resumen debe leer el modo REAL del frente elegido (Manual / Asistido / Automático), no hardcodear “Modo Asistido”.
- S08 Andrés Peña = restricción estudio. S17 debe seguir mostrando el bloqueo T1 el jue 10 sep.

════════════════════════════════════════
5. GRILLA EMPLEADO Y TOGGLE
════════════════════════════════════════
- S24: mostrar el mes completo (30 días), no 14. Sigue solo lectura. Chip “● Yo” en Laura.
- S25: el toggle Semana | Mes. El activo usa btn-primary; el otro btn-secondary. No mezclar ambas clases en el mismo botón.
- S16: Virtual oculta/limpia Sitio. Presencial e Híbrido exigen Sitio. Segundo turno + flag Extra se mantiene.

════════════════════════════════════════
6. LOOK — no redibujar el producto, solo no mentir el shell
════════════════════════════════════════
NO reconstruyas Angular. NO copies PrimeNG pixel a pixel.
SÍ:
- Sidebar GRH: Inicio, Mi organización, Funcionarios, Hojas de vida / Contratación, Malla de turnos (activo). Quita “Nómina y pagos” y “Tiempo y asistencia” si no existen en GRH; no inventes módulos.
- Íconos: menos emoji en el sidebar (usa un glifo simple o inicial). Los emoji en la grilla (🏢🏠⚡) pueden quedarse: son semántica de modalidad y van CON texto.
- No toques tokens de color.

════════════════════════════════════════
NO HAGAS
════════════════════════════════════════
- No borres flujos felices CC / Sitio / modalidad.
- No agregues aceptación de turno por el empleado.
- No agregues $ ni liquidación.
- No crees pantalla “Elemento”.
- No pases Sitio a “publicada no editable”.

Al terminar, verifica en voz alta estos 5 clicks:
1) S00 → S11 Sitio = automática + publicada editable SÍ + arma Coordinador de sitio
2) Strip/Más → S06 y S07 existen
3) Ver como Analista de mesa → S15 Publicar disabled “Sin permiso”; S21 sí entra
4) S21 filtro SPT Restrepo → Héctor Molina; filtro que no existe → empty
5) S24 mes completo · S25 toggle Semana/Mes con un solo estilo de botón activo
```
