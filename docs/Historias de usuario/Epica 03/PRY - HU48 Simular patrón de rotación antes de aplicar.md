# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-03 — Validación, cobertura y rotación
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Simular patrón de rotación antes de aplicar. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Simular patrón de rotación antes de aplicar |
| Id. Requerimiento | MT-EP03-HU48 |
| Id asociado | REQ-MT-48 / EP-03 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla, quiero ejecutar un simulación del patrón que muestre asignaciones propuestas y conflictos sin alterar la malla, para revisar el impacto antes de escribir.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP03-HU47 |
| 2 | MT-EP03-HU49 |
| 3 | MT-EP01-HU25 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de simular patrón de rotación antes de aplicar.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando simula.
   - Sistema: Entonces muestra propuesta sin cambiar malla.

Resultado esperado: Simular patrón de rotación antes de aplicar queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Simular patrón de rotación antes de aplicar» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Dry-run: dado que vínculo válido, cuando simula, entonces muestra propuesta sin cambiar malla.
2. Conflictos: dado que hay violaciones, cuando simula, entonces lista conflictos detectados.
3. Exclusiones: dado que personas excluidas, cuando simula, entonces no propone cambios para ellas.
4. Reintentar: dado que ajusta parámetros, cuando vuelve a simular, entonces actualiza propuesta.
5. Permisos: dado que sin ACTUALIZAR, cuando simula si LEER+política lo permite o niega escritura posterior, entonces según permisos.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: La simulación no escribe celdas.
- RN-02: Debe mostrar qué sería automático y qué queda excluido (HU49).
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Vinculación patrón-grupo | N/A | Selección | SI | SI | SI | Configuración a simular |
| Confirmar simulación | 1 | Booleano | SI | NO | SI | Ejecuta la simulación sin persistir |


---

*Documento para cliente y diseño.*
