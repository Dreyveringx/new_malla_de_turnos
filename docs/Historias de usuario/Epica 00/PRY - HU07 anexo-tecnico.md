# Anexo técnico — MT-EP00-HU07

Audiencia: desarrollo / arquitectura. No presentar al cliente.

## Event types sugeridos (códigos orientativos)

- MALLA_PUBLICADA
- MALLA_CELDA_CAMBIADA
- MALLA_NOVEDAD_APLICADA
- MALLA_INTERCAMBIO_SOLICITADA
- MALLA_INTERCAMBIO_RESUELTA

## Integración

- notification-service: dispatch EMAIL+POPUP
- audit timeline: hechos de alto nivel
- Historial de celda (HU62) = detalle de dominio append-only
- Idempotencia por business event key


---
*Generado 05/09/2026 con backlog definitivo v2.0.*
