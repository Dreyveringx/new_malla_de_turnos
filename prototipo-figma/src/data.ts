// ─── Types ────────────────────────────────────────────────────────────────────

export type MallaEstado = 'borrador' | 'revision' | 'publicada' | 'rechazada';
export type ModoArmado = 'manual' | 'asistido' | 'automatico';
export type Modalidad = 'presencial' | 'virtual' | 'hibrido';
export type Severidad = 'info' | 'advertencia' | 'bloqueo';
export type Rol = 'coordinadora_cc' | 'coordinador' | 'analista_mesa' | 'operador' | 'th_nomina';

export interface Frente {
  id: string;
  nombre: string;
  descripcion?: string;
  modo: ModoArmado;
  periodo: 'semana' | 'mes';
  mallaPublicadaEditable: boolean;
  responsableArma: string;
  responsablePublica: string;
  usaTerritorioZona: boolean;
  usaCampanas: boolean;
  usaModalidad: boolean;
  intercambioActivo: boolean;
  activo: boolean;
}

export interface Persona {
  id: string;
  nombre: string;
  iniciales: string;
  cargo: string;
  frenteId: string;
  zona?: string;
}

export interface TurnoPlantilla {
  codigo: string;
  nombre: string;
  inicio: string;
  fin: string;
  tipo: 'manana' | 'tarde' | 'noche' | 'transversal';
  colorClass: string;
  nocturno: boolean;
  frenteId: string;
  activo: boolean;
  dias: string;
}

export interface EstadoCelda {
  codigo: string;
  nombre: string;
  sumaHoras: boolean;
  asignable: boolean; // asignable a casos
  colorClass: string;
  activo: boolean;
}

export interface ReglaCelda {
  codigo: string;
  nombre: string;
  descripcion?: string; // alias of nombre for new screens
  alcance: 'empresa' | 'frente';
  frenteId?: string;
  parametro?: string; // valor editable, ej. "42" o "3"
  unidad?: string;
  severidad: Severidad;
  prioridad: number;
  activo: boolean;
}

export interface Campana {
  id: string;
  nombre: string;
  codigo: string;
  frenteId: string;
  activo: boolean;
}

export interface Sitio {
  id: string;
  nombre: string;
  direccion: string;
  activo: boolean;
}

export interface TerritoriNodo {
  id: string;
  nivel: number;
  nombreNivel: string;
  nombre: string;
  padreId?: string;
}

export interface Malla {
  id: string;
  nombre: string;
  frenteId: string;
  frenteNombre: string;
  periodo: string;
  estado: MallaEstado;
  modo: ModoArmado;
  responsable: string;
  actualizado: string;
  motivoRechazo?: string;
  fechaCreacion?: string;
  fechaPublicacion?: string;
}

export interface GrillaCell {
  turno?: string;
  estado?: string;
  modalidad?: Modalidad;
  sitio?: string;
  zona?: string;
  campana?: string;
  nota?: string;
  extra?: boolean;
}

export type GrillaData = Record<string, Record<string, GrillaCell>>;

export interface HistorialEntry {
  id: string;
  fecha: string;
  usuario: string;
  valorAntes: string;
  valorDespues: string;
  motivo: string;
  origen: 'manual' | 'automatico' | 'novedad' | 'intercambio';
}

export interface Conflicto {
  tipo: 'advertencia' | 'bloqueo';
  severidad?: 'advertencia' | 'bloqueo'; // alias for tipo
  codigoRegla: string;
  mensaje: string;
  persona?: string;
  fecha?: string;
}

export interface SolicitudIntercambio {
  id: string;
  solicitanteId: string;
  solicitante: string;
  receptorId: string;
  receptor: string;
  fechaOrigen: string;
  turnoOrigen: string;
  fechaDestino: string;
  turnoDestino: string;
  frenteId: string;
  estado: 'pendiente' | 'aprobada' | 'rechazada' | 'aplicada';
  motivoRechazo?: string;
  motivo?: string;
  fechaSolicitud: string;
  // New fields for SF screens
  solicitanteNombre?: string;
  contraparteNombre?: string;
  diaOrigen?: string;
  diaDestino?: string;
  advertencias?: string[];
}

// ─── Roles y permisos (simula GRH: menú = plan ∩ LEER por submódulo) ───────────

export type PermisoCrud = 'CREAR' | 'LEER' | 'ACTUALIZAR' | 'ELIMINAR';
export type SubmoduloId =
  | 'parametrizacion'
  | 'construccion'
  | 'consulta-operativa'
  | 'mi-programacion'
  | 'reportes';

export interface SubmoduloPage {
  screen: string;
  label: string;
  isNew?: boolean;
  /** Si true, solo se muestra cuando el frente tiene esa capacidad */
  requiereCapacidad?: 'usaCampanas' | 'usaTerritorioZona' | 'usaModalidad';
}

/** Scope de navegación interna tras el dashboard de frentes. */
export type NavScope = 'dashboard' | 'empresa' | 'frente';
export const EMPRESA_SCOPE = '__EMPRESA__';

export const ICONOS_FRENTE: Record<string, string> = {
  CC: '🎧',
  SITIO: '🛠️',
  MESA: '🖥️',
  LAB: '🔬',
};

