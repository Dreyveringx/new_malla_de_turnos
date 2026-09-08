import { useState } from 'react';
import { Breadcrumb, Modal, Field, Chip, EstadoChip, EmptyState, DisabledBtn } from '../Shell';
import {
  FRENTES, REGLAS_MOTOR, MODALIDADES, SITIOS_S09 as SITIOS,
  TURNOS_WITH_HOURS as TURNOS, ESTADOS_CELDA_V2 as ESTADOS_CELDA,
  ICONOS_FRENTE, EMPRESA_SCOPE,
  type Frente, type ReglaCelda, type Rol, puedeEditar, severidadClass,
} from '../data';
import { descargarPlantillaImportacionCatalogos } from '../utils/plantillaImportacionExcel';

interface Props {
  screen: string;
  navigate: (s: string, p?: any) => void;
  params: any;
  onToast: (msg: string, desc: string, type: 'success' | 'error' | 'warning') => void;
  role: Rol;
  frenteCtx?: string | null;
  enterFrente?: (frenteId: string) => void;
  enterEmpresa?: () => void;
  clearFrenteCtx?: () => void;
}

function GuiaLink({ navigate }: { navigate: Props['navigate'] }) {
  return (
    <div className="helper-text" style={{ marginBottom: 14, display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
      <span>¿Qué va primero? Revisa la <strong>guía de arranque</strong> (alcance Empresa).</span>
      <button className="btn-secondary" type="button" style={{ height: 28, fontSize: 11 }} onClick={() => navigate('S0P')}>
        Ver guía →
      </button>
    </div>
  );
}

function FrenteCardButton({
  icon,
  code,
  title,
  desc,
  meta,
  onClick,
}: {
  icon: string;
  code: string;
  title: string;
  desc: string;
  meta: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      style={{
        textAlign: 'left',
        padding: '18px 18px 16px',
        border: '1px solid var(--clr-border)',
        borderRadius: 10,
        background: '#fff',
        cursor: 'pointer',
        boxShadow: '0 1px 2px rgba(0,0,0,0.04)',
      }}
      onMouseEnter={e => {
        e.currentTarget.style.borderColor = 'var(--clr-primary)';
        e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.08)';
      }}
      onMouseLeave={e => {
        e.currentTarget.style.borderColor = 'var(--clr-border)';
        e.currentTarget.style.boxShadow = '0 1px 2px rgba(0,0,0,0.04)';
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
        <span style={{ fontSize: 28 }}>{icon}</span>
        <code style={{ fontSize: 11, background: '#F3F4F6', padding: '2px 6px', borderRadius: 4 }}>{code}</code>
      </div>
      <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 4 }}>{title}</div>
      <div style={{ fontSize: 12, color: 'var(--clr-text-muted)', marginBottom: 14, lineHeight: 1.4, minHeight: 34 }}>{desc}</div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--clr-primary)' }}>{meta}</span>
        <span style={{ fontSize: 12, color: 'var(--clr-primary)' }}>Entrar →</span>
      </div>
    </button>
  );
}

// ─── S0D Dashboard Parametrización (elige frente / empresa) ───────────────────
function S0DDashboard({ enterFrente, enterEmpresa }: Props) {
  const frentes = FRENTES.filter(f => f.activo);
  return (
    <div style={{ padding: '24px 28px', maxWidth: 1100 }}>
      <Breadcrumb items={[{ label: 'Parametrización' }, { label: 'Elegir alcance' }]} />
      <div className="page-header">
        <div>
          <div className="page-title">Parametrización</div>
          <div className="page-subtitle">
            Primero elige el frente operativo. Luego verás solo las pantallas que aplican a ese frente.
          </div>
        </div>
      </div>

      <div className="section-header" style={{ marginBottom: 12 }}>Frentes operativos</div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 14, marginBottom: 28 }}>
        {frentes.map(f => {
          const caps = [
            f.usaModalidad && 'Modalidad',
            f.usaCampanas && 'Campañas',
            f.usaTerritorioZona && 'Territorio',
          ].filter(Boolean);
          return (
            <FrenteCardButton
              key={f.id}
              icon={ICONOS_FRENTE[f.id] ?? '🏬'}
              code={f.id}
              title={f.nombre}
              desc={f.descripcion || `Configuración y catálogos de ${f.nombre}`}
              meta={caps.length ? caps.join(' · ') : 'Sin atributos extra'}
              onClick={() => enterFrente?.(f.id)}
            />
          );
        })}
      </div>

      <div className="section-header" style={{ marginBottom: 12 }}>Alcance empresa</div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 14 }}>
        <FrenteCardButton
          icon="🏢"
          code="EMP"
          title="Catálogos de empresa"
          desc="Frentes, estados de celda, festivos, cortes, tipos de hora e importación Excel. No dependen de un frente."
          meta="Guía · Frentes · Estados · Calendario"
          onClick={() => enterEmpresa?.()}
        />
      </div>

      <div className="helper-text" style={{ marginTop: 18 }}>
        Tip: las plantillas de turno, sitios y campañas viven <strong>dentro del frente</strong>.
        Festivos y estados son de <strong>empresa</strong>.
      </div>
      <div className="screen-id">S0D</div>
    </div>
  );
}

const PASOS_PARAM = [
  {
    n: 1,
    screen: 'S01',
    title: 'Frentes operativos',
    hu: 'HU09 + HU10',
    must: true,
    body: 'Crea cada operación (CC, Mesa, Sitio, Lab…). Solo código, nombre, descripción y activo. Luego, con ⚙️, configura capacidades, quién arma, quién publica y si hay intercambio.',
  },
  {
    n: 2,
    screen: 'S03',
    title: 'Plantillas de turno',
    hu: 'HU11–13',
    must: true,
    body: 'Elige el frente en tarjetas y define sus turnos (T1, T5…). Luego configuras horario por día y breaks. Sin turnos no hay grilla útil.',
  },
  {
    n: 3,
    screen: 'S05',
    title: 'Estados de celda',
    hu: 'HU14',
    must: true,
    body: 'DES, VAC, INC, CAP… con flags (suma horas, asignable). Complementan al turno en cada celda.',
  },
  {
    n: 4,
    screen: 'S08',
    title: 'Modalidades',
    hu: 'HU17',
    must: false,
    body: 'Presencial / Virtual / Híbrido u otras. Solo si el frente tiene la capacidad “modalidad” encendida en ⚙️ Configuración.',
  },
  {
    n: 5,
    screen: 'S09',
    title: 'Sitios de asistencia',
    hu: 'HU18',
    must: false,
    body: 'Sedes, laboratorios, puntos físicos. Se asocian en la grilla cuando el frente usa sitio.',
  },
  {
    n: 6,
    screen: 'S06',
    title: 'Campañas / tareas',
    hu: 'HU15',
    must: false,
    body: 'Qué campaña o tarea atiende la persona ese día. Solo frentes con capacidad “campañas”.',
  },
  {
    n: 7,
    screen: 'S07',
    title: 'Territorio (Regional / Zona / SPT…)',
    hu: 'HU16',
    must: false,
    body: 'Jerarquía operativa (nombres configurables). Ej.: SPT Kennedy. Solo frentes con capacidad “territorio”.',
  },
  {
    n: 8,
    screen: 'S10',
    title: 'Restricciones de persona',
    hu: 'HU19',
    must: false,
    body: 'Exclusiones concretas (esta persona no puede T1). No confundir con umbrales del motor de reglas.',
  },
  {
    n: 9,
    screen: 'S11',
    title: 'Festivos · Cortes · Tipos de hora',
    hu: 'HU20–22',
    must: true,
    body: 'Calendario de festivos (empresa), cortes de nómina y clasificación de horas (ordinaria, nocturna…).',
  },
  {
    n: 10,
    screen: 'S12',
    title: 'Cobertura y compensatorios',
    hu: 'HU23–24',
    must: false,
    body: 'Umbrales de cobertura mínima y parámetros de compensatorio. El motor (paso 11) los usa al validar.',
  },
  {
    n: 11,
    screen: 'S13',
    title: 'Motor de reglas',
    hu: 'HU25',
    must: true,
    body: 'Activa/desactiva reglas, severidad (info / advertencia / bloqueo) y parámetros numéricos.',
  },
  {
    n: 12,
    screen: 'S15',
    title: 'Importación Excel (opcional)',
    hu: 'HU27',
    must: false,
    body: 'Atajo para cargar catálogos al inicio. No reemplaza la parametrización ni es la fuente permanente.',
  },
];

