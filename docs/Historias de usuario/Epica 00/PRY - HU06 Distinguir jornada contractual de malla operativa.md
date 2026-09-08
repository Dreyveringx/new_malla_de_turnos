# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-00 — Integración del módulo a la plataforma GRH
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Distinguir jornada contractual de malla operativa. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Distinguir jornada contractual de malla operativa |
| Id. Requerimiento | MT-EP00-HU06 |
| Id asociado | REQ-MT-06 / EP-00 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol), quiero consultar la jornada contractual como referencia sin modificarla al programar la malla, para separar condición laboral de la programación operativa diaria.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP00-HU05 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de distinguir jornada contractual de malla operativa.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando se le asigna un turno en malla distinto al habitual.
   - Sistema: Entonces la jornada contractual permanece igual.

Resultado esperado: Distinguir jornada contractual de malla operativa queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Distinguir jornada contractual de malla operativa» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. No escritura: dado que un funcionario tiene jornada contractual definida, cuando se le asigna un turno en malla distinto al habitual, entonces la jornada contractual permanece igual.
2. Referencia: dado que el coordinador consulta la ficha del funcionario en contexto de malla, cuando abre la referencia de jornada, entonces ve la jornada contractual en modo lectura.
3. Independencia: dado que no hay jornada contractual cargada, cuando se crea una celda operativa, entonces la malla permite programar según reglas del frente (sin bloquear por ausencia de jornada, salvo regla explícita).
4. Permisos: dado que el usuario solo tiene permisos de Malla, cuando intenta editar jornada contractual desde Malla, entonces no existe esa acción.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: La jornada contractual define condiciones laborales; la malla define la operación por fecha.
- RN-02: Guardar una celda no altera la jornada contractual.
- RN-03: Las diferencias entre jornada y malla pueden advertirse si existe una regla configurada; no se corrigen escribiendo la jornada.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

Esta historia no captura datos propios de formulario. El alcance y la empresa provienen del contexto autenticado.


---

*Documento para cliente y diseño.*