/** Los 5 submódulos de menú (HU01). Pantallas Sxx = navegación interna, no ítems RBAC. */
export const SUBMODULOS_MALLA: {
  id: SubmoduloId;
  label: string;
  icon: string;
  route: string;
  entryScreen: string;
  desc: string;
  /** true = primero elige frente (o Empresa) antes de ver tabs */
  usaDashboardFrente?: boolean;
  pages: SubmoduloPage[];
  pagesEmpresa?: SubmoduloPage[];
  pagesFrente?: SubmoduloPage[];
}[] = [
  {
    id: 'parametrizacion',
    label: 'Parametrización',
    icon: '⚙️',
    route: 'malla-turnos/main/parametrizacion',
    entryScreen: 'S0D',
    desc: 'Catálogos del módulo: frentes, turnos, estados, reglas…',
    usaDashboardFrente: true,
    pagesEmpresa: [
      { screen: 'S0P', label: 'Guía de arranque', isNew: true },
      { screen: 'S01', label: 'Frentes operativos' },
      { screen: 'S05', label: 'Estados de celda' },
      { screen: 'S11', label: 'Festivos · Cortes · Horas' },
      { screen: 'S15', label: 'Importación Excel', isNew: true },
    ],
    pagesFrente: [
      { screen: 'S02', label: 'Configuración' },
      { screen: 'S03', label: 'Plantillas de turno' },
      { screen: 'S08', label: 'Modalidades', requiereCapacidad: 'usaModalidad' },
      { screen: 'S09', label: 'Sitios de asistencia' },
      { screen: 'S06', label: 'Campañas / tareas', requiereCapacidad: 'usaCampanas' },
      { screen: 'S07', label: 'Territorio (SPT…)', requiereCapacidad: 'usaTerritorioZona' },
      { screen: 'S10', label: 'Restricciones' },
      { screen: 'S12', label: 'Cobertura / compensatorio' },
      { screen: 'S13', label: 'Motor de reglas', isNew: true },
    ],
    // Unión para lookup de pantallas (no se muestran todas a la vez)
    pages: [
      { screen: 'S0D', label: 'Dashboard frentes' },
      { screen: 'S0P', label: 'Guía de arranque' },
      { screen: 'S01', label: 'Frentes' },
      { screen: 'S02', label: 'Configuración' },
      { screen: 'S03', label: 'Plantillas' },
      { screen: 'S04', label: 'Horario turno' },
      { screen: 'S05', label: 'Estados' },
      { screen: 'S06', label: 'Campañas' },
      { screen: 'S07', label: 'Territorio' },
      { screen: 'S08', label: 'Modalidades' },
      { screen: 'S09', label: 'Sitios' },
      { screen: 'S10', label: 'Restricciones' },
      { screen: 'S11', label: 'Festivos' },
      { screen: 'S12', label: 'Cobertura' },
      { screen: 'S13', label: 'Motor' },
      { screen: 'S15', label: 'Importación' },
    ],
  },
  {
    id: 'construccion',
    label: 'Construcción',
    icon: '🗓️',
    route: 'malla-turnos/main/construccion',
    entryScreen: 'S16',
    desc: 'Mallas, grilla, rotación, publicación e intercambio (aprobación)',
    pages: [
      { screen: 'S16', label: 'Lista de mallas' },
      { screen: 'S17', label: 'Crear malla' },
      { screen: 'S18', label: 'Grilla operativa' },
      { screen: 'S20', label: 'Cobertura y conflictos' },
      { screen: 'S21', label: 'Patrones de rotación' },
      { screen: 'S22', label: 'Simular / Aplicar rotación' },
      { screen: 'S24', label: 'Publicación' },
      { screen: 'S38', label: 'Config. intercambio', isNew: true },
      { screen: 'S40', label: 'Validar intercambio', isNew: true },
      { screen: 'S41', label: 'Aprobar / rechazar', isNew: true },
      { screen: 'S42', label: 'Auditoría intercambio', isNew: true },
    ],
  },
  {
    id: 'consulta-operativa',
    label: 'Consulta operativa',
    icon: '🔍',
    route: 'malla-turnos/main/consulta-operativa',
    entryScreen: 'S28',
    desc: 'Novedades, historial, quién está y cobertura del día',
    pages: [
      { screen: 'S25', label: 'Novedad en celda' },
      { screen: 'S26', label: 'Historial de celda' },
      { screen: 'S27', label: 'Historial por funcionario' },
      { screen: 'S28', label: 'Quién está / Disponible' },
      { screen: 'S29', label: 'Cobertura del día' },
    ],
  },
  {
    id: 'mi-programacion',
    label: 'Mi programación',
    icon: '👤',
    route: 'malla-turnos/main/mi-programacion',
    entryScreen: 'S30',
    desc: 'Vista del grupo, mi turno y solicitud de intercambio',
    pages: [
      { screen: 'S30', label: 'Programación del grupo' },
      { screen: 'S31', label: 'Mi programación' },
      { screen: 'S32', label: 'Historial de mis turnos' },
      { screen: 'S39', label: 'Solicitar intercambio', isNew: true },
      { screen: 'S43', label: 'Mis solicitudes', isNew: true },
    ],
  },
  {
    id: 'reportes',
    label: 'Reportes',
    icon: '📊',
    route: 'malla-turnos/main/reportes',
    entryScreen: 'S33',
    desc: 'Horas (sin pesos), exportación y cruce TH',
    pages: [
      { screen: 'S33', label: 'Horas del periodo' },
      { screen: 'S34', label: 'Exportar Excel / PDF' },
      { screen: 'S35', label: 'Dashboard cobertura' },
      { screen: 'S36', label: 'Cobertura terceros' },
      { screen: 'S37', label: 'Cruce vs novedades TH' },
    ],
  },
];

/** Tabs visibles según dashboard: Empresa vs frente (capacidades). */
export function tabsDelSubmodulo(smId: SubmoduloId, frenteCtx: string | null, frentes: Frente[]): SubmoduloPage[] {
  const sm = SUBMODULOS_MALLA.find(s => s.id === smId);
  if (!sm) return [];
  if (!sm.usaDashboardFrente) return sm.pages;
  if (!frenteCtx) return [];
  if (frenteCtx === EMPRESA_SCOPE) return sm.pagesEmpresa ?? [];
  const frente = frentes.find(f => f.id === frenteCtx);
  return (sm.pagesFrente ?? []).filter(p => {
    if (!p.requiereCapacidad || !frente) return true;
    return !!frente[p.requiereCapacidad];
  });
}
/** Matriz demo = lo que en GRH vive en permission_submodules por rol de empresa. */
export const ROLE_SUBMODULE_PERMS: Record<Rol, Partial<Record<SubmoduloId, PermisoCrud[]>>> = {
  coordinadora_cc: {
    parametrizacion: ['LEER', 'CREAR', 'ACTUALIZAR'],
    construccion: ['LEER', 'CREAR', 'ACTUALIZAR'],
    'consulta-operativa': ['LEER', 'CREAR', 'ACTUALIZAR'],
    'mi-programacion': ['LEER'],
    reportes: ['LEER'],
  },
  coordinador: {
    parametrizacion: ['LEER', 'ACTUALIZAR'],
    construccion: ['LEER', 'CREAR', 'ACTUALIZAR', 'ELIMINAR'],
    'consulta-operativa': ['LEER', 'CREAR', 'ACTUALIZAR'],
    'mi-programacion': ['LEER'],
    reportes: ['LEER', 'CREAR', 'ACTUALIZAR'],
  },
  analista_mesa: {
    'consulta-operativa': ['LEER'],
    'mi-programacion': ['LEER'],
  },
  operador: {
    'mi-programacion': ['LEER', 'CREAR'],
  },
  th_nomina: {
    reportes: ['LEER', 'CREAR'],
  },
};

