# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Parametrizar modalidades de trabajo. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Parametrizar modalidades de trabajo |
| Id. Requerimiento | MT-EP01-HU17 |
| Id asociado | REQ-MT-17 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero registrar modalidades (presencial, virtual u otras) con flag que indique si requieren sitio, para extender modalidades sin enums fijos.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU10 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de parametrizar modalidades de trabajo.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando crea modalidad con requiereSitio.
   - Sistema: Entonces al asignar, si requiereSitio y capacidad sitio on, exige sitio.

Resultado esperado: Parametrizar modalidades de trabajo queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Parametrizar modalidades de trabajo» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Alta: dado que permiso de parametrización, cuando crea modalidad con requiereSitio, entonces al asignar, si requiereSitio y capacidad sitio on, exige sitio.
2. Nueva modalidad: dado que se necesita una modalidad nueva, cuando se crea en catálogo, entonces no requiere despliegue de código.
3. Tenant: dado que otra empresa, cuando lista, entonces aislada.
4. Capacidad off: dado que frente sin modalidad, cuando edita celda, entonces no pide modalidad.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Presencial/virtual/híbrido son ejemplos de datos, no tipos de sistema.
- RN-02: La obligatoriedad de sitio la define el flag + capacidad del frente.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Código | 20 | Alfanumérico | SI | NO | SI | Identificador único del modalidad de trabajo en la empresa |
| Nombre | 120 | Alfanumérico | SI | NO | SI | Nombre visible del modalidad de trabajo |
| Descripción | N/A | Texto | NO | NO | SI | Texto de ayuda o detalle |
| Activo | 1 | Booleano | SI | NO | SI | Indica si está disponible para uso |


---

*Documento para cliente y diseño.*
