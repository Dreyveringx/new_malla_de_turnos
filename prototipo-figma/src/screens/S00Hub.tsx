import { Breadcrumb, EstadoChip } from '../Shell';
import {
  MALLAS,
  FRENTES,
  SUBMODULOS_MALLA,
  puedeLeerSubmodulo,
  permisosSubmodulo,
  type Rol,
} from '../data';

interface Props {
  navigate: (screen: string, params?: any) => void;
  role: Rol;
}

const COLORS: Record<string, { bg: string; color: string }> = {
  parametrizacion: { bg: '#EFF4FB', color: '#4A628A' },
  construccion: { bg: '#EFF6FF', color: '#1E5EA8' },
  'consulta-operativa': { bg: '#F0FFF4', color: '#1A6641' },
  'mi-programacion': { bg: '#FFF8E1', color: '#92650A' },
  reportes: { bg: '#F5F0FF', color: '#4A148C' },
};

export default function S00Hub({ navigate, role }: Props) {
  const visibles = SUBMODULOS_MALLA.filter(sm => puedeLeerSubmodulo(role, sm.id));
  const anyIntercambioOn = FRENTES.some(f => f.intercambioActivo);

  return (
    <div style={{ padding: '24px 28px', maxWidth: 1200 }}>
      <Breadcrumb items={[{ label: 'Inicio del módulo' }]} navigate={navigate} />
      <div className="page-header" style={{ marginTop: 4 }}>
        <div>
          <div className="page-title">Malla de turnos</div>
          <div className="page-subtitle">
            Submódulos del menú GRH (RBAC por sección) — Data Center S.A.
          </div>
        </div>
      </div>

      <div className="helper-text" style={{ marginBottom: 20 }}>
        En GRH el menú lateral muestra solo estos <strong>submódulos</strong> si el rol tiene <strong>LEER</strong>.
        Las pantallas S01–S42 viven <strong>dentro</strong> de cada submódulo (tabs internas), no como permisos aparte.
        Intercambio (EP-09) no es un 6.º ítem de menú: está dentro de Construcción / Mi programación.
        {!anyIntercambioOn && <> · Hoy todos los frentes tienen intercambio <strong>OFF</strong>.</>}
      </div>

      {visibles.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">🔒</div>
          <div className="empty-state-title">Sin secciones visibles</div>
          <div className="empty-state-desc">Este rol no tiene permiso LEER en ningún submódulo de Malla.</div>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16, marginBottom: 24 }}>
          {visibles.map(sm => {
            const c = COLORS[sm.id] ?? { bg: '#EFF4FB', color: '#4A628A' };
            const perms = permisosSubmodulo(role, sm.id);
            return (
              <div
                key={sm.id}
                className="hub-block"
                style={{ background: c.bg, borderColor: `${c.color}30` }}
                onClick={() => navigate(sm.entryScreen)}
                role="button"
                tabIndex={0}
                onKeyDown={e => e.key === 'Enter' && navigate(sm.entryScreen)}
                aria-label={`Ir a ${sm.label}`}
              >
                <div className="hub-block-letter">{sm.icon}</div>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: 10 }}>
                  <div className="hub-block-icon" style={{ background: `${c.color}18` }}>{sm.icon}</div>
                  <div style={{ flex: 1 }}>
                    <div className="hub-block-title" style={{ color: c.color }}>{sm.label}</div>
                    <div style={{ fontSize: 10, color: 'var(--clr-text-muted)', marginTop: 2, fontFamily: 'monospace' }}>
                      {sm.route}
                    </div>
                  </div>
                </div>
                <div className="hub-block-desc">{sm.desc}</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 8 }}>
                  {perms.map(p => (
                    <span key={p} className="chip" style={{ background: '#fff', border: `1px solid ${c.color}40`, color: c.color, fontSize: 10 }}>
                      {p}
                    </span>
                  ))}
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 3, marginTop: 10 }}>
                  {sm.pages.slice(0, 4).map(s => (
                    <div key={s.screen} style={{ fontSize: 11, color: c.color, display: 'flex', alignItems: 'center', gap: 5 }}>
                      <span style={{ opacity: 0.5 }}>›</span> {s.label}
                    </div>
                  ))}
                  {sm.pages.length > 4 && (
                    <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>+{sm.pages.length - 4} pantallas internas…</div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header">Leyenda — estados de malla</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 16 }}>
            {[
              { cls: 'estado-borrador', label: 'Borrador', desc: 'En construcción. El responsable asignado edita.' },
              { cls: 'estado-revision', label: 'En revisión', desc: 'Enviada al coordinador para aprobación.' },
              { cls: 'estado-publicada', label: 'Publicada', desc: 'Visible para el grupo.' },
              { cls: 'estado-rechazada', label: 'Rechazada', desc: 'Devuelta con motivo.' },
            ].map(e => (
              <div key={e.label} style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <span className={`chip ${e.cls}`} style={{ minWidth: 96, justifyContent: 'center' }}>{e.label}</span>
                <span style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>{e.desc}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card" style={{ padding: '18px 20px' }}>
          <div className="section-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            Mallas recientes
            {puedeLeerSubmodulo(role, 'construccion') && (
              <button className="btn-secondary" style={{ fontSize: 11, height: 28, borderRadius: 6 }} onClick={() => navigate('S16')}>Ver todas</button>
            )}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 16 }}>
            {MALLAS.slice(0, 4).map(m => (
              <div
                key={m.id}
                style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 12px', borderRadius: 8, border: '1px solid var(--clr-border)', cursor: puedeLeerSubmodulo(role, 'construccion') ? 'pointer' : 'default' }}
                onClick={() => puedeLeerSubmodulo(role, 'construccion') && navigate('S18', { mallaId: m.id })}
              >
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 13, fontWeight: 500, color: 'var(--clr-text-strong)' }}>{m.nombre}</div>
                  <div style={{ fontSize: 11, color: 'var(--clr-text-muted)' }}>{m.frenteNombre} · {m.periodo}</div>
                </div>
                <EstadoChip estado={m.estado} />
              </div>
            ))}
          </div>
          <div className="section-header">Frentes activos ({FRENTES.filter(f => f.activo).length})</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {FRENTES.filter(f => f.activo).map(f => (
              <div key={f.id} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12 }}>
                <span style={{ fontWeight: 500, flex: 1, color: 'var(--clr-text-strong)' }}>{f.nombre}</span>
                <span className="badge-mode">{f.modo === 'automatico' ? 'Auto' : f.modo === 'asistido' ? 'Asistido' : 'Manual'}</span>
                {f.intercambioActivo && <span className="chip" style={{ background: '#F0FDF4', color: '#166534', border: '1px solid #A7F3D0', fontSize: 10 }}>🔄 ON</span>}
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="screen-id">S00</div>
    </div>
  );
}