export const ROLES: { id: Rol; label: string; desc: string }[] = [
  { id: 'coordinadora_cc', label: 'Coordinadora CC', desc: 'Parametriza y arma borrador; no publica' },
  { id: 'coordinador', label: 'Coordinador', desc: 'Publica, conflictos, reportes, aprueba intercambio' },
  { id: 'analista_mesa', label: 'Analista de mesa', desc: 'Solo LEER en Consulta y Mi programación' },
  { id: 'operador', label: 'Operador/Técnico', desc: 'Solo Mi programación (+ solicitar intercambio)' },
  { id: 'th_nomina', label: 'TH / Nómina', desc: 'Solo Reportes (exportar horas)' },
];

export function submoduloDePantalla(screen: string): SubmoduloId | null {
  if (screen === 'S00' || screen === 'home') return null;
  if (screen === 'S0D' || screen === 'S0P') return 'parametrizacion';
  for (const sm of SUBMODULOS_MALLA) {
    if (sm.pages.some(p => p.screen === screen) || sm.entryScreen === screen) return sm.id;
    if (sm.pagesEmpresa?.some(p => p.screen === screen)) return sm.id;
    if (sm.pagesFrente?.some(p => p.screen === screen)) return sm.id;
  }
  const n = parseInt(screen.replace('S', ''), 10);
  if (Number.isNaN(n)) return null;
  if (n >= 1 && n <= 15) return 'parametrizacion';
  if (n >= 16 && n <= 24) return 'construccion';
  if (n >= 25 && n <= 29) return 'consulta-operativa';
  if (n >= 30 && n <= 32) return 'mi-programacion';
  if (n >= 33 && n <= 37) return 'reportes';
  if (n === 39) return 'mi-programacion';
  if (n >= 38 && n <= 42) return 'construccion';
  return null;
}

export function permisosSubmodulo(rol: Rol, subId: SubmoduloId): PermisoCrud[] {
  return ROLE_SUBMODULE_PERMS[rol]?.[subId] ?? [];
}

export function puedeLeerSubmodulo(rol: Rol, subId: SubmoduloId): boolean {
  return permisosSubmodulo(rol, subId).includes('LEER');
}

export function puedeAccionSubmodulo(rol: Rol, subId: SubmoduloId, accion: PermisoCrud): boolean {
  return permisosSubmodulo(rol, subId).includes(accion);
}

export function submodulosVisibles(rol: Rol) {
  return SUBMODULOS_MALLA.filter(sm => puedeLeerSubmodulo(rol, sm.id));
}

export function puedeVerPantalla(rol: Rol, screen: string): boolean {
  if (screen === 'S00' || screen === 'home') return true;
  const sm = submoduloDePantalla(screen);
  return sm ? puedeLeerSubmodulo(rol, sm) : false;
}

/** Compat con pantallas existentes (editar = ACTUALIZAR en Construcción o Parametrización). */
export function puedeEditar(rol: Rol): boolean {
  return (
    puedeAccionSubmodulo(rol, 'construccion', 'ACTUALIZAR') ||
    puedeAccionSubmodulo(rol, 'parametrizacion', 'ACTUALIZAR') ||
    puedeAccionSubmodulo(rol, 'consulta-operativa', 'ACTUALIZAR')
  );
}
export function puedePublicar(rol: Rol): boolean {
  return rol === 'coordinador' && puedeAccionSubmodulo(rol, 'construccion', 'ACTUALIZAR');
}
export function puedeVerReportes(rol: Rol): boolean {
  return puedeLeerSubmodulo(rol, 'reportes');
}
export function puedeExportar(rol: Rol): boolean {
  return puedeAccionSubmodulo(rol, 'reportes', 'CREAR') || puedeAccionSubmodulo(rol, 'reportes', 'ACTUALIZAR');
}

// ─── Demo: Frentes (catálogo CRUD, no enum fijo) ──────────────────────────────

export const FRENTES: Frente[] = [
  {
    id: 'CC',
    nombre: 'Contact Center',
    descripcion: 'Atención telefónica y chat — operación 24/7',
    modo: 'asistido',
    periodo: 'mes',
    mallaPublicadaEditable: true,
    responsableArma: 'Supervisora CC',
    responsablePublica: 'Coordinador CC',
    usaTerritorioZona: false,
    usaCampanas: true,
    usaModalidad: true,
    intercambioActivo: false,
    activo: true,
  },
  {
    id: 'SITIO',
    nombre: 'Soporte en sitio',
    descripcion: 'Técnicos desplazados a clientes y SPT',
    modo: 'automatico',
    periodo: 'semana',
    mallaPublicadaEditable: true,
    responsableArma: 'Coordinador de sitio',
    responsablePublica: 'Coordinador de sitio',
    usaTerritorioZona: true,
    usaCampanas: false,
    usaModalidad: true,
    intercambioActivo: false,
    activo: true,
  },
  {
    id: 'MESA',
    nombre: 'Mesa de servicio',
    descripcion: 'Soporte nivel 1 y 2 — presencial e híbrido',
    modo: 'manual',
    periodo: 'semana',
    mallaPublicadaEditable: true,
    responsableArma: 'Coordinador de mesa',
    responsablePublica: 'Coordinador de mesa',
    usaTerritorioZona: false,
    usaCampanas: false,
    usaModalidad: false,
    intercambioActivo: false,
    activo: true,
  },
  {
    id: 'LAB',
    nombre: 'Laboratorio',
    descripcion: 'Pruebas, mantenimiento y certificación de equipos',
    modo: 'manual',
    periodo: 'semana',
    mallaPublicadaEditable: false,
    responsableArma: 'Coordinador de laboratorio',
    responsablePublica: 'Coordinador de laboratorio',
    usaTerritorioZona: false,
    usaCampanas: false,
    usaModalidad: false,
    intercambioActivo: false,
    activo: true,
  },
];

// ─── Demo: Personas ────────────────────────────────────────────────────────────