// ─── S0P Guía de arranque Parametrización ─────────────────────────────────────
function S0PGuia({ navigate }: Props) {
  return (
    <div style={{ padding: '24px 28px', maxWidth: 920 }}>
      <Breadcrumb items={[{ label: 'Parametrización' }, { label: 'Guía de arranque' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Sesión inicial — Parametrización</div>
          <div className="page-subtitle">
            Qué configura este submódulo y en qué orden hacerlo antes de armar la primera malla
          </div>
        </div>
        <button className="btn-primary" type="button" onClick={() => navigate('S01')}>
          Empezar por Frentes →
        </button>
      </div>

      <div className="card" style={{ padding: '18px 20px', marginBottom: 16, background: '#F0F7FA', border: '1px solid #B8D4E8' }}>
        <div style={{ fontWeight: 600, marginBottom: 8 }}>¿Para qué sirve?</div>
        <div style={{ fontSize: 13, lineHeight: 1.55 }}>
          Aquí defines los <strong>catálogos y reglas de la empresa</strong>: frentes, turnos, estados y atributos
          (modalidad, sitio, campaña, territorio). En <strong>Construcción</strong> solo se usan; no se inventan.
          Cada empresa arma su propio set — no hay lista fija de “CC / Mesa / Sitio” en el producto.
        </div>
      </div>

      <div className="card" style={{ padding: '18px 20px', marginBottom: 16 }}>
        <div className="section-header">Orden recomendado</div>
        <div style={{ fontSize: 12, color: 'var(--clr-text-muted)', marginBottom: 12 }}>
          Los pasos <Chip label="Obligatorio" /> conviene tenerlos antes de crear mallas.
          Los <Chip label="Según frente" /> solo si activaste esa capacidad en la configuración del frente (⚙️).
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {PASOS_PARAM.map(p => (
            <div
              key={p.n}
              style={{
                display: 'grid',
                gridTemplateColumns: '40px 1fr auto',
                gap: 12,
                alignItems: 'start',
                padding: '12px 14px',
                border: '1px solid var(--clr-border)',
                borderRadius: 8,
                background: '#FAFBFC',
              }}
            >
              <div
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: 16,
                  background: 'var(--clr-primary)',
                  color: '#fff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: 13,
                }}
              >
                {p.n}
              </div>
              <div>
                <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap', marginBottom: 4 }}>
                  <span style={{ fontWeight: 600, fontSize: 14 }}>{p.title}</span>
                  <span style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{p.hu}</span>
                  {p.must ? <Chip label="Obligatorio" /> : <Chip label="Según frente" />}
                </div>
                <div style={{ fontSize: 12, lineHeight: 1.5, color: 'var(--clr-text-body)' }}>{p.body}</div>
              </div>
              <button className="btn-secondary" type="button" style={{ whiteSpace: 'nowrap' }} onClick={() => navigate(p.screen)}>
                Ir →
              </button>
            </div>
          ))}
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, marginBottom: 16 }}>
        <div className="card" style={{ padding: '16px 18px' }}>
          <div className="section-header">Frente vs configuración (importante)</div>
          <ul style={{ margin: 0, paddingLeft: 18, fontSize: 12, lineHeight: 1.55 }}>
            <li>
              <strong>Alta del frente (HU09):</strong> solo identidad — código, nombre, descripción, activo.
            </li>
            <li>
              <strong>Configuración ⚙️ (HU10):</strong> periodo, estrategia de armado, separar quien arma / quien publica,
              editabilidad post-publicación, intercambio y <em>qué atributos pide la grilla</em>.
            </li>
            <li>
              Los campos “quien arma / quien publica” <strong>no</strong> van en el alta inicial: se definen en ⚙️
              como perfiles o roles de negocio del frente.
            </li>
          </ul>
        </div>
        <div className="card" style={{ padding: '16px 18px' }}>
          <div className="section-header">Qué no se parametriza aquí</div>
          <ul style={{ margin: 0, paddingLeft: 18, fontSize: 12, lineHeight: 1.55 }}>
            <li>Permisos de menú y alcance de frentes por usuario → plataforma / EP-00.</li>
            <li>Crear mallas, asignar celdas, publicar → submódulo Construcción.</li>
            <li>Datos de empresa (NIT, razón social) → administración de empresa GRH.</li>
            <li>Asociar modalidad/sitio/campaña a una persona → en la <strong>grilla</strong>, no en el wizard de personas.</li>
          </ul>
        </div>
      </div>

      <div className="helper-text">
        Tip: si vienes de Excel operativo, puedes empezar por <button type="button" className="btn-secondary" style={{ height: 26, fontSize: 11, margin: '0 4px' }} onClick={() => navigate('S15')}>Importación</button>
        y luego revisar cada catálogo. Si partes de cero, sigue el orden 1 → 11.
      </div>
      <div className="screen-id">S0P</div>
    </div>
  );
}

// ─── S01 Frentes operativos ───────────────────────────────────────────────────
function S01Frentes({ navigate, onToast, role }: Props) {
  const [frentes, setFrentes] = useState<Frente[]>(FRENTES);
  const [modal, setModal] = useState<{ open: boolean; frente?: Frente }>({ open: false });
  const [form, setForm] = useState({
    codigo: '',
    nombre: '',
    descripcion: '',
    activo: true,
  });
  const canEdit = puedeEditar(role);

  function toggleActivo(id: string) {
    setFrentes(fs => fs.map(f => f.id === id ? { ...f, activo: !f.activo } : f));
    onToast('Frente actualizado', '', 'success');
  }

  function openNew() {
    setForm({ codigo: '', nombre: '', descripcion: '', activo: true });
    setModal({ open: true, frente: undefined });
  }
  function openEdit(f: Frente) {
    setForm({
      codigo: f.id,
      nombre: f.nombre,
      descripcion: f.descripcion ?? '',
      activo: f.activo,
    });
    setModal({ open: true, frente: f });
  }

  function guardar() {
    if (!form.codigo.trim() || !form.nombre.trim()) {
      onToast('Completa código y nombre', '', 'warning');
      return;
    }
    const dup = frentes.some(f => f.id === form.codigo.trim().toUpperCase() && f.id !== modal.frente?.id);
    if (dup) {
      onToast('Código duplicado', 'Ya existe un frente con ese código en la empresa', 'error');
      return;
    }
    onToast(modal.frente ? 'Frente actualizado' : 'Frente creado — ahora abre ⚙️ Configuración', form.nombre, 'success');
    setModal({ open: false });
  }

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1200 }}>
      <Breadcrumb items={[{ label: 'Parametrización' }, { label: 'Frentes operativos' }]} navigate={navigate} />
      <GuiaLink navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Frentes operativos</div>
          <div className="page-subtitle">Paso 1 — Identidad del frente (código, nombre, activo). HU09. La operación del frente se configura con ⚙️ (HU10).</div>
        </div>
        {canEdit
          ? <button className="btn-primary" type="button" onClick={openNew}>+ Nuevo frente</button>
          : <DisabledBtn label="+ Nuevo frente" reason="Sin permiso CREAR/ACTUALIZAR en Parametrización" />}
      </div>

      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%', minWidth: 900 }}>
          <thead>
            <tr>
              <th>Código</th><th>Nombre</th><th>Quien arma / publica</th>
              <th>Modo armado</th><th>Intercambio</th><th>Activo</th><th></th>
            </tr>
          </thead>
          <tbody>
            {frentes.map(f => (
              <tr key={f.id} style={{ opacity: f.activo ? 1 : 0.55 }}>
                <td><code style={{ fontWeight: 700 }}>{f.id}</code></td>
                <td style={{ fontWeight: 500 }}>{f.nombre}</td>
                <td style={{ fontSize: 12, lineHeight: 1.4 }}>
                  <div>Arma: {f.responsableArma}</div>
                  <div style={{ color: 'var(--clr-text-muted)' }}>Publica: {f.responsablePublica}</div>
                </td>
                <td><span className="badge-mode">{f.modo}</span></td>
                <td>
                  <span className="chip" style={{ background: f.intercambioActivo ? '#DCFCE7' : '#F3F4F6', color: f.intercambioActivo ? '#15803D' : '#6B7280', border: `1px solid ${f.intercambioActivo ? '#BBF7D0' : '#E5E7EB'}` }}>
                    {f.intercambioActivo ? 'ON' : 'OFF'}
                  </span>
                </td>
                <td>
                  <label className="toggle-switch" aria-label={`Frente ${f.nombre} ${f.activo ? 'activo' : 'inactivo'}`}>
                    <input type="checkbox" checked={f.activo} onChange={() => canEdit ? toggleActivo(f.id) : undefined} disabled={!canEdit} />
                    <span className="toggle-track"></span>
                  </label>
                </td>
                <td className="td-actions">
                  {canEdit && <button className="btn-icon" type="button" title="Editar identidad" onClick={() => openEdit(f)}>✏️</button>}
                  <button className="btn-icon" type="button" title="Configurar frente (HU10)" onClick={() => navigate('S02', { frenteId: f.id })}>⚙️</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="helper-text" style={{ marginTop: 12 }}>
        El alta del frente (✏️) solo define identidad. Quien arma / publica, capacidades y publicación se editan con <strong>⚙️ Configuración</strong> (HU10).
        Un frente inactivo no acepta nuevas mallas (HU09).
      </div>

      {modal.open && (
        <Modal title={modal.frente ? 'Editar frente operativo' : 'Nuevo frente operativo'} onClose={() => setModal({ open: false })}>
          <div className="field-group">
            <div className="field-row">
              <Field label="Código" required helper="Único en la empresa. Máx. 6 caracteres.">
                <input
                  className="input-field"
                  value={form.codigo}
                  onChange={e => setForm(f => ({ ...f, codigo: e.target.value.toUpperCase() }))}
                  placeholder="Ej: LAB"
                  maxLength={6}
                  disabled={!!modal.frente}
                />
              </Field>
              <Field label="Nombre" required>
                <input className="input-field" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} placeholder="Ej: Laboratorio" />
              </Field>
            </div>
            <Field label="Descripción">
              <textarea className="input-field" rows={2} value={form.descripcion} onChange={e => setForm(f => ({ ...f, descripcion: e.target.value }))} placeholder="Qué operación cubre este frente" />
            </Field>
            <label className="checkbox-label">
              <input type="checkbox" checked={form.activo} onChange={e => setForm(f => ({ ...f, activo: e.target.checked }))} />
              Frente activo (visible para nuevas mallas)
            </label>
            <div className="helper-text">
              Después de guardar, abre <strong>⚙️ Configuración</strong> para: periodo, estrategia de armado,
              perfiles que arman/publican, atributos de celda (modalidad, sitio, campaña, territorio) e intercambio.
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 20 }}>
            <button className="btn-secondary" type="button" onClick={() => setModal({ open: false })}>Cancelar</button>
            <button className="btn-primary" type="button" onClick={guardar}>
              {modal.frente ? 'Guardar identidad' : 'Crear frente'}
            </button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S01</div>
    </div>
  );
}

