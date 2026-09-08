# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-03 — Validación, cobertura y rotación
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Definir patrón de rotación genérico. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Definir patrón de rotación genérico |
| Id. Requerimiento | MT-EP03-HU46 |
| Id asociado | REQ-MT-46 / EP-03 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización, quiero crear patrones como secuencia ordenada de elementos (turno/estado), cada uno con duración, formando un ciclo, para representar cualquier rotación (incluidos ejemplos 15/15 o 2×1) sin tipos enum de patrón.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU11 |
| 2 | MT-EP01-HU14 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de definir patrón de rotación genérico.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando guarda.
   - Sistema: Entonces patrón reutilizable en la empresa.

Resultado esperado: Definir patrón de rotación genérico queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Definir patrón de rotación genérico» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Alta: dado que define secuencia de plantillas con duraciones, cuando guarda, entonces patrón reutilizable en la empresa.
2. Ciclo: dado que secuencia completa, cuando se consulta longitud de ciclo, entonces es la suma de duraciones.
3. Sin enum: dado que lista tipos de patrón del sistema, cuando consulta, entonces no hay tipos especiales; solo patrones creados.
4. Tenant: dado que patrón ajeno, cuando invisible, entonces OK.
5. Inactivo: dado que patrón inactivo, cuando aplicar, entonces no ofrecido.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Un patrón es solo datos: secuencia, duraciones, ciclo, prioridad, vigencia.
- RN-02: No existen tipos de patrón de producto.
- RN-03: Ejemplos de negocio son seeds o instancias.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Código del patrón | 40 | Alfanumérico | SI | NO | SI | Identificador del patrón de rotación |
| Nombre | 120 | Alfanumérico | SI | NO | SI | Nombre del patrón |
| Paso / día relativo | 5 | Número | SI | NO | SI | Orden del paso en el patrón |
| Turno o estado del paso | N/A | Selección | SI | SI | SI | Asignación del paso |
| Activo | 1 | Booleano | SI | NO | SI | Indica si el patrón está disponible |


---

*Documento para cliente y diseño.*
