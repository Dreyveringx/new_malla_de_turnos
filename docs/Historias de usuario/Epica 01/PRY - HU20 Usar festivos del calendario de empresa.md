# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Usar festivos del calendario de empresa. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Usar festivos del calendario de empresa |
| Id. Requerimiento | MT-EP01-HU20 |
| Id asociado | REQ-MT-20 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol), quiero considerar los festivos definidos en el calendario GRH de la empresa al programar y calcular horas, para no duplicar calendarios.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP00-HU05 |
| 2 | MT-EP01-HU22 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de usar festivos del calendario de empresa.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando se visualiza el día en malla.
   - Sistema: Entonces se identifica como festivo.

Resultado esperado: Usar festivos del calendario de empresa queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Usar festivos del calendario de empresa» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Lectura: dado que hay festivo en calendario empresa, cuando se visualiza el día en malla, entonces se identifica como festivo.
2. Horas: dado que existen reglas de tipo hora festiva, cuando se calcula el día festivo, entonces se clasifica según reglas HU22/HU70.
3. Tenant: dado que festivos de otra empresa, cuando consulta, entonces no aplican.
4. Sin calendario: dado que empresa sin festivos cargados, cuando opera malla, entonces no inventa festivos.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Fuente de verdad de festivos = calendario de empresa GRH.
- RN-02: Malla no mantiene un calendario paralelo de festivos.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Año | 4 | Número | SI | NO | SI | Año del calendario de festivos a consultar |
| Fecha festivo | 10 | Fecha | N/A | SI | SI | Fecha aportada por el calendario de empresa |
| Nombre festivo | 120 | Alfanumérico | N/A | SI | SI | Nombre del festivo consultado |


---

*Documento para cliente y diseño.*
