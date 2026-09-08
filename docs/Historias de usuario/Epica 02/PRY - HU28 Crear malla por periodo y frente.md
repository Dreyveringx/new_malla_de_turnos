# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-02 — Construcción de la malla
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Crear malla por periodo y frente. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Crear malla por periodo y frente |
| Id. Requerimiento | MT-EP02-HU28 |
| Id asociado | REQ-MT-28 / EP-02 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol), quiero crear una malla asociada a un frente, con rango de fechas según el periodo configurado, en estado borrador, para iniciar la programación operativa del periodo.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU10 |
| 2 | MT-EP00-HU03 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de crear malla por periodo y frente.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando crea malla con fechas.
   - Sistema: Entonces queda en borrador.

Resultado esperado: Crear malla por periodo y frente queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Crear malla por periodo y frente» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Alta: dado que frente activo y alcance OK, cuando crea malla con fechas, entonces queda en borrador.
2. Sin alcance: dado que frente fuera de alcance, cuando intenta crear, entonces rechazo.
3. Tenant: dado que frente de otra empresa, cuando crear, entonces imposible.
4. Duplicidad: dado que ya existe malla solapada si la regla del frente lo prohíbe, cuando crea, entonces aplica severidad de la regla.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: La malla pertenece a la empresa del usuario y a un frente de su alcance.
- RN-02: El periodo por defecto proviene de la config del frente; el usuario puede ajustar dentro de lo permitido.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Frente operativo | N/A | Selección | SI | SI | SI | Frente de la malla |
| Fecha inicio del periodo | 10 | Fecha | SI | NO | SI | Inicio del periodo de la malla |
| Fecha fin del periodo | 10 | Fecha | SI | NO | SI | Fin del periodo de la malla |
| Modo de armado | 20 | Selección | SI | SI | SI | Según estrategia configurada del frente |
| Nombre o etiqueta | 120 | Alfanumérico | NO | NO | SI | Referencia opcional de la malla |


---

*Documento para cliente y diseño.*
