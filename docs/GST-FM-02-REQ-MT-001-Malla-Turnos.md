# GST-FM-02 — Necesidad del cliente

| Campo | Valor |
| ----- | ----- |
| Formato | GST-FM-02 FORMATO NECESIDAD DEL CLIENTE |
| Producto | Plataforma GRH |
| Requerimiento | REQ-MT-001 — Módulo Malla de Turnos |
| Proyecto | PRY-677705 — Proyecto interno GRH |
| Fecha solicitud | 07/09/2026 |
| Elaboró | Jair Uribe |
| Fuente | Levantamiento 27/08/2026 + backlog definitivo + propuesta de épicas/HU v1.0 |

Este markdown es el **contenido para copiar** al Word vacío `GST-FM-02 FORMATO NECESIDAD DEL CLIENTE (2).docx`.  
Al final está la guía de cómo pegarlo sección por sección.

---

## 0. Tipo de requerimiento

Nuevo módulo / funcionalidad de producto (desarrollo de software).

Alternativa si el formato usa casillas: marcar **Desarrollo de nuevo módulo** (o “Nuevo requerimiento funcional”) dentro de la Plataforma GRH.

---

## 1. Datos del producto

### Nombre producto / requerimiento

REQ-MT-001 — Módulo Malla de Turnos (Plataforma GRH)

### Nombre del Sponsor / Líder funcional / Líder de proyecto

- Sponsor / Líder funcional: Ricardo Rojas Sierra
- Líder funcional Contact Center: Oscar Ariel Acuña Sánchez
- Líder técnico: Héctor Mauricio Coronado Gutiérrez
- Elaboración del requerimiento: Jair Uribe
- Análisis / seguimiento: Tatiana Valcárcel Rodríguez

### Objetivo del requerimiento

Reemplazar la programación de turnos que hoy se hace en Excel (Contact Center, Soporte en sitio, Mesa de soporte técnico y Laboratorio) por un módulo de la Plataforma GRH que permita:

- parametrizar turnos, estados y catálogos por empresa y frente operativo;
- construir, validar y publicar mallas semanales o mensuales;
- gestionar novedades con trazabilidad;
- consultar quién está en turno o disponible;
- que el empleado vea su programación;
- generar y exportar las horas que Talento Humano / nómina requiere para el pago (sin liquidar dinero).

---

## 2. Entes afectados

- Operación Contact Center (supervisoras, coordinadores)
- Soporte en sitio / regionales / SPT
- Mesa de soporte técnico (analistas que consultan disponibilidad)
- Laboratorio (cobertura cruzada cuando aplique)
- Talento Humano / nómina (receptor de horas y cruce de novedades)
- Empleados operativos (consulta de su programación)
- Super-administración y administración de empresa GRH (módulo, plan, permisos)
- Gerencia de Soluciones Tecnológicas / equipo de desarrollo GRH

No incluido en esta necesidad (sesiones pendientes o fuera de alcance): mesa de segundo nivel y personal de fábrica.

---

## 3. Descripción del requerimiento

### Situación actual

Hoy cada frente arma su malla en Excel, con reglas y catálogos distintos, sin un sistema único ni trazabilidad formal.

Contact Center: las supervisoras construyen una malla mensual con turnos tipificados entre semana y en domingo/festivo; el coordinador revisa y la envía aproximadamente una semana antes del mes. Incluye marcaciones para vacaciones, festivos, campañas, breaks, almuerzos, rotación, asistencia a sede y cruce manual contra el formato de novedades de nómina. Se reportan horas extra festivas y recargo nocturno según cortes de nómina.

Soporte en sitio / Mesa / Laboratorio: Excel con varios turnos, programación por regional, zona y SPT (alrededor de 40 técnicos en Bogotá). Se envía el viernes y se modifica casi a diario por novedades. Un técnico puede cubrir dos turnos el mismo día (extras). Si alguien descansa sábado, se cubre con laboratorio o mesa. Jornada de referencia 42 h semanales. Mesa consulta en línea quién está en turno/zona/SPT para asignar casos. Estados típicos: DES, incapacidad, permiso, capacitación, actividad (no recibe casos).

El empleado no acepta el cambio: se le informa. No se versiona la malla completa: el cambio es puntual.

### Situación propuesta

