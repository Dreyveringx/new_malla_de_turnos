# Prototipo Figma Make — Malla de Turnos

Copia local del diseño interactivo generado en Figma Make:

https://www.figma.com/make/6JW2Cr9xieMOYNaekfFKvb/Módulo-Malla-de-Turnos

**No es el front de producción GRH** (Angular). Es un prototipo React + Vite para revisar pantallas S00–S42 alineadas a las HU.

## Requisitos

- Node.js 20+ (recomendado)

## Cómo correrlo

```bash
cd prototipo-figma
npm install
npm run dev
```

Abre http://localhost:5173

## Qué incluye

| Bloque | Pantallas | Contenido |
|--------|-----------|-----------|
| Hub | S00 | Entrada al módulo |
| A Parametrización | S01–S15 | Frentes, turnos, motor de reglas, import Excel |
| B Construcción | S16–S24 | Mallas, grilla, rotación, publicación |
| C Novedades / Consulta | S25–S29 | Novedades, historial, quién está, cobertura |
| D Mi programación | S30–S32 | Vista empleado |
| E Reportes | S33–S37 | Horas, export, cruce TH |
| F Intercambio | S38–S42 | EP-09 (OFF por defecto por frente) |

En la barra superior usa **Ver como** para cambiar el rol demo (coordinadora, coordinador, operador, TH, etc.).

## Notas

- Datos 100 % mock en `src/data.ts`.
- El `vite.config` de Figma Make usa plugins internos; aquí se reemplazó por Vite + React + Tailwind 4 estándar.
- Si Figma Make se actualiza, se puede volver a bajar el source y sobrescribir `src/`.