export const PERSONAS_CC: Persona[] = [
  { id: 'p1', nombre: 'Laura Méndez', iniciales: 'LM', cargo: 'Agente Contact Center', frenteId: 'CC' },
  { id: 'p2', nombre: 'Camilo Restrepo', iniciales: 'CR', cargo: 'Agente Contact Center', frenteId: 'CC' },
  { id: 'p3', nombre: 'Diana López', iniciales: 'DL', cargo: 'Analista Senior', frenteId: 'CC' },
  { id: 'p4', nombre: 'Andrés Peña', iniciales: 'AP', cargo: 'Agente Contact Center', frenteId: 'CC' },
  { id: 'p5', nombre: 'Natalia Cruz', iniciales: 'NC', cargo: 'Coordinadora turno', frenteId: 'CC' },
];

export const PERSONAS_SITIO: Persona[] = [
  { id: 'p6', nombre: 'Jennifer Ruiz', iniciales: 'JR', cargo: 'Técnico de soporte', frenteId: 'SITIO', zona: 'Zona Norte' },
  { id: 'p7', nombre: 'Héctor Molina', iniciales: 'HM', cargo: 'Técnico especialista', frenteId: 'SITIO', zona: 'SPT Restrepo' },
  { id: 'p8', nombre: 'Luis Suárez', iniciales: 'LS', cargo: 'Técnico de soporte', frenteId: 'SITIO', zona: 'Zona Norte' },
];

export const PERSONAS_MESA: Persona[] = [
  { id: 'p9', nombre: 'Carolina Vargas', iniciales: 'CV', cargo: 'Analista Mesa', frenteId: 'MESA' },
  { id: 'p10', nombre: 'Felipe Torres', iniciales: 'FT', cargo: 'Analista Mesa', frenteId: 'MESA' },
];

export const TODAS_PERSONAS = [...PERSONAS_CC, ...PERSONAS_SITIO, ...PERSONAS_MESA];

// ─── Demo: Turnos ─────────────────────────────────────────────────────────────

export const TURNOS: TurnoPlantilla[] = [
  { codigo: 'T1', nombre: 'Mañana A', inicio: '06:00', fin: '14:00', tipo: 'manana', colorClass: 'turno-T1', nocturno: false, frenteId: 'CC', activo: true, dias: 'Lun–Dom' },
  { codigo: 'T2', nombre: 'Mañana B', inicio: '07:00', fin: '15:00', tipo: 'manana', colorClass: 'turno-T1', nocturno: false, frenteId: 'CC', activo: true, dias: 'Lun–Vie' },
  { codigo: 'T3', nombre: 'Mañana C', inicio: '08:00', fin: '16:00', tipo: 'manana', colorClass: 'turno-T1', nocturno: false, frenteId: 'CC', activo: true, dias: 'Lun–Sáb' },
  { codigo: 'T4', nombre: 'Mediodía', inicio: '10:00', fin: '18:00', tipo: 'manana', colorClass: 'turno-T1', nocturno: false, frenteId: 'CC', activo: true, dias: 'Lun–Vie' },
  { codigo: 'T5', nombre: 'Tarde A', inicio: '14:00', fin: '22:00', tipo: 'tarde', colorClass: 'turno-T5', nocturno: false, frenteId: 'CC', activo: true, dias: 'Lun–Dom' },
  { codigo: 'T6', nombre: 'Tarde B', inicio: '15:00', fin: '23:00', tipo: 'tarde', colorClass: 'turno-T5', nocturno: false, frenteId: 'CC', activo: true, dias: 'Lun–Sáb' },
  { codigo: 'T7', nombre: 'Tarde C', inicio: '12:00', fin: '20:00', tipo: 'tarde', colorClass: 'turno-T5', nocturno: false, frenteId: 'CC', activo: true, dias: 'Lun–Vie' },
  { codigo: 'T8', nombre: 'Especial flexible', inicio: '07:00', fin: '15:30', tipo: 'manana', colorClass: 'turno-T8', nocturno: false, frenteId: 'CC', activo: true, dias: 'L–J 07–15:30 / V 07–16:00' },
  { codigo: 'T9', nombre: 'Fin de semana', inicio: '08:00', fin: '16:00', tipo: 'transversal', colorClass: 'turno-T8', nocturno: false, frenteId: 'CC', activo: true, dias: 'Sáb–Dom' },
  { codigo: 'TN1', nombre: 'Noche A', inicio: '22:00', fin: '06:00', tipo: 'noche', colorClass: 'turno-T5', nocturno: true, frenteId: 'CC', activo: true, dias: 'Lun–Dom' },
  { codigo: 'TN2', nombre: 'Noche B', inicio: '21:00', fin: '05:00', tipo: 'noche', colorClass: 'turno-T5', nocturno: true, frenteId: 'CC', activo: true, dias: 'Lun–Vie' },
  { codigo: 'T12', nombre: '12 horas', inicio: '07:00', fin: '19:00', tipo: 'transversal', colorClass: 'turno-T8', nocturno: false, frenteId: 'CC', activo: true, dias: 'Lun–Dom (ciclo)' },
  { codigo: 'TS1', nombre: 'Turno Sitio Día', inicio: '08:00', fin: '17:00', tipo: 'transversal', colorClass: 'turno-T1', nocturno: false, frenteId: 'SITIO', activo: true, dias: 'Lun–Sáb' },
  { codigo: 'TS2', nombre: 'Turno Sitio Noche', inicio: '20:00', fin: '06:00', tipo: 'noche', colorClass: 'turno-T5', nocturno: true, frenteId: 'SITIO', activo: true, dias: 'Lun–Dom' },
];

// ─── Demo: Estados ────────────────────────────────────────────────────────────
// CAP y ACT: asignable=false (NO se pueden asignar a casos mientras están en este estado)

export const ESTADOS_CELDA: EstadoCelda[] = [
  { codigo: 'DES', nombre: 'Descanso', sumaHoras: false, asignable: false, colorClass: 'turno-DES', activo: true },
  { codigo: 'INC', nombre: 'Incapacidad', sumaHoras: false, asignable: false, colorClass: 'turno-INC', activo: true },
  { codigo: 'VAC', nombre: 'Vacaciones', sumaHoras: false, asignable: false, colorClass: 'turno-VAC', activo: true },
  { codigo: 'PER', nombre: 'Permiso', sumaHoras: false, asignable: false, colorClass: 'turno-PER', activo: true },
  { codigo: 'CAP', nombre: 'Capacitación', sumaHoras: true, asignable: false, colorClass: 'turno-CAP', activo: true },
  { codigo: 'ACT', nombre: 'Actividad', sumaHoras: true, asignable: false, colorClass: 'turno-ACT', activo: true },
  { codigo: 'COM', nombre: 'Compensatorio', sumaHoras: false, asignable: false, colorClass: 'turno-COM', activo: true },
];

