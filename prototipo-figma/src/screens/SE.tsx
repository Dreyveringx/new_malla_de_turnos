import { useState } from 'react';
import { Breadcrumb, Chip, DisabledBtn } from '../Shell';
import { PERSONAS, MALLAS, FRENTES, TURNOS, type Rol, puedeVerReportes, puedeExportar } from '../data';

interface Props {
  screen: string;
  navigate: (s: string, p?: any) => void;
  params: any;
  onToast: (msg: string, desc: string, type: 'success' | 'error' | 'warning') => void;
  role: Rol;
}

const HORAS_DEMO = [
  { nombre: 'Pérez González, J.', cedula: '1090456789', frente: 'CC', ordi: 88, noct: 12, dom: 8, fest: 4, hexa: 2, hexn: 0, total: 114 },
  { nombre: 'Ramírez Castro, A.', cedula: '1090567890', frente: 'CC', ordi: 96, noct: 0, dom: 8, fest: 0, hexa: 0, hexn: 0, total: 104 },
  { nombre: 'Torres Medina, L.', cedula: '1092345678', frente: 'SITIO', ordi: 80, noct: 16, dom: 0, fest: 8, hexa: 0, hexn: 4, total: 108 },
  { nombre: 'García Ruíz, R.', cedula: '1091234567', frente: 'CC', ordi: 72, noct: 8, dom: 8, fest: 4, hexa: 4, hexn: 0, total: 96 },
  { nombre: 'Martínez J., P.', cedula: '1093456789', frente: 'MESA', ordi: 104, noct: 0, dom: 0, fest: 0, hexa: 0, hexn: 0, total: 104 },
];

