# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-00 — Integración del módulo a la plataforma GRH
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Reutilizar empleados, áreas, cargos y calendario de festivos de GRH. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Reutilizar empleados, áreas, cargos y calendario de festivos de GRH |
| Id. Requerimiento | MT-EP00-HU05 |
| Id asociado | REQ-MT-05 / EP-00 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol), quiero usar los funcionarios, áreas, cargos y festivos ya existentes en GRH al armar mallas, para no duplicar padrones ni calendarios.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP00-HU04 |
| 2 | MT-EP00-HU08 |
| 3 | MT-EP01-HU18 |
| 4 | MT-EP01-HU20 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de reutilizar empleados, áreas, cargos y calendario de festivos de grh.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando el coordinador arma el grupo de la malla.
   - Sistema: Entonces selecciona desde el padrón GRH de su empresa.

Resultado esperado: Reutilizar empleados, áreas, cargos y calendario de festivos de GRH queda operativa, aislada por empresa y gobernada por configuración.

---

## Flujos alternos

- FA-01: Si falta configuración previa requerida, el sistema indica qué falta y no continúa.
- FA-02: Si el frente o la capacidad están deshabilitados, la acción no aparece o se informa.
- FA-03: Si hay advertencias de reglas, el usuario puede confirmar solo cuando la configuración lo permita.

---

## Errores

- E-01: Datos incompletos o inválidos.
  - Comportamiento esperado: No guarda; indica el problema.
- E-02: Sin permiso o fuera de alcance de frente.
  - Comportamiento esperado: Acceso no permitido.
- E-03: Intento de operar datos de otra empresa.
  - Comportamiento esperado: No visible / rechazado.
- E-04: Fallo al guardar.
  - Comportamiento esperado: Mensaje claro; no deja información inconsistente.

---

## Prototipo de interfaz de usuario y/o reportes

Pantalla o flujo de «Reutilizar empleados, áreas, cargos y calendario de festivos de GRH» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Empleados: dado que existen empleados activos en la empresa, cuando el coordinador arma el grupo de la malla, entonces selecciona desde el padrón GRH de su empresa.
2. Áreas y cargos: dado que se filtra por área o cargo, cuando se aplican filtros, entonces los valores vienen de maestros GRH.
3. Festivos: dado que el calendario de empresa tiene un festivo, cuando se consulta el día en malla, entonces el sistema reconoce el festivo sin catálogo paralelo de festivos en Malla.
4. Sin sedes GRH: dado que se necesita un sitio de asistencia, cuando el usuario busca sedes en GRH, entonces usa el catálogo de sitios de Malla (HU18), no un maestro inexistente de sedes.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Malla no mantiene un padrón paralelo de empleados.
- RN-02: Áreas y cargos se leen de parametrización GRH.
- RN-03: Festivos se leen del calendario de empresa.
- RN-04: Sitios de asistencia son catálogo propio de Malla.
- RN-05: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-06: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

Esta historia no captura datos propios de formulario. El alcance y la empresa provienen del contexto autenticado.


---

*Documento para cliente y diseño.*