// ─── Demo: Motor de reglas de validación (HU25) ────────────────────────────────
// Parámetros son editables; no hardcodeados en UI

export const REGLAS_MOTOR: ReglaCelda[] = [
  { codigo: 'NO_SOLAPE', nombre: 'No solapamiento de turnos', descripcion: 'Dos turnos no pueden solaparse en el mismo día para la misma persona.', alcance: 'empresa', severidad: 'bloqueo', prioridad: 1, activo: true },
  { codigo: 'MAX_HORAS_PERIODO', nombre: 'Máximo de horas en el periodo', descripcion: 'Límite de horas programables por funcionario en un corte de nómina.', alcance: 'frente', frenteId: 'CC', parametro: '46', unidad: 'horas', severidad: 'bloqueo', prioridad: 2, activo: true },
  { codigo: 'MAX_DIAS_CONSECUTIVOS', nombre: 'Máximo días consecutivos trabajados', descripcion: 'Número máximo de días seguidos sin descanso.', alcance: 'frente', frenteId: 'CC', parametro: '5', unidad: 'días', severidad: 'advertencia', prioridad: 3, activo: true },
  { codigo: 'MIN_COBERTURA_FRANJA', nombre: 'Cobertura mínima por franja horaria', descripcion: 'Mínimo de agentes activos (no en CAP/ACT/INC/VAC/DES) en cada franja.', alcance: 'frente', frenteId: 'CC', parametro: '2', unidad: 'personas', severidad: 'advertencia', prioridad: 4, activo: true },
  { codigo: 'COMPENSATORIO_DIAS_TIPO', nombre: 'Días especiales antes de sugerir compensatorio', descripcion: 'Al superar este número de domingos/festivos trabajados se sugiere compensatorio.', alcance: 'frente', frenteId: 'CC', parametro: '3', unidad: 'días domingo/festivo', severidad: 'advertencia', prioridad: 5, activo: true },
  { codigo: 'MIN_COB_SITIO_FESTIVO', nombre: 'Cobertura mínima en sitio — domingo/festivo', descripcion: 'Mínimo de técnicos en campo en domingos o festivos por zona.', alcance: 'frente', frenteId: 'SITIO', parametro: '1', unidad: 'técnico por zona', severidad: 'bloqueo', prioridad: 2, activo: true },
];

// ─── Demo: Campañas ───────────────────────────────────────────────────────────

export const CAMPANAS: Campana[] = [
  { id: 'c1', nombre: 'Data Service', codigo: 'DS', frenteId: 'CC', activo: true },
  { id: 'c2', nombre: 'Pagos de gobierno', codigo: 'PG', frenteId: 'CC', activo: true },
  { id: 'c3', nombre: 'Canguro', codigo: 'CAN', frenteId: 'CC', activo: true },
];

// ─── Demo: Sitios (todos iguales en jerarquía de catálogo) ────────────────────

export const SITIOS: Sitio[] = [
  { id: 's1', nombre: 'Elemento', direccion: 'Cra. 15 #93-75, Bogotá', activo: true },
  { id: 's2', nombre: 'Sede Calle 26', direccion: 'Av. Calle 26 #69-76, Bogotá', activo: true },
  { id: 's3', nombre: 'SPT Restrepo', direccion: 'Cra. 19 #17-50, Bogotá', activo: true },
  { id: 's4', nombre: 'Laboratorio Bogotá', direccion: 'Cll. 100 #8A-55, Bogotá', activo: true },
];

// ─── Demo: Territorio (niveles configurables, no fijos) ───────────────────────

export const TERRITORIO_CONFIG = {
  niveles: [
    { nivel: 1, nombre: 'Regional' },
    { nivel: 2, nombre: 'Zona' },
    { nivel: 3, nombre: 'SPT' },
  ],
};

export const TERRITORIO_NODOS: TerritoriNodo[] = [
  { id: 't1', nivel: 1, nombreNivel: 'Regional', nombre: 'Región Bogotá' },
  { id: 't2', nivel: 2, nombreNivel: 'Zona', nombre: 'Zona Norte', padreId: 't1' },
  { id: 't3', nivel: 2, nombreNivel: 'Zona', nombre: 'Zona Sur', padreId: 't1' },
  { id: 't4', nivel: 3, nombreNivel: 'SPT', nombre: 'SPT Restrepo', padreId: 't2' },
  { id: 't5', nivel: 3, nombreNivel: 'SPT', nombre: 'SPT Usaquén', padreId: 't2' },
  { id: 't6', nivel: 3, nombreNivel: 'SPT', nombre: 'SPT Kennedy', padreId: 't3' },
];

// ─── Demo: Mallas ─────────────────────────────────────────────────────────────

export const MALLAS: Malla[] = [
  { id: 'm1', nombre: 'CC Septiembre 2026', frenteId: 'CC', frenteNombre: 'Contact Center', periodo: 'Sep 2026', estado: 'publicada', modo: 'asistido', responsable: 'Natalia Cruz', actualizado: '29 ago 2026 · 10:32', fechaCreacion: '1 ago 2026', fechaPublicacion: '29 ago 2026' },
  { id: 'm2', nombre: 'Sitio Sem. 31 ago–6 sep', frenteId: 'SITIO', frenteNombre: 'Soporte en sitio', periodo: '31 ago–6 sep 2026', estado: 'revision', modo: 'automatico', responsable: 'Héctor Molina', actualizado: '30 ago 2026 · 17:05', fechaCreacion: '28 ago 2026' },
  { id: 'm3', nombre: 'Lab Sábado 5 sep', frenteId: 'LAB', frenteNombre: 'Laboratorio', periodo: '5 sep 2026', estado: 'borrador', modo: 'manual', responsable: 'Felipe Torres', actualizado: '28 ago 2026 · 09:14', fechaCreacion: '28 ago 2026' },
  { id: 'm4', nombre: 'Mesa Sem. 24–30 ago', frenteId: 'MESA', frenteNombre: 'Mesa de servicio', periodo: '24–30 ago 2026', estado: 'publicada', modo: 'manual', responsable: 'Carolina Vargas', actualizado: '23 ago 2026 · 16:20', fechaCreacion: '20 ago 2026', fechaPublicacion: '23 ago 2026' },
  { id: 'm5', nombre: 'CC Agosto 2026', frenteId: 'CC', frenteNombre: 'Contact Center', periodo: 'Ago 2026', estado: 'rechazada', modo: 'asistido', responsable: 'Natalia Cruz', actualizado: '2 ago 2026 · 11:08', motivoRechazo: 'Faltan 3 días de cobertura nocturna sin asignar — semanas 3 y 4.', fechaCreacion: '1 jul 2026' },
];

