import { useState } from 'react';
import { Breadcrumb, Modal, Field, Chip, EstadoChip, DisabledBtn } from '../Shell';
import { PERSONAS, MALLAS, ESTADOS_CELDA_V2 as ESTADOS_CELDA, TURNOS, FRENTES, type Rol, puedeEditar } from '../data';

interface Props {
  screen: string;
  navigate: (s: string, p?: any) => void;
  params: any;
  onToast: (msg: string, desc: string, type: 'success' | 'error' | 'warning') => void;
  role: Rol;
}

// ─── S25 Novedad en celda ─────────────────────────────────────────────────────
function S25Novedad({ navigate, params, onToast, role }: Props) {
  const persona = PERSONAS.find(p => p.id === params?.personaId) ?? PERSONAS[0];
  const [tipo, setTipo] = useState('INC');
  const [fecha, setFecha] = useState('2025-03-10');
  const [nota, setNota] = useState('');
  const canEdit = puedeEditar(role);

  const TIPOS_NOV = ESTADOS_CELDA.filter(e => ['INC', 'VAC', 'PER', 'COM'].includes(e.codigo));

  return (
    <div style={{ padding: '24px 28px', maxWidth: 700 }}>
      <Breadcrumb items={[{ label: 'C. Consulta' }, { label: 'S25 Novedad en celda' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Registrar novedad en celda</div>
          <div className="page-subtitle">Modifica una celda de una malla publicada. HU48</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <div className="card" style={{ padding: '20px 22px' }}>
          <div className="section-header">Datos de la novedad</div>
          <Field label="Funcionario">
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 12px', border: '1px solid var(--clr-border)', borderRadius: 6, background: 'var(--clr-filter-bg)' }}>
              <div className="avatar-circle" style={{ width: 28, height: 28, fontSize: 11 }}>{persona.nombre.split(' ').map(w => w[0]).join('').slice(0, 2)}</div>
              <div>
                <div style={{ fontSize: 13, fontWeight: 500 }}>{persona.nombre}</div>
                <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{persona.cargo} · {persona.cedula}</div>
              </div>
            </div>
          </Field>
          <Field label="Frente"><input className="input-field" defaultValue={persona.frenteId} disabled /></Field>
          <Field label="Fecha afectada" required>
            <input className="input-field" type="date" value={fecha} onChange={e => setFecha(e.target.value)} disabled={!canEdit} />
          </Field>
          <Field label="Tipo de novedad" required>
            <select className="input-field" value={tipo} onChange={e => setTipo(e.target.value)} disabled={!canEdit}>
              {TIPOS_NOV.map(t => <option key={t.codigo} value={t.codigo}>{t.codigo} — {t.nombre}</option>)}
            </select>
          </Field>
          <Field label="Nota / justificación">
            <textarea className="input-field" rows={3} value={nota} onChange={e => setNota(e.target.value)} placeholder="Número de radicado, EPS, etc." disabled={!canEdit} style={{ resize: 'vertical' }} />
          </Field>
          {canEdit
            ? <button className="btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: 8 }} onClick={() => { onToast('Novedad registrada', `${persona.nombre} → ${tipo}`, 'success'); navigate('S26', { personaId: persona.id }); }}>Registrar novedad →</button>
            : <DisabledBtn label="Registrar novedad" reason="Sin permiso" />}
        </div>

        <div className="card" style={{ padding: '20px 22px' }}>
          <div className="section-header">Impacto del cambio</div>
          <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 16 }}>
            <div>
              <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>Antes</div>
              <span className="chip turno-T1" style={{ fontSize: 12 }}>T1 — 8h</span>
            </div>
            <span style={{ fontSize: 20, color: 'var(--clr-text-muted)' }}>→</span>
            <div>
              <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>Después</div>
              <span className={`chip turno-${tipo}`} style={{ fontSize: 12 }}>{tipo}</span>
            </div>
          </div>
          <div style={{ padding: '10px 14px', background: '#FFF8E1', borderRadius: 8, border: '1px solid #FDE68A', marginBottom: 12 }}>
            <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 4 }}>⚠️ Aviso de cobertura</div>
            <div style={{ fontSize: 11 }}>Esta novedad reduce la cobertura del frente a 2/3 agentes en la franja 06:00–14:00 del {fecha}. El motor de reglas alertará si baja del mínimo.</div>
          </div>
          <div style={{ fontSize: 12, color: 'var(--clr-text-muted)', marginBottom: 8 }}>El historial de la celda registrará este cambio como punto de cambio inmutable.</div>
          <button className="btn-secondary" style={{ width: '100%', justifyContent: 'center' }} onClick={() => navigate('S26', { personaId: persona.id })}>Ver historial celda (S26)</button>
        </div>
      </div>
      <div className="screen-id">S25</div>
    </div>
  );
}

