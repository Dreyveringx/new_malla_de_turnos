/**
 * Genera la plantilla .xlsx en public/ para descarga directa (sin CSV).
 * Ejecutar: node scripts/generar-plantilla-importacion.mjs
 */
import ExcelJS from 'exceljs';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outPath = path.join(__dirname, '../public/Plantilla_Importacion_Catalogos_Malla_Turnos.xlsx');

const HEADER_FILL = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4A628A' } };
const HEADER_FONT = { bold: true, color: { argb: 'FFFFFFFF' }, size: 11, name: 'Calibri' };
const EXAMPLE_FILL = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF7FBFC' } };
const THIN = { style: 'thin', color: { argb: 'FFB8C4D4' } };
const BORDERS = { top: THIN, left: THIN, bottom: THIN, right: THIN };

const GROUP_FILLS = [
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD6E4F5' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD6F0F2' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD6F0F2' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD6F0F2' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD6F0F2' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFF0D6' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFF0D6' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFDDF5E5' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFDDF5E5' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFEDE4F8' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFEDE4F8' } },
  { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF0F0F0' } },
];

const HEADERS = [
  'Código frente',
  'Código turno',
  'Nombre del turno',
  'Hora inicio',
  'Hora fin',
  'Código estado',
  'Nombre del estado',
  'Código sitio',
  'Nombre del sitio',
  'Código modalidad',
  'Código campaña',
  'Nota / observación',
];

const HELP_ROW = [
  'Obligatorio. Ej: CC, SITIO, LAB',
  'Si define un turno',
  'Nombre visible del turno',
  'Formato 24h: 06:00',
  'Formato 24h: 14:00',
  'Si define un estado (DES, VAC…)',
  'Nombre visible del estado',
  'Si define un sitio',
  'Nombre del sitio de asistencia',
  'Ej: PRE, VIR, HIB',
  'Código de campaña (opcional)',
  'Texto libre opcional',
];

const EXAMPLE_ROWS = [
  ['CC', 'T1', 'Mañana estándar', '06:00', '14:00', '', '', '', '', 'PRE', '', 'Ejemplo: solo turno + modalidad'],
  ['CC', 'T5', 'Tarde', '14:00', '22:00', '', '', '', '', 'VIR', '', 'Turno tarde virtual'],
  ['CC', '', '', '', '', 'DES', 'Descanso', '', '', '', '', 'Ejemplo: solo estado (sin turno)'],
  ['CC', '', '', '', '', 'VAC', 'Vacaciones', '', '', '', '', 'Estado de ausencia'],
  ['SITIO', 'T8', 'Jornada sitio', '08:00', '17:00', '', '', 'S01', 'Elemento', 'PRE', '', 'Turno + sitio + modalidad'],
  ['LAB', 'T1', 'Lab mañana', '07:00', '15:00', '', '', 'S04', 'Laboratorio Bogotá', 'PRE', 'CAN', 'Con campaña opcional'],
];

const wb = new ExcelJS.Workbook();
wb.creator = 'Malla de Turnos · GRH';
wb.created = new Date();
wb.title = 'Plantilla importación catálogos — Malla de Turnos';

// —— Instrucciones ——
{
  const ws = wb.addWorksheet('1. Instrucciones', { properties: { tabColor: { argb: 'FF4A628A' } } });
  ws.getColumn(1).width = 96;
  ws.getRow(1).getCell(1).value = 'Plantilla de importación — Catálogos Malla de Turnos';
  ws.getRow(1).getCell(1).font = { bold: true, size: 16, color: { argb: 'FF4A628A' }, name: 'Calibri' };
  ws.getRow(1).height = 28;
  ws.getRow(2).getCell(1).value =
    'Módulo GRH · Importación asistida (HU27) · El Excel NO es la base de datos: solo sirve para descubrir catálogos.';
  ws.getRow(2).getCell(1).font = { size: 11, italic: true, color: { argb: 'FF5A6A7A' }, name: 'Calibri' };

  const lines = [
    '',
    '¿Para qué sirve este archivo?',
    'Para cargar de forma asistida turnos, estados, sitios, modalidades y campañas de un frente. El sistema leerá las columnas, detectará valores nuevos y te pedirá confirmarlos antes de crearlos.',
    '',
    'Cómo usarlo (paso a paso)',
    '1. Abre la hoja «2. Datos a importar».',
    '2. No borres ni renombres la fila 1 (encabezados). Son los nombres de columna que el sistema espera.',
    '3. La fila 2 es solo una guía (colores por grupo): puedes dejarla o borrarla; no se importa.',
    '4. A partir de la fila 3 escribe tus datos. Puedes borrar las filas de ejemplo y poner las tuyas.',
    '5. Cada fila puede definir un turno, un estado, un sitio, o una combinación. Deja en blanco lo que no aplique.',
    '6. Guarda el archivo como .xlsx y súbelo en la pantalla de Importación asistida.',
    '',
    'Reglas importantes',
    '• Código frente es obligatorio en cada fila.',
    '• Horas en formato 24 horas (06:00, 14:00, 22:00). Si el turno cruza medianoche, indícalo en la Nota.',
    '• No mezcles en la misma celda varios códigos (un valor por celda).',
    '• No uses este archivo para nómina ni liquidación en pesos.',
    '• No es un espejo de la malla operativa: tras importar, los catálogos viven en el sistema.',
    '',
    'Hojas de este libro',
    '• 1. Instrucciones — esta guía.',
    '• 2. Datos a importar — completa aquí (hoja principal).',
    '• 3. Leyenda de columnas — significado de cada columna y colores.',
  ];
  lines.forEach((t, i) => {
    const row = ws.getRow(4 + i);
    const bold = t.startsWith('¿') || t.startsWith('Cómo') || t.startsWith('Reglas') || t.startsWith('Hojas');
    row.getCell(1).value = t;
    row.getCell(1).font = {
      bold,
      size: bold ? 12 : 11,
      color: { argb: bold ? 'FF1F2A37' : 'FF334155' },
      name: 'Calibri',
    };
    row.getCell(1).alignment = { wrapText: true, vertical: 'top' };
    if (t.length > 90) row.height = 38;
  });
}

// —— Datos ——
{
  const ws = wb.addWorksheet('2. Datos a importar', {
    properties: { tabColor: { argb: 'FF78D1D7' } },
    views: [{ state: 'frozen', ySplit: 1 }],
  });
  [16, 14, 22, 12, 12, 14, 20, 14, 22, 16, 16, 36].forEach((w, i) => {
    ws.getColumn(i + 1).width = w;
  });

  const headerRow = ws.getRow(1);
  HEADERS.forEach((h, i) => {
    const cell = headerRow.getCell(i + 1);
    cell.value = h;
    cell.fill = HEADER_FILL;
    cell.font = HEADER_FONT;
    cell.border = BORDERS;
    cell.alignment = { vertical: 'middle', horizontal: 'center', wrapText: true };
  });
  headerRow.height = 32;

  const helpRow = ws.getRow(2);
  HELP_ROW.forEach((h, i) => {
    const cell = helpRow.getCell(i + 1);
    cell.value = h;
    cell.fill = GROUP_FILLS[i];
    cell.font = { italic: true, size: 9, color: { argb: 'FF4B5563' }, name: 'Calibri' };
    cell.border = BORDERS;
    cell.alignment = { wrapText: true, vertical: 'top' };
  });
  helpRow.height = 42;

  EXAMPLE_ROWS.forEach((vals, rIdx) => {
    const row = ws.getRow(3 + rIdx);
    vals.forEach((v, cIdx) => {
      const cell = row.getCell(cIdx + 1);
      cell.value = v;
      cell.fill = EXAMPLE_FILL;
      cell.font = { size: 10, name: 'Calibri' };
      cell.border = BORDERS;
      cell.alignment = { vertical: 'middle' };
    });
  });

  for (let r = 0; r < 10; r++) {
    const row = ws.getRow(3 + EXAMPLE_ROWS.length + r);
    HEADERS.forEach((_, cIdx) => {
      row.getCell(cIdx + 1).border = BORDERS;
    });
  }

  const noteRow = ws.getRow(3 + EXAMPLE_ROWS.length + 11);
  noteRow.getCell(1).value =
    'Tip: borra las filas de ejemplo (3–8) si no las necesitas. Deja vacías las columnas que no apliquen. No renombres los encabezados de la fila 1.';
  noteRow.getCell(1).font = { italic: true, size: 9, color: { argb: 'FF6B7280' }, name: 'Calibri' };
  ws.mergeCells(noteRow.number, 1, noteRow.number, HEADERS.length);
}

// —— Leyenda ——
{
  const ws = wb.addWorksheet('3. Leyenda de columnas', { properties: { tabColor: { argb: 'FF9CA3AF' } } });
  ws.getColumn(1).width = 22;
  ws.getColumn(2).width = 14;
  ws.getColumn(3).width = 58;
  ws.getColumn(4).width = 16;

  ['Columna', 'Grupo', 'Qué debes escribir', '¿Obligatoria?'].forEach((t, i) => {
    const cell = ws.getRow(1).getCell(i + 1);
    cell.value = t;
    cell.fill = HEADER_FILL;
    cell.font = HEADER_FONT;
    cell.border = BORDERS;
  });

  const rows = [
    ['Código frente', 'Frente', 'Código del frente operativo (ej. CC).', 'Sí', 'FFD6E4F5'],
    ['Código turno', 'Turno', 'Código corto del turno (ej. T1, T5).', 'Si creas turno', 'FFD6F0F2'],
    ['Nombre del turno', 'Turno', 'Nombre que verán en la grilla.', 'Si creas turno', 'FFD6F0F2'],
    ['Hora inicio', 'Turno', 'Hora de inicio en 24h (HH:MM).', 'Si creas turno', 'FFD6F0F2'],
    ['Hora fin', 'Turno', 'Hora de fin en 24h (HH:MM).', 'Si creas turno', 'FFD6F0F2'],
    ['Código estado', 'Estado', 'Código de estado (DES, VAC, INC…).', 'Si creas estado', 'FFFFF0D6'],
    ['Nombre del estado', 'Estado', 'Nombre visible del estado.', 'Si creas estado', 'FFFFF0D6'],
    ['Código sitio', 'Sitio', 'Código del sitio de asistencia.', 'Si creas sitio', 'FFDDF5E5'],
    ['Nombre del sitio', 'Sitio', 'Nombre / dirección corta.', 'Si creas sitio', 'FFDDF5E5'],
    ['Código modalidad', 'Modalidad', 'PRE, VIR, HIB u otro código.', 'No', 'FFEDE4F8'],
    ['Código campaña', 'Campaña', 'Código de campaña (si aplica).', 'No', 'FFEDE4F8'],
    ['Nota / observación', 'Nota', 'Texto libre opcional.', 'No', 'FFF0F0F0'],
  ];

  rows.forEach((r, idx) => {
    const row = ws.getRow(2 + idx);
    r.slice(0, 4).forEach((val, c) => {
      const cell = row.getCell(c + 1);
      cell.value = val;
      cell.border = BORDERS;
      cell.font = { size: 10, name: 'Calibri', bold: c === 0 };
      cell.alignment = { wrapText: true, vertical: 'middle' };
      if (c === 1) cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: r[4] } };
    });
    row.height = 28;
  });

  ws.getRow(16).getCell(1).value =
    'Colores: azul = frente · celeste = turno · ámbar = estado · verde = sitio · lila = modalidad/campaña · gris = nota.';
  ws.getRow(16).getCell(1).font = { italic: true, size: 10, color: { argb: 'FF4B5563' } };
  ws.mergeCells(16, 1, 16, 4);
}

fs.mkdirSync(path.dirname(outPath), { recursive: true });
const buffer = await wb.xlsx.writeBuffer();
fs.writeFileSync(outPath, Buffer.from(buffer));
console.log('Escrito:', outPath, `(${buffer.byteLength} bytes)`);
