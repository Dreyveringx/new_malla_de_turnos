# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-05 — Novedades, cambios y auditoría
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Definir ownership MVP de novedades. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Definir ownership MVP de novedades |
| Id. Requerimiento | MT-EP05-HU61 |
| Id asociado | REQ-MT-61 / EP-05 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización, quiero operar novedades como estado de celda con importación opcional, dejando explícito que no hay módulo TH en GRH hoy, para evitar dobles fuentes de verdad no gobernadas.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU14 |
| 2 | MT-EP08-HU74 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de definir ownership mvp de novedades.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando persiste.
   - Sistema: Entonces como estado de celda.

Resultado esperado: Definir ownership MVP de novedades queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Definir ownership MVP de novedades» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. MVP: dado que se aplica novedad, cuando persiste, entonces como estado de celda.
2. Import: dado que existe archivo, cuando importa, entonces propone/aplica estados según mapeo.
3. Sin módulo TH: dado que documentación/producto, cuando consulta capacidades GRH, entonces no asume módulo TH.
4. Tenant: dado que import, cuando empresa del usuario, entonces OK.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Fuente operativa MVP = estado de celda.
- RN-02: Archivo TH es complemento de cruce, no reemplaza el catálogo de estados.
- RN-03: Futuro conector TH no debe romper historial de celda.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Tipo de novedad | N/A | Selección | SI | SI | SI | Clase de novedad a configurar |
| Responsable MVP (ownership) | 40 | Selección | SI | NO | SI | Quién captura/aprueba en el MVP |
| Activo | 1 | Booleano | SI | NO | SI | Vigencia de la definición |


---

*Documento para cliente y diseño.*