Implementar el módulo Malla de Turnos en la Plataforma GRH, parametrizable por empresa y por frente operativo, reutilizando funcionarios, áreas, cargos, calendario/festivos, autenticación, notificaciones y línea de tiempo ya existentes.

El módulo debe permitir:

1. Integración al catálogo de módulos/submódulos, permisos y aislamiento por empresa.
2. Catálogos de frentes, plantillas de turno, estados de celda, campañas, territorio, modalidades, sitios, reglas de cobertura/compensatorio y motor de validación.
3. Construcción de malla (persona × día) con turno/estado, atributos opcionales, segundo turno, filtros, copia masiva y control de concurrencia.
4. Validación de conflictos, indicadores de cobertura y rotación híbrida (manual / asistida / automática) con simulación.
5. Ciclo de publicación: borrador → revisión → publicada / rechazada; edición controlada tras publicar según configuración del frente.
6. Novedades operativas, historial inmutable y notificación informativa al empleado (sin aceptación).
7. Consulta operativa (quién está en turno/disponible/cobertura del día) y vistas del empleado (propia y grupo según política).
8. Reportes de horas, exportación Excel/PDF, cruce con novedades TH e intercambio de turnos configurable (puede nacer deshabilitado).

Alcance documentado: épicas EP-00 a EP-09 e historias HU01 a HU81. Detalle funcional en GST-FM-04 del repositorio SharePoint del proyecto.

### Beneficios esperados

- Una sola herramienta en lugar de varios Excel desconectados.
- Menos errores de cobertura y de cruce con nómina.
- Trazabilidad de quién cambió un turno y por qué.
- El analista de mesa ve disponibilidad vigente, no un archivo del viernes.
- El empleado conoce su programación y los cambios sin depender del correo con el Excel completo.
- Horas listas para el corte de nómina, sin liquidar salarios (solo horas).
- Parametría por frente: Contact Center y Soporte conviven sin forzar el mismo catálogo.
- Construcción gobernada por permisos, publicación y reglas configurables (sin hardcoding de umbrales en el producto).

### Transacciones proyectadas – capacidad requerida

Volumen estimado (levantamiento 27/08/2026, sujeto a validación):

- Soporte en sitio: ~40 técnicos, varias regionales/SPT; cambios diarios de celda; consulta de disponibilidad en horario operativo (~06:00–21:00).
- Contact Center: malla mensual del grupo de operadores y supervisores; ajustes puntuales por novedad.
- Concurrencia: coordinadores/supervisoras editando; analistas de mesa consultando en paralelo.
- Grilla típica: decenas de personas × hasta 31 días.
- Histórico de cambios de celda: se conserva; no se sobrescribe.

La consulta “quién está ahora” debe reflejar el valor vigente de forma inmediata (segundos), no en el siguiente envío semanal. Cifras de picos transaccionales se cerrarán en diseño técnico.

Construcción orientativa: 9 sprints de 2 semanas (~18 semanas), equipo Fullstack + Backend + Frontend + QA.

---

## 5. Especificación del requerimiento

### Frontend

Necesidad de interfaz (negocio / diseño; detalle en GST-FM-04 y prototipos):

1. Parametrización: frentes, capacidades del frente, plantillas de turno (horario, color, medianoche, breaks), estados con flags, campañas, territorio, modalidades, sitios, restricciones, cortes, tipos de hora, reglas y motor de validación; importación asistida desde Excel.
2. Construcción: crear malla por periodo/frente, seleccionar grupo, grilla persona × días, asignar turno/estado/extra/atributos, filtros, copia masiva, fijar atributo por periodo.
3. Validación y rotación: indicadores de cobertura/equilibrio, conflictos, patrones, simulación, exclusiones, asistida, reequilibrio y ajuste manual.
4. Publicación: enviar a revisión, publicar, rechazar con motivo; editar publicada según configuración.
5. Novedades e historial: aplicar novedad, consultar historial por funcionario, notificaciones.
6. Consulta operativa: quién está en turno/disponible y cobertura del día.
7. Vista empleado: mi programación (día/semana/mes), programación del grupo según política, historial reciente.
8. Reportes: horas por tipo, export malla/cobertura, import/cruce TH, compensatorio.
9. Intercambio (si el frente lo habilita): solicitar, validar, aprobar/rechazar y aplicar.
10. No se requiere pantalla de indicadores de desempeño ni liquidación de nómina.

### Reglas de negocio

