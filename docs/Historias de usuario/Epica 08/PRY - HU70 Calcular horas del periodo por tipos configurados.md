# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-08 — Reportes y horas para nómina
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Calcular horas del periodo por tipos configurados. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Calcular horas del periodo por tipos configurados |
| Id. Requerimiento | MT-EP08-HU70 |
| Id asociado | REQ-MT-70 / EP-08 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de reportes, quiero calcular horas del periodo clasificadas por tipos de hora y afectadas por flags de estado, para entregar información de horas a nómina sin liquidar dinero.

---

## Actores

- Inicia: Usuario de la empresa con permiso de reportes
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU22 |
| 2 | MT-EP01-HU14 |
| 3 | MT-EP01-HU21 |
| 4 | MT-EP01-HU20 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de calcular horas del periodo por tipos configurados.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando ejecuta.
   - Sistema: Entonces obtiene horas por tipo.

Resultado esperado: Calcular horas del periodo por tipos configurados queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Calcular horas del periodo por tipos configurados» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Cálculo: dado que malla con turnos, cuando ejecuta, entonces obtiene horas por tipo.
2. Estado no suma: dado que flag off, cuando calcula, entonces excluye esas celdas del tipo afectado.
3. Festivo: dado que día festivo y regla festiva, cuando clasifica, entonces según HU22.
4. Sin dinero: dado que salida, cuando inspecciona, entonces sin campos monetarios.
5. Tenant: dado que OK, cuando OK, entonces OK.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Los topes de horas son reglas HU25, no constantes.
- RN-02: Salida = cantidades de hora por tipo, nunca montos.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Fecha desde | 10 | Fecha | SI | NO | SI | Inicio del periodo a consultar |
| Fecha hasta | 10 | Fecha | SI | NO | SI | Fin del periodo a consultar |
| Frente operativo | N/A | Selección | SI | SI | SI | Frente autorizado del usuario |
| Tipos de hora | N/A | Selección | NO | SI | SI | Tipos configurados a incluir |
| Funcionario | N/A | Selección | NO | SI | SI | Filtro opcional por persona |


---

*Documento para cliente y diseño.*
