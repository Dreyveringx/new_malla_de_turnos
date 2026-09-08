# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Parametrizar break y almuerzo del turno. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Parametrizar break y almuerzo del turno |
| Id. Requerimiento | MT-EP01-HU13 |
| Id asociado | REQ-MT-13 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero definir pausas (break, almuerzo u otros tipos de pausa del catálogo) asociadas a una plantilla, para que la operación programe pausas según configuración y no según reglas fijas por frente.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU11 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de parametrizar break y almuerzo del turno.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando se agregan una o más pausas con tipo e intervalo.
   - Sistema: Entonces quedan asociadas a la plantilla.

Resultado esperado: Parametrizar break y almuerzo del turno queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Parametrizar break y almuerzo del turno» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Alta pausa: dado que plantilla activa, cuando se agregan una o más pausas con tipo e intervalo, entonces quedan asociadas a la plantilla.
2. Sin pausas: dado que frente/plantilla sin pausas, cuando se asigna el turno, entonces no se exigen pausas.
3. Validación: dado que pausa fuera del horario del turno, cuando se guarda, entonces el sistema rechaza o advierte según regla configurada.
4. Tenant: dado que otra empresa, cuando consulta pausas, entonces no ve datos ajenos.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Las pausas son datos de plantilla; su obligatoriedad y efecto en cobertura lo definen reglas (HU25/HU24).
- RN-02: No se asume que todos los frentes usan break y almuerzo.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Plantilla de turno | N/A | Selección | SI | SI | SI | Plantilla asociada a la pausa |
| Tipo de pausa | 40 | Selección | SI | NO | SI | Break, almuerzo u otro tipo del catálogo |
| Duración (minutos) | 5 | Número | SI | NO | SI | Duración de la pausa |
| Remunerada | 1 | Booleano | SI | NO | SI | Indica si la pausa es remunerada |
| Hora inicio sugerida | 8 | Hora | NO | NO | SI | Inicio orientativo de la pausa |


---

*Documento para cliente y diseño.*