// ─── Demo: Grilla CC Septiembre 2026 ──────────────────────────────────────────
// Sep 2026: Sep 1 = Martes (dow=2). Demo festivo: Sep 22

export const SEP_DAYS_META = Array.from({ length: 30 }, (_, i) => {
  const d = new Date(2026, 8, i + 1);
  return {
    num: i + 1,
    str: `2026-09-${String(i + 1).padStart(2, '0')}`,
    dow: d.getDay(),
    festivo: i + 1 === 22,
  };
});

const CC_PATTERN: Record<string, string[]> = {
  p1: ['T1','T1','INC','INC','DES','DES','T8','T8','T1','T1','DES','DES','T8','T8','T1','T1','DES','DES','T5','T5','DES','DES','T1','T1','T5','T5','DES','DES','T1','DES'],
  p2: ['T5','T5','T5','T5','DES','DES','T1','T1','T5','T5','DES','DES','T1','T1','T5','T5','DES','DES','T1','T1','DES','DES','T5','T5','T1','T1','DES','DES','T5','DES'],
  p3: ['T8','T8','T8','T8','DES','DES','T5','T5','T8','T8','DES','DES','T5','T5','T8','T8','DES','DES','T8','T8','DES','DES','T8','T8','T5','DES','DES','T8','T8','DES'],
  p4: ['T1','DES','DES','T1','T5','T5','DES','DES','T1','T1','T5','T5','DES','DES','T8','T8','T1','T1','DES','DES','T5','T5','DES','DES','T1','T1','DES','DES','T8','DES'],
  p5: ['DES','DES','T5','T5','T1','T1','DES','DES','T8','T8','T1','T1','DES','DES','T1','T1','T5','T5','DES','DES','T8','T8','DES','DES','T5','T5','T1','T1','DES','DES'],
};

export const GRILLA_CC: GrillaData = {};
PERSONAS_CC.forEach(p => {
  GRILLA_CC[p.id] = {};
  SEP_DAYS_META.forEach((day, i) => {
    const t = CC_PATTERN[p.id][i];
    const isState = ['INC','VAC','DES','PER','CAP','ACT','COM'].includes(t);
    const modMap: Record<string, Modalidad> = { p1: 'presencial', p2: 'presencial', p3: 'presencial', p4: 'virtual', p5: 'hibrido' };
    const mod = modMap[p.id];
    GRILLA_CC[p.id][day.str] = {
      ...(isState ? { estado: t } : t ? { turno: t } : {}),
      ...(mod && !isState && t && t !== 'DES' ? { modalidad: mod } : {}),
      ...(mod === 'presencial' && !isState && t && t !== 'DES' ? { sitio: 'Elemento' } : {}),
      ...(mod === 'hibrido' && !isState && t && t !== 'DES' ? { sitio: 'Sede Calle 26' } : {}),
      ...(p.id === 'p1' && !isState && t === 'T1' ? { campana: 'DS' } : {}),
    };
  });
});

// ─── Demo: Grilla Sitio semana 31 ago–6 sep ─────────────────────────────────

export const SEMANA_SITIO = [
  { str: '2026-08-31', num: 31, mes: 'ago', dow: 1, festivo: false, label: 'Lun 31 ago' },
  { str: '2026-09-01', num: 1, mes: 'sep', dow: 2, festivo: false, label: 'Mar 1 sep' },
  { str: '2026-09-02', num: 2, mes: 'sep', dow: 3, festivo: false, label: 'Mié 2 sep' },
  { str: '2026-09-03', num: 3, mes: 'sep', dow: 4, festivo: false, label: 'Jue 3 sep' },
  { str: '2026-09-04', num: 4, mes: 'sep', dow: 5, festivo: false, label: 'Vie 4 sep' },
  { str: '2026-09-05', num: 5, mes: 'sep', dow: 6, festivo: false, label: 'Sáb 5 sep' },
  { str: '2026-09-06', num: 6, mes: 'sep', dow: 0, festivo: false, label: 'Dom 6 sep' },
];

const SITIO_PATTERN: Record<string, string[]> = {
  p6: ['TS1','TS1','TS1','TS1','TS1','DES','DES'],
  p7: ['TS1','TS1','TS1','TS1','DES','DES','TS2'],
  p8: ['DES','TS1','TS1','TS1','TS1','TS1','DES'],
};

export const GRILLA_SITIO: GrillaData = {};
PERSONAS_SITIO.forEach(p => {
  GRILLA_SITIO[p.id] = {};
  SEMANA_SITIO.forEach((day, i) => {
    const t = SITIO_PATTERN[p.id][i];
    const isState = ['DES','INC','VAC'].includes(t);
    GRILLA_SITIO[p.id][day.str] = {
      ...(isState ? { estado: t } : { turno: t }),
      modalidad: 'presencial',
      sitio: p.zona === 'SPT Restrepo' ? 'SPT Restrepo' : 'Elemento',
      ...(p.zona ? { zona: p.zona } : {}),
    };
  });
});

// ─── Demo: Historial celda Laura Méndez 3 sep ────────────────────────────────

export const HISTORIAL_LAURA_SEP3: HistorialEntry[] = [
  {
    id: 'h1',
    fecha: '3 sep 2026 · 08:17',
    usuario: 'Natalia Cruz (Supervisora CC)',
    valorAntes: 'T1 · Presencial · Elemento · Campaña DS',
    valorDespues: 'INC · Incapacidad (no suma horas)',
    motivo: 'Incapacidad médica radicada EPS — caso 2026-4821',
    origen: 'novedad',
  },
  {
    id: 'h2',
    fecha: '29 ago 2026 · 10:32',
    usuario: 'Natalia Cruz (Supervisora CC)',
    valorAntes: '(vacío)',
    valorDespues: 'T1 · Presencial · Elemento · Campaña DS',
    motivo: 'Creación de malla CC septiembre 2026 — asignación inicial',
    origen: 'automatico',
  },
];

// ─── Demo: Conflictos (leen reglas del motor) ─────────────────────────────────

