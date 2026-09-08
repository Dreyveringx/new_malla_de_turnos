import { useState } from 'react';
import { Breadcrumb, Modal, Field, EstadoChip, ConflictoItem, Chip, DisabledBtn } from '../Shell';
import {
  MALLAS, PERSONAS, FRENTES, TURNOS_WITH_HOURS as TURNOS,
  ESTADOS_CELDA_V2 as ESTADOS_CELDA, REGLAS_MOTOR, CONFLICTOS_CC,
  MODALIDADES, SITIOS_S09 as SITIOS, CAMPANAS, TERRITORIO_NODOS,
  type Malla, type MallaEstado, type Rol, puedeEditar, puedePublicar, severidadClass,
} from '../data';

interface Props {
  screen: string;
  navigate: (s: string, p?: any) => void;
  params: any;
  onToast: (msg: string, desc: string, type: 'success' | 'error' | 'warning') => void;
  role: Rol;
}

type CellAttrs = {
  codigo: string;
  modalidad?: string;
  sitio?: string;
  campana?: string;
  territorio?: string;
  nota?: string;
};

function emptyAttrs(codigo = ''): CellAttrs {
  return { codigo, modalidad: '', sitio: '', campana: '', territorio: '', nota: '' };
}

function normalizeCell(v: string | CellAttrs | undefined): CellAttrs {
  if (!v) return emptyAttrs();
  if (typeof v === 'string') return emptyAttrs(v);
  return { ...emptyAttrs(), ...v };
}