- RN-01. La malla operativa es distinta de la jornada contractual; no se mezcla con el dominio de jornada ya existente en GRH.
- RN-02. Toda información de negocio se aísla por empresa (multi-tenant).
- RN-03. El turno es plantilla reutilizable; la celda referencia la plantilla (o un estado), no redefine el catálogo.
- RN-04. Un empleado puede tener más de un turno el mismo día (slot extra); el solape horario indebido se impide o se valida según reglas.
- RN-05. Los atributos de celda (territorio, modalidad, sitio, campaña, etc.) se habilitan por configuración del frente.
- RN-06. Los estados definen comportamiento por flags (cuenta horas, asignable a casos, notifica, etc.), no por pantallas fijas por cada novedad.
- RN-07. Tras publicar, el cambio es puntual (no una versión completa nueva de toda la malla) y deja historial: valor anterior, nuevo, usuario, fecha y motivo.
- RN-08. El empleado no acepta el cambio; la notificación es informativa.
- RN-09. La edición y la consulta dependen de permisos de sección y del alcance de frentes del usuario/rol.
- RN-10. Nómina recibe horas (ordinaria, extra, festiva, recargo, etc. según catálogo), no el valor a pagar. Se respetan cortes de nómina.
- RN-11. Un recurso de otro frente/área puede cubrir el mismo día cuando la operación lo permita.
- RN-12. La visibilidad de la malla del grupo para el empleado depende de la política del frente.
- RN-13. Severidad de reglas (info / advertencia / bloqueo) es parametrizable; no se hardcodean umbrales de negocio en el producto.
- RN-14. El intercambio de turnos es opcional por frente (puede nacer deshabilitado).
- RN-15. Fuera de alcance de esta necesidad: liquidación en pesos, módulo completo de vacaciones/incapacidades TH, indicadores de desempeño, personal de fábrica, reportería gráfica avanzada corporativa.

### Backend

Necesidad de capacidades de servicio (no es diseño de APIs en este documento):

- Nuevo dominio de programación operativa (microservicio / BD propia), distinto de jornada contractual.
- Multi-tenant: mallas, catálogos y reportes por empresa.
- Reutilizar maestros de funcionario, área, cargo, calendario/festivos, usuarios/roles, notificaciones y timeline.
- Persistir frentes, plantillas, estados, reglas, mallas, celdas, historial, staging de importación TH e intercambio.
- Calcular horas por tipo según configuración, festivos y corte.
- Exponer consulta de asignación vigente para mesa y vistas de empleado.
- Autorización por rol/sección y por alcance de frente.
- Exportación Excel/PDF e importación asistida / cruce TH.
- El detalle de servicios, modelo de datos, GST-FM-03 y GST-FM-04 se elabora/valida con el backlog oficial del proyecto.

---

## 6. Reportes para operación y control

1. **Exportación de malla (Excel/PDF)**  
   Programación del periodo/frente con personas, días, turnos/estados y atributos habilitados.

2. **Reporte de horas del periodo**  
   Horas por tipo configurado (ordinaria, extra, festiva, recargo, etc.), por persona y/o frente, alineado a cortes de nómina.

3. **Horas de novedad vs operativas**  
   Separación de horas asociadas a novedades respecto de horas operativas.

4. **Cobertura del día / para terceros**  
   Cobertura por dimensiones habilitadas del frente (turno, sitio, territorio, etc.), exportable cuando se requiera entregar a terceros.

5. **Cruce con novedades TH**  
   Resultado del contraste entre programación y novedades importadas según plantilla parametrizada.

6. **Compensatorio en reporte**  
   Aplicación de reglas de compensatorio configuradas sobre el periodo reportado.

7. **Historial de cambios**  
   Consulta operativa/auditoría por funcionario o celda (quién cambió, cuándo, antes/después, motivo).

---

## 7. Requisitos de seguridad de la información

- Autenticación y sesión de la Plataforma GRH.
- Autorización por permisos de sección (crear/leer/actualizar/eliminar) y por alcance de frentes.
- Aislamiento estricto por empresa: un usuario no ve ni modifica datos de otra empresa.
- Trazabilidad de cambios relevantes en celdas (historial inmutable).
- Notificaciones solo a destinatarios autorizados / vinculados a la celda o rol.
- Exportaciones e importaciones sujetas a los mismos controles de permiso y tenant.
- Protección de la información en tránsito y de tokens/credenciales alineada a los estándares de la plataforma GRH:
  - **JWS** (JSON Web Signature) para firmar y verificar la integridad/autenticidad de tokens o mensajes firmados.
  - **AES-256** para cifrado simétrico de datos sensibles cuando aplique.
  - **HMAC** para integridad y autenticación de mensajes (p. ej. firmas de verificación asociadas a secretos compartidos).
