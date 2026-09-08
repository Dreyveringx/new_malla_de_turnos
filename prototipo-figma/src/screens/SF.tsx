import { useState } from 'react';
import { Breadcrumb, Modal, Field, Chip, EstadoChip, DisabledBtn } from '../Shell';
import {
  FRENTES, PERSONAS, SOLICITUDES_INTERCAMBIO, REGLAS_MOTOR,
  type SolicitudIntercambio, type Rol, puedeEditar, severidadClass,
} from '../data';

interface Props {
  screen: string;
  navigate: (s: string, p?: any) => void;
  params: any;
  onToast: (msg: string, desc: string, type: 'success' | 'error' | 'warning') => void;
  role: Rol;
}

// ─── Helper: banner si intercambio OFF para frente ────────────────────────────
function IntercambioOffBanner({ frenteId, navigate }: { frenteId: string; navigate: (s: string, p?: any) => void }) {
  const frente = FRENTES.find(f => f.id === frenteId);
  if (!frente || frente.intercambioActivo) return null;
  return (
    <div style={{ padding: '16px 20px', background: '#FFF8E1', borderRadius: 8, border: '1px solid #FDE68A', marginBottom: 20 }}>
      <div style={{ fontWeight: 600, marginBottom: 4 }}>🔒 Intercambio deshabilitado — {frente.nombre}</div>
      <div style={{ fontSize: 12 }}>
        El módulo de intercambio de turnos está <strong>desactivado (OFF)</strong> para este frente por defecto (EP-09).
        Para habilitarlo, ve a <span style={{ textDecoration: 'underline', cursor: 'pointer', color: 'var(--clr-primary)' }} onClick={() => navigate('S02', { frenteId })}>S02 Configuración del frente</span> y activa el switch.
      </div>
    </div>
  );
}

