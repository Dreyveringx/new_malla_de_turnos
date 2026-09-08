# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-03 — Validación, cobertura y rotación
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Visualizar indicadores de cobertura y contadores. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Visualizar indicadores de cobertura y contadores |
| Id. Requerimiento | MT-EP03-HU43 |
| Id asociado | REQ-MT-43 / EP-03 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla, quiero ver indicadores de cobertura y contadores calculados según las reglas y plantillas del frente, para detectar faltantes o excesos sin fórmulas fijas por operación.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU24 |
| 2 | MT-EP02-HU35 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de visualizar indicadores de cobertura y contadores.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando abre indicadores.
   - Sistema: Entonces muestra min/max/actual por dimensión configurada.

Resultado esperado: Visualizar indicadores de cobertura y contadores queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Visualizar indicadores de cobertura y contadores» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Vista: dado que existen reglas de cobertura, cuando abre indicadores, entonces muestra min/max/actual por dimensión configurada.
2. Recalc: dado que cambia una celda relevante, cuando guarda, entonces actualiza indicadores afectados.
3. Capacidad: dado que dimensión no habilitada, cuando abre indicadores, entonces no muestra esa dimensión.
4. Tenant: dado que consulta, cuando datos, entonces solo su empresa.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Los contadores se derivan de reglas HU24 y turnos/estados del catálogo, no de fórmulas Excel de un frente.
- RN-02: Personas con estado que no afecta cobertura no cuentan.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Fecha desde | 10 | Fecha | SI | NO | SI | Inicio del periodo a consultar |
| Fecha hasta | 10 | Fecha | SI | NO | SI | Fin del periodo a consultar |
| Frente operativo | N/A | Selección | SI | SI | SI | Frente autorizado del usuario |


---

*Documento para cliente y diseño.*
