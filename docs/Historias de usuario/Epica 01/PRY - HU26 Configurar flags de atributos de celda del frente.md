# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Configurar flags de atributos de celda del frente. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Configurar flags de atributos de celda del frente |
| Id. Requerimiento | MT-EP01-HU26 |
| Id asociado | REQ-MT-26 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero activar o desactivar qué atributos puede tener una celda en el frente (territorio, campaña, modalidad, sitio, nota, doble turno, etc.), para mostrar en grilla solo lo que la operación necesita.

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

1. El usuario entra a la función de configurar flags de atributos de celda del frente.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando se edita celda.
   - Sistema: Entonces no permite segundo turno.

Resultado esperado: Configurar flags de atributos de celda del frente queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Configurar flags de atributos de celda del frente» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Flag off: dado que doble turno deshabilitado, cuando se edita celda, entonces no permite segundo turno.
2. Flag on: dado que nota habilitada, cuando se edita celda, entonces permite observación.
3. Consistencia: dado que se deshabilita campaña con celdas ya etiquetadas, cuando se consulta histórico, entonces se conserva dato histórico; nuevas celdas no piden campaña.
4. Tenant: dado que config ajena, cuando no visible, entonces OK.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: HU10 define estrategia/publicación/vínculos; HU26 detalla atributos de celda visibles/editables.
- RN-02: Atributo off ⇒ no se captura en UI ni se exige en función del sistema de celda.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Frente operativo | N/A | Selección | SI | SI | SI | Frente a configurar |
| Atributo de celda | 40 | Selección | SI | NO | SI | Territorio, campaña, modalidad, sitio, etc. |
| Habilitado | 1 | Booleano | SI | NO | SI | Muestra el atributo en la grilla del frente |
| Obligatorio al asignar | 1 | Booleano | NO | NO | SI | Exige el atributo al guardar la celda |


---

*Documento para cliente y diseño.*
