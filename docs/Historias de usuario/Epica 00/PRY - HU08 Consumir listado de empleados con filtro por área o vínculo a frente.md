# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-00 — Integración del módulo a la plataforma GRH
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Consumir listado de empleados con filtro por área o vínculo a frente. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Consumir listado de empleados con filtro por área o vínculo a frente |
| Id. Requerimiento | MT-EP00-HU08 |
| Id asociado | REQ-MT-08 / EP-00 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol), quiero listar funcionarios aplicables al frente filtrando por área, cargo y estado sin traer toda la empresa de golpe, para armar grupos de malla de forma usable y tenant-safe.

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
| 2 | MT-EP01-HU10 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de consumir listado de empleados con filtro por área o vínculo a frente.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando se abre el selector de grupo.
   - Sistema: Entonces se cargan páginas o resultados filtrados, no un volcado único no paginado obligatorio.

Resultado esperado: Consumir listado de empleados con filtro por área o vínculo a frente queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Consumir listado de empleados con filtro por área o vínculo a frente» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Paginación: dado que la empresa tiene cientos de empleados, cuando se abre el selector de grupo, entonces se cargan páginas o resultados filtrados, no un volcado único no paginado obligatorio.
2. Filtro área: dado que el frente está vinculado a una o más áreas, cuando se listan candidatos, entonces se priorizan o filtran empleados de esas áreas según configuración.
3. Tenant: dado que existen empleados en otra empresa, cuando se lista, entonces no aparecen.
4. Estado: dado que hay empleados inactivos, cuando se aplica filtro de activos, entonces solo se ofrecen los que cumplen el filtro.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Toda consulta de empleados usa la empresa del contexto autenticado.
- RN-02: Si el servicio de empleados no expone filtro por área, Malla debe paginar y filtrar de forma explícita documentada, o solicitar la extensión del función del sistema.
- RN-03: No se cachea padrón completo de otra empresa.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Área organizacional | N/A | Selección | NO | SI | SI | Filtro de empleados por área |
| Texto de búsqueda | 120 | Alfanumérico | NO | NO | SI | Nombre o documento a buscar |
| Solo activos | 1 | Booleano | NO | NO | SI | Limita el listado a empleados activos |


---

*Documento para cliente y diseño.*
