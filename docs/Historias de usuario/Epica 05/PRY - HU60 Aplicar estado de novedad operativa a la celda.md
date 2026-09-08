# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-05 — Novedades, cambios y auditoría
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Aplicar estado de novedad operativa a la celda. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Aplicar estado de novedad operativa a la celda |
| Id. Requerimiento | MT-EP05-HU60 |
| Id asociado | REQ-MT-60 / EP-05 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla, quiero cambiar el estado de una celda a un estado de novedad del catálogo (vacaciones, incapacidad u otros ítems), para reflejar la disponibilidad real sin inventar un módulo TH inexistente.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU14 |
| 2 | MT-EP05-HU61 |
| 3 | MT-EP04-HU59 |
| 4 | MT-EP05-HU62 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de aplicar estado de novedad operativa a la celda.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando asigna a celda.
   - Sistema: Entonces flags determinan cobertura/horas/notificación.

Resultado esperado: Aplicar estado de novedad operativa a la celda queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Aplicar estado de novedad operativa a la celda» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Aplicar: dado que estado novedad del catálogo, cuando asigna a celda, entonces flags determinan cobertura/horas/notificación.
2. Motivo: dado que requiere motivo, cuando sin motivo, entonces bloquea/advierte.
3. Publicada: dado que políticas HU59, cuando aplica, entonces historial + posible notificación.
4. Sin hardcode: dado que cualquier código de estado, cuando mismo flujo, entonces OK.
5. Tenant: dado que OK, cuando OK, entonces OK.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Ownership MVP: la novedad operativa vive como estado de celda (HU61).
- RN-02: No existen estados especiales en código; solo flags.
- RN-03: ex-HU50 absorbida: si el estado no cuenta horas, HU70 no las suma.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Celda | N/A | Selección | SI | SI | SI | Celda donde se aplica la novedad |
| Estado de novedad | N/A | Selección | SI | SI | SI | Estado operativo de novedad |
| Fecha desde | 10 | Fecha | SI | NO | SI | Inicio de la novedad |
| Fecha hasta | 10 | Fecha | NO | NO | SI | Fin de la novedad |
| Motivo | N/A | Texto | NO | NO | SI | Obligatorio si el estado lo exige |


---

*Documento para cliente y diseño.*
