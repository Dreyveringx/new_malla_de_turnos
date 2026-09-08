# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-00 — Integración del módulo a la plataforma GRH
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Aislar información por empresa. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Aislar información por empresa |
| Id. Requerimiento | MT-EP00-HU04 |
| Id asociado | REQ-MT-04 / EP-00 |

### Descripción de historia de usuario

Como Administrador de empresa / Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol), quiero que toda la información de Malla de Turnos pertenezca únicamente a mi empresa, para impedir fugas de datos entre tenants.

---

## Actores

- Inicia: Administrador de empresa / Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP00-HU01 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de aislar información por empresa.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando un usuario de la empresa B lista frentes o mallas.
   - Sistema: Entonces no ve datos de A.

Resultado esperado: Aislar información por empresa queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Aislar información por empresa» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Lectura aislada: dado que la empresa A tiene frentes y mallas, cuando un usuario de la empresa B lista frentes o mallas, entonces no ve datos de A.
2. Escritura aislada: dado que un usuario autenticado en empresa A, cuando intenta crear un recurso indicando empresa B en el cuerpo, entonces el sistema ignora ese valor y persiste solo bajo A, o rechaza la petición.
3. Empleados: dado que se seleccionan funcionarios para una malla, cuando se listan candidatos, entonces solo aparecen empleados de la misma empresa.
4. Reportes: dado que se exporta un reporte, cuando se genera el archivo, entonces solo incluye datos de la empresa del usuario.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: El identificador de empresa proviene del contexto autenticado; no se confía en el valor enviado por el cliente como fuente de verdad.
- RN-02: Todas las consultas y escrituras están filtradas por empresa.
- RN-03: Catálogos, mallas, reglas, solicitudes de intercambio y exportaciones son tenant-scoped.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

Esta historia no captura datos propios de formulario. El alcance y la empresa provienen del contexto autenticado.


---

*Documento para cliente y diseño.*