export const CONFLICTOS_CC: Conflicto[] = [
  { tipo: 'advertencia', codigoRegla: 'MAX_DIAS_CONSECUTIVOS', mensaje: 'Laura Méndez: 5 días consecutivos (parámetro: 5 días)', persona: 'Laura Méndez', fecha: '7–11 sep' },
  { tipo: 'advertencia', codigoRegla: 'MIN_COBERTURA_FRANJA', mensaje: 'Franja 06–14 h del 12 sep: 1 persona activa (mínimo configurado: 2)', fecha: '12 sep' },
  { tipo: 'bloqueo', codigoRegla: 'NO_SOLAPE', mensaje: 'Andrés Peña: restricción de estudio (no diurno jue) — conflicto con T1 el jue 10 sep', persona: 'Andrés Peña', fecha: '10 sep' },
];

// ─── Demo: Patrones de rotación ───────────────────────────────────────────────

export const PATRONES = [
  { id: 'r1', nombre: '15 días mañana / 15 tarde', frenteId: 'CC', secuencia: 'T1×15 → T5×15', duracion: '30 días', activo: true },
  { id: 'r2', nombre: '2 trabajan / 1 descansa', frenteId: 'CC', secuencia: 'T1,T1,DES (o T5,T5,DES)', duracion: 'continuo', activo: true },
  { id: 'r3', nombre: 'Sin repetir tipo semana a semana', frenteId: 'CC', secuencia: 'alterno semanal', duracion: '2 semanas', activo: true },
  { id: 'r4', nombre: 'Sitio 15/15 día-noche', frenteId: 'SITIO', secuencia: 'TS1×15 → TS2×15', duracion: '30 días', activo: true },
];

// ─── Demo: Cortes de nómina y tipos de hora ───────────────────────────────────

export const CORTES_NOMINA = [
  { id: 'cn1', nombre: 'Primera quincena sep 2026', inicio: '1 sep', fin: '15 sep', activo: true },
  { id: 'cn2', nombre: 'Segunda quincena sep 2026', inicio: '16 sep', fin: '30 sep', activo: false },
  { id: 'cn3', nombre: 'Primera quincena ago 2026', inicio: '1 ago', fin: '15 ago', activo: false },
];

export const TIPOS_HORA = [
  { codigo: 'ORD', nombre: 'Hora ordinaria diurna' },
  { codigo: 'EXDI', nombre: 'Hora extra diurna' },
  { codigo: 'FEDI', nombre: 'Hora festiva diurna' },
  { codigo: 'FENO', nombre: 'Hora festiva nocturna' },
  { codigo: 'RENO', nombre: 'Recargo nocturno' },
];

// ─── Demo: Horas para nómina ──────────────────────────────────────────────────

export const HORAS_NOMINA = [
  { persona: 'Laura Méndez', ordinaria: 136, extraDiurna: 0, festivaDiurna: 8, festivaNocturna: 0, recargoNocturno: 0 },
  { persona: 'Camilo Restrepo', ordinaria: 144, extraDiurna: 8, festivaDiurna: 0, festivaNocturna: 0, recargoNocturno: 16 },
  { persona: 'Diana López', ordinaria: 144, extraDiurna: 0, festivaDiurna: 8, festivaNocturna: 8, recargoNocturno: 0 },
  { persona: 'Andrés Peña', ordinaria: 140, extraDiurna: 4, festivaDiurna: 0, festivaNocturna: 0, recargoNocturno: 0 },
  { persona: 'Natalia Cruz', ordinaria: 144, extraDiurna: 0, festivaDiurna: 8, festivaNocturna: 0, recargoNocturno: 8 },
];

// ─── Demo: Solicitudes de intercambio ────────────────────────────────────────

export const SOLICITUDES_INTERCAMBIO: SolicitudIntercambio[] = [
  {
    id: 'SIC-001',
    solicitanteId: 'P001',
    solicitante: 'Laura Méndez',
    solicitanteNombre: 'Laura Méndez',
    receptorId: 'P002',
    receptor: 'Camilo Restrepo',
    contraparteNombre: 'Camilo Restrepo',
    fechaOrigen: '2026-09-10',
    diaOrigen: '2026-09-10',
    turnoOrigen: 'T1',
    fechaDestino: '2026-09-17',
    diaDestino: '2026-09-17',
    turnoDestino: 'T5',
    frenteId: 'CC',
    estado: 'pendiente',
    fechaSolicitud: '2026-09-08 09:12',
    motivo: 'Cita médica no posponible',
    advertencias: ['Cobertura CC 06:00–14:00 baja a 2/3 el Lun 10-Sep'],
  },
  {
    id: 'SIC-002',
    solicitanteId: 'P001',
    solicitante: 'Laura Méndez',
    solicitanteNombre: 'Laura Méndez',
    receptorId: 'P003',
    receptor: 'Diana López',
    contraparteNombre: 'Diana López',
    fechaOrigen: '2026-08-20',
    diaOrigen: '2026-08-20',
    turnoOrigen: 'T5',
    fechaDestino: '2026-08-22',
    diaDestino: '2026-08-22',
    turnoDestino: 'T1',
    frenteId: 'CC',
    estado: 'aplicada',
    fechaSolicitud: '2026-08-15 11:04',
    motivo: 'Compromiso familiar',
    advertencias: [],
  },
  {
    id: 'SIC-003',
    solicitanteId: 'P001',
    solicitante: 'Laura Méndez',
    solicitanteNombre: 'Laura Méndez',
    receptorId: 'P004',
    receptor: 'Andrés Peña',
    contraparteNombre: 'Andrés Peña',
    fechaOrigen: '2026-08-05',
    diaOrigen: '2026-08-05',
    turnoOrigen: 'T1',
    fechaDestino: '2026-08-06',
    diaDestino: '2026-08-06',
    turnoDestino: 'T8',
    frenteId: 'CC',
    estado: 'rechazada',
    fechaSolicitud: '2026-08-01 16:40',
    motivo: 'Cambio de turno preferido',
    motivoRechazo: 'Dejaría cobertura de mañana por debajo del mínimo del frente.',
    advertencias: [],
  },
  {
    id: 'SIC-004',
    solicitanteId: 'P003',
    solicitante: 'Diana López',
    solicitanteNombre: 'Diana López',
    receptorId: 'P004',
    receptor: 'Andrés Peña',
    contraparteNombre: 'Andrés Peña',
    fechaOrigen: '2026-09-15',
    diaOrigen: '2026-09-15',
    turnoOrigen: 'T8',
    fechaDestino: '2026-09-16',
    diaDestino: '2026-09-16',
    turnoDestino: 'T1',
    frenteId: 'CC',
    estado: 'aprobada',
    fechaSolicitud: '2026-09-07 14:22',
    advertencias: [],
  },
];