- Datos de prueba preferiblemente no productivos u ofuscados (ver sección 8).
- Cumplir políticas internas de seguridad de la información de Datacenter / DCSAS aplicables a GRH.

---

## 8. Datos de prueba

En esta fase se solicita autorización del cliente sobre el tipo de datos para pruebas.

**Propuesta:**

- Ambientes de desarrollo y QA: datos de prueba / ofuscados (empresas y personas ficticias o anonimizadas), con catálogos y mallas representativos de Contact Center y Soporte.
- No usar datos reales de producción salvo autorización explícita y controlada.
- Para UAT / piloto: conjunto acotado de datos reales o semireales de un frente piloto, con permiso del sponsor/líder funcional.

Marcar en el Word la opción que autorice el cliente: **datos de producción** / **datos ofuscados o no reales** / **mixto para piloto**.

---

## 9. Aprobación

| Nombre | Rol / Cargo | Firma |
| ------ | ----------- | ----- |
| Ricardo Rojas Sierra | Líder funcional / Sponsor operativo | Pendiente de firma |
| Héctor Mauricio Coronado Gutiérrez | Líder técnico del proyecto | Pendiente de firma |
| Oscar Ariel Acuña Sánchez | Líder funcional Contact Center | Pendiente de firma (si aplica) |

Fecha de la solicitud: 07/09/2026  
(Levantamiento base: 27/08/2026. Actualización de alcance: propuesta épicas/HU v1.0 y backlog definitivo.)

---

## Cómo diligenciar el Word (paso a paso)

Archivo plantilla: `Malla-Turnos/GST-FM-02  FORMATO NECESIDAD DEL CLIENTE (2).docx`

1. Abre el Word vacío y guarda una copia, por ejemplo:  
   `GST-FM-02-REQ-MT-001-Malla-Turnos-v1.docx` (en `docs/` o en SharePoint de requerimientos).

2. **Tipo de requerimiento** (primera tabla)  
   Copia el texto de la sección 0 (o marca la casilla de “nuevo módulo / desarrollo” si el formato trae opciones).

3. **Datos del producto**  
   - Nombre producto/requerimiento → sección 1  
   - Sponsor / líderes → sección 1  
   - Objetivo → sección 1  

4. **Entes afectados**  
   Pega la lista de la sección 2 (viñetas o texto corrido).

5. **Descripción del requerimiento**  
   - Columna Situación actual → “Situación actual”  
   - Columna Situación propuesta → “Situación propuesta”  
   - Beneficios esperados → sección beneficios  
   - Transacciones / capacidad → sección transacciones  

6. **Especificación**  
   - FRONTEND → bloque Frontend  
   - REGLAS DE NEGOCIO → RN-01…RN-15  
   - BACKEND → bloque Backend  

7. **Reportes**  
   Pega los 7 reportes de la sección 6.

8. **Seguridad**  
   Pega la sección 7.

9. **Datos de prueba**  
   Completa la autorización debajo del texto estándar del formato usando la “Propuesta” de la sección 8.

10. **Aprobación**  
    Nombres, roles y deja firma en blanco / “Pendiente de firma”. Fecha 07/09/2026 (o la fecha real de radicación).

11. Revisa ortografía, quita referencias técnicas de más si el lector es 100 % negocio (opcional: en Backend puedes dejar solo el párrafo de capacidades sin nombres de microservicios).

12. Sube el Word firmado/listo a la carpeta de requerimientos del proyecto en SharePoint.

---

## Referencias internas (no pegar al cliente si no aplica)

- Propuesta: `docs/malla_turnos_propuesta.pdf`
- Backlog HU: `docs/Backlog definitivo/`
- Sprints: `docs/BACKLOG-SPRINTS-Malla-Turnos.xlsx` / `...-DETALLADO.xlsx`
- Historias GST-FM-04: carpeta SharePoint “Historias de usuario” del PRY Malla de turnos