// ─── S16 Lista de mallas ─────────────────────────────────────────────────────
function S16Lista({ navigate, onToast, role }: Props) {
  const [mallas, setMallas] = useState<Malla[]>(MALLAS);
  const [filtroFrente, setFiltroFrente] = useState('');
  const [filtroEstado, setFiltroEstado] = useState<MallaEstado | ''>('');
  const canEdit = puedeEditar(role);

  const visible = mallas.filter(m =>
    (!filtroFrente || m.frenteId === filtroFrente) &&
    (!filtroEstado || m.estado === filtroEstado)
  );

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1200 }}>
      <Breadcrumb items={[{ label: 'B. Construcción' }, { label: 'S16 Lista de mallas' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Mallas de turno</div>
          <div className="page-subtitle">Gestión y seguimiento de todas las mallas. HU28</div>
        </div>
        {canEdit
          ? <button className="btn-primary" onClick={() => navigate('S17')}>+ Nueva malla</button>
          : <DisabledBtn label="+ Nueva malla" reason="Sin permiso" />}
      </div>

      <div className="filter-bar" style={{ marginBottom: 16 }}>
        <select className="input-field" style={{ width: 180 }} value={filtroFrente} onChange={e => setFiltroFrente(e.target.value)}>
          <option value="">Todos los frentes</option>
          {FRENTES.filter(f => f.activo).map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
        </select>
        <select className="input-field" style={{ width: 160 }} value={filtroEstado} onChange={e => setFiltroEstado(e.target.value as any)}>
          <option value="">Todos los estados</option>
          <option value="borrador">Borrador</option>
          <option value="revision">En revisión</option>
          <option value="publicada">Publicada</option>
          <option value="rechazada">Rechazada</option>
        </select>
      </div>

      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead>
            <tr><th>Nombre</th><th>Frente</th><th>Periodo</th><th>Responsable</th><th>Estado</th><th>Creada</th><th></th></tr>
          </thead>
          <tbody>
            {visible.map(m => (
              <tr key={m.id}>
                <td>
                  <div style={{ fontWeight: 500, cursor: 'pointer', color: 'var(--clr-primary)' }} onClick={() => navigate('S18', { mallaId: m.id })}>
                    {m.nombre}
                  </div>
                  {m.motivoRechazo && <div style={{ fontSize: 11, color: '#DC2626', marginTop: 2 }}>↩ {m.motivoRechazo}</div>}
                </td>
                <td><Chip label={m.frenteNombre} /></td>
                <td style={{ fontSize: 12 }}>{m.periodo}</td>
                <td style={{ fontSize: 12 }}>{m.responsable}</td>
                <td><EstadoChip estado={m.estado} /></td>
                <td style={{ fontSize: 12 }}>{m.fechaCreacion}</td>
                <td>
                  <div style={{ display: 'flex', gap: 4 }}>
                    <button className="btn-icon" title="Abrir grilla" onClick={() => navigate('S18', { mallaId: m.id })}>📋</button>
                    {m.estado === 'borrador' && canEdit && (
                      <button className="btn-icon" title="Enviar a revisión" onClick={() => { setMallas(ms => ms.map(x => x.id === m.id ? { ...x, estado: 'revision' as MallaEstado } : x)); onToast('Enviada a revisión', m.nombre, 'success'); }}>📤</button>
                    )}
                    {m.estado === 'rechazada' && canEdit && (
                      <button className="btn-icon" title="Reabrir borrador" onClick={() => { setMallas(ms => ms.map(x => x.id === m.id ? { ...x, estado: 'borrador' as MallaEstado, motivoRechazo: undefined } : x)); onToast('Malla reabierta', m.nombre, 'success'); }}>🔁</button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {visible.length === 0 && (
              <tr><td colSpan={7} style={{ textAlign: 'center', padding: '32px 0', color: 'var(--clr-text-muted)' }}>Sin resultados para los filtros seleccionados.</td></tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="screen-id">S16</div>
    </div>
  );
}

// ─── S17 Crear malla (wizard) ─────────────────────────────────────────────────
function S17Crear({ navigate, onToast, role }: Props) {
  const [step, setStep] = useState(0);
  const [frenteId, setFrenteId] = useState('CC');
  const [nombre, setNombre] = useState('');
  const [periodoInicio, setPeriodoInicio] = useState('2025-03-01');
  const [periodoFin, setPeriodoFin] = useState('2025-03-31');
  const canEdit = puedeEditar(role);

  const frente = FRENTES.find(f => f.id === frenteId) ?? FRENTES[0];
  const STEPS = ['Datos básicos', 'Personas', 'Confirmar'];

  return (
    <div style={{ padding: '24px 28px', maxWidth: 760 }}>
      <Breadcrumb items={[{ label: 'B. Construcción' }, { label: 'S16', onClick: () => navigate('S16') }, { label: 'S17 Crear malla' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Nueva malla de turnos</div>
          <div className="page-subtitle">Wizard de creación — 3 pasos. HU29</div>
        </div>
      </div>

      <div className="wizard-steps" style={{ marginBottom: 24 }}>
        {STEPS.map((s, i) => (
          <div key={s} className={`wizard-step ${i === step ? 'active' : i < step ? 'done' : ''}`} style={{ cursor: i < step ? 'pointer' : 'default' }} onClick={() => i < step && setStep(i)}>
            <div className="wizard-step-num">{i < step ? '✓' : i + 1}</div>
            <div className="wizard-step-label">{s}</div>
          </div>
        ))}
      </div>

      {step === 0 && (
        <div className="card" style={{ padding: '24px' }}>
          <Field label="Nombre de la malla" required>
            <input className="input-field" value={nombre} onChange={e => setNombre(e.target.value)} placeholder="Ej: Malla CC — Marzo 2025" />
          </Field>
          <Field label="Frente operativo" required>
            <select className="input-field" value={frenteId} onChange={e => setFrenteId(e.target.value)}>
              {FRENTES.filter(f => f.activo).map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
            </select>
          </Field>
          <Field label="Responsable arma malla">
            <input className="input-field" defaultValue={frente.responsableArma} readOnly />
          </Field>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            <Field label="Inicio del periodo" required>
              <input className="input-field" type="date" value={periodoInicio} onChange={e => setPeriodoInicio(e.target.value)} />
            </Field>
            <Field label="Fin del periodo" required>
              <input className="input-field" type="date" value={periodoFin} onChange={e => setPeriodoFin(e.target.value)} />
            </Field>
          </div>
          <div className="helper-text" style={{ marginBottom: 12 }}>
            Capacidades del frente: {[
              frente.usaModalidad && 'modalidad',
              'sitio/SPT',
              frente.usaCampanas && 'campañas',
              frente.usaTerritorioZona && 'territorio',
            ].filter(Boolean).join(' · ') || 'solo turno/estado'}.
            Se configuran después en la grilla.
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" onClick={() => navigate('S16')}>Cancelar</button>
            <button className="btn-primary" onClick={() => setStep(1)} disabled={!nombre}>Siguiente →</button>
          </div>
        </div>
      )}

      {step === 1 && (
        <div className="card" style={{ padding: '24px' }}>
          <div className="card" style={{ padding: '12px 14px', marginBottom: 14, background: '#F0F7FA', border: '1px solid #B8D4E8' }}>
            <div style={{ fontWeight: 600, fontSize: 13, marginBottom: 4 }}>¿Dónde asigno modalidad, sitio, campaña o SPT?</div>
            <div style={{ fontSize: 12, lineHeight: 1.45 }}>
              Aquí solo defines <strong>quién</strong> entra a la malla. Los atributos operativos (modalidad, sitio/SPT, campaña, territorio)
              se asocian en la <strong>grilla</strong>, celda a celda (persona × día), o se pueden <strong>fijar para todo el periodo</strong> de una persona.
              Solo aparecen los que el frente tenga habilitados en Parametrización.
            </div>
          </div>
          <div className="section-header">Seleccionar personas del frente {frente.nombre}</div>
          <div className="helper-text" style={{ marginBottom: 12 }}>Funcionarios existentes en GRH — el módulo NO crea empleados.</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginBottom: 16 }}>
            {PERSONAS.filter(p => p.frenteId === frenteId || frenteId === 'CC').slice(0, 8).map(p => (
              <label key={p.id} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 12px', borderRadius: 6, border: '1px solid var(--clr-border)', cursor: 'pointer' }}>
                <input type="checkbox" defaultChecked style={{ marginRight: 4 }} />
                <div className="avatar-circle" style={{ width: 28, height: 28, fontSize: 11 }}>{p.nombre.split(' ').map(w => w[0]).join('').slice(0, 2)}</div>
                <div>
                  <div style={{ fontSize: 13, fontWeight: 500 }}>{p.nombre}</div>
                  <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{p.cargo} · {p.cedula}</div>
                </div>
              </label>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
            <button className="btn-secondary" onClick={() => setStep(0)}>← Atrás</button>
            <button className="btn-primary" onClick={() => setStep(2)}>Siguiente →</button>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="card" style={{ padding: '24px' }}>
          <div className="section-header">Confirmar creación</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 20 }}>
            {[
              { label: 'Malla', value: nombre || 'Malla sin nombre' },
              { label: 'Frente', value: frente.nombre },
              { label: 'Periodo', value: `${periodoInicio} – ${periodoFin}` },
              { label: 'Personas', value: `${PERSONAS.filter(p => p.frenteId === frenteId || frenteId === 'CC').length} seleccionadas` },
              { label: 'Estado inicial', value: 'Borrador' },
              { label: 'Responsable arma', value: frente.responsableArma },
            ].map(i => (
              <div key={i.label} style={{ padding: '10px 14px', background: 'var(--clr-filter-bg)', borderRadius: 8 }}>
                <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{i.label}</div>
                <div style={{ fontSize: 13, fontWeight: 500 }}>{i.value}</div>
              </div>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
            <button className="btn-secondary" onClick={() => setStep(1)}>← Atrás</button>
            <button className="btn-primary" onClick={() => { onToast('Malla creada', nombre || 'Nueva malla', 'success'); navigate('S18', { mallaId: 'NEW' }); }}>Crear malla ✓</button>
          </div>
        </div>
      )}
      <div className="screen-id">S17</div>
    </div>
  );
}

// ─── S18 Grilla operativa (core) ──────────────────────────────────────────────
const DIAS_SEM = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
const FECHAS_DEMO = Array.from({ length: 14 }, (_, i) => {
  const d = new Date(2025, 2, 3 + i);
  return { label: `${DIAS_SEM[d.getDay() === 0 ? 6 : d.getDay() - 1]} ${d.getDate()}`, dom: d.getDay() === 0 };
});

const INIT_GRILLA: Record<string, Record<string, CellAttrs>> = {
  P001: {
    '0': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '1': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '2': { codigo: 'DES' },
    '3': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'PG' },
    '4': { codigo: 'T1', modalidad: 'VIR', campana: 'PG' },
    '5': { codigo: 'T1', modalidad: 'VIR', campana: 'PG' },
    '6': { codigo: 'DES' },
    '7': { codigo: 'T5', modalidad: 'VIR', campana: 'DS' },
    '8': { codigo: 'T5', modalidad: 'VIR', campana: 'DS' },
    '9': { codigo: 'DES' },
    '10': { codigo: 'T5', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '11': { codigo: 'T5', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '12': { codigo: 'VAC' },
    '13': { codigo: 'VAC' },
  },
  P002: {
    '0': { codigo: 'T5', modalidad: 'PRE', sitio: 'S02', campana: 'DS' },
    '1': { codigo: 'T5', modalidad: 'PRE', sitio: 'S02', campana: 'DS' },
    '2': { codigo: 'DES' },
    '3': { codigo: 'T5', modalidad: 'HIB', sitio: 'S01', campana: 'PG' },
    '4': { codigo: 'DES' },
    '5': { codigo: 'T5', modalidad: 'VIR', campana: 'PG' },
    '6': { codigo: 'T5', modalidad: 'VIR', campana: 'PG' },
    '7': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '8': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '9': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '10': { codigo: 'DES' },
    '11': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '12': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '13': { codigo: 'DES' },
  },
  P003: {
    '0': { codigo: 'DES' },
    '1': { codigo: 'T8', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '2': { codigo: 'T8', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '3': { codigo: 'T8', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '4': { codigo: 'T8', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '5': { codigo: 'DES' },
    '6': { codigo: 'T8', modalidad: 'VIR', campana: 'PG' },
    '7': { codigo: 'DES' },
    '8': { codigo: 'T8', modalidad: 'PRE', sitio: 'S02', campana: 'CAN' },
    '9': { codigo: 'T8', modalidad: 'PRE', sitio: 'S02', campana: 'CAN' },
    '10': { codigo: 'T8', modalidad: 'PRE', sitio: 'S02', campana: 'CAN' },
    '11': { codigo: 'T8', modalidad: 'PRE', sitio: 'S02', campana: 'CAN' },
    '12': { codigo: 'DES' },
    '13': { codigo: 'INC' },
  },
  P004: {
    '0': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '1': { codigo: 'DES' },
    '2': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '3': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '4': { codigo: 'T1', modalidad: 'PRE', sitio: 'S01', campana: 'DS' },
    '5': { codigo: 'T1', modalidad: 'VIR', campana: 'PG' },
    '6': { codigo: 'DES' },
    '7': { codigo: 'T8', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '8': { codigo: 'DES' },
    '9': { codigo: 'T8', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '10': { codigo: 'T8', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '11': { codigo: 'T8', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '12': { codigo: 'T8', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '13': { codigo: 'DES' },
  },
  P005: {
    '0': { codigo: 'T5', modalidad: 'PRE', sitio: 'S02', campana: 'DS' },
    '1': { codigo: 'T5', modalidad: 'PRE', sitio: 'S02', campana: 'DS' },
    '2': { codigo: 'T5', modalidad: 'PRE', sitio: 'S02', campana: 'DS' },
    '3': { codigo: 'DES' },
    '4': { codigo: 'T5', modalidad: 'VIR', campana: 'PG' },
    '5': { codigo: 'DES' },
    '6': { codigo: 'COM' },
    '7': { codigo: 'T5', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '8': { codigo: 'T5', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '9': { codigo: 'DES' },
    '10': { codigo: 'T5', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '11': { codigo: 'T5', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '12': { codigo: 'T5', modalidad: 'PRE', sitio: 'S01', campana: 'CAN' },
    '13': { codigo: 'DES' },
  },
};

function S18Grilla({ navigate, params, onToast, role }: Props) {
  const malla = MALLAS.find(m => m.id === (params?.mallaId)) ?? MALLAS[0];
  const frente = FRENTES.find(f => f.id === malla.frenteId) ?? FRENTES[0];
  const personas = PERSONAS.filter(p => p.frenteId === malla.frenteId).slice(0, 5);
  const [grilla, setGrilla] = useState<Record<string, Record<string, CellAttrs>>>(INIT_GRILLA);
  const [drawerCell, setDrawerCell] = useState<{ personaId: string; diaIdx: number } | null>(null);
  const [draft, setDraft] = useState<CellAttrs>(emptyAttrs());
  const [showConflictos, setShowConflictos] = useState(false);
  const [concurrencyBanner, setConcurrencyBanner] = useState(true);
  const [selectedCells, setSelectedCells] = useState<Set<string>>(new Set());
  const [massModal, setMassModal] = useState(false);
  const [fixPeriodoModal, setFixPeriodoModal] = useState<{ personaId: string } | null>(null);
  const [massTurno, setMassTurno] = useState('T1');
  const [massAttrs, setMassAttrs] = useState({ modalidad: 'PRE', sitio: 'S01', campana: 'DS', territorio: '' });
  const canEdit = puedeEditar(role); // En prod: también depende de estado malla + published_editable del frente
  const turnosFrente = TURNOS.filter(t => t.frenteId === frente.id || (frente.id === 'CC' && ['T1', 'T2', 'T3', 'T5', 'T6', 'T8', 'TN1', 'T12'].includes(t.codigo)));
  const turnosPanel = (turnosFrente.length ? turnosFrente : TURNOS).slice(0, 10);

  const cellKey = (pid: string, d: number) => `${pid}|${d}`;

  function openDrawer(personaId: string, diaIdx: number) {
    const cur = normalizeCell(grilla[personaId]?.[String(diaIdx)]);
    setDraft({ ...cur });
    setDrawerCell({ personaId, diaIdx });
  }

  function toggleSelect(pid: string, d: number) {
    if (!canEdit) return;
    const k = cellKey(pid, d);
    setSelectedCells(s => { const n = new Set(s); n.has(k) ? n.delete(k) : n.add(k); return n; });
  }

  function applyMass() {
    setGrilla(g => {
      const n = { ...g };
      selectedCells.forEach(k => {
        const [pid, d] = k.split('|');
        const prev = normalizeCell(n[pid]?.[d]);
        n[pid] = {
          ...n[pid],
          [d]: {
            ...prev,
            codigo: massTurno,
            modalidad: frente.usaModalidad ? massAttrs.modalidad : prev.modalidad,
            sitio: massAttrs.sitio || prev.sitio,
            campana: frente.usaCampanas ? massAttrs.campana : prev.campana,
            territorio: frente.usaTerritorioZona ? massAttrs.territorio : prev.territorio,
          },
        };
      });
      return n;
    });
    setSelectedCells(new Set());
    setMassModal(false);
    onToast('Asignación masiva aplicada', `${selectedCells.size} celdas → ${massTurno}`, 'success');
  }

  function saveDrawer(close = true) {
    if (!drawerCell) return;
    setGrilla(g => ({
      ...g,
      [drawerCell.personaId]: {
        ...g[drawerCell.personaId],
        [String(drawerCell.diaIdx)]: { ...draft },
      },
    }));
    onToast('Celda actualizada', `${draft.codigo || 'sin turno'} + atributos`, 'success');
    if (close) setDrawerCell(null);
  }

  function fijarPeriodo(personaId: string, attrs: Partial<CellAttrs>) {
    setGrilla(g => {
      const n = { ...g };
      const row = { ...(n[personaId] ?? {}) };
      FECHAS_DEMO.forEach((_, di) => {
        const prev = normalizeCell(row[String(di)]);
        row[String(di)] = {
          ...prev,
          modalidad: attrs.modalidad !== undefined ? attrs.modalidad : prev.modalidad,
          sitio: attrs.sitio !== undefined ? attrs.sitio : prev.sitio,
          campana: attrs.campana !== undefined ? attrs.campana : prev.campana,
          territorio: attrs.territorio !== undefined ? attrs.territorio : prev.territorio,
        };
      });
      n[personaId] = row;
      return n;
    });
    setFixPeriodoModal(null);
    onToast('Atributos fijados en el periodo', 'HU42 — se pueden ajustar celda a celda después', 'success');
  }

  function copyWeek(fromWeek: number) {
    setGrilla(g => {
      const n = { ...g };
      personas.forEach(p => {
        const src = n[p.id] ?? {};
        for (let d = 0; d < 7; d++) {
          n[p.id] = { ...n[p.id], [d + 7]: { ...normalizeCell(src[String(d)]) } };
        }
      });
      return n;
    });
    onToast('Semana copiada', 'Semana 1 → Semana 2', 'success');
  }

  const drawerPersona = drawerCell ? personas.find(p => p.id === drawerCell.personaId) : null;
  const drawerDia = drawerCell ? FECHAS_DEMO[drawerCell.diaIdx] : null;
  const sitiosFrente = SITIOS.filter(s => s.frente === frente.id || s.frente === 'CC');
  const campanasFrente = CAMPANAS.filter(c => c.frenteId === frente.id);
  const territorios = TERRITORIO_NODOS.filter(t => t.nivel >= 2);

  return (
    <div style={{ padding: '24px 28px', maxWidth: '100%' }}>
      <Breadcrumb items={[{ label: 'B. Construcción' }, { label: 'S16', onClick: () => navigate('S16') }, { label: `S18 Grilla — ${malla.nombre}` }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">{malla.nombre}</div>
          <div className="page-subtitle">{frente.nombre} · {malla.periodo} · <EstadoChip estado={malla.estado} /></div>
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          {selectedCells.size > 0 && (
            <button className="btn-secondary" onClick={() => setMassModal(true)}>Asignar masivo ({selectedCells.size})</button>
          )}
          <button className="btn-secondary" onClick={() => copyWeek(0)}>Copiar sem. 1 →</button>
          <button className="btn-secondary" onClick={() => setShowConflictos(c => !c)}>
            ⚠️ Conflictos ({CONFLICTOS_CC.length})
          </button>
          {puedePublicar(role)
            ? <button className="btn-primary" onClick={() => navigate('S24', { mallaId: malla.id })}>Publicar →</button>
            : <DisabledBtn label="Publicar" reason="Solo coordinador puede publicar" />}
        </div>
      </div>

      <div className="card" style={{ padding: '10px 14px', marginBottom: 12, background: '#F0F7FA', border: '1px solid #B8D4E8' }}>
        <strong style={{ fontSize: 12 }}>Asociación de atributos:</strong>{' '}
        <span style={{ fontSize: 12 }}>
          clic en una celda → panel lateral (turno/estado + modalidad
          {frente.usaCampanas ? ' + campaña' : ''}
          {' + sitio/SPT'}
          {frente.usaTerritorioZona ? ' + territorio' : ''}
          ). También puedes fijar atributos de una persona para todo el periodo (botón en la fila).
        </span>
      </div>

      {concurrencyBanner && (
        <div className="concurrency-banner" style={{ marginBottom: 12 }}>
          <span>⚡ <strong>Ana M.</strong> también está editando esta malla ahora. Los cambios se sincronizan al guardar.</span>
          <button className="btn-icon" onClick={() => setConcurrencyBanner(false)}>✕</button>
        </div>
      )}

      {showConflictos && (
        <div className="card" style={{ padding: '16px 18px', marginBottom: 12, borderLeft: '4px solid #F59E0B' }}>
          <div className="section-header" style={{ marginBottom: 8 }}>Conflictos detectados por el motor de reglas</div>
          {CONFLICTOS_CC.map((c, i) => <ConflictoItem key={i} conflicto={c} codigoRegla={c.codigoRegla} />)}
        </div>
      )}

      <div style={{ overflowX: 'auto', borderRadius: 8, border: '1px solid var(--clr-border)' }}>
        <table style={{ borderCollapse: 'collapse', minWidth: 900 }}>
          <thead>
            <tr style={{ background: 'var(--clr-primary)' }}>
              <th style={{ position: 'sticky', left: 0, background: 'var(--clr-primary)', color: '#fff', fontSize: 11, padding: '8px 12px', textAlign: 'left', minWidth: 180, zIndex: 10 }}>Persona</th>
              {FECHAS_DEMO.map((d, i) => (
                <th key={i} style={{ color: d.dom ? '#FCA5A5' : '#fff', fontSize: 10, padding: '6px 4px', textAlign: 'center', minWidth: 52, fontWeight: d.dom ? 700 : 500 }}>
                  {d.label}{i === 7 && <div style={{ fontSize: 8, opacity: 0.7 }}>sem 2</div>}
                </th>
              ))}
              <th style={{ color: '#fff', fontSize: 10, padding: '6px 8px', textAlign: 'center' }}>Total h</th>
            </tr>
          </thead>
          <tbody>
            {personas.map(p => {
              const celdas = grilla[p.id] ?? {};
              const totalH = Object.values(celdas).reduce((sum, c) => {
                const cell = normalizeCell(c);
                const t = TURNOS.find(x => x.codigo === cell.codigo);
                return sum + (t ? t.horasNetas : 0);
              }, 0);
              return (
                <tr key={p.id} style={{ borderBottom: '1px solid var(--clr-border)' }}>
                  <td style={{ position: 'sticky', left: 0, background: '#fff', zIndex: 5, padding: '6px 12px', borderRight: '2px solid var(--clr-border)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <div className="avatar-circle" style={{ width: 26, height: 26, fontSize: 10, flexShrink: 0 }}>{p.nombre.split(' ').map(w => w[0]).join('').slice(0, 2)}</div>
                      <div style={{ minWidth: 0 }}>
                        <div style={{ fontSize: 12, fontWeight: 500, whiteSpace: 'nowrap' }}>{p.nombre.split(' ').slice(0, 2).join(' ')}</div>
                        <div style={{ fontSize: 10, color: 'var(--clr-text-muted)' }}>{p.cedula}</div>
                        {canEdit && (
                          <button
                            type="button"
                            className="btn-secondary"
                            style={{ height: 22, fontSize: 10, marginTop: 4, padding: '0 6px' }}
                            onClick={() => setFixPeriodoModal({ personaId: p.id })}
                            title="Fijar modalidad/sitio/campaña en todo el periodo"
                          >
                            Fijar periodo
                          </button>
                        )}
                      </div>
                    </div>
                  </td>
                  {FECHAS_DEMO.map((_, di) => {
                    const cell = normalizeCell(celdas[String(di)]);
                    const val = cell.codigo;
                    const isSelected = selectedCells.has(cellKey(p.id, di));
                    const hasAttrs = !!(cell.modalidad || cell.sitio || cell.campana || cell.territorio);
                    return (
                      <td
                        key={di}
                        style={{
                          padding: 3,
                          textAlign: 'center',
                          verticalAlign: 'middle',
                          background: isSelected ? '#E8F0FE' : undefined,
                          outline: isSelected ? '2px solid var(--clr-primary)' : undefined,
                          cursor: canEdit ? 'pointer' : 'default',
                        }}
                        onClick={() => {
                          if (canEdit) {
                            if (selectedCells.size > 0) toggleSelect(p.id, di);
                            else openDrawer(p.id, di);
                          }
                        }}
                        onContextMenu={e => { e.preventDefault(); if (canEdit) toggleSelect(p.id, di); }}
                        title={val
                          ? `${val}${cell.modalidad ? ` · ${cell.modalidad}` : ''}${cell.sitio ? ` · ${cell.sitio}` : ''}${cell.campana ? ` · ${cell.campana}` : ''} — click editar`
                          : 'Vacío — click para asignar'}
                      >
                        {val
                          ? (
                            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
                              <span className={`malla-chip turno-${val}`}>{val}</span>
                              {hasAttrs && (
                                <span style={{ fontSize: 8, color: 'var(--clr-text-muted)', lineHeight: 1.1, maxWidth: 48, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                  {[cell.modalidad, cell.sitio || cell.territorio, cell.campana].filter(Boolean).join('·')}
                                </span>
                              )}
                            </div>
                          )
                          : <span style={{ color: '#ccc', fontSize: 11 }}>—</span>}
                      </td>
                    );
                  })}
                  <td style={{ textAlign: 'center', fontSize: 11, fontWeight: 700, padding: '4px 8px', color: totalH > 46 ? '#DC2626' : 'var(--clr-text-strong)' }}>
                    {totalH}h {totalH > 46 && <span title="Supera límite MAX_HORAS_PERIODO (46h)">⚠️</span>}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="grilla-pager" style={{ marginTop: 10 }}>
        <span style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>Mostrando 5 de 22 personas</span>
        <div style={{ display: 'flex', gap: 4 }}>
          <button className="btn-secondary" style={{ height: 28, fontSize: 11 }}>← Ant.</button>
          <button className="btn-secondary" style={{ height: 28, fontSize: 11 }}>Sig. →</button>
        </div>
        <span style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>Clic = editar celda · Clic derecho = selección masiva</span>
      </div>

      {/* Drawer celda */}
      {drawerCell && drawerPersona && drawerDia && (
        <div className="drawer-overlay" onClick={() => setDrawerCell(null)}>
          <div className="drawer" onClick={e => e.stopPropagation()} style={{ width: 380, maxWidth: '92vw' }}>
            <div className="drawer-header">
              <div>
                <div style={{ fontWeight: 600, fontSize: 15 }}>{drawerPersona.nombre}</div>
                <div style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>{drawerDia.label} · atributos de esta celda</div>
              </div>
              <button className="btn-icon" onClick={() => setDrawerCell(null)}>✕</button>
            </div>
            <div style={{ padding: '16px 20px', flex: 1, overflowY: 'auto' }}>
              <div className="section-header">1. Turno o estado</div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 6, marginBottom: 16 }}>
                {turnosPanel.map(t => (
                  <button
                    key={t.codigo}
                    type="button"
                    className={`chip turno-${t.codigo}`}
                    style={{ cursor: 'pointer', padding: '8px 4px', border: draft.codigo === t.codigo ? '2px solid var(--clr-primary)' : '1px solid #ccc', borderRadius: 6, fontWeight: 600, fontSize: 11 }}
                    onClick={() => setDraft(d => ({ ...d, codigo: t.codigo }))}
                  >
                    {t.codigo}
                    <div style={{ fontSize: 9, fontWeight: 400, marginTop: 2 }}>{t.horasNetas}h</div>
                  </button>
                ))}
                {ESTADOS_CELDA.filter(e => e.asignable).map(e => (
                  <button
                    key={e.codigo}
                    type="button"
                    className={`chip turno-${e.codigo}`}
                    style={{ cursor: 'pointer', padding: '8px 4px', border: draft.codigo === e.codigo ? '2px solid var(--clr-primary)' : '1px solid #ccc', borderRadius: 6, fontWeight: 600, fontSize: 11 }}
                    onClick={() => setDraft(d => ({ ...d, codigo: e.codigo, modalidad: '', sitio: '', campana: '', territorio: '' }))}
                  >
                    {e.codigo}
                  </button>
                ))}
              </div>

              <div className="section-header">2. Atributos operativos del frente</div>
              <div className="helper-text" style={{ marginBottom: 10 }}>
                Estos campos asocian modalidad / sitio / campaña / territorio a <em>esta persona en este día</em>.
              </div>

              {frente.usaModalidad && (
                <Field label="Modalidad de trabajo" required>
                  <select className="input-field" value={draft.modalidad || ''} onChange={e => setDraft(d => ({ ...d, modalidad: e.target.value }))}>
                    <option value="">— seleccionar —</option>
                    {MODALIDADES.map(m => <option key={m.codigo} value={m.codigo}>{m.icono} {m.nombre}</option>)}
                  </select>
                </Field>
              )}

              <Field label="Sitio / SPT de asistencia">
                <select className="input-field" value={draft.sitio || ''} onChange={e => setDraft(d => ({ ...d, sitio: e.target.value }))}>
                  <option value="">— ninguno / remoto —</option>
                  {(sitiosFrente.length ? sitiosFrente : SITIOS).map(s => (
                    <option key={s.codigo} value={s.codigo}>{s.nombre} ({s.tipo})</option>
                  ))}
                </select>
              </Field>

              {frente.usaCampanas && (
                <Field label="Campaña / tarea que atiende">
                  <select className="input-field" value={draft.campana || ''} onChange={e => setDraft(d => ({ ...d, campana: e.target.value }))}>
                    <option value="">— ninguna —</option>
                    {(campanasFrente.length ? campanasFrente : CAMPANAS).map(c => (
                      <option key={c.id} value={c.codigo}>{c.nombre}</option>
                    ))}
                  </select>
                </Field>
              )}

              {frente.usaTerritorioZona && (
                <Field label="Territorio / zona / SPT operativo">
                  <select className="input-field" value={draft.territorio || ''} onChange={e => setDraft(d => ({ ...d, territorio: e.target.value }))}>
                    <option value="">— seleccionar —</option>
                    {territorios.map(t => (
                      <option key={t.id} value={t.id}>{t.nombreNivel}: {t.nombre}</option>
                    ))}
                  </select>
                </Field>
              )}

              <Field label="Nota / observación">
                <input className="input-field" value={draft.nota || ''} onChange={e => setDraft(d => ({ ...d, nota: e.target.value }))} placeholder="Ej: cubriendo incapacidad" />
              </Field>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 16 }}>
                <button className="btn-primary" type="button" style={{ width: '100%', justifyContent: 'center' }} onClick={() => saveDrawer(true)} disabled={!canEdit}>
                  Guardar celda
                </button>
                <button className="btn-secondary" type="button" style={{ width: '100%', justifyContent: 'center' }} onClick={() => { setFixPeriodoModal({ personaId: drawerCell.personaId }); }}>
                  Fijar estos atributos en todo el periodo (HU42)
                </button>
                <button className="btn-secondary" type="button" style={{ width: '100%', justifyContent: 'center' }} onClick={() => navigate('S19', { personaId: drawerCell.personaId, diaIdx: drawerCell.diaIdx })}>
                  → Ver cobertura / historial
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {massModal && (
        <Modal title={`Asignación masiva — ${selectedCells.size} celdas`} onClose={() => setMassModal(false)}>
          <Field label="Turno / Estado a aplicar">
            <select className="input-field" value={massTurno} onChange={e => setMassTurno(e.target.value)}>
              {TURNOS.filter(t => t.frenteId === frente.id || t.frenteId === 'CC').map(t => <option key={t.codigo} value={t.codigo}>{t.codigo} — {t.nombre}</option>)}
              {ESTADOS_CELDA.filter(e => e.asignable).map(e => <option key={e.codigo} value={e.codigo}>{e.codigo} — {e.nombre}</option>)}
            </select>
          </Field>
          {frente.usaModalidad && (
            <Field label="Modalidad">
              <select className="input-field" value={massAttrs.modalidad} onChange={e => setMassAttrs(a => ({ ...a, modalidad: e.target.value }))}>
                {MODALIDADES.map(m => <option key={m.codigo} value={m.codigo}>{m.nombre}</option>)}
              </select>
            </Field>
          )}
          <Field label="Sitio / SPT">
            <select className="input-field" value={massAttrs.sitio} onChange={e => setMassAttrs(a => ({ ...a, sitio: e.target.value }))}>
              <option value="">— sin cambiar / vacío —</option>
              {SITIOS.map(s => <option key={s.codigo} value={s.codigo}>{s.nombre}</option>)}
            </select>
          </Field>
          {frente.usaCampanas && (
            <Field label="Campaña">
              <select className="input-field" value={massAttrs.campana} onChange={e => setMassAttrs(a => ({ ...a, campana: e.target.value }))}>
                {CAMPANAS.map(c => <option key={c.id} value={c.codigo}>{c.nombre}</option>)}
              </select>
            </Field>
          )}
          <div className="helper-text">Sobrescribe las {selectedCells.size} celdas seleccionadas. Queda en historial.</div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" onClick={() => setMassModal(false)}>Cancelar</button>
            <button className="btn-primary" onClick={applyMass}>Aplicar →</button>
          </div>
        </Modal>
      )}

      {fixPeriodoModal && (
        <Modal title="Fijar atributos en todo el periodo" onClose={() => setFixPeriodoModal(null)}>
          <div className="helper-text" style={{ marginBottom: 12 }}>
            Persona: <strong>{personas.find(x => x.id === fixPeriodoModal.personaId)?.nombre}</strong>.
            Aplica los mismos atributos a todos los días del periodo (no cambia el turno/estado de cada día). HU42.
          </div>
          {frente.usaModalidad && (
            <Field label="Modalidad">
              <select className="input-field" id="fix-mod" defaultValue="PRE">
                {MODALIDADES.map(m => <option key={m.codigo} value={m.codigo}>{m.nombre}</option>)}
              </select>
            </Field>
          )}
          <Field label="Sitio / SPT">
            <select className="input-field" id="fix-sitio" defaultValue="S01">
              <option value="">— ninguno —</option>
              {SITIOS.map(s => <option key={s.codigo} value={s.codigo}>{s.nombre}</option>)}
            </select>
          </Field>
          {frente.usaCampanas && (
            <Field label="Campaña">
              <select className="input-field" id="fix-camp" defaultValue="DS">
                <option value="">— ninguna —</option>
                {CAMPANAS.map(c => <option key={c.id} value={c.codigo}>{c.nombre}</option>)}
              </select>
            </Field>
          )}
          {frente.usaTerritorioZona && (
            <Field label="Territorio">
              <select className="input-field" id="fix-terr" defaultValue="">
                <option value="">— ninguno —</option>
                {territorios.map(t => <option key={t.id} value={t.id}>{t.nombre}</option>)}
              </select>
            </Field>
          )}
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" type="button" onClick={() => setFixPeriodoModal(null)}>Cancelar</button>
            <button
              className="btn-primary"
              type="button"
              onClick={() => {
                const modalidad = (document.getElementById('fix-mod') as HTMLSelectElement | null)?.value;
                const sitio = (document.getElementById('fix-sitio') as HTMLSelectElement | null)?.value ?? '';
                const campana = (document.getElementById('fix-camp') as HTMLSelectElement | null)?.value;
                const territorio = (document.getElementById('fix-terr') as HTMLSelectElement | null)?.value;
                fijarPeriodo(fixPeriodoModal.personaId, {
                  modalidad: frente.usaModalidad ? modalidad : undefined,
                  sitio,
                  campana: frente.usaCampanas ? campana : undefined,
                  territorio: frente.usaTerritorioZona ? territorio : undefined,
                });
              }}
            >
              Aplicar a todo el periodo
            </button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S18</div>
    </div>
  );
}

// ─── S19 Panel cobertura y conflictos ────────────────────────────────────────
function S19Cobertura({ navigate, params, onToast, role }: Props) {
  const malla = MALLAS.find(m => m.id === params?.mallaId) ?? MALLAS[0];
  return (
    <div style={{ padding: '24px 28px', maxWidth: 860 }}>
      <Breadcrumb items={[{ label: 'B. Construcción' }, { label: 'S18', onClick: () => navigate('S18', params) }, { label: 'S19 Cobertura/Conflictos' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Cobertura y conflictos</div>
          <div className="page-subtitle">{malla.nombre} — resultados del motor de reglas. HU33</div>
        </div>
        <button className="btn-secondary" onClick={() => navigate('S13')}>→ Motor de reglas (S13)</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 14, marginBottom: 20 }}>
        {[
          { label: 'Celdas asignadas', value: 62, total: 70, ok: true },
          { label: 'Conflictos', value: CONFLICTOS_CC.length, ok: CONFLICTOS_CC.length === 0 },
          { label: 'Cobertura promedio', value: '88%', ok: true },
        ].map(s => (
          <div key={s.label} className="card" style={{ padding: '16px 18px', textAlign: 'center' }}>
            <div style={{ fontSize: 26, fontWeight: 700, color: s.ok ? '#15803D' : '#DC2626' }}>{s.value}</div>
            <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{s.label}</div>
          </div>
        ))}
      </div>

      <div className="card" style={{ padding: '18px 20px', marginBottom: 16 }}>
        <div className="section-header">Conflictos activos (motor de reglas)</div>
        {CONFLICTOS_CC.length === 0
          ? <div style={{ color: '#15803D', fontSize: 13 }}>✅ Sin conflictos — malla apta para publicación</div>
          : CONFLICTOS_CC.map((c, i) => <ConflictoItem key={i} conflicto={c} codigoRegla={c.codigoRegla} />)}
      </div>

      <div className="card" style={{ padding: '18px 20px' }}>
        <div className="section-header">Cobertura por franja horaria</div>
        {[
          { franja: '06:00–14:00', cubierto: 3, minimo: 3 },
          { franja: '14:00–22:00', cubierto: 2, minimo: 3 },
          { franja: '22:00–06:00', cubierto: 1, minimo: 2 },
        ].map(f => (
          <div key={f.franja} style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 10 }}>
            <span style={{ fontSize: 12, width: 120 }}>{f.franja}</span>
            <div style={{ flex: 1, background: '#F3F4F6', borderRadius: 4, height: 12 }}>
              <div style={{ width: `${(f.cubierto / Math.max(f.minimo, f.cubierto)) * 100}%`, height: '100%', background: f.cubierto >= f.minimo ? '#22C55E' : '#EF4444', borderRadius: 4 }} />
            </div>
            <span style={{ fontSize: 12, color: f.cubierto >= f.minimo ? '#15803D' : '#DC2626' }}>{f.cubierto}/{f.minimo}</span>
          </div>
        ))}
      </div>
      <div className="screen-id">S19</div>
    </div>
  );
}

// ─── S20 Historial de la malla ────────────────────────────────────────────────
function S20Historial({ navigate, params, onToast, role }: Props) {
  const malla = MALLAS.find(m => m.id === params?.mallaId) ?? MALLAS[0];
  return (
    <div style={{ padding: '24px 28px', maxWidth: 860 }}>
      <Breadcrumb items={[{ label: 'B. Construcción' }, { label: 'S18', onClick: () => navigate('S18', params) }, { label: 'S20 Historial malla' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Historial de la malla</div>
          <div className="page-subtitle">{malla.nombre} — registro inmutable. HU34</div>
        </div>
      </div>
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead><tr><th>Fecha/hora</th><th>Usuario</th><th>Acción</th><th>Detalle</th></tr></thead>
          <tbody>
            {[
              { ts: '2025-03-03 08:12', user: 'jlopez@dc.co', accion: 'Creación', detalle: 'Malla creada en borrador' },
              { ts: '2025-03-03 09:45', user: 'jlopez@dc.co', accion: 'Asignación', detalle: 'Pérez González → T1 (lun 03-Mar)' },
              { ts: '2025-03-03 10:22', user: 'jlopez@dc.co', accion: 'Asignación masiva', detalle: '8 celdas → DES (semana 1 DOM)' },
              { ts: '2025-03-04 14:30', user: 'amorales@dc.co', accion: 'Env. revisión', detalle: 'Enviada al coordinador' },
              { ts: '2025-03-04 16:55', user: 'coord.cc@dc.co', accion: 'Rechazo', detalle: 'Faltan 2 agentes T5 martes 11' },
              { ts: '2025-03-05 09:10', user: 'jlopez@dc.co', accion: 'Corrección', detalle: 'García Ruíz → T5 (mar 11-Mar)' },
              { ts: '2025-03-05 11:00', user: 'jlopez@dc.co', accion: 'Env. revisión', detalle: 'Segunda revisión' },
              { ts: '2025-03-05 14:20', user: 'coord.cc@dc.co', accion: 'Publicación', detalle: 'Malla aprobada y publicada' },
            ].map((r, i) => (
              <tr key={i}>
                <td style={{ fontSize: 11, fontFamily: 'monospace' }}>{r.ts}</td>
                <td style={{ fontSize: 11 }}>{r.user}</td>
                <td><Chip label={r.accion} /></td>
                <td style={{ fontSize: 12 }}>{r.detalle}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="helper-text" style={{ marginTop: 8 }}>Registro inmutable — no se puede editar ni eliminar.</div>
      <div className="screen-id">S20</div>
    </div>
  );
}

// ─── S21 Patrones de rotación ─────────────────────────────────────────────────
function S21Patrones({ navigate, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({
    nombre: '',
    frente: 'CC',
    ciclo: '6',
    secuencia: 'T1,T1,T1,T1,DES,DES',
  });
  return (
    <div style={{ padding: '24px 28px', maxWidth: 860 }}>
      <Breadcrumb items={[{ label: 'B. Construcción' }, { label: 'S21 Patrones de rotación' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Patrones de rotación</div>
          <div className="page-subtitle">Plantillas de ciclo para modo Automático. HU35</div>
        </div>
        {canEdit
          ? <button className="btn-primary" type="button" onClick={() => setModalOpen(true)}>+ Nuevo patrón</button>
          : <DisabledBtn label="+ Nuevo patrón" reason="Sin permiso" />}
      </div>
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead><tr><th>Nombre</th><th>Ciclo (días)</th><th>Frente</th><th>Secuencia</th><th>Activo</th></tr></thead>
          <tbody>
            {[
              { nombre: 'Patrón 4x2', ciclo: 6, frente: 'CC', sec: ['T1', 'T1', 'T1', 'T1', 'DES', 'DES'] },
              { nombre: 'Rotación 5x2', ciclo: 7, frente: 'CC', sec: ['T5', 'T5', 'T5', 'T5', 'T5', 'DES', 'DES'] },
              { nombre: 'Híbrido 3T', ciclo: 9, frente: 'SITIO', sec: ['T1', 'T1', 'T1', 'DES', 'T8', 'T8', 'T8', 'DES', 'T5'] },
            ].map(p => (
              <tr key={p.nombre}>
                <td style={{ fontWeight: 500 }}>{p.nombre}</td>
                <td>{p.ciclo}</td>
                <td><Chip label={p.frente} /></td>
                <td>
                  <div style={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
                    {p.sec.map((t, i) => <span key={i} className={`chip turno-${t}`} style={{ fontSize: 9, padding: '2px 5px' }}>{t}</span>)}
                  </div>
                </td>
                <td><span style={{ color: '#15803D' }}>●</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {modalOpen && (
        <Modal title="Nuevo patrón de rotación" onClose={() => setModalOpen(false)}>
          <div className="field-group">
            <Field label="Nombre" required>
              <input className="input-field" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} placeholder="Ej: Ciclo 3x1 noche" />
            </Field>
            <div className="field-row">
              <Field label="Frente">
                <select className="input-field" value={form.frente} onChange={e => setForm(f => ({ ...f, frente: e.target.value }))}>
                  {FRENTES.filter(f => f.activo).map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
                </select>
              </Field>
              <Field label="Duración del ciclo (días)" required>
                <input className="input-field" type="number" min={1} max={60} value={form.ciclo} onChange={e => setForm(f => ({ ...f, ciclo: e.target.value }))} />
              </Field>
            </div>
            <Field label="Secuencia (códigos separados por coma)" required helper="Usa códigos de plantilla o estado: T1, T5, DES, VAC…">
              <input className="input-field" value={form.secuencia} onChange={e => setForm(f => ({ ...f, secuencia: e.target.value.toUpperCase() }))} placeholder="T1,T1,T1,DES" />
            </Field>
            <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginTop: 4 }}>
              {form.secuencia.split(',').map(s => s.trim()).filter(Boolean).map((t, i) => (
                <span key={i} className={`chip turno-${t}`} style={{ fontSize: 10 }}>{t}</span>
              ))}
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" type="button" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button className="btn-primary" type="button" onClick={() => {
              if (!form.nombre.trim() || !form.secuencia.trim()) { onToast('Completa nombre y secuencia', '', 'warning'); return; }
              onToast('Patrón creado', form.nombre, 'success');
              setModalOpen(false);
            }}>Guardar patrón</button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S21</div>
    </div>
  );
}

// ─── S22 Simular / Aplicar rotación ──────────────────────────────────────────
function S22Simular({ navigate, params, onToast, role }: Props) {
  const [simDone, setSimDone] = useState(false);
  const malla = MALLAS.find(m => m.id === params?.mallaId) ?? MALLAS[0];
  const canEdit = puedeEditar(role);
  return (
    <div style={{ padding: '24px 28px', maxWidth: 800 }}>
      <Breadcrumb items={[{ label: 'B. Construcción' }, { label: 'S18', onClick: () => navigate('S18', params) }, { label: 'S22 Simular rotación' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Simular y aplicar rotación</div>
          <div className="page-subtitle">{malla.nombre} — vista previa antes de aplicar. HU36</div>
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <div className="card" style={{ padding: '20px 22px' }}>
          <div className="section-header">Configuración</div>
          <Field label="Patrón de rotación">
            <select className="input-field">
              <option>Patrón 4x2 (CC)</option>
              <option>Rotación 5x2 (CC)</option>
              <option>Híbrido 3T (SITIO)</option>
            </select>
          </Field>
          <Field label="Inicio del ciclo">
            <input className="input-field" type="date" defaultValue="2025-03-03" />
          </Field>
          <Field label="Personas">
            <select className="input-field"><option>Todas las personas (5)</option><option>Solo agentes T1</option></select>
          </Field>
          <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
            <button className="btn-secondary" style={{ flex: 1, justifyContent: 'center' }} onClick={() => setSimDone(true)}>🔍 Simular</button>
            {simDone && canEdit && (
              <button className="btn-primary" style={{ flex: 1, justifyContent: 'center' }} onClick={() => { onToast('Rotación aplicada', 'Patrón 4x2 → 5 personas', 'success'); navigate('S18', params); }}>✓ Aplicar</button>
            )}
          </div>
        </div>
        <div className="card" style={{ padding: '20px 22px' }}>
          <div className="section-header">Vista previa</div>
          {!simDone
            ? <div style={{ textAlign: 'center', color: 'var(--clr-text-muted)', padding: '32px 0' }}>Configura y haz clic en <em>Simular</em> para ver la previsualización.</div>
            : (
              <>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 3, marginBottom: 8 }}>
                  {DIAS_SEM.map(d => <div key={d} style={{ textAlign: 'center', fontSize: 10, fontWeight: 600, color: 'var(--clr-text-muted)' }}>{d}</div>)}
                  {['T1', 'T1', 'T1', 'T1', 'DES', 'DES', 'DES', 'T1', 'T1', 'T1', 'T1', 'DES', 'DES', 'DES'].map((t, i) => (
                    <div key={i} className={`chip turno-${t}`} style={{ justifyContent: 'center', fontSize: 9, padding: '4px 0' }}>{t}</div>
                  ))}
                </div>
                <div className="helper-text">Vista patrón 4x2. El ajuste manual siempre queda en historial (modo Automático).</div>
              </>
            )}
        </div>
      </div>
      <div className="screen-id">S22</div>
    </div>
  );
}

// ─── S23 (número reservado — redirige a S18) ──────────────────────────────────
// No existe como pantalla independiente según HU backlog.

// ─── S24 Publicación ──────────────────────────────────────────────────────────
function S24Publicacion({ navigate, params, onToast, role }: Props) {
  const [mallas, setMallas] = useState<Malla[]>(MALLAS);
  const malla = mallas.find(m => m.id === (params?.mallaId ?? MALLAS[0].id)) ?? mallas[0];
  const [motivoRechazo, setMotivoRechazo] = useState('');
  const [showRechazo, setShowRechazo] = useState(false);
  const canPublish = puedePublicar(role);

  function publicar() {
    setMallas(ms => ms.map(m => m.id === malla.id ? { ...m, estado: 'publicada' as MallaEstado } : m));
    onToast('Malla publicada', malla.nombre, 'success');
    navigate('S16');
  }

  function rechazar() {
    if (!motivoRechazo.trim()) { onToast('Indica el motivo', '', 'warning'); return; }
    setMallas(ms => ms.map(m => m.id === malla.id ? { ...m, estado: 'rechazada' as MallaEstado, motivoRechazo } : m));
    onToast('Malla rechazada', motivoRechazo, 'warning');
    setShowRechazo(false);
    navigate('S16');
  }

  return (
    <div style={{ padding: '24px 28px', maxWidth: 760 }}>
      <Breadcrumb items={[{ label: 'B. Construcción' }, { label: 'S16', onClick: () => navigate('S16') }, { label: 'S24 Publicación' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Flujo de publicación</div>
          <div className="page-subtitle">{malla.nombre} — aprobación y publicación. HU37</div>
        </div>
      </div>

      <div className="card" style={{ padding: '22px 24px', marginBottom: 20 }}>
        <div className="section-header">Estado actual</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 20 }}>
          <EstadoChip estado={malla.estado} />
          <span style={{ fontSize: 13, color: 'var(--clr-text-muted)' }}>{malla.periodo} · {malla.frenteNombre}</span>
        </div>

        {/* Timeline */}
        <div className="timeline">
          {[
            { label: 'Borrador', ok: true, ts: '2025-03-03 08:12' },
            { label: 'En revisión', ok: malla.estado === 'revision' || malla.estado === 'publicada', ts: malla.estado !== 'borrador' ? '2025-03-04 14:30' : '' },
            { label: 'Publicada', ok: malla.estado === 'publicada', ts: malla.estado === 'publicada' ? '2025-03-05 14:20' : '' },
          ].map((step, i) => (
            <div key={i} className={`timeline-item ${step.ok ? 'done' : ''}`}>
              <div className="timeline-dot" />
              <div>
                <div style={{ fontSize: 13, fontWeight: 500 }}>{step.label}</div>
                {step.ts && <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{step.ts}</div>}
              </div>
            </div>
          ))}
        </div>

        {malla.estado === 'rechazada' && (
          <div style={{ padding: '12px 16px', background: '#FEF2F2', borderRadius: 8, border: '1px solid #FECACA', marginTop: 16 }}>
            <div style={{ fontSize: 12, fontWeight: 600, color: '#DC2626', marginBottom: 4 }}>↩ Malla rechazada</div>
            <div style={{ fontSize: 12, color: '#7F1D1D' }}>{malla.motivoRechazo}</div>
          </div>
        )}
      </div>

      <div className="card" style={{ padding: '22px 24px' }}>
        <div className="section-header">Checklist previo a publicación</div>
        {[
          { label: 'Sin conflictos de bloqueo en el motor de reglas', ok: CONFLICTOS_CC.filter(c => c.tipo === 'bloqueo').length === 0 },
          { label: 'Cobertura mínima cubierta en todas las franjas', ok: false },
          { label: 'Malla en estado "En revisión"', ok: malla.estado === 'revision' },
          { label: 'Responsable de publicación con permiso activo', ok: canPublish },
        ].map(c => (
          <div key={c.label} style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
            <span style={{ fontSize: 16 }}>{c.ok ? '✅' : '❌'}</span>
            <span style={{ fontSize: 13, color: c.ok ? 'var(--clr-text-body)' : '#DC2626' }}>{c.label}</span>
          </div>
        ))}

        <div style={{ display: 'flex', gap: 8, marginTop: 20 }}>
          {canPublish ? (
            <>
              <button className="btn-primary" style={{ flex: 1, justifyContent: 'center' }} onClick={publicar}>
                ✓ Publicar malla
              </button>
              <button className="btn-secondary" style={{ flex: 1, justifyContent: 'center', borderColor: '#EF4444', color: '#DC2626' }} onClick={() => setShowRechazo(true)}>
                ✗ Rechazar
              </button>
            </>
          ) : (
            <DisabledBtn label="Solo el coordinador puede publicar" reason="Sin permiso de publicación para este rol" />
          )}
        </div>
      </div>

      {showRechazo && (
        <Modal title="Rechazar malla" onClose={() => setShowRechazo(false)}>
          <Field label="Motivo del rechazo" required>
            <textarea className="input-field" rows={3} value={motivoRechazo} onChange={e => setMotivoRechazo(e.target.value)} placeholder="Describe qué debe corregir el responsable…" style={{ resize: 'vertical' }} />
          </Field>
          <div className="helper-text">El responsable recibirá una notificación. La malla vuelve a estado <strong>Rechazada</strong> y el responsable la puede corregir y reenviar.</div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" onClick={() => setShowRechazo(false)}>Cancelar</button>
            <button className="btn-primary" style={{ background: '#DC2626' }} onClick={rechazar}>Confirmar rechazo</button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S24</div>
    </div>
  );
}

// ─── Router ───────────────────────────────────────────────────────────────────
export default function SB(props: Props) {
  const { screen } = props;
  if (screen === 'S16') return <S16Lista {...props} />;
  if (screen === 'S17') return <S17Crear {...props} />;
  if (screen === 'S18') return <S18Grilla {...props} />;
  if (screen === 'S19') return <S19Cobertura {...props} />;
  if (screen === 'S20') return <S20Historial {...props} />;
  if (screen === 'S21') return <S21Patrones {...props} />;
  if (screen === 'S22') return <S22Simular {...props} />;
  if (screen === 'S24') return <S24Publicacion {...props} />;
  return <S16Lista {...props} />;
}
