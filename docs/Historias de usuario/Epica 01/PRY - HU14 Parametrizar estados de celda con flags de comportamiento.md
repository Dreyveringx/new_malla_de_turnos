# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Parametrizar estados de celda con flags de comportamiento. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Parametrizar estados de celda con flags de comportamiento |
| Id. Requerimiento | MT-EP01-HU14 |
| Id asociado | REQ-MT-14 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero registrar estados operativos de celda con código, nombre, color y flags que definen su comportamiento, para representar novedades y situaciones operativas sin HUs ni enums por cada estado de negocio.

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

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de parametrizar estados de celda con flags de comportamiento.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando crea estado con flags.
   - Sistema: Entonces queda disponible en celdas de la empresa (y frentes según aplicabilidad).

Resultado esperado: Parametrizar estados de celda con flags de comportamiento queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Parametrizar estados de celda con flags de comportamiento» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Alta estado: dado que usuario con permiso, cuando crea estado con flags, entonces queda disponible en celdas de la empresa (y frentes según aplicabilidad).
2. No suma horas: dado que estado con flag cuenta horas ordinarias = no, cuando se calcula el periodo, entonces esa celda no aporta horas ordinarias.
3. Afecta cobertura: dado que estado con afecta cobertura = no, cuando se evalúa cobertura, entonces la persona no cuenta para el mínimo de esa dimensión.
4. Motivo: dado que estado requiere motivo = sí, cuando se aplica a celda sin motivo, entonces el sistema bloquea o advierte según severidad configurada.
5. Tenant: dado que estados de empresa A, cuando empresa B lista, entonces no los ve.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Los estados son catálogo; vacaciones/incapacidad/actividad/descanso son ítems de datos, no tipos de sistema.
- RN-02: El efecto en horas lo determinan los flags + motor de horas (HU70).
- RN-03: Si un estado no es asignable a casos, la consulta operativa lo excluye de disponibilidad operativa según flag.
- RN-04: ex-HU50 y ex-HU54 originales quedan absorbidas por estos flags.
- RN-05: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-06: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Código | 20 | Alfanumérico | SI | NO | SI | Identificador único del estado de celda en la empresa |
| Nombre | 120 | Alfanumérico | SI | NO | SI | Nombre visible del estado de celda |
| Descripción | N/A | Texto | NO | NO | SI | Texto de ayuda o detalle |
| Color | 7 | Color | NO | NO | SI | Color de visualización del estado |
| Cuenta horas | 1 | Booleano | SI | NO | SI | El estado aporta horas al cálculo |
| Afecta cobertura | 1 | Booleano | SI | NO | SI | Impacta indicadores de cobertura |
| Asignable a casos | 1 | Booleano | SI | NO | SI | Persona disponible para asignación |
| Requiere motivo | 1 | Booleano | SI | NO | SI | Obliga a registrar motivo al aplicar |
| Permite turno | 1 | Booleano | SI | NO | SI | Permite coexistir con plantilla de turno |
| Permite ubicación | 1 | Booleano | SI | NO | SI | Permite sitio/modalidad en la celda |
| Notifica empleado | 1 | Booleano | SI | NO | SI | Dispara notificación al aplicar |
| Requiere soporte | 1 | Booleano | SI | NO | SI | Marca necesidad de cobertura de soporte |
| Activo | 1 | Booleano | SI | NO | SI | Indica si el estado está disponible |


---

*Documento para cliente y diseño.*