// ─── S26 Historial de celda ────────────────────────────────────────────────────
function S26HistorialCelda({ navigate, params, onToast, role }: Props) {
  const persona = PERSONAS.find(p => p.id === params?.personaId) ?? PERSONAS[0];
  return (
    <div style={{ padding: '24px 28px', maxWidth: 860 }}>
      <Breadcrumb items={[{ label: 'C. Consulta' }, { label: 'S26 Historial de celda' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Historial de celda</div>
          <div className="page-subtitle">{persona.nombre} — registro inmutable de cambios. HU49</div>
        </div>
      </div>
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead><tr><th>Fecha/hora</th><th>Día afectado</th><th>Antes</th><th>Después</th><th>Usuario</th><th>Motivo</th></tr></thead>
          <tbody>
            {[
              { ts: '2025-03-03 09:45', dia: 'Lun 03-Mar', antes: '—', despues: 'T1', user: 'jlopez@dc.co', motivo: 'Asignación inicial' },
              { ts: '2025-03-05 11:22', dia: 'Lun 03-Mar', antes: 'T1', despues: 'INC', user: 'jlopez@dc.co', motivo: 'Incapacidad médica radicado 2025-0341' },
              { ts: '2025-03-07 08:10', dia: 'Vie 07-Mar', antes: '—', despues: 'T5', user: 'jlopez@dc.co', motivo: 'Asignación inicial' },
              { ts: '2025-03-08 14:30', dia: 'Vie 07-Mar', antes: 'T5', despues: 'VAC', user: 'jlopez@dc.co', motivo: 'Vacaciones aprobadas RH-2025-112' },
            ].map((r, i) => (
              <tr key={i}>
                <td style={{ fontSize: 11, fontFamily: 'monospace' }}>{r.ts}</td>
                <td style={{ fontSize: 12 }}>{r.dia}</td>
                <td>{r.antes === '—' ? <span style={{ color: 'var(--clr-text-muted)' }}>—</span> : <span className={`chip turno-${r.antes}`}>{r.antes}</span>}</td>
                <td><span className={`chip turno-${r.despues}`}>{r.despues}</span></td>
                <td style={{ fontSize: 11 }}>{r.user}</td>
                <td style={{ fontSize: 11 }}>{r.motivo}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="helper-text" style={{ marginTop: 8 }}>Registro inmutable — cada punto de cambio conserva el valor anterior y el usuario responsable.</div>
      <div className="screen-id">S26</div>
    </div>
  );
}

// ─── S27 Historial por funcionario ────────────────────────────────────────────
function S27HistorialFuncionario({ navigate, params, onToast, role }: Props) {
  const [personaId, setPersonaId] = useState(params?.personaId ?? PERSONAS[0].id);
  const persona = PERSONAS.find(p => p.id === personaId) ?? PERSONAS[0];

  return (
    <div style={{ padding: '24px 28px', maxWidth: 900 }}>
      <Breadcrumb items={[{ label: 'C. Consulta' }, { label: 'S27 Historial funcionario' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Historial por funcionario</div>
          <div className="page-subtitle">Línea de tiempo completa de cambios en todas sus celdas. HU50</div>
        </div>
      </div>

      <div className="filter-bar" style={{ marginBottom: 16 }}>
        <select className="input-field" style={{ width: 260 }} value={personaId} onChange={e => setPersonaId(e.target.value)}>
          {PERSONAS.map(p => <option key={p.id} value={p.id}>{p.nombre} — {p.cedula}</option>)}
        </select>
        <input className="input-field" type="date" defaultValue="2025-03-01" style={{ width: 160 }} />
        <input className="input-field" type="date" defaultValue="2025-03-31" style={{ width: 160 }} />
        <button className="btn-primary">Filtrar</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: 20 }}>
        <div className="card" style={{ padding: '16px 18px' }}>
          <div className="section-header">Funcionario</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
            <div className="avatar-circle" style={{ width: 44, height: 44, fontSize: 16 }}>{persona.nombre.split(' ').map(w => w[0]).join('').slice(0, 2)}</div>
            <div>
              <div style={{ fontWeight: 600 }}>{persona.nombre}</div>
              <div style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>{persona.cargo}</div>
              <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{persona.cedula}</div>
            </div>
          </div>
          <div className="section-header">Resumen marzo 2025</div>
          {[
            { label: 'Turnos T1', value: 9, color: '#4A628A' },
            { label: 'Turnos T5', value: 4, color: '#5C4DB1' },
            { label: 'Descansos', value: 8, color: '#6B7280' },
            { label: 'Incapacidades', value: 1, color: '#B91C1C' },
            { label: 'Vacaciones', value: 2, color: '#0E7490' },
            { label: 'Total horas', value: '104h', color: '#15803D' },
          ].map(s => (
            <div key={s.label} style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', borderBottom: '1px solid var(--clr-border)', fontSize: 12 }}>
              <span style={{ color: 'var(--clr-text-muted)' }}>{s.label}</span>
              <span style={{ fontWeight: 600, color: s.color }}>{s.value}</span>
            </div>
          ))}
        </div>

        <div className="card" style={{ padding: '16px 18px' }}>
          <div className="section-header">Cambios en el periodo</div>
          <div className="timeline">
            {[
              { ts: '2025-03-05', evento: 'T1 → INC (Lun 03-Mar)', motivo: 'Incapacidad radicado 2025-0341', tipo: 'novedad' },
              { ts: '2025-03-08', evento: 'T5 → VAC (Vie 07-Mar)', motivo: 'Vacaciones aprobadas RH-2025-112', tipo: 'novedad' },
              { ts: '2025-03-12', evento: 'Asignación masiva: 4 celdas → DES', motivo: 'Ajuste semana festiva', tipo: 'masivo' },
              { ts: '2025-03-15', evento: 'DES → COM (Mar 11-Mar)', motivo: 'Compensatorio por domingo trabajado', tipo: 'compensatorio' },
            ].map((ev, i) => (
              <div key={i} className="timeline-item done">
                <div className="timeline-dot" style={{ background: ev.tipo === 'novedad' ? '#DC2626' : ev.tipo === 'compensatorio' ? '#7C3AED' : '#4A628A' }} />
                <div>
                  <div style={{ fontSize: 12, fontWeight: 500 }}>{ev.evento}</div>
                  <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{ev.ts} · {ev.motivo}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="screen-id">S27</div>
    </div>
  );
}

// ─── S28 Quién está / Disponible ──────────────────────────────────────────────
function S28QuienEsta({ navigate, params, onToast, role }: Props) {
  const [fecha, setFecha] = useState('2025-03-10');
  const [filtroFrente, setFiltroFrente] = useState('');
  const [soloAsignables, setSoloAsignables] = useState(false);

  const personasFiltradas = PERSONAS
    .filter(p => !filtroFrente || p.frenteId === filtroFrente)
    .slice(0, 10);

  const ESTADO_MOCK: Record<string, string> = {
    'P001': 'T1', 'P002': 'DES', 'P003': 'INC', 'P004': 'T8', 'P005': 'COM',
    'P006': 'T5', 'P007': 'CAP', 'P008': 'VAC', 'P009': 'T1', 'P010': 'ACT',
  };

  const noAsignables = new Set(['CAP', 'ACT', 'INC', 'VAC', 'DES']);

  const visible = personasFiltradas.filter(p => {
    const est = ESTADO_MOCK[p.id] ?? 'T1';
    if (soloAsignables && noAsignables.has(est)) return false;
    return true;
  });

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1000 }}>
      <Breadcrumb items={[{ label: 'C. Consulta' }, { label: 'S28 Quién está / Disponible' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Quién está · Disponibilidad</div>
          <div className="page-subtitle">Consulta en tiempo real por frente y fecha. HU51–HU52</div>
        </div>
      </div>

      <div className="filter-bar" style={{ marginBottom: 16 }}>
        <input className="input-field" type="date" value={fecha} onChange={e => setFecha(e.target.value)} style={{ width: 180 }} />
        <select className="input-field" style={{ width: 200 }} value={filtroFrente} onChange={e => setFiltroFrente(e.target.value)}>
          <option value="">Todos los frentes</option>
          {FRENTES.filter(f => f.activo).map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
        </select>
        <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, cursor: 'pointer' }}>
          <input type="checkbox" checked={soloAsignables} onChange={e => setSoloAsignables(e.target.checked)} />
          Solo disponibles para asignar
          <span className="helper-text" style={{ marginLeft: 4 }}>(excluye CAP, ACT, INC, VAC, DES)</span>
        </label>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: 12, marginBottom: 20 }}>
        {visible.map(p => {
          const est = ESTADO_MOCK[p.id] ?? 'T1';
          const asignable = !noAsignables.has(est);
          return (
            <div key={p.id} className="card" style={{ padding: '14px 16px', borderLeft: `4px solid ${asignable ? '#22C55E' : '#9CA3AF'}` }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                <div className="avatar-circle" style={{ width: 32, height: 32, fontSize: 12 }}>{p.nombre.split(' ').map(w => w[0]).join('').slice(0, 2)}</div>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600 }}>{p.nombre.split(' ').slice(0, 2).join(' ')}</div>
                  <div style={{ fontSize: 10, color: 'var(--clr-text-muted)' }}>{p.cargo}</div>
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span className={`chip turno-${est}`} style={{ fontSize: 10 }}>{est}</span>
                {asignable
                  ? <span style={{ fontSize: 10, color: '#15803D', fontWeight: 600 }}>● Disponible</span>
                  : <span style={{ fontSize: 10, color: '#9CA3AF' }}>○ No asignable</span>}
                {(est === 'CAP' || est === 'ACT') && (
                  <span style={{ fontSize: 9, color: '#DC2626', fontStyle: 'italic' }}>no-asignable a casos</span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div className="helper-text">
        <strong>CAP (Capacitación) y ACT (Actividad)</strong> son estados <strong>no-asignables a casos</strong> (asignable=false en catálogo).
        El filtro "Solo disponibles" los excluye automáticamente. No existe pantalla separada de actividades — esta vista integra la consulta.
      </div>

      <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
        <button className="btn-secondary" onClick={() => navigate('S29')}>→ Cobertura del día (S29)</button>
        <button className="btn-secondary" onClick={() => navigate('S25')}>→ Registrar novedad (S25)</button>
      </div>
      <div className="screen-id">S28</div>
    </div>
  );
}

// ─── S29 Cobertura del día ────────────────────────────────────────────────────
function S29Cobertura({ navigate, params, onToast, role }: Props) {
  const [fecha, setFecha] = useState('2025-03-10');
  const [frenteId, setFrenteId] = useState('CC');

  return (
    <div style={{ padding: '24px 28px', maxWidth: 860 }}>
      <Breadcrumb items={[{ label: 'C. Consulta' }, { label: 'S29 Cobertura del día' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Cobertura del día</div>
          <div className="page-subtitle">Panel de cobertura operativa por frente y franja. HU53</div>
        </div>
      </div>

      <div className="filter-bar" style={{ marginBottom: 20 }}>
        <input className="input-field" type="date" value={fecha} onChange={e => setFecha(e.target.value)} style={{ width: 180 }} />
        <select className="input-field" style={{ width: 200 }} value={frenteId} onChange={e => setFrenteId(e.target.value)}>
          {FRENTES.filter(f => f.activo).map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
        </select>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 20 }}>
        {[
          { franja: '06:00–14:00', asignados: 3, minimo: 3, personas: ['Pérez G.', 'Ramírez C.', 'Torres M.'] },
          { franja: '14:00–22:00', asignados: 2, minimo: 3, personas: ['García R.', 'Martínez J.'] },
          { franja: '22:00–06:00', asignados: 1, minimo: 2, personas: ['López H.'] },
          { franja: 'Total disponibles', asignados: 6, minimo: 8, personas: [] },
        ].map(f => {
          const ok = f.asignados >= f.minimo;
          return (
            <div key={f.franja} className="card" style={{ padding: '16px 18px', borderLeft: `4px solid ${ok ? '#22C55E' : '#EF4444'}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                <span style={{ fontSize: 13, fontWeight: 600 }}>{f.franja}</span>
                <span style={{ fontSize: 20, fontWeight: 700, color: ok ? '#15803D' : '#DC2626' }}>{f.asignados}/{f.minimo}</span>
              </div>
              <div style={{ background: '#F3F4F6', borderRadius: 4, height: 8, marginBottom: 10 }}>
                <div style={{ width: `${Math.min((f.asignados / f.minimo) * 100, 100)}%`, height: '100%', background: ok ? '#22C55E' : '#EF4444', borderRadius: 4 }} />
              </div>
              {f.personas.length > 0 && (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                  {f.personas.map(n => <span key={n} style={{ fontSize: 10, background: '#E5E7EB', borderRadius: 10, padding: '2px 8px' }}>{n}</span>)}
                </div>
              )}
              {!ok && <div style={{ fontSize: 11, color: '#DC2626', marginTop: 6 }}>⚠️ Cobertura por debajo del mínimo (parámetro motor: MIN_COBERTURA_FRANJA={f.minimo})</div>}
            </div>
          );
        })}
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        <button className="btn-secondary" onClick={() => navigate('S28')}>← Quién está (S28)</button>
        <button className="btn-secondary" onClick={() => navigate('S25')}>+ Novedad en celda (S25)</button>
      </div>
      <div className="screen-id">S29</div>
    </div>
  );
}

// ─── Router ───────────────────────────────────────────────────────────────────
export default function SC(props: Props) {
  const { screen } = props;
  if (screen === 'S25') return <S25Novedad {...props} />;
  if (screen === 'S26') return <S26HistorialCelda {...props} />;
  if (screen === 'S27') return <S27HistorialFuncionario {...props} />;
  if (screen === 'S28') return <S28QuienEsta {...props} />;
  if (screen === 'S29') return <S29Cobertura {...props} />;
  return <S28QuienEsta {...props} />;
}