// ─── S38 Configuración intercambio por frente ────────────────────────────────
function S38ConfigIntercambio({ navigate, onToast, role }: Props) {
  const [frentes, setFrentes] = useState(FRENTES);
  const canEdit = puedeEditar(role);

  function toggle(id: string) {
    setFrentes(fs => fs.map(f => f.id === id ? { ...f, intercambioActivo: !f.intercambioActivo } : f));
    const f = frentes.find(x => x.id === id);
    onToast('Intercambio actualizado', `${f?.nombre} → ${f?.intercambioActivo ? 'OFF' : 'ON'}`, 'success');
  }

  return (
    <div style={{ padding: '24px 28px', maxWidth: 860 }}>
      <Breadcrumb items={[{ label: 'F. Intercambio' }, { label: 'S38 Config. intercambio' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Configuración de intercambio por frente <span className="new-badge" style={{ marginLeft: 8 }}>EP-09</span></div>
          <div className="page-subtitle">Habilita o deshabilita el flujo de intercambio para cada frente. Por defecto: OFF. HU69</div>
        </div>
      </div>

      <div className="helper-text" style={{ marginBottom: 20 }}>
        El intercambio de turnos es una funcionalidad <strong>opcional por frente</strong>. Cuando está OFF, las pantallas S39–S42 muestran un aviso y no permiten solicitar. El coordinador de cada frente debe habilitarlo explícitamente.
      </div>

      <div className="card" style={{ padding: 0, overflowX: 'auto', marginBottom: 20 }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead>
            <tr><th>Frente</th><th>Coordinador</th><th>Intercambio</th><th>Máx solicitudes/mes</th><th>Requiere aprobación</th><th>Activo</th></tr>
          </thead>
          <tbody>
            {frentes.map(f => (
              <tr key={f.id}>
                <td><span style={{ fontWeight: 600 }}>{f.nombre}</span></td>
                <td style={{ fontSize: 12 }}>{f.responsablePublica}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <label className="toggle-switch">
                      <input type="checkbox" checked={f.intercambioActivo} onChange={() => canEdit && toggle(f.id)} disabled={!canEdit} />
                      <span className="toggle-track"></span>
                    </label>
                    <span style={{ fontSize: 12, color: f.intercambioActivo ? '#15803D' : '#9CA3AF', fontWeight: 500 }}>
                      {f.intercambioActivo ? 'ON' : 'OFF (default)'}
                    </span>
                  </div>
                </td>
                <td>
                  <input className="input-field" type="number" defaultValue={f.intercambioActivo ? 3 : 0} style={{ width: 70 }} disabled={!canEdit || !f.intercambioActivo} />
                </td>
                <td>
                  <input type="checkbox" defaultChecked disabled={!canEdit || !f.intercambioActivo} />
                </td>
                <td><span style={{ color: f.activo ? '#15803D' : '#9CA3AF' }}>●</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="helper-text">
        Cuando el intercambio está ON, el empleado puede solicitar desde S39 (vista Mi programación). El motor de reglas (S40) valida automáticamente antes de enviar al coordinador.
      </div>

      <div style={{ marginTop: 16 }}>
        <button className="btn-secondary" onClick={() => navigate('S39')}>→ Solicitar intercambio (S39)</button>
      </div>
      <div className="screen-id">S38</div>
    </div>
  );
}

// ─── S39 Solicitar intercambio (vista empleado) ───────────────────────────────
function S39Solicitar({ navigate, params, onToast, role }: Props) {
  const [frenteId, setFrenteId] = useState('CC');
  const [diaOrigen, setDiaOrigen] = useState('2026-09-10');
  const [diaDestino, setDiaDestino] = useState('2026-09-17');
  const [contraparteId, setContraparteId] = useState('P002');
  const [motivo, setMotivo] = useState('');
  /** Demo diseño: forzar ver el formulario aunque el frente esté OFF */
  const [previewOn, setPreviewOn] = useState(true);

  const frente = FRENTES.find(f => f.id === frenteId) ?? FRENTES[0];
  const personas = PERSONAS.filter(p => p.frenteId === frenteId);
  const habilitado = frente.intercambioActivo || previewOn;

  return (
    <div style={{ padding: '24px 28px', maxWidth: 860 }}>
      <Breadcrumb items={[{ label: 'Mi programación' }, { label: 'Solicitar intercambio' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Solicitar intercambio de turno <span className="new-badge" style={{ marginLeft: 8 }}>EP-09</span></div>
          <div className="page-subtitle">El empleado propone el intercambio — no lo confirma. HU70</div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn-secondary" type="button" onClick={() => navigate('S43')}>Mis solicitudes →</button>
          <button className="btn-secondary" type="button" onClick={() => navigate('S38')}>Config. por frente →</button>
        </div>
      </div>

      {!frente.intercambioActivo && (
        <div className="card" style={{ padding: '14px 16px', marginBottom: 14, background: '#FFF8E1', border: '1px solid #FDE68A' }}>
          <div style={{ fontWeight: 600, marginBottom: 4 }}>Este frente tiene intercambio OFF (default EP-09)</div>
          <div style={{ fontSize: 13, marginBottom: 10 }}>
            En producción el formulario estaría bloqueado. Aquí mostramos la <strong>vista de diseño habilitada</strong> para que veas qué campos llenar cuando el coordinador active el frente en S38.
          </div>
          <label className="checkbox-label">
            <input type="checkbox" checked={previewOn} onChange={e => setPreviewOn(e.target.checked)} />
            Mostrar formulario como si estuviera ON (demo diseño)
          </label>
        </div>
      )}

      {habilitado ? (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
            <div className="card" style={{ padding: '20px 22px' }}>
              <div className="section-header">1. Mi turno a ceder</div>
              <Field label="Solicitante">
                <div style={{ padding: '8px 12px', background: 'var(--clr-filter-bg)', borderRadius: 6, border: '1px solid var(--clr-border)', fontSize: 13 }}>
                  {PERSONAS[0].nombre} — {PERSONAS[0].cedula}
                </div>
              </Field>
              <Field label="Frente">
                <select className="input-field" value={frenteId} onChange={e => setFrenteId(e.target.value)}>
                  {FRENTES.filter(f => f.activo).map(f => (
                    <option key={f.id} value={f.id}>
                      {f.nombre} {f.intercambioActivo ? '(ON)' : '(OFF)'}
                    </option>
                  ))}
                </select>
              </Field>
              <Field label="Día que quiero cambiar" required>
                <input className="input-field" type="date" value={diaOrigen} onChange={e => setDiaOrigen(e.target.value)} />
              </Field>
              <Field label="Mi turno ese día (solo lectura)">
                <div style={{ padding: '8px 12px', background: '#EFF4FB', borderRadius: 6, border: '1px solid #BFD0EC', fontSize: 13, fontWeight: 600 }}>
                  <span className="chip turno-T1">T1</span> 06:00–14:00 · Presencial · Elemento
                </div>
              </Field>
            </div>

            <div className="card" style={{ padding: '20px 22px' }}>
              <div className="section-header">2. Turno que propongo recibir</div>
              <Field label="Compañero/a" required helper="Solo personas de tu frente / grupo de malla">
                <select className="input-field" value={contraparteId} onChange={e => setContraparteId(e.target.value)}>
                  {personas.filter(p => p.id !== PERSONAS[0].id).map(p => (
                    <option key={p.id} value={p.id}>{p.nombre}</option>
                  ))}
                </select>
              </Field>
              <Field label="Día del compañero" required>
                <input className="input-field" type="date" value={diaDestino} onChange={e => setDiaDestino(e.target.value)} />
              </Field>
              <Field label="Turno del compañero (solo lectura)">
                <div style={{ padding: '8px 12px', background: '#F5F0FF', borderRadius: 6, border: '1px solid #D8B4FE', fontSize: 13, fontWeight: 600 }}>
                  <span className="chip turno-T5">T5</span> 14:00–22:00 · Virtual
                </div>
              </Field>
              <Field label="Motivo de la solicitud" required>
                <textarea
                  className="input-field"
                  rows={3}
                  value={motivo}
                  onChange={e => setMotivo(e.target.value)}
                  placeholder="Ej: cita médica no posponible / compromiso personal"
                  style={{ resize: 'vertical' }}
                />
              </Field>
            </div>
          </div>

          <div className="helper-text" style={{ marginTop: 12 }}>
            Completa los datos y usa <strong>Enviar solicitud</strong>. El sistema validará reglas y la dejará pendiente de aprobación del coordinador.
          </div>

          <div className="solicitud-actions-bar">
            <button className="btn-secondary" type="button" onClick={() => navigate('S31')}>Cancelar</button>
            <button
              className="btn-secondary"
              type="button"
              onClick={() => {
                if (!motivo.trim()) { onToast('Indica el motivo antes de validar', '', 'warning'); return; }
                navigate('S40', { solicitudId: 'SIC-001' });
              }}
            >
              Validar con motor
            </button>
            <button
              className="btn-primary"
              type="button"
              onClick={() => {
                if (!motivo.trim()) { onToast('Indica el motivo para enviar', '', 'warning'); return; }
                if (!frente.intercambioActivo && previewOn) {
                  onToast('Solicitud enviada (demo)', 'Pendiente de aprobación del coordinador', 'success');
                } else {
                  onToast('Solicitud enviada', 'Pendiente de aprobación', 'success');
                }
                navigate('S43', { solicitudId: 'SIC-001', recienEnviada: true });
              }}
            >
              Enviar solicitud →
            </button>
          </div>
        </>
      ) : (
        <div style={{ textAlign: 'center', padding: '48px 0', color: 'var(--clr-text-muted)' }}>
          <div style={{ fontSize: 48 }}>🔒</div>
          <div style={{ fontSize: 15, fontWeight: 500, marginTop: 12 }}>Intercambio no disponible para este frente</div>
          <div style={{ fontSize: 12, marginTop: 6, marginBottom: 16 }}>Actívalo en S38 o marca la casilla de vista previa de diseño.</div>
          <button className="btn-secondary" type="button" onClick={() => setPreviewOn(true)}>Ver formulario (diseño ON)</button>
        </div>
      )}
      <div className="screen-id">S39</div>
    </div>
  );
}

// ─── S40 Validación motor de reglas ───────────────────────────────────────────
function S40Validacion({ navigate, params, onToast, role }: Props) {
  const [validando, setValidando] = useState(false);
  const [resultado, setResultado] = useState<'ok' | 'advertencia' | 'bloqueo' | null>(null);

  function validar() {
    setValidando(true);
    setTimeout(() => { setValidando(false); setResultado('advertencia'); }, 1200);
  }

  return (
    <div style={{ padding: '24px 28px', maxWidth: 760 }}>
      <Breadcrumb items={[{ label: 'F. Intercambio' }, { label: 'S39', onClick: () => navigate('S39') }, { label: 'S40 Validación motor' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Validación con motor de reglas <span className="new-badge" style={{ marginLeft: 8 }}>EP-09</span></div>
          <div className="page-subtitle">El motor verifica el intercambio antes de enviarlo al coordinador. HU71</div>
        </div>
      </div>

      <div className="card" style={{ padding: '20px 22px', marginBottom: 20 }}>
        <div className="section-header">Resumen del intercambio a validar</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          {[
            { label: 'Solicitante', value: 'Pérez González, J. — 1090456789' },
            { label: 'Contraparte', value: 'Ramírez Castro, A. — 1090567890' },
            { label: 'Día A (solicitante)', value: 'Lun 10-Mar — T1 (06:00–14:00)' },
            { label: 'Día B (contraparte)', value: 'Lun 17-Mar — T5 (14:00–22:00)' },
          ].map(i => (
            <div key={i.label} style={{ padding: '8px 12px', background: 'var(--clr-filter-bg)', borderRadius: 6 }}>
              <div style={{ fontSize: 10, color: 'var(--clr-text-muted)', marginBottom: 2 }}>{i.label}</div>
              <div style={{ fontSize: 12, fontWeight: 500 }}>{i.value}</div>
            </div>
          ))}
        </div>
      </div>

      {!resultado && (
        <div style={{ textAlign: 'center', padding: '24px 0' }}>
          {validando ? (
            <div>
              <div style={{ fontSize: 32, marginBottom: 10 }}>⚙️</div>
              <div style={{ fontSize: 14 }}>Ejecutando motor de reglas…</div>
            </div>
          ) : (
            <button className="btn-primary" style={{ padding: '10px 28px' }} onClick={validar}>
              🔍 Ejecutar validación
            </button>
          )}
        </div>
      )}

      {resultado && (
        <div className="card" style={{ padding: '20px 22px', marginBottom: 20 }}>
          <div className="section-header">Resultado de la validación</div>
          <div style={{ marginBottom: 16 }}>
            {[
              { regla: 'NO_SOLAPE', ok: true, desc: 'Sin solapamiento con otros turnos' },
              { regla: 'MAX_HORAS_PERIODO', ok: true, desc: 'Horas resultantes dentro del límite (46h)' },
              { regla: 'MIN_COBERTURA_FRANJA', ok: false, desc: 'Cobertura 06:00–14:00 baja a 2/3 el Lun 10-Mar', sev: 'advertencia' },
              { regla: 'MAX_DIAS_CONSECUTIVOS', ok: true, desc: 'Días consecutivos dentro del máximo (5)' },
            ].map(r => (
              <div key={r.regla} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 12px', borderRadius: 6, border: `1px solid ${r.ok ? '#D1FAE5' : '#FDE68A'}`, background: r.ok ? '#F0FDF4' : '#FFFBEB', marginBottom: 6 }}>
                <span>{r.ok ? '✅' : '⚠️'}</span>
                <div style={{ flex: 1 }}>
                  <code style={{ fontSize: 11 }}>{r.regla}</code>
                  <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{r.desc}</div>
                </div>
                {!r.ok && r.sev && (
                  <span className={`chip severidad-${r.sev}`}>{r.sev}</span>
                )}
              </div>
            ))}
          </div>

          <div style={{ padding: '12px 16px', background: '#FFF8E1', borderRadius: 8, border: '1px solid #FDE68A', marginBottom: 16 }}>
            <div style={{ fontWeight: 600, marginBottom: 4 }}>⚠️ Advertencia — no bloquea</div>
            <div style={{ fontSize: 12 }}>El intercambio puede proceder, pero el coordinador verá la advertencia de cobertura antes de aprobar.</div>
          </div>

          <div style={{ display: 'flex', gap: 8 }}>
            <button className="btn-secondary" onClick={() => navigate('S39')}>← Editar solicitud</button>
            <button className="btn-primary" onClick={() => { onToast('Solicitud enviada', 'Quedó pendiente de aprobación', 'success'); navigate('S43', { solicitudId: params?.solicitudId ?? 'SIC-001' }); }}>Enviar al coordinador →</button>
          </div>
        </div>
      )}
      <div className="screen-id">S40</div>
    </div>
  );
}

// ─── S41 Aprobar / Rechazar intercambio ───────────────────────────────────────
function S41Aprobar({ navigate, params, onToast, role }: Props) {
  const [solicitudes, setSolicitudes] = useState<SolicitudIntercambio[]>(SOLICITUDES_INTERCAMBIO);
  const [motivoRechazo, setMotivoRechazo] = useState('');
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);

  function aprobar(id: string) {
    setSolicitudes(ss => ss.map(s => s.id === id ? { ...s, estado: 'aprobada' } : s));
    onToast('Intercambio aprobado', `Solicitud ${id}`, 'success');
    navigate('S42', { solicitudId: id });
  }

  function rechazar(id: string) {
    if (!motivoRechazo.trim()) { onToast('Indica el motivo', '', 'warning'); return; }
    setSolicitudes(ss => ss.map(s => s.id === id ? { ...s, estado: 'rechazada', motivo: motivoRechazo } : s));
    onToast('Intercambio rechazado', motivoRechazo, 'warning');
    setShowModal(false);
    setMotivoRechazo('');
    setSelectedId(null);
  }

  const pendientes = solicitudes.filter(s => s.estado === 'pendiente');
  const resueltas = solicitudes.filter(s => s.estado !== 'pendiente');

  return (
    <div style={{ padding: '24px 28px', maxWidth: 900 }}>
      <Breadcrumb items={[{ label: 'F. Intercambio' }, { label: 'S41 Aprobar/Rechazar' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Gestión de solicitudes de intercambio <span className="new-badge" style={{ marginLeft: 8 }}>EP-09</span></div>
          <div className="page-subtitle">El coordinador aprueba o rechaza — con advertencias del motor. HU72</div>
        </div>
      </div>

      {pendientes.length === 0 && (
        <div style={{ textAlign: 'center', padding: '32px 0', color: 'var(--clr-text-muted)' }}>
          ✅ Sin solicitudes pendientes de revisión.
          <div style={{ marginTop: 12 }}>
            <button className="btn-secondary" onClick={() => navigate('S39')}>Nueva solicitud demo</button>
          </div>
        </div>
      )}

      {pendientes.map(s => (
        <div key={s.id} className="card" style={{ padding: '18px 20px', marginBottom: 12 }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: 16 }}>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Solicitud {s.id}</div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, fontSize: 12 }}>
                <div><span style={{ color: 'var(--clr-text-muted)' }}>Solicitante:</span> {s.solicitanteNombre}</div>
                <div><span style={{ color: 'var(--clr-text-muted)' }}>Contraparte:</span> {s.contraparteNombre}</div>
                <div><span style={{ color: 'var(--clr-text-muted)' }}>Día A:</span> {s.diaOrigen} — <span className={`chip turno-${s.turnoOrigen}`} style={{ display: 'inline-flex' }}>{s.turnoOrigen}</span></div>
                <div><span style={{ color: 'var(--clr-text-muted)' }}>Día B:</span> {s.diaDestino} — <span className={`chip turno-${s.turnoDestino}`} style={{ display: 'inline-flex' }}>{s.turnoDestino}</span></div>
              </div>
              {s.advertencias && s.advertencias.length > 0 && (
                <div style={{ marginTop: 10, padding: '8px 12px', background: '#FFFBEB', borderRadius: 6, border: '1px solid #FDE68A' }}>
                  {s.advertencias.map((a, i) => <div key={i} style={{ fontSize: 11 }}>⚠️ {a}</div>)}
                </div>
              )}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6, flexShrink: 0 }}>
              <button className="btn-primary" style={{ minWidth: 100 }} onClick={() => aprobar(s.id)}>✓ Aprobar</button>
              <button className="btn-secondary" style={{ minWidth: 100, borderColor: '#EF4444', color: '#DC2626' }} onClick={() => { setSelectedId(s.id); setShowModal(true); }}>✗ Rechazar</button>
            </div>
          </div>
        </div>
      ))}

      {resueltas.length > 0 && (
        <div>
          <div className="section-header" style={{ marginTop: 20 }}>Resueltas</div>
          {resueltas.map(s => (
            <div key={s.id} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '8px 14px', borderRadius: 6, border: '1px solid var(--clr-border)', marginBottom: 6 }}>
              <span className={s.estado === 'aprobada' ? 'chip estado-publicada' : 'chip estado-rechazada'}>{s.estado}</span>
              <span style={{ fontSize: 12 }}>{s.solicitanteNombre} ↔ {s.contraparteNombre}</span>
              <span style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{s.diaOrigen} / {s.diaDestino}</span>
              {s.estado === 'aprobada' && <button className="btn-icon" onClick={() => navigate('S42', { solicitudId: s.id })}>📋</button>}
            </div>
          ))}
        </div>
      )}

      {showModal && selectedId && (
        <Modal title="Rechazar solicitud de intercambio" onClose={() => setShowModal(false)}>
          <Field label="Motivo del rechazo" required>
            <textarea className="input-field" rows={3} value={motivoRechazo} onChange={e => setMotivoRechazo(e.target.value)} placeholder="Ej: Cobertura insuficiente en el frente ese día." style={{ resize: 'vertical' }} />
          </Field>
          <div className="helper-text">Ambas personas recibirán notificación con el motivo.</div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" onClick={() => setShowModal(false)}>Cancelar</button>
            <button className="btn-primary" style={{ background: '#DC2626' }} onClick={() => rechazar(selectedId)}>Confirmar rechazo</button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S41</div>
    </div>
  );
}

// ─── S42 Aplicar + auditoría + notificar ──────────────────────────────────────
function S42Aplicar({ navigate, params, onToast, role }: Props) {
  const solicitud = SOLICITUDES_INTERCAMBIO.find(s => s.id === params?.solicitudId) ?? SOLICITUDES_INTERCAMBIO[0];

  return (
    <div style={{ padding: '24px 28px', maxWidth: 800 }}>
      <Breadcrumb items={[{ label: 'F. Intercambio' }, { label: 'S41', onClick: () => navigate('S41') }, { label: 'S42 Aplicar + auditoría' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Aplicar intercambio + auditoría <span className="new-badge" style={{ marginLeft: 8 }}>EP-09</span></div>
          <div className="page-subtitle">El intercambio aprobado se aplica en la malla y queda en auditoría. HU73</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 20 }}>
        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Cambios aplicados en la malla</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            <div style={{ padding: '10px 14px', background: '#F0FDF4', borderRadius: 8, border: '1px solid #BBF7D0' }}>
              <div style={{ fontSize: 11, color: 'var(--clr-text-muted)', marginBottom: 4 }}>{solicitud.solicitanteNombre} — {solicitud.diaOrigen}</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span className={`chip turno-${solicitud.turnoOrigen}`}>{solicitud.turnoOrigen}</span>
                <span>→</span>
                <span className={`chip turno-${solicitud.turnoDestino}`}>{solicitud.turnoDestino}</span>
              </div>
            </div>
            <div style={{ padding: '10px 14px', background: '#F0FDF4', borderRadius: 8, border: '1px solid #BBF7D0' }}>
              <div style={{ fontSize: 11, color: 'var(--clr-text-muted)', marginBottom: 4 }}>{solicitud.contraparteNombre} — {solicitud.diaDestino}</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span className={`chip turno-${solicitud.turnoDestino}`}>{solicitud.turnoDestino}</span>
                <span>→</span>
                <span className={`chip turno-${solicitud.turnoOrigen}`}>{solicitud.turnoOrigen}</span>
              </div>
            </div>
          </div>
          <div className="helper-text" style={{ marginTop: 10 }}>Los cambios quedan como puntos de cambio en el historial de cada celda (S26).</div>
        </div>

        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Registro de auditoría</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {[
              { ts: '2025-03-08 09:12', evento: 'Solicitud creada', user: 'jlopez@dc.co' },
              { ts: '2025-03-08 09:14', evento: 'Motor validó — advertencia cobertura', user: 'sistema' },
              { ts: '2025-03-08 10:30', evento: 'Aprobada por coordinador', user: 'coord.cc@dc.co' },
              { ts: '2025-03-08 10:31', evento: 'Cambios aplicados en malla', user: 'sistema' },
              { ts: '2025-03-08 10:31', evento: 'Notificación enviada (x2 personas)', user: 'sistema' },
            ].map((e, i) => (
              <div key={i} style={{ display: 'flex', gap: 8, fontSize: 11, borderBottom: '1px solid var(--clr-border)', paddingBottom: 6 }}>
                <span style={{ fontFamily: 'monospace', color: 'var(--clr-text-muted)', flexShrink: 0 }}>{e.ts}</span>
                <span style={{ flex: 1 }}>{e.evento}</span>
                <span style={{ color: 'var(--clr-text-muted)', flexShrink: 0 }}>{e.user}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card" style={{ padding: '18px 20px' }}>
        <div className="section-header">Notificaciones enviadas</div>
        {[solicitud.solicitanteNombre, solicitud.contraparteNombre].map(n => (
          <div key={n} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 12px', borderRadius: 6, background: '#F0FDF4', border: '1px solid #BBF7D0', marginBottom: 6 }}>
            <span>📧</span>
            <span style={{ fontSize: 12 }}>{n} — notificación informativa enviada (sin requerimiento de confirmación)</span>
            <span style={{ fontSize: 11, color: '#15803D', marginLeft: 'auto' }}>Entregada ✓</span>
          </div>
        ))}
        <div className="helper-text" style={{ marginTop: 8 }}>Las notificaciones son <strong>informativas</strong> — el empleado no confirma ni acepta turnos.</div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
        <button className="btn-secondary" onClick={() => navigate('S41')}>← Volver a solicitudes</button>
        <button className="btn-secondary" onClick={() => navigate('S26', { personaId: 'P001' })}>Ver historial celda (S26)</button>
        <button className="btn-primary" onClick={() => navigate('S38')}>Ir a config. intercambio</button>
      </div>
      <div className="screen-id">S42</div>
    </div>
  );
}

function estadoSolicitudChip(estado: SolicitudIntercambio['estado']) {
  const map: Record<SolicitudIntercambio['estado'], { label: string; cls: string }> = {
    pendiente: { label: 'Pendiente de aprobación', cls: 'estado-revision' },
    aprobada: { label: 'Aprobada (por aplicar)', cls: 'estado-borrador' },
    rechazada: { label: 'Rechazada', cls: 'estado-rechazada' },
    aplicada: { label: 'Aplicada en malla', cls: 'estado-publicada' },
  };
  const m = map[estado];
  return <span className={`chip ${m.cls}`}>{m.label}</span>;
}

function timelineStep(done: boolean, current: boolean, label: string) {
  return (
    <div style={{ flex: 1, textAlign: 'center', minWidth: 90 }}>
      <div style={{
        width: 12, height: 12, borderRadius: '50%', margin: '0 auto 6px',
        background: done || current ? 'var(--clr-primary)' : '#D1D5DB',
        boxShadow: current ? '0 0 0 4px rgba(74,98,138,0.25)' : undefined,
      }} />
      <div style={{ fontSize: 10, fontWeight: current ? 700 : 500, color: done || current ? 'var(--clr-text-strong)' : 'var(--clr-text-muted)' }}>{label}</div>
    </div>
  );
}

// ─── S43 Mis solicitudes (seguimiento empleado) ───────────────────────────────
function S43MisSolicitudes({ navigate, params, role }: Props) {
  const yo = PERSONAS[0];
  const mias = SOLICITUDES_INTERCAMBIO.filter(s => s.solicitanteId === yo.id);
  const destacada = mias.find(s => s.id === params?.solicitudId) ?? mias.find(s => s.estado === 'pendiente') ?? mias[0];

  return (
    <div style={{ padding: '24px 28px', maxWidth: 980 }}>
      <Breadcrumb items={[{ label: 'Mi programación' }, { label: 'Mis solicitudes de intercambio' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Mis solicitudes de intercambio <span className="new-badge" style={{ marginLeft: 8 }}>EP-09</span></div>
          <div className="page-subtitle">Seguimiento del estado — no editas la malla desde aquí. HU78 / seguimiento</div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn-secondary" type="button" onClick={() => navigate('S31')}>← Mi programación</button>
          <button className="btn-primary" type="button" onClick={() => navigate('S39')}>+ Nueva solicitud</button>
        </div>
      </div>

      <div className="helper-text" style={{ marginBottom: 14 }}>
        No es la grilla operativa de Construcción: es tu <strong>bandeja de solicitudes</strong>. Aquí ves si está pendiente, aprobada, rechazada o ya aplicada en la malla.
      </div>

      {destacada && (
        <div className="card" style={{ padding: '18px 20px', marginBottom: 16, borderLeft: '4px solid var(--clr-primary)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, marginBottom: 14 }}>
            <div>
              <div style={{ fontWeight: 600 }}>Solicitud {destacada.id}</div>
              <div style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>Enviada {destacada.fechaSolicitud}</div>
            </div>
            {estadoSolicitudChip(destacada.estado)}
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 4, marginBottom: 16, padding: '8px 0' }}>
            {timelineStep(true, false, 'Enviada')}
            <div style={{ flex: 0.3, height: 2, background: '#D1D5DB', marginBottom: 18 }} />
            {timelineStep(destacada.estado !== 'pendiente', destacada.estado === 'pendiente', 'En revisión')}
            <div style={{ flex: 0.3, height: 2, background: '#D1D5DB', marginBottom: 18 }} />
            {timelineStep(['aprobada', 'rechazada', 'aplicada'].includes(destacada.estado), destacada.estado === 'aprobada' || destacada.estado === 'rechazada', destacada.estado === 'rechazada' ? 'Rechazada' : 'Decisión')}
            <div style={{ flex: 0.3, height: 2, background: '#D1D5DB', marginBottom: 18 }} />
            {timelineStep(destacada.estado === 'aplicada', destacada.estado === 'aplicada', 'En malla')}
          </div>

          <div className="section-header" style={{ marginBottom: 8 }}>Resumen del intercambio propuesto</div>
          <div style={{ overflowX: 'auto' }}>
            <table className="table-malla-readonly" style={{ minWidth: 420 }}>
              <thead>
                <tr>
                  <th className="col-persona">Persona</th>
                  <th>
                    <div className="day-name">Mi día</div>
                    <div className="day-num">{destacada.diaOrigen ?? destacada.fechaOrigen}</div>
                  </th>
                  <th>
                    <div className="day-name">Día compañero</div>
                    <div className="day-num">{destacada.diaDestino ?? destacada.fechaDestino}</div>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr className="row-me">
                  <td className="col-persona"><strong>Yo</strong> · {destacada.solicitanteNombre}</td>
                  <td>
                    <div style={{ fontSize: 10, color: 'var(--clr-text-muted)' }}>Cedo</div>
                    <span className={`malla-chip turno-${destacada.turnoOrigen}`}>{destacada.turnoOrigen}</span>
                  </td>
                  <td>
                    <div style={{ fontSize: 10, color: 'var(--clr-text-muted)' }}>Recibo</div>
                    <span className={`malla-chip turno-${destacada.turnoDestino}`}>{destacada.turnoDestino}</span>
                  </td>
                </tr>
                <tr>
                  <td className="col-persona">{destacada.contraparteNombre}</td>
                  <td>
                    <div style={{ fontSize: 10, color: 'var(--clr-text-muted)' }}>Recibe</div>
                    <span className={`malla-chip turno-${destacada.turnoOrigen}`}>{destacada.turnoOrigen}</span>
                  </td>
                  <td>
                    <div style={{ fontSize: 10, color: 'var(--clr-text-muted)' }}>Cede</div>
                    <span className={`malla-chip turno-${destacada.turnoDestino}`}>{destacada.turnoDestino}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          {destacada.motivo && (
            <div style={{ marginTop: 12, fontSize: 12 }}><strong>Motivo:</strong> {destacada.motivo}</div>
          )}
          {destacada.estado === 'rechazada' && destacada.motivoRechazo && (
            <div style={{ marginTop: 10, padding: '10px 12px', background: '#FFEBEE', borderRadius: 6, border: '1px solid #FFCDD2', fontSize: 12 }}>
              <strong>Motivo del rechazo:</strong> {destacada.motivoRechazo}
            </div>
          )}
          {destacada.estado === 'pendiente' && destacada.advertencias && destacada.advertencias.length > 0 && (
            <div style={{ marginTop: 10, padding: '10px 12px', background: '#FFFBEB', borderRadius: 6, border: '1px solid #FDE68A', fontSize: 12 }}>
              {destacada.advertencias.map((a, i) => <div key={i}>⚠️ {a} (visible también para el aprobador)</div>)}
            </div>
          )}
          {destacada.estado === 'aplicada' && (
            <div style={{ marginTop: 12 }}>
              <button className="btn-secondary" type="button" onClick={() => navigate('S31')}>Ver mi programación actualizada →</button>
            </div>
          )}
        </div>
      )}

      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ minWidth: 720, width: '100%' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Fecha solicitud</th>
              <th>Intercambio</th>
              <th>Contraparte</th>
              <th>Estado</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {mias.map(s => (
              <tr key={s.id} style={{ background: s.id === destacada?.id ? '#F0F7FA' : undefined }}>
                <td><code>{s.id}</code></td>
                <td style={{ whiteSpace: 'nowrap', fontSize: 12 }}>{s.fechaSolicitud}</td>
                <td style={{ fontSize: 12 }}>
                  <span className={`chip turno-${s.turnoOrigen}`}>{s.turnoOrigen}</span>
                  {' '}{s.diaOrigen} →{' '}
                  <span className={`chip turno-${s.turnoDestino}`}>{s.turnoDestino}</span>
                  {' '}{s.diaDestino}
                </td>
                <td style={{ fontSize: 12 }}>{s.contraparteNombre}</td>
                <td>{estadoSolicitudChip(s.estado)}</td>
                <td>
                  <button className="btn-icon" type="button" title="Ver detalle" onClick={() => navigate('S43', { solicitudId: s.id })}>👁</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {role === 'coordinadora_cc' || role === 'coordinador' ? (
        <div className="helper-text" style={{ marginTop: 12 }}>
          Vista empleado. Como coordinador también puedes ir a la <button className="btn-secondary" style={{ height: 28, fontSize: 11, marginLeft: 6 }} type="button" onClick={() => navigate('S41')}>bandeja de aprobación (S41)</button>
        </div>
      ) : null}

      <div className="screen-id">S43</div>
    </div>
  );
}

// ─── Router ───────────────────────────────────────────────────────────────────
export default function SF(props: Props) {
  const { screen } = props;
  if (screen === 'S38') return <S38ConfigIntercambio {...props} />;
  if (screen === 'S39') return <S39Solicitar {...props} />;
  if (screen === 'S40') return <S40Validacion {...props} />;
  if (screen === 'S41') return <S41Aprobar {...props} />;
  if (screen === 'S42') return <S42Aplicar {...props} />;
  if (screen === 'S43') return <S43MisSolicitudes {...props} />;
  return <S38ConfigIntercambio {...props} />;
}
