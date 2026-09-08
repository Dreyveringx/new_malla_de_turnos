# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-08 — Reportes y horas para nómina
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Reportar horas de novedad versus operativas. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Reportar horas de novedad versus operativas |
| Id. Requerimiento | MT-EP08-HU72 |
| Id asociado | REQ-MT-72 / EP-08 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de reportes, quiero distinguir horas asociadas a estados de novedad frente a horas operativas según flags, para analizar no disponibilidad vs operación.

---

## Actores

- Inicia: Usuario de la empresa con permiso de reportes
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP08-HU70 |
| 2 | MT-EP01-HU14 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de reportar horas de novedad versus operativas.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando reporte.
   - Sistema: Entonces separa totales.

Resultado esperado: Reportar horas de novedad versus operativas queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Reportar horas de novedad versus operativas» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Desglose: dado que hay estados novedad y operativos, cuando reporte, entonces separa totales.
2. Flag: dado que estado marca no operativa, cuando clasifica, entonces va a novedad.
3. Permisos: dado que reportes, cuando OK, entonces OK.
4. Tenant: dado que OK, cuando OK, entonces OK.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: No asume lista fija de novedades; usa flags del catálogo.
- RN-02: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-03: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Fecha desde | 10 | Fecha | SI | NO | SI | Inicio del periodo a consultar |
| Fecha hasta | 10 | Fecha | SI | NO | SI | Fin del periodo a consultar |
| Frente operativo | N/A | Selección | SI | SI | SI | Frente autorizado del usuario |
| Funcionario | N/A | Selección | NO | SI | SI | Filtro opcional por persona |


---

*Documento para cliente y diseño.*