// ─── Helpers ──────────────────────────────────────────────────────────────────

export const DOW_LABELS = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
export const DOW_FULL = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

export function turnoInfo(codigo: string) {
  const t = TURNOS.find(x => x.codigo === codigo);
  const e = ESTADOS_CELDA.find(x => x.codigo === codigo);
  if (t) return { label: codigo, sub: `${t.inicio}–${t.fin}`, colorClass: t.colorClass, esTurno: true };
  if (e) return { label: codigo, sub: e.nombre, colorClass: e.colorClass, esTurno: false };
  return { label: '·', sub: '', colorClass: 'turno-empty', esTurno: false };
}

export function cellKey(cell: GrillaCell): string {
  return cell.turno || cell.estado || '';
}

export function modalidadIcon(m?: Modalidad): string {
  if (m === 'presencial') return '🏢';
  if (m === 'virtual') return '🏠';
  if (m === 'hibrido') return '⚡';
  return '';
}

export function severidadClass(s: Severidad): string {
  return s === 'bloqueo' ? 'severidad-bloqueo' : s === 'advertencia' ? 'severidad-advertencia' : 'severidad-info';
}

// ─── Compatibility aliases for new screens ────────────────────────────────────

const CEDULAS: Record<string, string> = {
  p1: '1090456789', p2: '1090567890', p3: '1091234567', p4: '1092345678',
  p5: '1093456789', p6: '1094567890', p7: '1095678901', p8: '1096789012',
  p9: '1097890123', p10: '1098901234',
};
const PERSONAS_IDS: Record<string, string> = {
  p1: 'P001', p2: 'P002', p3: 'P003', p4: 'P004', p5: 'P005',
  p6: 'P006', p7: 'P007', p8: 'P008', p9: 'P009', p10: 'P010',
};
export const PERSONAS = TODAS_PERSONAS.map(p => ({
  ...p,
  id: PERSONAS_IDS[p.id] ?? p.id,
  cedula: CEDULAS[p.id] ?? '—',
}));

export const MODALIDADES = [
  { codigo: 'PRE', icono: '🏢', nombre: 'Presencial', frentes: ['CC', 'SITIO', 'LAB', 'MESA'] },
  { codigo: 'VIR', icono: '🏠', nombre: 'Virtual', frentes: ['CC', 'MESA'] },
  { codigo: 'HIB', icono: '⚡', nombre: 'Híbrido', frentes: ['CC', 'SITIO', 'MESA'] },
];

// Extend SITIOS with frente and tipo for S09
export const SITIOS_EXTENDED = SITIOS.map((s, i) => ({
  ...s,
  codigo: `S${String(i + 1).padStart(2, '0')}`,
  frente: i < 2 ? 'CC' : i === 2 ? 'SITIO' : 'LAB',
  tipo: i < 2 ? 'Sede' : i === 2 ? 'SPT' : 'Laboratorio',
}));

// Re-export extended SITIOS
export { SITIOS_EXTENDED as SITIOS_V2 };

// Extend TURNOS with computed horaInicio/horaFin/horasNetas/frentes
export const TURNOS_EXTENDED = TURNOS.map(t => ({
  ...t,
  horaInicio: t.inicio,
  horaFin: t.fin,
  horasNetas: t.fin < t.inicio ? 8 : Math.round(
    (parseInt(t.fin.split(':')[0]) * 60 + parseInt(t.fin.split(':')[1]) -
     parseInt(t.inicio.split(':')[0]) * 60 - parseInt(t.inicio.split(':')[1])) / 60
  ),
  frentes: [t.frenteId],
}));

// Re-export TURNOS as extended (add fields to existing export)
export { TURNOS_EXTENDED as TURNOS_WITH_HOURS };

// Extend ESTADOS_CELDA with color/descuentaHoras/requiereSoporte
export const ESTADOS_CELDA_V2 = ESTADOS_CELDA.map(e => ({
  ...e,
  color: e.colorClass === 'turno-INC' ? '#FEE2E2' :
         e.colorClass === 'turno-VAC' ? '#E0F2FE' :
         e.colorClass === 'turno-PER' ? '#FEF9C3' :
         e.colorClass === 'turno-CAP' ? '#F3E8FF' :
         e.colorClass === 'turno-ACT' ? '#FFEDD5' :
         e.colorClass === 'turno-COM' ? '#DCFCE7' :
         e.colorClass === 'turno-DES' ? '#F3F4F6' : '#E5E7EB',
  descuentaHoras: ['INC', 'VAC', 'PER'].includes(e.codigo),
  requiereSoporte: ['INC'].includes(e.codigo),
}));

// Extend REGLAS_MOTOR with descripcion field
export const REGLAS_MOTOR_EXTENDED = REGLAS_MOTOR.map(r => ({
  ...r,
  descripcion: r.nombre,
}));

// Extend SolicitudIntercambio data with new field names
export const SOLICITUDES_INTERCAMBIO_V2 = SOLICITUDES_INTERCAMBIO.map(s => ({
  ...s,
  solicitanteNombre: s.solicitante,
  contraparteNombre: s.receptor,
  diaOrigen: s.fechaOrigen,
  diaDestino: s.fechaDestino,
  turnoOrigen: s.turnoOrigen.split(' ')[0],
  turnoDestino: s.turnoDestino.split(' ')[0],
  motivo: s.motivoRechazo,
  advertencias: s.estado === 'pendiente' ? ['Cobertura CC 06:00–14:00 baja a 2/3 tras el intercambio'] : [],
}));

// Extend Malla with missing fields
export const MALLAS_EXTENDED = MALLAS.map(m => ({
  ...m,
  fechaCreacion: m.actualizado.split(' · ')[0],
  fechaPublicacion: m.estado === 'publicada' ? m.actualizado.split(' · ')[0] : undefined,
}));

// Extend SITIOS with frente/tipo/codigo for S09
export const SITIOS_S09 = SITIOS.map((s, i) => ({
  ...s,
  codigo: `S${String(i + 1).padStart(2, '0')}`,
  frente: (['CC', 'CC', 'SITIO', 'LAB'] as const)[i] ?? 'CC',
  tipo: (['Sede', 'Sede', 'SPT', 'Laboratorio'] as const)[i] ?? 'Sede',
}));