// ─── S33 Horas del periodo (nómina) ───────────────────────────────────────────
function S33Horas({ navigate, params, onToast, role }: Props) {
  const canVer = puedeVerReportes(role);
  const canExport = puedeExportar(role);
  const [filtroFrente, setFiltroFrente] = useState('');
  const [corte, setCorte] = useState('Corte 02 — 16/01 al 31/01');

  const visible = HORAS_DEMO.filter(h => !filtroFrente || h.frente === filtroFrente);

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1200 }}>
      <Breadcrumb items={[{ label: 'E. Reportes' }, { label: 'S33 Horas del periodo' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Horas del periodo — nómina</div>
          <div className="page-subtitle">Reporte de horas por tipo. Sin liquidación en pesos — solo horas. HU64</div>
        </div>
        {canExport
          ? <button className="btn-primary" onClick={() => { onToast('Excel generado', 'horas_nomina_CC_2025-01.xlsx', 'success'); navigate('S34'); }}>Exportar →</button>
          : <DisabledBtn label="Exportar" reason="Sin permiso de exportación" />}
      </div>

      {!canVer && (
        <div style={{ padding: '12px 16px', background: '#FEF2F2', borderRadius: 8, border: '1px solid #FECACA', marginBottom: 16 }}>
          <strong style={{ color: '#DC2626' }}>Acceso restringido</strong> — Solo TH/Nómina puede ver el reporte de horas completo.
        </div>
      )}

      <div className="filter-bar" style={{ marginBottom: 16 }}>
        <select className="input-field" style={{ width: 260 }} value={corte} onChange={e => setCorte(e.target.value)}>
          <option>Corte 01 — 01/01 al 15/01</option>
          <option>Corte 02 — 16/01 al 31/01</option>
          <option>Corte 03 — 01/02 al 15/02</option>
        </select>
        <select className="input-field" style={{ width: 180 }} value={filtroFrente} onChange={e => setFiltroFrente(e.target.value)}>
          <option value="">Todos los frentes</option>
          {FRENTES.map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
        </select>
      </div>

      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead>
            <tr>
              <th>Funcionario</th><th>Cédula</th><th>Frente</th>
              <th title="Horas ordinarias">ORDI</th>
              <th title="Horas nocturnas">NOCT</th>
              <th title="Horas dominicales">DOM</th>
              <th title="Horas festivas">FEST</th>
              <th title="Horas extra diurnas">H.EXD</th>
              <th title="Horas extra nocturnas">H.EXN</th>
              <th style={{ fontWeight: 700 }}>Total h</th>
            </tr>
          </thead>
          <tbody>
            {visible.map(h => (
              <tr key={h.cedula}>
                <td style={{ fontWeight: 500, fontSize: 12 }}>{h.nombre}</td>
                <td style={{ fontSize: 11, fontFamily: 'monospace' }}>{h.cedula}</td>
                <td><Chip label={h.frente} /></td>
                <td style={{ textAlign: 'right' }}>{h.ordi}</td>
                <td style={{ textAlign: 'right', color: h.noct > 0 ? '#4A628A' : 'inherit' }}>{h.noct}</td>
                <td style={{ textAlign: 'right', color: h.dom > 0 ? '#7C3AED' : 'inherit' }}>{h.dom}</td>
                <td style={{ textAlign: 'right', color: h.fest > 0 ? '#B45309' : 'inherit' }}>{h.fest}</td>
                <td style={{ textAlign: 'right', color: h.hexa > 0 ? '#0E7490' : 'inherit' }}>{h.hexa}</td>
                <td style={{ textAlign: 'right', color: h.hexn > 0 ? '#DC2626' : 'inherit' }}>{h.hexn}</td>
                <td style={{ textAlign: 'right', fontWeight: 700 }}>{h.total}</td>
              </tr>
            ))}
            <tr style={{ background: '#F3F4F6', fontWeight: 700 }}>
              <td colSpan={3}>TOTAL</td>
              <td style={{ textAlign: 'right' }}>{visible.reduce((s, h) => s + h.ordi, 0)}</td>
              <td style={{ textAlign: 'right' }}>{visible.reduce((s, h) => s + h.noct, 0)}</td>
              <td style={{ textAlign: 'right' }}>{visible.reduce((s, h) => s + h.dom, 0)}</td>
              <td style={{ textAlign: 'right' }}>{visible.reduce((s, h) => s + h.fest, 0)}</td>
              <td style={{ textAlign: 'right' }}>{visible.reduce((s, h) => s + h.hexa, 0)}</td>
              <td style={{ textAlign: 'right' }}>{visible.reduce((s, h) => s + h.hexn, 0)}</td>
              <td style={{ textAlign: 'right' }}>{visible.reduce((s, h) => s + h.total, 0)}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div className="helper-text" style={{ marginTop: 8 }}>
        <strong>Sin pesos.</strong> Este módulo entrega solo horas a nómina. La liquidación se hace en el módulo de Nómina de GRH.
      </div>
      <div className="screen-id">S33</div>
    </div>
  );
}

// ─── S34 Exportación Excel/PDF ────────────────────────────────────────────────
function S34Export({ navigate, params, onToast, role }: Props) {
  const canExport = puedeExportar(role);
  const [formato, setFormato] = useState<'xlsx' | 'pdf' | 'csv'>('xlsx');

  return (
    <div style={{ padding: '24px 28px', maxWidth: 760 }}>
      <Breadcrumb items={[{ label: 'E. Reportes' }, { label: 'S34 Exportación' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Exportación de reportes</div>
          <div className="page-subtitle">Excel, PDF y CSV de mallas, horas y cobertura. HU65</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {[
          { titulo: 'Malla completa del periodo', desc: 'Grilla con todos los turnos y estados por funcionario', icon: '📋' },
          { titulo: 'Horas para nómina', desc: 'ORDI / NOCT / DOM / FEST / H.EXD / H.EXN por persona', icon: '⏱️' },
          { titulo: 'Reporte de cobertura', desc: 'Cobertura por franja horaria y comparativa con mínimos', icon: '📊' },
          { titulo: 'Historial de cambios', desc: 'Novedades y modificaciones del periodo seleccionado', icon: '📜' },
        ].map(r => (
          <div key={r.titulo} className="card" style={{ padding: '18px 20px' }}>
            <div style={{ fontSize: 28, marginBottom: 8 }}>{r.icon}</div>
            <div style={{ fontWeight: 600, fontSize: 13, marginBottom: 4 }}>{r.titulo}</div>
            <div style={{ fontSize: 11, color: 'var(--clr-text-muted)', marginBottom: 14 }}>{r.desc}</div>
            <div style={{ display: 'flex', gap: 6, marginBottom: 12 }}>
              {(['xlsx', 'pdf', 'csv'] as const).map(f => (
                <button key={f} className={formato === f ? 'btn-primary' : 'btn-secondary'} style={{ height: 28, fontSize: 11 }} onClick={() => setFormato(f)}>.{f}</button>
              ))}
            </div>
            {canExport
              ? <button className="btn-primary" style={{ width: '100%', justifyContent: 'center' }} onClick={() => onToast(`Descargando ${formato}`, r.titulo, 'success')}>Descargar {formato.toUpperCase()} ↓</button>
              : <DisabledBtn label={`Descargar ${formato.toUpperCase()}`} reason="Sin permiso de exportación" />}
          </div>
        ))}
      </div>
      <div className="screen-id">S34</div>
    </div>
  );
}

// ─── S35 Dashboard cobertura ──────────────────────────────────────────────────
function S35Dashboard({ navigate, params, onToast, role }: Props) {
  return (
    <div style={{ padding: '24px 28px', maxWidth: 1000 }}>
      <Breadcrumb items={[{ label: 'E. Reportes' }, { label: 'S35 Dashboard cobertura' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Dashboard de cobertura</div>
          <div className="page-subtitle">Métricas de ocupación y cobertura por frente. HU66</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 14, marginBottom: 20 }}>
        {[
          { label: 'Horas programadas', value: '1 840h', color: '#4A628A' },
          { label: 'Cobertura media', value: '91%', color: '#15803D' },
          { label: 'Días bajo mínimo', value: '3', color: '#DC2626' },
          { label: 'Novedades mes', value: '12', color: '#92400E' },
        ].map(m => (
          <div key={m.label} className="card" style={{ padding: '16px 18px', textAlign: 'center' }}>
            <div style={{ fontSize: 24, fontWeight: 700, color: m.color }}>{m.value}</div>
            <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{m.label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Cobertura por frente (%)</div>
          {FRENTES.filter(f => f.activo).map(f => {
            const pct = f.id === 'CC' ? 88 : f.id === 'SITIO' ? 95 : f.id === 'MESA' ? 100 : 76;
            return (
              <div key={f.id} style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
                <span style={{ fontSize: 12, width: 80 }}>{f.nombre}</span>
                <div style={{ flex: 1, background: '#F3F4F6', borderRadius: 4, height: 10 }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: pct >= 90 ? '#22C55E' : pct >= 75 ? '#F59E0B' : '#EF4444', borderRadius: 4 }} />
                </div>
                <span style={{ fontSize: 12, fontWeight: 600, color: pct >= 90 ? '#15803D' : pct >= 75 ? '#92400E' : '#DC2626', width: 36 }}>{pct}%</span>
              </div>
            );
          })}
        </div>
        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Top novedades del mes</div>
          {[
            { tipo: 'INC', cant: 5, label: 'Incapacidades' },
            { tipo: 'VAC', cant: 4, label: 'Vacaciones' },
            { tipo: 'PER', cant: 2, label: 'Permisos' },
            { tipo: 'COM', cant: 1, label: 'Compensatorios' },
          ].map(n => (
            <div key={n.tipo} style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
              <span className={`chip turno-${n.tipo}`} style={{ minWidth: 40, justifyContent: 'center' }}>{n.tipo}</span>
              <div style={{ flex: 1, background: '#F3F4F6', borderRadius: 4, height: 8 }}>
                <div style={{ width: `${(n.cant / 5) * 100}%`, height: '100%', background: 'var(--clr-primary)', borderRadius: 4 }} />
              </div>
              <span style={{ fontSize: 12 }}>{n.cant}</span>
              <span style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{n.label}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="screen-id">S35</div>
    </div>
  );
}

// ─── S36 Exportar cobertura terceros ──────────────────────────────────────────
function S36CobertTerceros({ navigate, params, onToast, role }: Props) {
  const canExport = puedeExportar(role);
  return (
    <div style={{ padding: '24px 28px', maxWidth: 760 }}>
      <Breadcrumb items={[{ label: 'E. Reportes' }, { label: 'S36 Cobertura terceros' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Reporte cobertura — terceros</div>
          <div className="page-subtitle">Exportar cobertura para validación de terceros/outsourcing. HU67</div>
        </div>
        {canExport
          ? <button className="btn-primary" onClick={() => onToast('Reporte terceros generado', '', 'success')}>Generar reporte</button>
          : <DisabledBtn label="Generar reporte" reason="Sin permiso" />}
      </div>
      <div className="card" style={{ padding: '20px 22px' }}>
        <div className="section-header">Filtros de exportación</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          <div>
            <label style={{ fontSize: 12, color: 'var(--clr-text-muted)', display: 'block', marginBottom: 4 }}>Proveedor / Tercero</label>
            <select className="input-field">
              <option>DataServ SAS</option><option>TechOps Colombia</option><option>Todos</option>
            </select>
          </div>
          <div>
            <label style={{ fontSize: 12, color: 'var(--clr-text-muted)', display: 'block', marginBottom: 4 }}>Frente</label>
            <select className="input-field">
              {FRENTES.map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
            </select>
          </div>
          <div>
            <label style={{ fontSize: 12, color: 'var(--clr-text-muted)', display: 'block', marginBottom: 4 }}>Periodo inicio</label>
            <input className="input-field" type="date" defaultValue="2025-03-01" />
          </div>
          <div>
            <label style={{ fontSize: 12, color: 'var(--clr-text-muted)', display: 'block', marginBottom: 4 }}>Periodo fin</label>
            <input className="input-field" type="date" defaultValue="2025-03-31" />
          </div>
        </div>
        <div style={{ marginTop: 16, padding: '12px 16px', background: 'var(--clr-filter-bg)', borderRadius: 8, fontSize: 12 }}>
          El reporte incluye: nombre persona, cédula, frente, horas por tipo, sin pesos. Compatible con formato SENA/SIGA.
        </div>
      </div>
      <div className="screen-id">S36</div>
    </div>
  );
}

// ─── S37 Cruce TH + novedades ─────────────────────────────────────────────────
function S37CruceTH({ navigate, params, onToast, role }: Props) {
  const [step, setStep] = useState(0);
  return (
    <div style={{ padding: '24px 28px', maxWidth: 860 }}>
      <Breadcrumb items={[{ label: 'E. Reportes' }, { label: 'S37 Cruce TH' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Importar TH + cruce de novedades</div>
          <div className="page-subtitle">Cruzar novedades de TH (licencias, permisos) con la malla publicada. HU68</div>
        </div>
      </div>

      <div className="wizard-steps" style={{ marginBottom: 20 }}>
        {['Subir archivo TH', 'Cruce automático', 'Diferencias', 'Aplicar ajustes'].map((s, i) => (
          <div key={s} className={`wizard-step ${i === step ? 'active' : i < step ? 'done' : ''}`}>
            <div className="wizard-step-num">{i < step ? '✓' : i + 1}</div>
            <div className="wizard-step-label">{s}</div>
          </div>
        ))}
      </div>

      {step === 0 && (
        <div className="card" style={{ padding: '24px' }}>
          <div className="import-dropzone">
            <div style={{ fontSize: 36 }}>📁</div>
            <div style={{ fontSize: 14, fontWeight: 500, marginTop: 10 }}>Subir archivo de novedades TH</div>
            <div style={{ fontSize: 12, color: 'var(--clr-text-muted)', marginTop: 4 }}>Formato: .xlsx — columnas: CEDULA, TIPO_NOVEDAD, FECHA_INICIO, FECHA_FIN</div>
          </div>
          <div style={{ textAlign: 'right', marginTop: 16 }}>
            <button className="btn-primary" onClick={() => setStep(1)}>Cargar demo →</button>
          </div>
        </div>
      )}

      {step === 1 && (
        <div className="card" style={{ padding: '24px' }}>
          <div className="section-header">Cruce automático</div>
          <div className="helper-text" style={{ marginBottom: 12 }}>TH reporta 18 novedades para el periodo. El sistema cruzó con la malla publicada:</div>
          {[
            { match: 'Coincide', cant: 14, color: '#15803D', icon: '✅' },
            { match: 'TH sin malla', cant: 3, color: '#92400E', icon: '⚠️' },
            { match: 'Conflicto (tipo difiere)', cant: 1, color: '#DC2626', icon: '❌' },
          ].map(r => (
            <div key={r.match} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 14px', borderRadius: 8, border: `1px solid ${r.color}30`, background: `${r.color}08`, marginBottom: 8 }}>
              <span style={{ fontSize: 20 }}>{r.icon}</span>
              <span style={{ fontSize: 13, flex: 1 }}>{r.match}</span>
              <span style={{ fontSize: 18, fontWeight: 700, color: r.color }}>{r.cant}</span>
            </div>
          ))}
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 12 }}>
            <button className="btn-secondary" onClick={() => setStep(0)}>← Atrás</button>
            <button className="btn-primary" onClick={() => setStep(2)}>Ver diferencias →</button>
          </div>
        </div>
      )}

      {step >= 2 && (
        <div className="card" style={{ padding: '24px' }}>
          <div className="section-header">Diferencias a resolver</div>
          <div className="card" style={{ padding: '12px 16px', marginBottom: 12, borderLeft: '4px solid #F59E0B' }}>
            <div style={{ fontSize: 12, fontWeight: 600 }}>Pérez González — 2025-03-15</div>
            <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>TH: INC · Malla: T1 · Acción: aplicar INC en malla</div>
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
            <button className="btn-secondary" onClick={() => setStep(1)}>← Atrás</button>
            <button className="btn-primary" onClick={() => { setStep(0); onToast('Cruce TH aplicado', '1 ajuste en malla', 'success'); }}>Aplicar ajustes ✓</button>
          </div>
        </div>
      )}
      <div className="screen-id">S37</div>
    </div>
  );
}

// ─── Router ───────────────────────────────────────────────────────────────────
export default function SE(props: Props) {
  const { screen } = props;
  if (screen === 'S33') return <S33Horas {...props} />;
  if (screen === 'S34') return <S34Export {...props} />;
  if (screen === 'S35') return <S35Dashboard {...props} />;
  if (screen === 'S36') return <S36CobertTerceros {...props} />;
  if (screen === 'S37') return <S37CruceTH {...props} />;
  return <S33Horas {...props} />;
}
