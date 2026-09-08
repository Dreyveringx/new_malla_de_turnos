# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Configurar capacidades, estrategia de armado y publicación del frente. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Configurar capacidades, estrategia de armado y publicación del frente |
| Id. Requerimiento | MT-EP01-HU10 |
| Id asociado | REQ-MT-10 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero definir para cada frente el periodo de planificación por defecto, la estrategia de armado, la separación constructor/publicador, la editabilidad post-publicación y las capacidades disponibles, para que el mismo producto se adapte a cada operación sin redesplegar código.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU09 |
| 2 | MT-EP00-HU03 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de configurar capacidades, estrategia de armado y publicación del frente.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando se edita una celda.
   - Sistema: Entonces no se solicita ni muestra territorio.

Resultado esperado: Configurar capacidades, estrategia de armado y publicación del frente queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Configurar capacidades, estrategia de armado y publicación del frente» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Capacidad off: dado que el frente tiene deshabilitado territorio, cuando se edita una celda, entonces no se solicita ni muestra territorio.
2. Estrategia: dado que estrategia = manual, cuando el usuario abre rotación automática, entonces la acción no está disponible e indica que la configuración del frente no la habilita.
3. Constructor: dado que separación constructor/publicador activa, cuando el constructor intenta publicar, entonces solo puede enviar a revisión o se le niega publicar según config.
4. Intercambio off: dado que solicitudes deshabilitadas en el frente, cuando un empleado abre su programación, entonces no ve la acción de solicitar intercambio.
5. Auditoría config: dado que se cambia la estrategia de armado, cuando se guarda, entonces queda trazabilidad de antes/después, usuario y fecha.
6. Tenant: dado que se edita config de un frente, cuando persiste, entonces solo afecta a la empresa dueña del frente.
7. Solo se muestran o modifican datos de la empresa del usuario autenticado.
8. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Si una capacidad está deshabilitada, la UI y las función del sistema no exigen ni persisten ese atributo en celdas nuevas.
- RN-02: Si la estrategia es manual, las acciones de rotación automática permanecen deshabilitadas.
- RN-03: Si constructor/publicador está separado, quien solo construye no publica; envía a revisión según flujo HU57.
- RN-04: Publicar con advertencias solo si el flag del frente lo permite.
- RN-05: El vínculo a áreas GRH es opcional; el frente sigue siendo entidad propia.
- RN-06: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-07: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Frente operativo | N/A | Selección | SI | SI | SI | Frente a configurar |
| Periodo de planificación por defecto | 20 | Selección | SI | NO | SI | Semana, mes u otro valor del catálogo |
| Estrategia de armado | 20 | Selección | SI | NO | SI | Ninguna, manual, asistida o automática |
| Separar constructor y publicador | 1 | Booleano | SI | NO | SI | Exige roles distintos en el ciclo de publicación |
| Editable tras publicación | 1 | Booleano | SI | NO | SI | Permite editar malla publicada |
| Solicitudes de intercambio habilitadas | 1 | Booleano | SI | NO | SI | Activa EP-09 en el frente |
| Áreas vinculadas | N/A | Selección | NO | SI | SI | Áreas GRH asociadas al frente |
| Capacidad / atributo | 40 | Selección | SI | NO | SI | Capacidad del frente a habilitar o deshabilitar |
| Capacidad habilitada | 1 | Booleano | SI | NO | SI | Estado de la capacidad seleccionada |


---

*Documento para cliente y diseño.*
