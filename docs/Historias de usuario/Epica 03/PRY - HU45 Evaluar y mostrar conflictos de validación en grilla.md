# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-03 — Validación, cobertura y rotación
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Evaluar y mostrar conflictos de validación en grilla. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Evaluar y mostrar conflictos de validación en grilla |
| Id. Requerimiento | MT-EP03-HU45 |
| Id asociado | REQ-MT-45 / EP-03 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla, quiero ejecutar el motor de reglas y mostrar hallazgos en la grilla y un panel de conflictos, para corregir problemas antes de publicar.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU25 |
| 2 | MT-EP02-HU35 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de evaluar y mostrar conflictos de validación en grilla.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando ejecuta validación.
   - Sistema: Entonces lista hallazgos con severidad.

Resultado esperado: Evaluar y mostrar conflictos de validación en grilla queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Evaluar y mostrar conflictos de validación en grilla» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Eval: dado que hay violaciones, cuando ejecuta validación, entonces lista hallazgos con severidad.
2. Navegar: dado que selecciona un hallazgo, cuando hace clic, entonces enfoca la celda.
3. Filtro: dado que filtra solo bloqueos, cuando aplica, entonces oculta info/advertencias.
4. Sin hardcode: dado que regla max_hours_period=N, cuando muestra mensaje, entonces incluye N desde la regla.
5. Tenant: dado que validación, cuando solo malla propia, entonces OK.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Los mensajes muestran el nombre de la regla y sus parámetros, no constantes de producto.
- RN-02: Bloqueos impiden publicar si la config de publicación exige cero bloqueos.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Malla | N/A | Selección | SI | SI | SI | Malla a validar |
| Severidad mínima a mostrar | 20 | Selección | NO | NO | SI | Info, advertencia o bloqueo |


---

*Documento para cliente y diseño.*
