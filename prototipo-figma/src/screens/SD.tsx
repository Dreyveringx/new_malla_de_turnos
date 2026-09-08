import { useMemo, useState } from 'react';
import { Breadcrumb } from '../Shell';
import { PERSONAS, MALLAS, TURNOS_WITH_HOURS as TURNOS, type Rol } from '../data';

interface Props {
  screen: string;
  navigate: (s: string, p?: any) => void;
  params: any;
  onToast: (msg: string, desc: string, type: 'success' | 'error' | 'warning') => void;
  role: Rol;
}

const DIAS_SEM = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];

type VistaPeriodo = 'semana' | 'quincena' | 'mes';

type DayCell = {
  d: Date;
  num: number;
  dow: string;
  dom: boolean;
  label: string;
  code: string;
  offset: number;
};

function codeForDay(dayOffset: number, seed = 0): string {
  const cycle = ['T1', 'T1', 'DES', 'T1', 'T5', 'T5', 'DES'];
  return cycle[(dayOffset + seed) % cycle.length];
}

function horaOf(code: string): string {
  const t = TURNOS.find(x => x.codigo === code);
  if (t) return `${t.horaInicio}–${t.horaFin}`;
  if (code === 'DES' || code === 'VAC' || code === 'INC') return '—';
  return '—';
}

function modalityOf(code: string): string {
  if (code === 'DES' || code === 'VAC' || code === 'INC') return '—';
  return code === 'T5' || code === 'T6' || code === 'TN1' ? 'Virtual' : 'Presencial';
}

function buildDays(vista: VistaPeriodo, anchor: Date): DayCell[] {
  const start = new Date(anchor);
  let count = 7;
  if (vista === 'quincena') count = 15;
  if (vista === 'mes') {
    const y = start.getFullYear();
    const m = start.getMonth();
    count = new Date(y, m + 1, 0).getDate();
    start.setDate(1);
  } else if (vista === 'semana') {
    const dow = start.getDay();
    const delta = dow === 0 ? -6 : 1 - dow;
    start.setDate(start.getDate() + delta);
  } else if (vista === 'quincena') {
    const dow = start.getDay();
    const delta = dow === 0 ? -6 : 1 - dow;
    start.setDate(start.getDate() + delta);
  }
  return Array.from({ length: count }, (_, i) => {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    return {
      d,
      num: d.getDate(),
      dow: DIAS_SEM[d.getDay() === 0 ? 6 : d.getDay() - 1],
      dom: d.getDay() === 0,
      label: `${DIAS_SEM[d.getDay() === 0 ? 6 : d.getDay() - 1]} ${d.getDate()}`,
      code: codeForDay(i),
      offset: i,
    };
  });
}

/** Celdas de calendario Lun–Dom con huecos al inicio/fin */
function toCalendarGrid(dias: DayCell[]) {
  if (dias.length === 0) return [] as Array<DayCell | null>;
  const first = dias[0].d;
  const padStart = first.getDay() === 0 ? 6 : first.getDay() - 1;
  const cells: Array<DayCell | null> = Array.from({ length: padStart }, () => null);
  dias.forEach(d => cells.push(d));
  while (cells.length % 7 !== 0) cells.push(null);
  return cells;
}

function VistaToggle({
  vista,
  setVista,
}: {
  vista: VistaPeriodo;
  setVista: (v: VistaPeriodo) => void;
}) {
  return (
    <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }}>
      <span style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>Periodo</span>
      {([
        ['semana', 'Semana'],
        ['quincena', 'Quincena'],
        ['mes', 'Mes'],
      ] as const).map(([id, label]) => (
        <button
          key={id}
          type="button"
          className={vista === id ? 'btn-primary' : 'btn-secondary'}
          style={{ height: 34, fontSize: 12 }}
          onClick={() => setVista(id)}
        >
          {label}
        </button>
      ))}
    </div>
  );
}

