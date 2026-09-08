# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-03 — Validación, cobertura y rotación
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Aplicar resultado de rotación a la malla. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Aplicar resultado de rotación a la malla |
| Id. Requerimiento | MT-EP03-HU50 |
| Id asociado | REQ-MT-50 / EP-03 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla, quiero aplicar la propuesta simulada aceptada, marcando origen automático y dejando historial, para materializar la rotación de forma trazable.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP03-HU48 |
| 2 | MT-EP05-HU62 |
| 3 | MT-EP00-HU07 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de aplicar resultado de rotación a la malla.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando aplica.
   - Sistema: Entonces celdas actualizadas con origen automático.

Resultado esperado: Aplicar resultado de rotación a la malla queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Aplicar resultado de rotación a la malla» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Aplicar: dado que simulación aceptada sin bloqueos críticos, cuando aplica, entonces celdas actualizadas con origen automático.
2. Parcial: dado que algunas celdas bloqueadas, cuando aplica, entonces omite bloqueadas y reporta.
3. Historial: dado que celda cambia, cuando consulta historial, entonces antes/después + origen automático.
4. Sin simulación: dado que config exige simulación, cuando aplica directo, entonces rechaza.
5. Notificación: dado que si flags de estado/config lo requieren, cuando aplica, entonces despacha eventos HU07.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Toda celda escrita por rotación registra origen automático.
- RN-02: Ajustes posteriores manuales cambian origen a manual (HU56).
- RN-03: Se revalidan reglas; bloqueos impiden aplicar esas celdas.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Resultado de simulación | N/A | Selección | SI | SI | SI | Simulación a aplicar |
| Confirmar aplicación | 1 | Booleano | SI | NO | SI | Persiste el resultado en la malla |


---

*Documento para cliente y diseño.*