// ─── S02 Configuración del frente ─────────────────────────────────────────────
function S02ConfigFrente({ navigate, params, onToast, role }: Props) {
  const frente = FRENTES.find(f => f.id === (params?.frenteId ?? 'CC')) ?? FRENTES[0];
  const canEdit = puedeEditar(role);
  const [intercambio, setIntercambio] = useState(frente.intercambioActivo);
  const [modo, setModo] = useState(frente.modo);
  const [periodo, setPeriodo] = useState(frente.periodo);
  const [editPublicada, setEditPublicada] = useState(frente.mallaPublicadaEditable || frente.id === 'SITIO');
  const [separarRoles, setSepararRoles] = useState(frente.responsableArma !== frente.responsablePublica);
  const [arma, setArma] = useState(frente.responsableArma);
  const [publica, setPublica] = useState(frente.responsablePublica);
  const [caps, setCaps] = useState({
    modalidad: frente.usaModalidad,
    sitio: true,
    campanas: frente.usaCampanas,
    territorio: frente.usaTerritorioZona,
  });

  function toggleCap(key: keyof typeof caps) {
    if (!canEdit) return;
    setCaps(c => ({ ...c, [key]: !c[key] }));
  }

  return (
    <div style={{ padding: '24px 28px', maxWidth: 920 }}>
      <Breadcrumb
        items={[
          { label: 'Parametrización' },
          { label: 'Frentes', onClick: () => navigate('S01') },
          { label: `Config. ${frente.nombre}` },
        ]}
        navigate={navigate}
      />
      <GuiaLink navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Configuración — {frente.nombre}</div>
          <div className="page-subtitle">
            Paso 1b — Cómo opera el frente: armado, publicación y qué pide cada celda. HU10 + HU26
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn-secondary" type="button" onClick={() => navigate('S01')}>← Frentes</button>
          {canEdit
            ? <button className="btn-primary" type="button" onClick={() => onToast('Configuración guardada', frente.nombre, 'success')}>Guardar</button>
            : <DisabledBtn label="Guardar" reason="Sin permiso" />}
        </div>
      </div>

      <div className="helper-text" style={{ marginBottom: 16 }}>
        Aquí no creas el frente: ya existe. Defines <strong>cómo se arma y publica</strong> y qué atributos
        (modalidad, sitio, campaña, territorio) aparecerán al editar celdas en la grilla.
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Identidad (solo lectura)</div>
          <Field label="Código"><input className="input-field" defaultValue={frente.id} disabled /></Field>
          <Field label="Nombre"><input className="input-field" defaultValue={frente.nombre} disabled /></Field>
          <button className="btn-secondary" type="button" style={{ width: '100%', justifyContent: 'center' }} onClick={() => navigate('S01')}>
            Editar identidad en listado →
          </button>
        </div>

        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Planificación y armado</div>
          <Field label="Periodo de planificación por defecto" helper="Al crear mallas nuevas de este frente">
            <select className="input-field" value={periodo} onChange={e => setPeriodo(e.target.value as Frente['periodo'])} disabled={!canEdit}>
              <option value="semana">Semana</option>
              <option value="mes">Mes</option>
            </select>
          </Field>
          <Field label="Estrategia de armado">
            <select className="input-field" value={modo} onChange={e => setModo(e.target.value as Frente['modo'])} disabled={!canEdit}>
              <option value="manual">Manual (celda a celda)</option>
              <option value="asistido">Asistido (con advertencias)</option>
              <option value="automatico">Automático (patrones de rotación)</option>
            </select>
          </Field>
          {modo === 'automatico' && (
            <div className="helper-text">
              Los patrones se definen en Construcción → Patrones. El ajuste manual siempre queda en historial.
            </div>
          )}
        </div>

        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Quién arma y quién publica</div>
          <div className="helper-text" style={{ marginBottom: 12 }}>
            No es el nombre de una persona concreta: es el <strong>perfil / rol de negocio</strong> del frente
            (ej. “Coordinadora CC”). Sirve para el ciclo de publicación y para orientar a quién le toca cada paso.
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
            <label className="toggle-switch">
              <input type="checkbox" checked={separarRoles} onChange={e => canEdit && setSepararRoles(e.target.checked)} disabled={!canEdit} />
              <span className="toggle-track"></span>
            </label>
            <div>
              <div style={{ fontSize: 13, fontWeight: 500 }}>Separar quien construye y quien publica</div>
              <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>Si está ON, quien solo arma no puede publicar (envía a revisión)</div>
            </div>
          </div>
          <Field label="Perfil que arma / construye la malla" helper="Ej.: Coordinadora de operaciones CC">
            <input className="input-field" value={arma} onChange={e => setArma(e.target.value)} disabled={!canEdit} />
          </Field>
          <Field label="Perfil que publica / aprueba" helper="Puede ser el mismo si la separación está OFF">
            <input
              className="input-field"
              value={separarRoles ? publica : arma}
              onChange={e => setPublica(e.target.value)}
              disabled={!canEdit || !separarRoles}
            />
          </Field>
        </div>

        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Publicación e intercambio</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
            <label className="toggle-switch">
              <input type="checkbox" checked={editPublicada} onChange={e => canEdit && setEditPublicada(e.target.checked)} disabled={!canEdit} />
              <span className="toggle-track"></span>
            </label>
            <div>
              <div style={{ fontSize: 13, fontWeight: 500 }}>Malla publicada editable</div>
              <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>Permite ajustes con trazabilidad tras publicar</div>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
            <label className="toggle-switch">
              <input type="checkbox" checked={intercambio} onChange={e => canEdit && setIntercambio(e.target.checked)} disabled={!canEdit} />
              <span className="toggle-track"></span>
            </label>
            <div>
              <div style={{ fontSize: 13, fontWeight: 500 }}>Solicitudes de intercambio</div>
              <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>Por defecto OFF en cada frente</div>
            </div>
          </div>
          {!intercambio && (
            <div className="helper-text">Intercambio desactivado: el colaborador no verá “solicitar intercambio” en Mi programación.</div>
          )}
        </div>

        <div className="card" style={{ padding: '18px 20px', gridColumn: '1 / -1' }}>
          <div className="section-header">Atributos de celda que usa este frente (HU26)</div>
          <div style={{ fontSize: 12, color: 'var(--clr-text-muted)', marginBottom: 12 }}>
            Solo lo que actives aquí se pide al editar una celda en la grilla. Los catálogos (modalidades, sitios…) se cargan en los pasos 4–7.
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
            {([
              { key: 'modalidad' as const, label: 'Modalidad de trabajo', hint: 'Presencial / Virtual / Híbrido…', go: 'S08' },
              { key: 'sitio' as const, label: 'Sitio de asistencia', hint: 'Sede, laboratorio, punto físico…', go: 'S09' },
              { key: 'campanas' as const, label: 'Campaña / tarea', hint: 'Qué campaña atiende ese día', go: 'S06' },
              { key: 'territorio' as const, label: 'Territorio / SPT', hint: 'Regional → Zona → SPT…', go: 'S07' },
            ]).map(item => (
              <div key={item.key} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 12px', border: '1px solid var(--clr-border)', borderRadius: 8 }}>
                <label className="toggle-switch">
                  <input type="checkbox" checked={caps[item.key]} onChange={() => toggleCap(item.key)} disabled={!canEdit} />
                  <span className="toggle-track"></span>
                </label>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 13, fontWeight: 500 }}>{item.label}</div>
                  <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{item.hint}</div>
                </div>
                <button className="btn-secondary" type="button" style={{ height: 28, fontSize: 11 }} onClick={() => navigate(item.go)}>
                  Catálogo →
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="screen-id">S02</div>
    </div>
  );
}

// ─── S03 Plantillas de turno ──────────────────────────────────────────────────
function S03Plantillas({ navigate, params, onToast, role, frenteCtx, clearFrenteCtx }: Props) {
  const canEdit = puedeEditar(role);
  const frentesActivos = FRENTES.filter(f => f.activo);
  const lockedByCtx = !!(frenteCtx && frenteCtx !== EMPRESA_SCOPE);
  const [frenteLocal, setFrenteLocal] = useState<string | null>(params?.frenteId ?? null);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({
    codigo: '',
    nombre: '',
    inicio: '06:00',
    fin: '14:00',
    nocturno: false,
    color: 'turno-T1',
    activo: true,
  });

  const effectiveId = lockedByCtx ? frenteCtx! : (frenteLocal ?? params?.frenteId ?? null);
  const frente = frentesActivos.find(f => f.id === effectiveId) ?? null;
  const turnosFrente = frente
    ? TURNOS.filter(t => (t.frentes ?? [t.frenteId]).includes(frente.id) || t.frenteId === frente.id)
    : [];

  function countTurnos(fid: string) {
    return TURNOS.filter(t => (t.frentes ?? [t.frenteId]).includes(fid) || t.frenteId === fid).length;
  }

  function openNew() {
    if (!frente) return;
    setForm({ codigo: '', nombre: '', inicio: '06:00', fin: '14:00', nocturno: false, color: 'turno-T1', activo: true });
    setModalOpen(true);
  }

  function guardarPlantilla() {
    if (!frente) return;
    if (!form.codigo.trim() || !form.nombre.trim()) {
      onToast('Completa código y nombre', '', 'warning');
      return;
    }
    onToast('Plantilla creada', `${form.codigo.toUpperCase()} · ${frente.nombre}`, 'success');
    setModalOpen(false);
    navigate('S04', { turnoId: form.codigo.toUpperCase(), nuevo: true, frenteId: frente.id });
  }

  // ── Vista: elegir frente (solo si no hay contexto del Shell) ──
  if (!frente) {
    return (
      <div style={{ padding: '24px 28px', maxWidth: 1100 }}>
        <Breadcrumb items={[{ label: 'Parametrización' }, { label: 'Plantillas de turno' }]} navigate={navigate} />
        <GuiaLink navigate={navigate} />
        <div className="page-header">
          <div>
            <div className="page-title">Plantillas de turno</div>
            <div className="page-subtitle">Elige el frente y define sus turnos. HU11–13</div>
          </div>
        </div>

        <div className="helper-text" style={{ marginBottom: 16 }}>
          Preferible entrar desde el dashboard de Parametrización eligiendo el frente; aquí también puedes elegir la tarjeta.
        </div>

        {frentesActivos.length === 0 ? (
          <EmptyState
            title="No hay frentes activos"
            desc="Primero crea un frente operativo y actívalo."
            action={<button className="btn-primary" type="button" onClick={() => navigate('S01')}>Ir a Frentes</button>}
          />
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 14 }}>
            {frentesActivos.map(f => {
              const n = countTurnos(f.id);
              return (
                <FrenteCardButton
                  key={f.id}
                  icon={ICONOS_FRENTE[f.id] ?? '🏬'}
                  code={f.id}
                  title={f.nombre}
                  desc={f.descripcion || `Turnos de ${f.nombre}`}
                  meta={`${n} plantilla${n === 1 ? '' : 's'}`}
                  onClick={() => setFrenteLocal(f.id)}
                />
              );
            })}
          </div>
        )}
        <div className="screen-id">S03</div>
      </div>
    );
  }

  // ── Vista: turnos del frente ──
  return (
    <div style={{ padding: '24px 28px', maxWidth: 1100 }}>
      <Breadcrumb
        items={[
          { label: 'Parametrización' },
          { label: 'Plantillas', onClick: () => (lockedByCtx ? clearFrenteCtx?.() : setFrenteLocal(null)) },
          { label: frente.nombre },
        ]}
        navigate={navigate}
      />
      <div className="page-header">
        <div>
          <div className="page-title" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span>{ICONOS_FRENTE[frente.id] ?? '🏬'}</span>
            Turnos — {frente.nombre}
          </div>
          <div className="page-subtitle">
            Plantillas del frente <code>{frente.id}</code>. HU11–13
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          {!lockedByCtx && (
            <button className="btn-secondary" type="button" onClick={() => setFrenteLocal(null)}>← Otros frentes</button>
          )}
          {canEdit
            ? <button className="btn-primary" type="button" onClick={openNew}>+ Nueva plantilla</button>
            : <DisabledBtn label="+ Nueva plantilla" reason="Sin permiso" />}
        </div>
      </div>

      {turnosFrente.length === 0 ? (
        <div className="card" style={{ padding: '36px 24px', textAlign: 'center' }}>
          <div style={{ fontSize: 36, marginBottom: 10 }}>⏰</div>
          <div style={{ fontWeight: 600, marginBottom: 6 }}>Sin plantillas en {frente.nombre}</div>
          <div style={{ fontSize: 13, color: 'var(--clr-text-muted)', marginBottom: 16 }}>
            Crea el primer turno de este frente (código, horario y luego breaks).
          </div>
          {canEdit && (
            <button className="btn-primary" type="button" onClick={openNew}>+ Crear primer turno</button>
          )}
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
          <table className="table-grh" style={{ width: '100%', minWidth: 720 }}>
            <thead>
              <tr>
                <th>Código</th><th>Nombre</th><th>Inicio</th><th>Fin</th><th>Horas netas</th><th>Activo</th><th></th>
              </tr>
            </thead>
            <tbody>
              {turnosFrente.map(t => (
                <tr key={t.codigo}>
                  <td><span className={`chip turno-${t.codigo}`}>{t.codigo}</span></td>
                  <td style={{ fontWeight: 500 }}>{t.nombre}</td>
                  <td>{t.horaInicio}</td>
                  <td>{t.horaFin}</td>
                  <td style={{ fontWeight: 600 }}>{t.horasNetas}h</td>
                  <td><span style={{ color: '#15803D' }}>●</span></td>
                  <td className="td-actions">
                    {canEdit && (
                      <button
                        className="btn-icon"
                        type="button"
                        title="Horario y pausas"
                        onClick={() => navigate('S04', { turnoId: t.codigo, frenteId: frente.id })}
                      >
                        ✏️
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="helper-text" style={{ marginTop: 10 }}>
        Flujo: <strong>+ Nueva plantilla</strong> → datos básicos → horario y breaks → vuelve a este listado.
        {!lockedByCtx && <> Para otro frente usa <strong>← Otros frentes</strong> o el dashboard.</>}
      </div>

      {modalOpen && (
        <Modal title={`Nueva plantilla — ${frente.nombre}`} onClose={() => setModalOpen(false)}>
          <div className="helper-text" style={{ marginBottom: 14 }}>
            Este turno quedará asociado al frente <strong>{frente.nombre}</strong> (<code>{frente.id}</code>).
            No hace falta volver a elegir frente.
          </div>
          <div className="field-group">
            <div className="field-row">
              <Field label="Código" required helper="Único en la empresa">
                <input className="input-field" value={form.codigo} onChange={e => setForm(f => ({ ...f, codigo: e.target.value.toUpperCase() }))} placeholder="Ej: T9" maxLength={6} />
              </Field>
              <Field label="Nombre" required>
                <input className="input-field" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} placeholder="Ej: Turno especial sábado" />
              </Field>
            </div>
            <div className="field-row">
              <Field label="Hora inicio" required>
                <input className="input-field" type="time" value={form.inicio} onChange={e => setForm(f => ({ ...f, inicio: e.target.value }))} />
              </Field>
              <Field label="Hora fin" required>
                <input className="input-field" type="time" value={form.fin} onChange={e => setForm(f => ({ ...f, fin: e.target.value }))} />
              </Field>
            </div>
            <label className="checkbox-label">
              <input type="checkbox" checked={form.nocturno} onChange={e => setForm(f => ({ ...f, nocturno: e.target.checked }))} />
              Cruce de medianoche (hora fin al día siguiente)
            </label>
            <Field label="Color en grilla">
              <select className="input-field" value={form.color} onChange={e => setForm(f => ({ ...f, color: e.target.value }))}>
                <option value="turno-T1">Azul (mañana)</option>
                <option value="turno-T5">Naranja (tarde/noche)</option>
                <option value="turno-T8">Violeta (especial)</option>
              </select>
            </Field>
            <label className="checkbox-label">
              <input type="checkbox" checked={form.activo} onChange={e => setForm(f => ({ ...f, activo: e.target.checked }))} />
              Plantilla activa (disponible al asignar celdas)
            </label>
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 20 }}>
            <button className="btn-secondary" type="button" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button className="btn-primary" type="button" onClick={guardarPlantilla}>Crear y configurar horario →</button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S03</div>
    </div>
  );
}

// ─── S04 Detalle horario / breaks ─────────────────────────────────────────────
function S04Horario({ navigate, params, onToast, role }: Props) {
  const isNuevo = !!params?.nuevo;
  const t = TURNOS.find(x => x.codigo === params?.turnoId) ?? TURNOS[0];
  const canEdit = puedeEditar(role);
  const [pausas, setPausas] = useState([
    { label: 'Descanso', dur: '30' },
    { label: 'Refrigerio', dur: '15' },
  ]);
  const [diasDiff, setDiasDiff] = useState(false);

  return (
    <div style={{ padding: '24px 28px', maxWidth: 960 }}>
      <Breadcrumb
        items={[
          { label: 'Parametrización' },
          { label: 'Plantillas', onClick: () => navigate('S03', params?.frenteId ? { frenteId: params.frenteId } : undefined) },
          { label: isNuevo ? 'Nueva — horario' : `${t.codigo}` },
        ]}
        navigate={navigate}
      />
      <div className="page-header">
        <div>
          <div className="page-title">{isNuevo ? 'Configurar horario de la plantilla' : `Turno ${t.codigo} — ${t.nombre}`}</div>
          <div className="page-subtitle">
            {params?.frenteId ? <>Frente <code>{params.frenteId}</code> · </> : null}
            Horarios por día (HU12) y break/almuerzo (HU13)
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn-secondary" type="button" onClick={() => navigate('S03', params?.frenteId ? { frenteId: params.frenteId } : undefined)}>← Listado del frente</button>
          {canEdit && (
            <button className="btn-secondary" type="button" onClick={() => navigate('S03', params?.frenteId ? { frenteId: params.frenteId } : undefined)}>+ Crear otro turno</button>
          )}
          {canEdit
            ? <button className="btn-primary" type="button" onClick={() => { onToast('Turno guardado', params?.turnoId ?? t.codigo, 'success'); navigate('S03', params?.frenteId ? { frenteId: params.frenteId } : undefined); }}>Guardar y volver</button>
            : <DisabledBtn label="Guardar" reason="Sin permiso" />}
        </div>
      </div>

      <div className="helper-text" style={{ marginBottom: 16 }}>
        Esta pantalla es el detalle de <em>una</em> plantilla (horario por día + breaks). Para crear la siguiente plantilla vuelve al listado con <strong>+ Nueva plantilla</strong>.
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 20 }}>
        <div className="card" style={{ padding: '20px 22px' }}>
          <div className="section-header">Datos de la plantilla</div>
          <Field label="Código"><input className="input-field" defaultValue={params?.turnoId ?? t.codigo} disabled={!isNuevo || !canEdit} /></Field>
          <Field label="Nombre"><input className="input-field" defaultValue={isNuevo ? '' : t.nombre} placeholder="Nombre visible" disabled={!canEdit} /></Field>
          <div className="field-row">
            <Field label="Hora inicio"><input className="input-field" type="time" defaultValue={t.horaInicio} disabled={!canEdit} /></Field>
            <Field label="Hora fin"><input className="input-field" type="time" defaultValue={t.horaFin} disabled={!canEdit} /></Field>
          </div>
          <Field label="Horas netas (h)"><input className="input-field" type="number" defaultValue={t.horasNetas} disabled={!canEdit} /></Field>
          <Field label="Cruce medianoche">
            <select className="input-field" defaultValue={t.nocturno ? 'si' : 'no'} disabled={!canEdit}>
              <option value="no">No</option>
              <option value="si">Sí (+1 día)</option>
            </select>
          </Field>
        </div>

        <div className="card" style={{ padding: '20px 22px' }}>
          <div className="section-header">Pausas (break / almuerzo) — HU13</div>
          {pausas.map((p, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
              <input className="input-field" style={{ flex: 1 }} value={p.label} disabled={!canEdit} onChange={e => setPausas(ps => ps.map((x, j) => j === i ? { ...x, label: e.target.value } : x))} />
              <input className="input-field" style={{ width: 90 }} value={p.dur} disabled={!canEdit} onChange={e => setPausas(ps => ps.map((x, j) => j === i ? { ...x, dur: e.target.value } : x))} placeholder="min" />
              <span style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>min</span>
              {canEdit && <button className="btn-icon" type="button" title="Eliminar" onClick={() => setPausas(ps => ps.filter((_, j) => j !== i))}>🗑️</button>}
            </div>
          ))}
          {canEdit && (
            <button className="btn-secondary" type="button" style={{ width: '100%', justifyContent: 'center' }} onClick={() => setPausas(ps => [...ps, { label: 'Nueva pausa', dur: '15' }])}>
              + Pausa
            </button>
          )}
        </div>
      </div>

      <div className="card" style={{ padding: '20px 22px' }}>
        <div className="section-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span>Horarios distintos por día — HU12</span>
          <label className="checkbox-label">
            <input type="checkbox" checked={diasDiff} onChange={e => setDiasDiff(e.target.checked)} disabled={!canEdit} />
            Usar horario diferente por día
          </label>
        </div>
        {diasDiff ? (
          <div className="card" style={{ padding: 0, overflowX: 'auto', boxShadow: 'none', border: '1px solid var(--clr-border)' }}>
            <table className="table-grh">
              <thead>
                <tr><th>Día</th><th>Inicio</th><th>Fin</th><th>Aplica</th></tr>
              </thead>
              <tbody>
                {['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'].map((dia, i) => (
                  <tr key={dia}>
                    <td style={{ fontWeight: 500 }}>{dia}</td>
                    <td><input className="input-field" type="time" defaultValue={i < 5 ? t.horaInicio : '08:00'} disabled={!canEdit} style={{ width: 120 }} /></td>
                    <td><input className="input-field" type="time" defaultValue={i === 4 ? '16:00' : t.horaFin} disabled={!canEdit} style={{ width: 120 }} /></td>
                    <td><input type="checkbox" defaultChecked={i < 6} disabled={!canEdit} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="helper-text">Misma franja todos los días aplicables. Activa la opción para variar por día (ej. viernes distinto).</div>
        )}
      </div>
      <div className="screen-id">S04</div>
    </div>
  );
}

// ─── S05 Estados de celda ─────────────────────────────────────────────────────
function S05Estados({ navigate, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({
    codigo: '',
    nombre: '',
    asignable: true,
    descuentaHoras: false,
    requiereSoporte: false,
    sumaHoras: false,
  });

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1000 }}>
      <Breadcrumb items={[{ label: 'Parametrización' }, { label: 'Estados de celda' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Estados de celda</div>
          <div className="page-subtitle">Flags de comportamiento (asignable, horas, soporte). HU14</div>
        </div>
        {canEdit
          ? <button className="btn-primary" type="button" onClick={() => setModalOpen(true)}>+ Nuevo estado</button>
          : <DisabledBtn label="+ Nuevo estado" reason="Sin permiso" />}
      </div>
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%', minWidth: 720 }}>
          <thead>
            <tr>
              <th>Código</th><th>Nombre</th><th>Color</th>
              <th>Asignable en grilla</th><th>Descuenta horas</th><th>Requiere soporte</th>
            </tr>
          </thead>
          <tbody>
            {ESTADOS_CELDA.map(e => (
              <tr key={e.codigo}>
                <td><span className={`chip turno-${e.codigo}`}>{e.codigo}</span></td>
                <td style={{ fontWeight: 500 }}>{e.nombre}</td>
                <td><span style={{ display: 'inline-block', width: 20, height: 20, borderRadius: 4, background: e.color, border: '1px solid #ccc' }} /></td>
                <td>
                  <span style={{ color: e.asignable ? '#15803D' : '#DC2626', fontWeight: 600 }}>
                    {e.asignable ? '✓ Sí' : '✗ No'}
                  </span>
                  {(e.codigo === 'CAP' || e.codigo === 'ACT') && (
                    <span style={{ marginLeft: 8, fontSize: 11, color: '#DC2626' }}>no asignable a casos</span>
                  )}
                </td>
                <td>{e.descuentaHoras ? '✓' : '—'}</td>
                <td>{e.requiereSoporte ? '✓' : '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="helper-text" style={{ marginTop: 10 }}>
        CAP y ACT suelen ir con <code>asignable=false</code> (no aparecen al asignar en grilla / casos).
      </div>

      {modalOpen && (
        <Modal title="Nuevo estado de celda" onClose={() => setModalOpen(false)} size="sm">
          <div className="field-group">
            <div className="field-row">
              <Field label="Código" required>
                <input className="input-field" value={form.codigo} onChange={e => setForm(f => ({ ...f, codigo: e.target.value.toUpperCase() }))} maxLength={4} placeholder="Ej: LIC" />
              </Field>
              <Field label="Nombre" required>
                <input className="input-field" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} placeholder="Ej: Licencia" />
              </Field>
            </div>
            <label className="checkbox-label"><input type="checkbox" checked={form.asignable} onChange={e => setForm(f => ({ ...f, asignable: e.target.checked }))} /> Asignable en grilla / a casos</label>
            <label className="checkbox-label"><input type="checkbox" checked={form.sumaHoras} onChange={e => setForm(f => ({ ...f, sumaHoras: e.target.checked }))} /> Suma horas al reporte</label>
            <label className="checkbox-label"><input type="checkbox" checked={form.descuentaHoras} onChange={e => setForm(f => ({ ...f, descuentaHoras: e.target.checked }))} /> Descuenta horas productivas</label>
            <label className="checkbox-label"><input type="checkbox" checked={form.requiereSoporte} onChange={e => setForm(f => ({ ...f, requiereSoporte: e.target.checked }))} /> Requiere documento / soporte</label>
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 20 }}>
            <button className="btn-secondary" type="button" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button className="btn-primary" type="button" onClick={() => { onToast('Estado creado', form.codigo || form.nombre, 'success'); setModalOpen(false); }}>Guardar</button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S05</div>
    </div>
  );
}

// ─── S06 Campañas ─────────────────────────────────────────────────────────────
function S06Campanhas({ navigate, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({ nombre: '', codigo: '', frenteId: 'CC', inicio: '', fin: '', activa: true });

  return (
    <div style={{ padding: '24px 28px', maxWidth: 900 }}>
      <Breadcrumb items={[{ label: 'Parametrización' }, { label: 'Campañas' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Campañas / tareas de celda</div>
          <div className="page-subtitle">Código, vigencia y aplicabilidad a frentes. HU15</div>
        </div>
        {canEdit
          ? <button className="btn-primary" type="button" onClick={() => setModalOpen(true)}>+ Nueva campaña</button>
          : <DisabledBtn label="+ Nueva campaña" reason="Sin permiso" />}
      </div>
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%', minWidth: 640 }}>
          <thead><tr><th>Nombre</th><th>Frente</th><th>Inicio</th><th>Fin</th><th>Estado</th><th></th></tr></thead>
          <tbody>
            {[
              { nombre: 'Campaña Vacaciones 2025-I', frente: 'CC', inicio: '2025-01-06', fin: '2025-03-28', activa: true },
              { nombre: 'Mesa de ayuda Q1', frente: 'MESA', inicio: '2025-01-13', fin: '2025-03-31', activa: true },
              { nombre: 'Mantenimiento preventivo', frente: 'SITIO', inicio: '2025-02-01', fin: '2025-02-28', activa: false },
            ].map(c => (
              <tr key={c.nombre}>
                <td style={{ fontWeight: 500 }}>{c.nombre}</td>
                <td><Chip label={c.frente} /></td>
                <td style={{ fontSize: 12 }}>{c.inicio}</td>
                <td style={{ fontSize: 12 }}>{c.fin}</td>
                <td>
                  <span className={c.activa ? 'chip estado-publicada' : 'chip estado-rechazada'} style={{ minWidth: 70, justifyContent: 'center' }}>
                    {c.activa ? 'Activa' : 'Cerrada'}
                  </span>
                </td>
                <td>{canEdit && <button className="btn-icon" type="button" title="Editar">✏️</button>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="helper-text" style={{ marginTop: 10 }}>
        Solo aplica si el frente tiene la capacidad de campañas habilitada (HU10 / HU26).
      </div>

      {modalOpen && (
        <Modal title="Nueva campaña / tarea" onClose={() => setModalOpen(false)} size="sm">
          <div className="field-group">
            <Field label="Código" required>
              <input className="input-field" value={form.codigo} onChange={e => setForm(f => ({ ...f, codigo: e.target.value.toUpperCase() }))} placeholder="Ej: VAC-I" />
            </Field>
            <Field label="Nombre" required>
              <input className="input-field" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} placeholder="Nombre visible" />
            </Field>
            <Field label="Frente" required>
              <select className="input-field" value={form.frenteId} onChange={e => setForm(f => ({ ...f, frenteId: e.target.value }))}>
                {FRENTES.filter(f => f.activo).map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
              </select>
            </Field>
            <div className="field-row">
              <Field label="Vigencia desde"><input className="input-field" type="date" value={form.inicio} onChange={e => setForm(f => ({ ...f, inicio: e.target.value }))} /></Field>
              <Field label="Vigencia hasta"><input className="input-field" type="date" value={form.fin} onChange={e => setForm(f => ({ ...f, fin: e.target.value }))} /></Field>
            </div>
            <label className="checkbox-label">
              <input type="checkbox" checked={form.activa} onChange={e => setForm(f => ({ ...f, activa: e.target.checked }))} />
              Campaña vigente / activa
            </label>
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 20 }}>
            <button className="btn-secondary" type="button" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button className="btn-primary" type="button" onClick={() => { onToast('Campaña creada', form.nombre || form.codigo, 'success'); setModalOpen(false); }}>Guardar</button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S06</div>
    </div>
  );
}

// ─── S07 Territorio ───────────────────────────────────────────────────────────
function S07Territorio({ navigate, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({ codigo: '', nombre: '', nivel: '2', padre: 'REG-001', frente: 'CC' });
  return (
    <div style={{ padding: '24px 28px', maxWidth: 800 }}>
      <Breadcrumb items={[{ label: 'A. Parametrización' }, { label: 'S07 Territorio' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Territorio operativo</div>
          <div className="page-subtitle">Jerarquía de nodos — nombres configurables. HU16</div>
        </div>
        {canEdit
          ? <button className="btn-primary" type="button" onClick={() => setModalOpen(true)}>+ Nodo</button>
          : <DisabledBtn label="+ Nodo" reason="Sin permiso" />}
      </div>
      <div className="helper-text" style={{ marginBottom: 16 }}>
        Los nombres de nivel son configurables por empresa. Data Center S.A. usa: <strong>Nivel 1 → Regional</strong>, <strong>Nivel 2 → Zona</strong>, <strong>Nivel 3 → SPT</strong>.
      </div>
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead><tr><th>Código</th><th>Nombre</th><th>Nivel</th><th>Padre</th><th>Frente</th><th>Activo</th></tr></thead>
          <tbody>
            {[
              { cod: 'REG-001', nombre: 'Regional Bogotá', nivel: 'Regional (N1)', padre: '—', frente: 'Todos' },
              { cod: 'ZON-001', nombre: 'Zona Centro', nivel: 'Zona (N2)', padre: 'Regional Bogotá', frente: 'CC' },
              { cod: 'SPT-001', nombre: 'SPT Kennedy', nivel: 'SPT (N3)', padre: 'Zona Centro', frente: 'SITIO' },
              { cod: 'SPT-002', nombre: 'SPT Chapinero', nivel: 'SPT (N3)', padre: 'Zona Centro', frente: 'SITIO' },
            ].map(n => (
              <tr key={n.cod}>
                <td><code>{n.cod}</code></td>
                <td style={{ fontWeight: 500 }}>{n.nombre}</td>
                <td style={{ fontSize: 12 }}>{n.nivel}</td>
                <td style={{ fontSize: 12 }}>{n.padre}</td>
                <td><Chip label={n.frente} /></td>
                <td><span style={{ color: '#15803D' }}>●</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {modalOpen && (
        <Modal title="Nuevo nodo de territorio" onClose={() => setModalOpen(false)} size="sm">
          <div className="field-group">
            <Field label="Código" required>
              <input className="input-field" value={form.codigo} onChange={e => setForm(f => ({ ...f, codigo: e.target.value.toUpperCase() }))} placeholder="Ej: ZON-002" />
            </Field>
            <Field label="Nombre" required>
              <input className="input-field" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} placeholder="Ej: Zona Norte" />
            </Field>
            <Field label="Nivel">
              <select className="input-field" value={form.nivel} onChange={e => setForm(f => ({ ...f, nivel: e.target.value }))}>
                <option value="1">Nivel 1 — Regional</option>
                <option value="2">Nivel 2 — Zona</option>
                <option value="3">Nivel 3 — SPT</option>
              </select>
            </Field>
            <Field label="Nodo padre" helper="Vacío si es raíz (N1)">
              <select className="input-field" value={form.padre} onChange={e => setForm(f => ({ ...f, padre: e.target.value }))}>
                <option value="">— Sin padre (raíz) —</option>
                <option value="REG-001">Regional Bogotá</option>
                <option value="ZON-001">Zona Centro</option>
              </select>
            </Field>
            <Field label="Frente aplicable">
              <select className="input-field" value={form.frente} onChange={e => setForm(f => ({ ...f, frente: e.target.value }))}>
                <option value="Todos">Todos</option>
                {FRENTES.filter(f => f.activo).map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
              </select>
            </Field>
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" type="button" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button className="btn-primary" type="button" onClick={() => { onToast('Nodo guardado', form.nombre || form.codigo, 'success'); setModalOpen(false); }}>Guardar</button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S07</div>
    </div>
  );
}

// ─── S08 Modalidades ──────────────────────────────────────────────────────────
function S08Modalidades({ navigate, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({ codigo: '', nombre: '', icono: '🏢', frentes: ['CC'] as string[] });
  function toggleFrente(id: string) {
    setForm(f => ({
      ...f,
      frentes: f.frentes.includes(id) ? f.frentes.filter(x => x !== id) : [...f.frentes, id],
    }));
  }
  return (
    <div style={{ padding: '24px 28px', maxWidth: 760 }}>
      <Breadcrumb items={[{ label: 'A. Parametrización' }, { label: 'S08 Modalidades' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Modalidades de jornada</div>
          <div className="page-subtitle">Catálogo por empresa (Presencial / Virtual / Híbrido u otras). HU17</div>
        </div>
        {canEdit
          ? <button className="btn-primary" type="button" onClick={() => setModalOpen(true)}>+ Modalidad</button>
          : <DisabledBtn label="+ Modalidad" reason="Sin permiso" />}
      </div>
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead><tr><th>Código</th><th>Icono</th><th>Nombre</th><th>Frentes permitidos</th><th>Activo</th></tr></thead>
          <tbody>
            {MODALIDADES.map(m => (
              <tr key={m.codigo}>
                <td><code>{m.codigo}</code></td>
                <td style={{ fontSize: 18 }}>{m.icono}</td>
                <td style={{ fontWeight: 500 }}>{m.nombre}</td>
                <td><div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>{m.frentes.map(f => <Chip key={f} label={f} />)}</div></td>
                <td><span style={{ color: '#15803D' }}>●</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {modalOpen && (
        <Modal title="Nueva modalidad de jornada" onClose={() => setModalOpen(false)} size="sm">
          <div className="field-group">
            <div className="field-row">
              <Field label="Código" required>
                <input className="input-field" value={form.codigo} onChange={e => setForm(f => ({ ...f, codigo: e.target.value.toUpperCase() }))} placeholder="Ej: REM" maxLength={6} />
              </Field>
              <Field label="Icono">
                <select className="input-field" value={form.icono} onChange={e => setForm(f => ({ ...f, icono: e.target.value }))}>
                  <option value="🏢">🏢 Presencial</option>
                  <option value="🏠">🏠 Virtual</option>
                  <option value="⚡">⚡ Híbrido</option>
                  <option value="📍">📍 Otro</option>
                </select>
              </Field>
            </div>
            <Field label="Nombre" required>
              <input className="input-field" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} placeholder="Ej: Remoto asistido" />
            </Field>
            <Field label="Frentes donde aplica" required>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, marginTop: 4 }}>
                {FRENTES.filter(f => f.activo).map(f => (
                  <label key={f.id} className="checkbox-label">
                    <input type="checkbox" checked={form.frentes.includes(f.id)} onChange={() => toggleFrente(f.id)} />
                    {f.nombre}
                  </label>
                ))}
              </div>
            </Field>
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" type="button" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button className="btn-primary" type="button" onClick={() => {
              if (!form.codigo.trim() || !form.nombre.trim()) { onToast('Completa código y nombre', '', 'warning'); return; }
              onToast('Modalidad creada', form.codigo, 'success');
              setModalOpen(false);
            }}>Guardar</button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S08</div>
    </div>
  );
}

// ─── S09 Sitios ───────────────────────────────────────────────────────────────
function S09Sitios({ navigate, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({ codigo: '', nombre: '', frente: 'CC', tipo: 'Sede', direccion: '' });
  return (
    <div style={{ padding: '24px 28px', maxWidth: 800 }}>
      <Breadcrumb items={[{ label: 'A. Parametrización' }, { label: 'S09 Sitios' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Sitios de asistencia</div>
          <div className="page-subtitle">Ubicaciones físicas o virtuales del frente. HU18</div>
        </div>
        {canEdit
          ? <button className="btn-primary" type="button" onClick={() => setModalOpen(true)}>+ Sitio</button>
          : <DisabledBtn label="+ Sitio" reason="Sin permiso" />}
      </div>
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead><tr><th>Código</th><th>Nombre</th><th>Frente</th><th>Tipo</th><th>Dirección</th><th>Activo</th></tr></thead>
          <tbody>
            {SITIOS.map(s => (
              <tr key={s.codigo}>
                <td><code>{s.codigo}</code></td>
                <td style={{ fontWeight: 500 }}>{s.nombre}</td>
                <td><Chip label={s.frente} /></td>
                <td style={{ fontSize: 12 }}>{s.tipo}</td>
                <td style={{ fontSize: 12 }}>{s.direccion}</td>
                <td><span style={{ color: '#15803D' }}>●</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {modalOpen && (
        <Modal title="Nuevo sitio de asistencia" onClose={() => setModalOpen(false)} size="sm">
          <div className="field-group">
            <div className="field-row">
              <Field label="Código" required>
                <input className="input-field" value={form.codigo} onChange={e => setForm(f => ({ ...f, codigo: e.target.value.toUpperCase() }))} placeholder="Ej: S05" maxLength={8} />
              </Field>
              <Field label="Tipo">
                <select className="input-field" value={form.tipo} onChange={e => setForm(f => ({ ...f, tipo: e.target.value }))}>
                  <option>Sede</option>
                  <option>SPT</option>
                  <option>Laboratorio</option>
                  <option>Remoto</option>
                </select>
              </Field>
            </div>
            <Field label="Nombre" required>
              <input className="input-field" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} placeholder="Ej: Sede Calle 100" />
            </Field>
            <Field label="Frente">
              <select className="input-field" value={form.frente} onChange={e => setForm(f => ({ ...f, frente: e.target.value }))}>
                {FRENTES.filter(f => f.activo).map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
              </select>
            </Field>
            <Field label="Dirección / referencia">
              <input className="input-field" value={form.direccion} onChange={e => setForm(f => ({ ...f, direccion: e.target.value }))} placeholder="Dirección o 'Remoto'" />
            </Field>
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" type="button" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button className="btn-primary" type="button" onClick={() => {
              if (!form.codigo.trim() || !form.nombre.trim()) { onToast('Completa código y nombre', '', 'warning'); return; }
              onToast('Sitio creado', form.nombre, 'success');
              setModalOpen(false);
            }}>Guardar</button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S09</div>
    </div>
  );
}

// ─── S10 Restricciones ────────────────────────────────────────────────────────
function S10Restricciones({ navigate, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({
    tipo: 'Horario',
    descripcion: '',
    aplica: 'Persona',
    personaOCargo: '',
    frente: 'Todos',
    turnosBloqueados: '',
  });
  return (
    <div style={{ padding: '24px 28px', maxWidth: 860 }}>
      <Breadcrumb items={[{ label: 'A. Parametrización' }, { label: 'S10 Restricciones' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Restricciones de asignación</div>
          <div className="page-subtitle">Límites por persona, cargo o turno (no confundir con el motor de reglas). HU19</div>
        </div>
        {canEdit
          ? <button className="btn-primary" type="button" onClick={() => setModalOpen(true)}>+ Restricción</button>
          : <DisabledBtn label="+ Restricción" reason="Sin permiso" />}
      </div>
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead><tr><th>Tipo</th><th>Descripción</th><th>Aplica a</th><th>Frente</th><th>Activo</th></tr></thead>
          <tbody>
            {[
              { tipo: 'Horario', desc: 'No asignar T1 a personas con restricción médica nocturna', aplica: 'Persona', frente: 'Todos' },
              { tipo: 'Rol', desc: 'Analistas no asignables a turno de madrugada', aplica: 'Cargo: Analista Sr.', frente: 'CC' },
              { tipo: 'Turno', desc: 'Bloquear T8 para personal en formación', aplica: 'Persona', frente: 'SITIO' },
            ].map((r, i) => (
              <tr key={i}>
                <td><Chip label={r.tipo} /></td>
                <td style={{ fontSize: 12 }}>{r.desc}</td>
                <td style={{ fontSize: 12 }}>{r.aplica}</td>
                <td><Chip label={r.frente} /></td>
                <td><span style={{ color: '#15803D' }}>●</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="helper-text" style={{ marginTop: 10 }}>
        Umbrales numéricos (máx. horas, domingos, cobertura) se parametrizan en el <strong>Motor de reglas (S13)</strong>. Aquí van exclusiones concretas persona/cargo/turno.
      </div>
      {modalOpen && (
        <Modal title="Nueva restricción de asignación" onClose={() => setModalOpen(false)}>
          <div className="field-group">
            <div className="field-row">
              <Field label="Tipo" required>
                <select className="input-field" value={form.tipo} onChange={e => setForm(f => ({ ...f, tipo: e.target.value }))}>
                  <option>Horario</option>
                  <option>Rol</option>
                  <option>Turno</option>
                  <option>Sitio</option>
                </select>
              </Field>
              <Field label="Aplica a">
                <select className="input-field" value={form.aplica} onChange={e => setForm(f => ({ ...f, aplica: e.target.value }))}>
                  <option>Persona</option>
                  <option>Cargo</option>
                  <option>Todos</option>
                </select>
              </Field>
            </div>
            <Field label="Persona / cargo" helper="Según 'Aplica a'">
              <input className="input-field" value={form.personaOCargo} onChange={e => setForm(f => ({ ...f, personaOCargo: e.target.value }))} placeholder="Ej: Pérez González o Analista Sr." />
            </Field>
            <Field label="Descripción" required>
              <textarea className="input-field" rows={2} value={form.descripcion} onChange={e => setForm(f => ({ ...f, descripcion: e.target.value }))} placeholder="Qué no se puede asignar y por qué" style={{ resize: 'vertical' }} />
            </Field>
            <div className="field-row">
              <Field label="Frente">
                <select className="input-field" value={form.frente} onChange={e => setForm(f => ({ ...f, frente: e.target.value }))}>
                  <option value="Todos">Todos</option>
                  {FRENTES.filter(f => f.activo).map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
                </select>
              </Field>
              <Field label="Turnos / códigos bloqueados">
                <input className="input-field" value={form.turnosBloqueados} onChange={e => setForm(f => ({ ...f, turnosBloqueados: e.target.value }))} placeholder="Ej: T1, T8" />
              </Field>
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" type="button" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button className="btn-primary" type="button" onClick={() => {
              if (!form.descripcion.trim()) { onToast('Indica la descripción', '', 'warning'); return; }
              onToast('Restricción guardada', form.tipo, 'success');
              setModalOpen(false);
            }}>Guardar</button>
          </div>
        </Modal>
      )}
      <div className="screen-id">S10</div>
    </div>
  );
}

// ─── S11 Festivos, cortes y tipos de hora ────────────────────────────────────
function S11Festivos({ navigate, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  return (
    <div style={{ padding: '24px 28px', maxWidth: 860 }}>
      <Breadcrumb items={[{ label: 'A. Parametrización' }, { label: 'S11 Festivos + Cortes + Tipos hora' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Festivos · Cortes · Tipos de hora</div>
          <div className="page-subtitle">Calendario de festivos, cortes de nómina y clasificación de horas. HU20–HU22</div>
        </div>
        {canEdit ? <button className="btn-primary" onClick={() => onToast('Guardado', '', 'success')}>Guardar</button> : <DisabledBtn label="Guardar" reason="Sin permiso" />}
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16 }}>
        <div className="card" style={{ padding: '16px 18px' }}>
          <div className="section-header">Festivos 2025</div>
          {['01-Ene Año Nuevo', '06-Ene Reyes', '24-Mar Palmas', '17-Abr Jueves Santo', '01-May Trabajo', '29-May Ascensión', '19-Jun Corpus', '30-Jun Sagrado', '20-Jul Independencia', '07-Ago Boyacá', '18-Ago Asunción', '13-Oct Raza', '03-Nov Todos Santos', '17-Nov Cartagena', '08-Dic Inmaculada', '25-Dic Navidad'].map(f => (
            <div key={f} style={{ fontSize: 11, padding: '3px 0', borderBottom: '1px solid var(--clr-border)', color: 'var(--clr-text-body)' }}>{f}</div>
          ))}
        </div>
        <div className="card" style={{ padding: '16px 18px' }}>
          <div className="section-header">Cortes de nómina</div>
          {['Corte 01 — 01/01 al 15/01', 'Corte 02 — 16/01 al 31/01', 'Corte 03 — 01/02 al 15/02', 'Corte 04 — 16/02 al 28/02', 'Corte 05 — 01/03 al 15/03', 'Corte 06 — 16/03 al 31/03'].map(c => (
            <div key={c} style={{ fontSize: 11, padding: '5px 0', borderBottom: '1px solid var(--clr-border)' }}>{c}</div>
          ))}
          <button className="btn-secondary" style={{ width: '100%', justifyContent: 'center', marginTop: 10 }} disabled={!canEdit}>+ Corte</button>
        </div>
        <div className="card" style={{ padding: '16px 18px' }}>
          <div className="section-header">Tipos de hora</div>
          {[
            { tipo: 'ORDI', desc: 'Hora ordinaria' },
            { tipo: 'NOCT', desc: 'Hora nocturna (+35%)' },
            { tipo: 'DOM', desc: 'Hora dominical (+75%)' },
            { tipo: 'FEST', desc: 'Hora festiva (+75%)' },
            { tipo: 'HEXA', desc: 'Hora extra diurna (+25%)' },
            { tipo: 'HEXN', desc: 'Hora extra nocturna (+75%)' },
          ].map(t => (
            <div key={t.tipo} style={{ display: 'flex', gap: 8, alignItems: 'center', padding: '4px 0', borderBottom: '1px solid var(--clr-border)' }}>
              <code style={{ fontSize: 10, background: '#F3F4F6', padding: '2px 5px', borderRadius: 3, minWidth: 42 }}>{t.tipo}</code>
              <span style={{ fontSize: 11 }}>{t.desc}</span>
            </div>
          ))}
          <div className="helper-text" style={{ marginTop: 8 }}>Solo horas — sin liquidación en pesos en este módulo.</div>
        </div>
      </div>
      <div className="screen-id">S11</div>
    </div>
  );
}

// ─── S12 Cobertura y compensatorios ──────────────────────────────────────────
function S12Cobertura({ navigate, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  return (
    <div style={{ padding: '24px 28px', maxWidth: 800 }}>
      <Breadcrumb items={[{ label: 'A. Parametrización' }, { label: 'S12 Cobertura + Compensatorios' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Cobertura mínima y compensatorios</div>
          <div className="page-subtitle">Umbrales de alerta parametrizables por franja y frente. HU23–HU24</div>
        </div>
        {canEdit ? <button className="btn-primary" onClick={() => onToast('Umbrales guardados', '', 'success')}>Guardar</button> : <DisabledBtn label="Guardar" reason="Sin permiso" />}
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Cobertura mínima por franja</div>
          {[
            { franja: '06:00–14:00', min: 3 }, { franja: '14:00–22:00', min: 3 },
            { franja: '22:00–06:00', min: 2 }, { franja: 'Festivos', min: 2 },
          ].map(f => (
            <div key={f.franja} style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 10 }}>
              <span style={{ flex: 1, fontSize: 12 }}>{f.franja}</span>
              <input className="input-field" type="number" defaultValue={f.min} style={{ width: 70 }} disabled={!canEdit} />
              <span style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>agentes mín.</span>
            </div>
          ))}
          <div className="helper-text">Umbral configurable por frente — el motor de reglas lee este valor (parámetro MIN_COBERTURA_FRANJA).</div>
        </div>
        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Compensatorios</div>
          <Field label="Días compensatorio por domingos trabajados">
            <input className="input-field" type="number" defaultValue={3} disabled={!canEdit} />
            <div className="helper-text" style={{ marginTop: 4 }}>Parámetro COMPENSATORIO_DIAS_TIPO en motor de reglas.</div>
          </Field>
          <Field label="Máx días consecutivos sin descanso">
            <input className="input-field" type="number" defaultValue={5} disabled={!canEdit} />
          </Field>
          <Field label="Horas máximas por periodo (h)">
            <input className="input-field" type="number" defaultValue={46} disabled={!canEdit} />
            <div className="helper-text" style={{ marginTop: 4 }}>Parámetro MAX_HORAS_PERIODO. Frente CC: 46h. Motor emite advertencia.</div>
          </Field>
          <button className="btn-secondary" style={{ width: '100%', justifyContent: 'center' }} onClick={() => navigate('S13')}>
            → Ver motor de reglas (S13)
          </button>
        </div>
      </div>
      <div className="screen-id">S12</div>
    </div>
  );
}

// ─── S13 Motor de reglas ──────────────────────────────────────────────────────
function S13Motor({ navigate, params, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  const [reglas, setReglas] = useState<ReglaCelda[]>(REGLAS_MOTOR);
  const [editIdx, setEditIdx] = useState<number | null>(null);
  const [paramVal, setParamVal] = useState('');

  function startEdit(i: number) { setEditIdx(i); setParamVal(reglas[i].parametro ?? ''); }
  function saveEdit(i: number) {
    setReglas(r => r.map((x, j) => j === i ? { ...x, parametro: paramVal } : x));
    setEditIdx(null);
    onToast('Parámetro actualizado', reglas[i].codigo, 'success');
  }
  function toggleActivo(i: number) {
    setReglas(r => r.map((x, j) => j === i ? { ...x, activo: !x.activo } : x));
    onToast('Regla actualizada', reglas[i].codigo, 'success');
  }

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1040 }}>
      <Breadcrumb items={[{ label: 'A. Parametrización' }, { label: 'S13 Motor de reglas' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Motor de reglas de validación <span className="new-badge" style={{ marginLeft: 8 }}>NUEVO — HU25</span></div>
          <div className="page-subtitle">Reglas parametrizables — sin hardcoding en UI. Los parámetros son los valores reales que usa la validación.</div>
        </div>
      </div>

      <div className="helper-text" style={{ marginBottom: 16 }}>
        Cada regla tiene un <strong>código</strong> único, <strong>alcance</strong> (empresa o frente específico), <strong>parámetro editable</strong> (valor que usa el motor), <strong>prioridad</strong> y <strong>severidad</strong>:
        <span className="chip severidad-info" style={{ margin: '0 6px' }}>Info</span> = informativa,
        <span className="chip severidad-advertencia" style={{ margin: '0 6px' }}>Advertencia</span> = muestra pero no bloquea,
        <span className="chip severidad-bloqueo" style={{ margin: '0 6px' }}>Bloqueo</span> = impide guardar.
      </div>

      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="table-grh" style={{ width: '100%' }}>
          <thead>
            <tr>
              <th>Código</th><th style={{ minWidth: 200 }}>Descripción</th><th>Alcance</th><th>Parámetro</th>
              <th>Prioridad</th><th>Severidad</th><th>Activo</th><th></th>
            </tr>
          </thead>
          <tbody>
            {reglas.map((r, i) => (
              <tr key={r.codigo} style={{ opacity: r.activo ? 1 : 0.5 }}>
                <td><code style={{ fontWeight: 700, fontSize: 11 }}>{r.codigo}</code></td>
                <td style={{ fontSize: 12 }}>{r.descripcion}</td>
                <td style={{ fontSize: 11 }}>{r.alcance === 'empresa' ? '🏢 Empresa' : `🏬 ${r.frenteId ?? r.alcance}`}</td>
                <td>
                  {editIdx === i ? (
                    <div style={{ display: 'flex', gap: 4 }}>
                      <input className="input-field" value={paramVal} onChange={e => setParamVal(e.target.value)} style={{ width: 80 }} autoFocus />
                      <button className="btn-primary" style={{ height: 28, fontSize: 11 }} onClick={() => saveEdit(i)}>OK</button>
                      <button className="btn-icon" onClick={() => setEditIdx(null)}>✕</button>
                    </div>
                  ) : (
                    <span style={{ fontFamily: 'monospace', fontSize: 12, background: '#F3F4F6', padding: '2px 8px', borderRadius: 4 }}>
                      {r.parametro ?? <em style={{ color: 'var(--clr-text-muted)' }}>n/a</em>}
                    </span>
                  )}
                </td>
                <td style={{ textAlign: 'center' }}>{r.prioridad}</td>
                <td>
                  <span className={`chip ${severidadClass(r.severidad)}`}>
                    {r.severidad === 'info' ? 'Info' : r.severidad === 'advertencia' ? 'Advertencia' : 'Bloqueo'}
                  </span>
                </td>
                <td>
                  <label className="toggle-switch">
                    <input type="checkbox" checked={r.activo} onChange={() => canEdit && toggleActivo(i)} disabled={!canEdit} />
                    <span className="toggle-track"></span>
                  </label>
                </td>
                <td>
                  {canEdit
                    ? <button className="btn-icon" title="Editar parámetro" onClick={() => startEdit(i)}>✏️</button>
                    : <DisabledBtn label="✏️" reason="Sin permiso" />}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="helper-text" style={{ marginTop: 10 }}>
        Los parámetros editados aplican en la próxima ejecución del motor. Cambios quedan en auditoría con usuario y fecha.
      </div>
      <div className="screen-id">S13</div>
    </div>
  );
}

// ─── S14 Configuración avanzada ────────────────────────────────────────────────
function S14Avanzada({ navigate, onToast, role }: Props) {
  const canEdit = puedeEditar(role);
  return (
    <div style={{ padding: '24px 28px', maxWidth: 700 }}>
      <Breadcrumb items={[{ label: 'A. Parametrización' }, { label: 'S14 Configuración avanzada' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Configuración avanzada</div>
          <div className="page-subtitle">Variables globales del módulo. HU26</div>
        </div>
        {canEdit ? <button className="btn-primary" onClick={() => onToast('Guardado', '', 'success')}>Guardar</button> : <DisabledBtn label="Guardar" reason="Sin permiso" />}
      </div>
      <div className="card" style={{ padding: '20px 22px' }}>
        <Field label="Nombre empresa"><input className="input-field" defaultValue="Data Center S.A." disabled={!canEdit} /></Field>
        <Field label="NIT"><input className="input-field" defaultValue="900.123.456-7" disabled={!canEdit} /></Field>
        <Field label="Zona horaria">
          <select className="input-field" disabled={!canEdit}><option>America/Bogota (UTC-5)</option></select>
        </Field>
        <Field label="Semana laboral inicia el">
          <select className="input-field" disabled={!canEdit}><option>Lunes</option><option>Domingo</option></select>
        </Field>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <input type="checkbox" defaultChecked disabled={!canEdit} id="notif-email" />
          <label htmlFor="notif-email" style={{ fontSize: 13 }}>Notificaciones por correo al publicar</label>
        </div>
      </div>
      <div className="screen-id">S14</div>
    </div>
  );
}

// ─── S15 Importación asistida desde Excel ─────────────────────────────────────
function S15Import({ navigate, onToast, role }: Props) {
  const [step, setStep] = useState(0);
  const canEdit = puedeEditar(role);

  const [descargando, setDescargando] = useState(false);

  const STEPS = ['Plantilla + subir', 'Descubrimiento', 'Confirmación', 'Resultado'];

  async function descargarPlantilla() {
    try {
      setDescargando(true);
      const fileName = await descargarPlantillaImportacionCatalogos();
      onToast('Plantilla Excel descargada', fileName, 'success');
    } catch (e) {
      console.error(e);
      onToast('No se pudo generar el Excel', 'Intenta de nuevo', 'error');
    } finally {
      setDescargando(false);
    }
  }

  return (
    <div style={{ padding: '24px 28px', maxWidth: 900 }}>
      <Breadcrumb items={[{ label: 'A. Parametrización' }, { label: 'S15 Importación Excel' }]} navigate={navigate} />
      <div className="page-header">
        <div>
          <div className="page-title">Importación asistida desde Excel <span className="new-badge" style={{ marginLeft: 8 }}>HU27</span></div>
          <div className="page-subtitle">Acelera el onboarding de catálogos (turnos, estados, sitios…) — el Excel no es el modelo de datos</div>
        </div>
      </div>

      <div className="card" style={{ padding: '14px 18px', marginBottom: 16, background: '#F0F7FA', border: '1px solid #B8D4E8' }}>
        <div style={{ fontWeight: 600, marginBottom: 6 }}>¿Qué se sube?</div>
        <div style={{ fontSize: 13, lineHeight: 1.5 }}>
          Un archivo de <strong>operación / catálogos</strong> (no la nómina, no el Excel histórico de mallas como fuente permanente).
          El sistema <strong>descubre</strong> valores nuevos (turnos, estados, sitios, campañas, modalidades) y te pide confirmarlos.
          Opcionalmente puede sugerir celdas de una malla en borrador; nunca reemplaza la BD con el archivo crudo.
        </div>
      </div>

      <div className="wizard-steps" style={{ marginBottom: 24 }}>
        {STEPS.map((s, i) => (
          <div key={s} className={`wizard-step ${i === step ? 'active' : i < step ? 'done' : ''}`} onClick={() => i < step && setStep(i)} style={{ cursor: i < step ? 'pointer' : 'default' }}>
            <div className="wizard-step-num">{i < step ? '✓' : i + 1}</div>
            <div className="wizard-step-label">{s}</div>
          </div>
        ))}
      </div>

      {step === 0 && (
        <div className="card" style={{ padding: '28px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 20 }}>
            <div style={{ padding: 16, border: '1px solid var(--clr-border)', borderRadius: 8, background: '#FAFBFC' }}>
              <div style={{ fontWeight: 600, marginBottom: 8 }}>1. Descarga la plantilla Excel</div>
              <div style={{ fontSize: 12, color: 'var(--clr-text-muted)', marginBottom: 12, lineHeight: 1.45 }}>
                Archivo <strong>.xlsx</strong> con 3 hojas: Instrucciones, Datos (columnas separadas + ejemplos) y Leyenda. Ábrelo en Excel o Google Sheets.
              </div>
              <button className="btn-secondary" type="button" disabled={descargando} onClick={() => void descargarPlantilla()}>
                {descargando ? 'Generando…' : '⬇ Descargar plantilla (.xlsx)'}
              </button>
            </div>
            <div style={{ padding: 16, border: '1px solid var(--clr-border)', borderRadius: 8, background: '#FAFBFC' }}>
              <div style={{ fontWeight: 600, marginBottom: 8 }}>Qué incluye la plantilla</div>
              <ul style={{ fontSize: 12, margin: 0, paddingLeft: 18, lineHeight: 1.55, color: 'var(--clr-text-body)' }}>
                <li>Encabezados en español, una columna por campo</li>
                <li>Fila guía (qué va en cada columna)</li>
                <li>Ejemplos de turno, estado y sitio</li>
                <li>Colores por grupo (frente / turno / estado / sitio)</li>
              </ul>
            </div>
          </div>

          <div className="import-dropzone">
            <div style={{ fontSize: 40, marginBottom: 12 }}>📂</div>
            <div style={{ fontSize: 15, fontWeight: 500, marginBottom: 6 }}>2. Sube el archivo ya diligenciado</div>
            <div style={{ fontSize: 12, color: 'var(--clr-text-muted)', marginBottom: 20 }}>.xlsx / .xls / .csv — máx 10 MB</div>
            <button className="btn-secondary" type="button" onClick={() => canEdit ? setStep(1) : onToast('Sin permiso', '', 'error')}>
              Seleccionar archivo…
            </button>
          </div>
          <div className="helper-text" style={{ marginTop: 16 }}>
            Tip demo: usa <strong>Continuar con demo</strong> para ver descubrimiento sin archivo real.
          </div>
          <div style={{ textAlign: 'right', marginTop: 16 }}>
            <button className="btn-primary" type="button" onClick={() => setStep(1)}>Continuar con demo →</button>
          </div>
        </div>
      )}

      {step === 1 && (
        <div className="card" style={{ padding: '24px' }}>
          <div className="section-header">Descubrimiento automático</div>
          <div className="helper-text" style={{ marginBottom: 16 }}>
            El archivo contiene valores que aún no existen en los catálogos de la empresa. Marca cuáles aceptar (HU27).
          </div>
          {[
            { tipo: 'Frente', valor: 'DATACENTER-NOC', accion: 'Crear nuevo frente', icon: '🏬' },
            { tipo: 'Turno', valor: 'T12 (07:00–19:00 / 12h)', accion: 'Crear nueva plantilla de turno', icon: '⏰' },
            { tipo: 'Modalidad', valor: 'HYB-ESPECIAL', accion: 'Crear modalidad "Híbrido especial"', icon: '⚡' },
            { tipo: 'Estado', valor: 'FRZ (Freezing)', accion: 'Crear estado de celda', icon: '🔵' },
          ].map(d => (
            <div key={d.valor} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 14px', borderRadius: 8, border: '1px solid var(--clr-accent)', background: '#F0FCFD', marginBottom: 8 }}>
              <span style={{ fontSize: 22 }}>{d.icon}</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 12, fontWeight: 600 }}>{d.tipo}: <code>{d.valor}</code></div>
                <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>Acción sugerida: {d.accion}</div>
              </div>
              <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12 }}>
                <input type="checkbox" defaultChecked /> Aceptar
              </label>
            </div>
          ))}
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 16 }}>
            <button className="btn-secondary" type="button" onClick={() => setStep(0)}>← Atrás</button>
            <button className="btn-primary" type="button" onClick={() => setStep(2)}>Confirmar descubrimiento →</button>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="card" style={{ padding: '24px' }}>
          <div className="section-header">Confirmación antes de aplicar</div>
          <div className="helper-text" style={{ marginBottom: 16 }}>
            Se crearán <strong>4 ítems de catálogo</strong>. Las celdas sugeridas (si las hay) irán a una malla en <strong>borrador</strong> — no publican solas.
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12, marginBottom: 16 }}>
            {[
              { label: 'Catálogos a crear', value: '4', color: '#15803D' },
              { label: 'Advertencias', value: '2', color: '#92400E' },
              { label: 'Filas omitidas', value: '1', color: '#DC2626' },
            ].map(s => (
              <div key={s.label} className="card" style={{ padding: '14px 18px', textAlign: 'center' }}>
                <div style={{ fontSize: 28, fontWeight: 700, color: s.color }}>{s.value}</div>
                <div style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>{s.label}</div>
              </div>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
            <button className="btn-secondary" type="button" onClick={() => setStep(1)}>← Atrás</button>
            <button className="btn-primary" type="button" onClick={() => { setStep(3); onToast('Importación completada', '4 catálogos creados', 'success'); }}>Aplicar importación ✓</button>
          </div>
        </div>
      )}

      {step === 3 && (
        <div className="card" style={{ padding: '32px', textAlign: 'center' }}>
          <div style={{ fontSize: 50, marginBottom: 12 }}>✅</div>
          <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 8 }}>Importación completada</div>
          <div style={{ fontSize: 13, color: 'var(--clr-text-muted)', marginBottom: 24 }}>
            Catálogos actualizados. Revisa plantillas de turno (S03) y estados (S05). El Excel no queda como fuente operativa.
          </div>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'center' }}>
            <button className="btn-secondary" type="button" onClick={() => navigate('S03')}>Ver plantillas →</button>
            <button className="btn-primary" type="button" onClick={() => setStep(0)}>Nueva importación</button>
          </div>
        </div>
      )}
      <div className="screen-id">S15</div>
    </div>
  );
}

// ─── Router ───────────────────────────────────────────────────────────────────
export default function SA(props: Props) {
  const { screen } = props;
  if (screen === 'S0D') return <S0DDashboard {...props} />;
  if (screen === 'S0P') return <S0PGuia {...props} />;
  if (screen === 'S01') return <S01Frentes {...props} />;
  if (screen === 'S02') return <S02ConfigFrente {...props} />;
  if (screen === 'S03') return <S03Plantillas {...props} />;
  if (screen === 'S04') return <S04Horario {...props} />;
  if (screen === 'S05') return <S05Estados {...props} />;
  if (screen === 'S06') return <S06Campanhas {...props} />;
  if (screen === 'S07') return <S07Territorio {...props} />;
  if (screen === 'S08') return <S08Modalidades {...props} />;
  if (screen === 'S09') return <S09Sitios {...props} />;
  if (screen === 'S10') return <S10Restricciones {...props} />;
  if (screen === 'S11') return <S11Festivos {...props} />;
  if (screen === 'S12') return <S12Cobertura {...props} />;
  if (screen === 'S13') return <S13Motor {...props} />;
  if (screen === 'S14') return <S14Avanzada {...props} />;
  if (screen === 'S15') return <S15Import {...props} />;
  return <S0DDashboard {...props} />;
}