function CalendarioMiTurno({ dias }: { dias: DayCell[] }) {
  const cells = toCalendarGrid(dias);
  return (
    <div className="cal-month">
      {DIAS_SEM.map(d => (
        <div key={d} className="cal-weekday">{d}</div>
      ))}
      {cells.map((day, i) => (
        <div
          key={i}
          className={`cal-day ${!day ? 'cal-day-empty' : ''} ${day?.dom ? 'cal-day-dom' : ''} ${day && day.code !== 'DES' ? 'cal-day-work' : ''}`}
        >
          {day && (
            <>
              <div className="cal-day-num">{day.num}</div>
              <span className={`malla-chip turno-${day.code}`}>{day.code}</span>
              <div className="cal-day-hora">{horaOf(day.code)}</div>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

// ─── S30 Malla del grupo (vista operador) ─────────────────────────────────────
function S30MallaGrupo({ navigate }: Props) {
  const persona = PERSONAS[0];
  const malla = MALLAS.find(m => m.estado === 'publicada' && m.frenteId === 'CC') ?? MALLAS[0];
  const grupoPersonas = PERSONAS.filter(p => p.frenteId === malla.frenteId).slice(0, 5);
  const [vista, setVista] = useState<VistaPeriodo>('semana');
  const dias = useMemo(() => buildDays(vista, new Date(2026, 8, 1)), [vista]);

  function cellFor(row: number, day: number): string {
    return codeForDay(day, row);
  }

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1200 }}>
      <Breadcrumb items={[{ label: 'Mi programación' }, { label: 'Malla del grupo' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Programación del grupo — {malla.frenteNombre}</div>
          <div className="page-subtitle">Vista de solo lectura para el colaborador. HU67</div>
        </div>
        <button className="btn-secondary" type="button" onClick={() => navigate('S31')}>Mi turno →</button>
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12, alignItems: 'center', marginBottom: 14 }}>
        <VistaToggle vista={vista} setVista={setVista} />
        <span style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>
          Mostrando {dias.length} día{dias.length === 1 ? '' : 's'} · {malla.periodo}
        </span>
      </div>

      <div className="helper-text" style={{ marginBottom: 12 }}>
        Vista de solo lectura. El operador <strong>no acepta ni rechaza turnos</strong> — las notificaciones son informativas.
      </div>

      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-malla-readonly">
          <thead>
            <tr>
              <th className="col-persona">Persona</th>
              {dias.map((x, i) => (
                <th key={i} className={x.dom ? 'day-dom' : undefined}>
                  <div className="day-name">{x.dow}</div>
                  <div className="day-num">{x.num}</div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {grupoPersonas.map((p, pi) => {
              const isMe = p.id === persona.id;
              return (
                <tr key={p.id} className={isMe ? 'row-me' : undefined}>
                  <td className="col-persona">
                    <div className="persona-cell">
                      <div className="avatar-circle" style={{ width: 28, height: 28, fontSize: 10 }}>
                        {p.nombre.split(' ').map(w => w[0]).join('').slice(0, 2)}
                      </div>
                      <div>
                        <div style={{ fontSize: 12, fontWeight: isMe ? 700 : 500 }}>
                          {p.nombre.split(' ').slice(0, 2).join(' ')}
                        </div>
                        {isMe && <span className="yo-badge">YO</span>}
                      </div>
                    </div>
                  </td>
                  {dias.map((_, di) => {
                    const code = cellFor(pi, di);
                    return (
                      <td key={di}>
                        <span className={`malla-chip turno-${code}`}>{code}</span>
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div style={{ fontSize: 12, color: 'var(--clr-text-muted)', marginTop: 12 }}>
        Publicada el {malla.fechaPublicacion ?? '—'}. En periodos largos desliza horizontalmente la tabla del grupo.
      </div>
      <div className="screen-id">S30</div>
    </div>
  );
}

// ─── S31 Mi programación (vista personal) ─────────────────────────────────────
function S31MiProgramacion({ navigate }: Props) {
  const persona = PERSONAS[0];
  const [vista, setVista] = useState<VistaPeriodo>('semana');
  const [mallaTab, setMallaTab] = useState<'actual' | 'proxima'>('actual');
  const [showCatalogo, setShowCatalogo] = useState(true);

  const mallasPublicadas = [
    {
      id: 'actual' as const,
      titulo: 'CC Septiembre 2026',
      periodo: '1–30 sep 2026',
      publicada: '29 ago 2026',
      vigente: true,
      anchor: new Date(2026, 8, 1),
    },
    {
      id: 'proxima' as const,
      titulo: 'CC Octubre 2026',
      periodo: '1–31 oct 2026',
      publicada: '25 sep 2026',
      vigente: false,
      anchor: new Date(2026, 9, 1),
    },
  ];

  const activa = mallasPublicadas[mallaTab === 'actual' ? 0 : 1];
  const dias = useMemo(() => buildDays(vista, activa.anchor), [vista, activa.anchor]);
  const useCalendar = vista === 'quincena' || vista === 'mes';

  const turnosFrente = TURNOS.filter(t => t.frentes?.includes(persona.frenteId) || t.frenteId === persona.frenteId);

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1200 }}>
      <Breadcrumb items={[{ label: 'Mi programación' }, { label: 'Mis turnos' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Mi programación</div>
          <div className="page-subtitle">Tus turnos publicados — {persona.nombre}. HU68</div>
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <button className="btn-secondary" type="button" onClick={() => navigate('S30')}>← Grupo</button>
          <button className="btn-secondary" type="button" onClick={() => navigate('S32')}>Historial</button>
          <button className="btn-secondary" type="button" onClick={() => navigate('S43')}>Mis solicitudes</button>
          <button className="btn-primary" type="button" onClick={() => navigate('S39')}>Solicitar intercambio</button>
        </div>
      </div>

      <div className="card" style={{ padding: '12px 16px', marginBottom: 14, background: '#FFF8E1', border: '1px solid #FDE68A' }}>
        <strong>Próxima agenda disponible.</strong>{' '}
        Contact Center publicó <em>CC Octubre 2026</em>. Puedes consultarla sin perder el mes vigente.
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, alignItems: 'center', marginBottom: 14 }}>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          {mallasPublicadas.map(m => (
            <button
              key={m.id}
              type="button"
              className={mallaTab === m.id ? 'btn-primary' : 'btn-secondary'}
              style={{ height: 34, fontSize: 12 }}
              onClick={() => setMallaTab(m.id)}
            >
              {m.titulo} · {m.vigente ? 'vigente' : 'próxima'}
            </button>
          ))}
        </div>
        <div style={{ flex: 1 }} />
        <VistaToggle vista={vista} setVista={setVista} />
      </div>

      <div className="mi-prog-layout">
        <div className="card" style={{ padding: '20px 22px' }}>
          <div className="section-header">Mi perfil</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
            <div className="avatar-circle" style={{ width: 52, height: 52, fontSize: 18 }}>
              {persona.nombre.split(' ').map(w => w[0]).join('').slice(0, 2)}
            </div>
            <div>
              <div style={{ fontWeight: 600 }}>{persona.nombre}</div>
              <div style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>{persona.cargo}</div>
              <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>Doc. · {persona.cedula}</div>
            </div>
          </div>
          <div style={{ fontSize: 12, marginBottom: 8 }}>
            <div style={{ color: 'var(--clr-text-muted)' }}>Malla seleccionada</div>
            <div style={{ fontWeight: 600 }}>{activa.titulo}</div>
            <div style={{ color: 'var(--clr-text-muted)' }}>{activa.periodo} · Pub. {activa.publicada}</div>
          </div>
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 6 }}>
              <span style={{ color: 'var(--clr-text-muted)' }}>Horas este periodo</span>
              <span style={{ fontWeight: 700 }}>{mallaTab === 'actual' ? '72h / 184h' : '0h / 184h'}</span>
            </div>
            <div style={{ background: '#F3F4F6', borderRadius: 4, height: 8 }}>
              <div style={{ width: mallaTab === 'actual' ? '39%' : '0%', height: '100%', background: 'var(--clr-primary)', borderRadius: 4 }} />
            </div>
          </div>
        </div>

        <div className="card" style={{ padding: '16px 18px' }}>
          <div className="section-header" style={{ marginBottom: 10 }}>
            {useCalendar ? `Calendario — ${vista}` : `Mi grilla — semana`}
          </div>

          {useCalendar ? (
            <>
              <div className="helper-text" style={{ marginBottom: 10 }}>
                Vista calendario (no se estira en horizontal): cada día en su celda dentro del mes/quincena.
              </div>
              <CalendarioMiTurno dias={dias} />
            </>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table className="table-malla-readonly" style={{ minWidth: 520, width: '100%' }}>
                <thead>
                  <tr>
                    {dias.map((x, i) => (
                      <th key={i} className={x.dom ? 'day-dom' : undefined}>
                        <div className="day-name">{x.dow}</div>
                        <div className="day-num">{x.num}</div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr className="row-me">
                    {dias.map((x, i) => (
                      <td key={i}>
                        <span className={`malla-chip turno-${x.code}`}>{x.code}</span>
                        <div style={{ fontSize: 9, color: 'var(--clr-text-muted)', marginTop: 2 }}>{horaOf(x.code)}</div>
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          )}

          {vista === 'semana' && (
            <>
              <div className="section-header" style={{ marginTop: 18, marginBottom: 8 }}>Detalle de la semana</div>
              <div className="card" style={{ padding: 0, overflowX: 'auto', boxShadow: 'none', border: '1px solid var(--clr-border)' }}>
                <table className="table-grh" style={{ minWidth: 480, width: '100%' }}>
                  <thead>
                    <tr>
                      <th>Día</th>
                      <th>Turno</th>
                      <th>Horario</th>
                      <th>Modalidad</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dias.map(t => (
                      <tr key={t.label} style={{ background: t.code === 'DES' ? '#FAFAFA' : undefined }}>
                        <td style={{ fontWeight: 500, whiteSpace: 'nowrap' }}>{t.label}</td>
                        <td><span className={`chip turno-${t.code}`}>{t.code}</span></td>
                        <td style={{ whiteSpace: 'nowrap' }}>{horaOf(t.code)}</td>
                        <td style={{ fontSize: 12 }}>{modalityOf(t.code)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Catálogo de turnos del frente — solo lectura operador */}
      <div className="card" style={{ padding: '16px 18px', marginBottom: 12 }}>
        <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>Cómo están formados los turnos de mi frente</span>
          <button className="btn-secondary" type="button" style={{ height: 30, fontSize: 11 }} onClick={() => setShowCatalogo(s => !s)}>
            {showCatalogo ? 'Ocultar' : 'Mostrar'}
          </button>
        </div>
        {showCatalogo && (
          <>
            <div className="helper-text" style={{ marginBottom: 12 }}>
              Catálogo publicado de <strong>Contact Center</strong>: {turnosFrente.length} plantillas activas (hora, días y si cruza medianoche). Solo consulta — no se editan aquí.
            </div>
            <div className="turnos-catalogo-grid">
              {turnosFrente.map(t => (
                <div key={t.codigo} className="turno-catalogo-card">
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                    <span className={`chip ${t.colorClass || `turno-${t.codigo}`}`}>{t.codigo}</span>
                    <strong style={{ fontSize: 13 }}>{t.nombre}</strong>
                  </div>
                  <div style={{ fontSize: 12, color: 'var(--clr-text-body)' }}>
                    <div><span style={{ color: 'var(--clr-text-muted)' }}>Horario:</span> {t.horaInicio} – {t.horaFin}{t.nocturno ? ' (+1 día)' : ''}</div>
                    <div><span style={{ color: 'var(--clr-text-muted)' }}>Días:</span> {t.dias}</div>
                    <div><span style={{ color: 'var(--clr-text-muted)' }}>Horas netas:</span> {t.horasNetas}h</div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      <div className="screen-id">S31</div>
    </div>
  );
}

// ─── S32 Historial mis turnos ─────────────────────────────────────────────────
function S32HistorialMios({ navigate }: Props) {
  const persona = PERSONAS[0];
  return (
    <div style={{ padding: '24px 28px', maxWidth: 1000 }}>
      <Breadcrumb
        items={[
          { label: 'Mi programación' },
          { label: 'Mis turnos', screen: 'S31', onClick: () => navigate('S31') },
          { label: 'Historial' },
        ]}
        navigate={navigate}
      />
      <div className="page-header">
        <div>
          <div className="page-title">Historial de mis turnos</div>
          <div className="page-subtitle">{persona.nombre} — cambios que me afectaron. HU69</div>
        </div>
      </div>
      <div className="filter-bar" style={{ marginBottom: 16 }}>
        <label className="filter-label">Periodo</label>
        <input className="input-field" type="month" defaultValue="2026-09" style={{ width: 180 }} />
        <button className="btn-primary" type="button">Filtrar</button>
      </div>
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ minWidth: 640 }}>
          <thead>
            <tr>
              <th>Fecha registro</th>
              <th>Día afectado</th>
              <th>Antes</th>
              <th>Después</th>
              <th>Motivo</th>
            </tr>
          </thead>
          <tbody>
            {[
              { ts: '2026-09-05', dia: 'Lun 01-Sep', antes: 'T1', despues: 'INC', motivo: 'Incapacidad médica registrada por su coordinador' },
              { ts: '2026-09-08', dia: 'Vie 05-Sep', antes: 'T5', despues: 'VAC', motivo: 'Vacaciones aprobadas por RH' },
              { ts: '2026-09-12', dia: 'Mié 10-Sep', antes: 'T1', despues: 'DES', motivo: 'Ajuste de cobertura — asignación masiva' },
            ].map((r, i) => (
              <tr key={i}>
                <td style={{ whiteSpace: 'nowrap' }}>{r.ts}</td>
                <td style={{ whiteSpace: 'nowrap' }}>{r.dia}</td>
                <td><span className={`chip turno-${r.antes}`}>{r.antes}</span></td>
                <td><span className={`chip turno-${r.despues}`}>{r.despues}</span></td>
                <td style={{ fontSize: 12 }}>{r.motivo}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="helper-text" style={{ marginTop: 10 }}>
        Vista de solo lectura. Las notificaciones son informativas — no se requiere aceptación.
      </div>
      <div className="screen-id">S32</div>
    </div>
  );
}

export default function SD(props: Props) {
  const { screen } = props;
  if (screen === 'S30') return <S30MallaGrupo {...props} />;
  if (screen === 'S31') return <S31MiProgramacion {...props} />;
  if (screen === 'S32') return <S32HistorialMios {...props} />;
  return <S30MallaGrupo {...props} />;
}
