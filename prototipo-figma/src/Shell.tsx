import { useEffect } from 'react';
import {
  ROLES,
  SUBMODULOS_MALLA,
  submodulosVisibles,
  submoduloDePantalla,
  puedeVerPantalla,
  permisosSubmodulo,
  type Rol,
  type SubmoduloId,
} from './data';

export { SUBMODULOS_MALLA as NAV_GROUPS };

// ── Shell ──────────────────────────────────────────────────────────────────────

interface Props {
  currentScreen: string;
  navigate: (screen: string, params?: any) => void;
  role: Rol;
  onRoleChange: (r: Rol) => void;
  children: React.ReactNode;
}

export default function Shell({ currentScreen, navigate, role, onRoleChange, children }: Props) {
  const roleMeta = ROLES.find(r => r.id === role);
  const visibles = submodulosVisibles(role);
  const activeSubId = submoduloDePantalla(currentScreen);
  const activeSub = SUBMODULOS_MALLA.find(s => s.id === activeSubId) ?? null;
  const inModule = currentScreen !== 'home';
  const showSectionTabs = !!activeSub && currentScreen !== 'S00';

  // Si el rol no tiene LEER en la pantalla actual → primer submódulo permitido o hub
  useEffect(() => {
    if (!puedeVerPantalla(role, currentScreen)) {
      const first = submodulosVisibles(role)[0];
      navigate(first ? first.entryScreen : 'S00');
    }
  }, [role, currentScreen, navigate]);

  function goSubmodulo(id: SubmoduloId) {
    const sm = SUBMODULOS_MALLA.find(s => s.id === id);
    if (sm) navigate(sm.entryScreen);
  }

  const permsLabel = activeSub
    ? permisosSubmodulo(role, activeSub.id).join(' · ') || 'Sin permisos'
    : '';

  return (
    <div className="app-shell sidebar-expanded">
      <aside className="sidebar expanded" aria-label="Menú del módulo Malla de turnos">
        <div className="logo-section">
          <div className="sidebar-logo-mark" title="GRH">GRH</div>
        </div>

        <div className="sidebar-module-label">Malla de turnos</div>

        <div className="content-section">
          <div
            className={`menu-item ${currentScreen === 'S00' ? 'selected' : ''}`}
            onClick={() => navigate('S00')}
            title="Hub del módulo"
          >
            <button type="button" className="menu-button" aria-label="Hub">
              <span className="icon">⌂</span>
            </button>
            <span className="item-text">Inicio módulo</span>
          </div>

          {visibles.map(sm => {
            const selected = activeSubId === sm.id;
            return (
              <div
                key={sm.id}
                className={`menu-item ${selected ? 'selected' : ''}`}
                onClick={() => goSubmodulo(sm.id)}
                title={`${sm.label} — menú con LEER`}
              >
                <button type="button" className="menu-button" aria-label={sm.label}>
                  <span className="icon">{sm.icon}</span>
                </button>
                <span className="item-text">{sm.label}</span>
              </div>
            );
          })}

          {visibles.length === 0 && (
            <div className="sidebar-empty-hint">
              Este rol no tiene LEER en ningún submódulo de Malla.
            </div>
          )}
        </div>

        <div className="sidebar-rbac-hint">
          <div className="sidebar-rbac-title">Menú = LEER</div>
          <div className="sidebar-rbac-desc">
            Solo aparecen submódulos con permiso LEER (como en GRH real).
          </div>
        </div>
      </aside>

      <div className="main-area">
        <header className="topbar expanded">
          <div className="topbar-left">
            <div className="company-module">
              <span className="company-module-icon">📅</span>
              <span>Malla de turnos</span>
            </div>
            <div className="topbar-sep" />
            <div className="role-selector">
              <label htmlFor="role-select">Ver como:</label>
              <select
                id="role-select"
                value={role}
                onChange={e => onRoleChange(e.target.value as Rol)}
                aria-label="Cambiar rol de vista"
              >
                {ROLES.map(r => (
                  <option key={r.id} value={r.id}>{r.label}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="topbar-right">
            <div className="topbar-company">
              Empresa activa: <strong>Data Center S.A.</strong>
            </div>
            <div className="topbar-sep" />
            <button className="btn-icon bell-btn" aria-label="Notificaciones" type="button">
              🔔
              <span className="bell-dot" />
            </button>
            <div className="profile-block">
              <div className="profile-text">
                <div className="username">{roleMeta?.label}</div>
                <div className="position">Data Center S.A.</div>
              </div>
              <div className="topbar-avatar" title={roleMeta?.label}>
                {role === 'coordinadora_cc' ? 'NC' : role === 'coordinador' ? 'AR' : role === 'analista_mesa' ? 'AM' : role === 'operador' ? 'OP' : 'TH'}
              </div>
            </div>
          </div>
        </header>

        {/* Navegación interna del submódulo (NO es menú RBAC) */}
        {showSectionTabs && activeSub && (
          <nav className="section-tabs" aria-label={`Pantallas internas de ${activeSub.label}`}>
            <div className="section-tabs-meta">
              <span className="section-tabs-title">{activeSub.label}</span>
              <span className="section-tabs-perms" title="Permisos CRUD del submódulo (demo)">
                {permsLabel}
              </span>
            </div>
            <div className="section-tabs-scroll">
              {activeSub.pages.map(p => (
                <button
                  key={p.screen}
                  type="button"
                  className={`section-tab ${currentScreen === p.screen ? 'active' : ''}`}
                  onClick={() => navigate(p.screen)}
                >
                  {p.label}
                  {p.isNew && <span className="new-badge">NUEVO</span>}
                  <span className="section-tab-sid">{p.screen}</span>
                </button>
              ))}
            </div>
            <div className="screen-badge">{currentScreen}</div>
          </nav>
        )}

        {!showSectionTabs && inModule && currentScreen === 'S00' && (
          <div className="hub-banner">
            Elige un submódulo del menú lateral. Solo ves los que tu rol tiene con <strong>LEER</strong>.
            Las pantallas internas (S01, S16…) no son entradas de menú con permiso propio.
          </div>
        )}

        <div className="main-content">
          {children}
        </div>
      </div>
    </div>
  );
}

// ── Shared UI helpers ─────────────────────────────────────────────────────────

interface BreadcrumbProps {
  items: { label: string; screen?: string; onClick?: () => void }[];
  navigate?: (s: string) => void;
}
export function Breadcrumb({ items, navigate }: BreadcrumbProps) {
  return (
    <div className="breadcrumb">
      <span className="breadcrumb-link" onClick={() => navigate?.('S00')} style={{ cursor: 'pointer' }}>Malla de turnos</span>
      {items.map((item, i) => (
        <span key={i} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span className="breadcrumb-sep">/</span>
          {i < items.length - 1 && (item.screen || item.onClick) && navigate
            ? <span className="breadcrumb-link" onClick={() => item.onClick ? item.onClick() : navigate(item.screen!)}>{item.label}</span>
            : <span className={i === items.length - 1 ? 'breadcrumb-current' : ''}>{item.label}</span>}
        </span>
      ))}
    </div>
  );
}

interface ModalProps {
  title: string;
  onClose: () => void;
  children: React.ReactNode;
  footer?: React.ReactNode;
  size?: 'sm' | 'md';
}
export function Modal({ title, onClose, children, footer, size = 'md' }: ModalProps) {
  return (
    <div className="modal-backdrop" onClick={e => { if (e.target === e.currentTarget) onClose(); }}>
      <div className={`modal-dialog ${size === 'sm' ? 'modal-dialog-sm' : ''}`}>
        <div className="modal-header">
          <div className="modal-title">{title}</div>
          <div className="modal-divider" />
        </div>
        <div className="modal-body">{children}</div>
        {footer && <div className="modal-footer">{footer}</div>}
      </div>
    </div>
  );
}

interface FieldProps { label: string; children: React.ReactNode; required?: boolean; helper?: string; }
export function Field({ label, children, required, helper }: FieldProps) {
  return (
    <div>
      <label className="input-label">{label}{required && <span style={{ color: 'var(--clr-error)', marginLeft: 2 }}>*</span>}</label>
      {children}
      {helper && <div style={{ fontSize: 11, color: 'var(--clr-text-muted)', marginTop: 4 }}>{helper}</div>}
    </div>
  );
}

export function Chip({ label, colorClass }: { label: string; colorClass?: string }) {
  return <span className={`chip ${colorClass || ''}`}>{label}</span>;
}

export function EstadoChip({ estado }: { estado: string }) {
  const map: Record<string, { label: string; cls: string }> = {
    borrador: { label: 'Borrador', cls: 'estado-borrador' },
    revision: { label: 'En revisión', cls: 'estado-revision' },
    publicada: { label: 'Publicada', cls: 'estado-publicada' },
    rechazada: { label: 'Rechazada', cls: 'estado-rechazada' },
  };
  const { label, cls } = map[estado] || { label: estado, cls: '' };
  return <span className={`chip ${cls}`}>{label}</span>;
}

export function EmptyState({ icon = '📋', title, desc, action }: { icon?: string; title: string; desc?: string; action?: React.ReactNode }) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon">{icon}</div>
      <div className="empty-state-title">{title}</div>
      {desc && <div className="empty-state-desc">{desc}</div>}
      {action}
    </div>
  );
}

export function ConflictoItem({ tipo, mensaje, codigoRegla, conflicto }: { tipo?: 'advertencia' | 'bloqueo'; mensaje?: string; codigoRegla?: string; conflicto?: { tipo: 'advertencia' | 'bloqueo'; mensaje: string } }) {
  const t = tipo ?? conflicto?.tipo ?? 'advertencia';
  const m = mensaje ?? conflicto?.mensaje ?? '';
  return (
    <div className={`conflict-item ${t === 'bloqueo' ? 'error' : 'warning'}`}>
      <span className={`conflict-badge ${t === 'bloqueo' ? 'error' : 'warning'}`}>{t === 'bloqueo' ? 'BLOQUEO' : 'ADVERTENCIA'}</span>
      <div style={{ flex: 1 }}>
        <div style={{ color: 'var(--clr-text-strong)', lineHeight: 1.5, fontSize: 12 }}>{m}</div>
        {codigoRegla && <div style={{ fontSize: 10, color: 'var(--clr-text-muted)', marginTop: 2, fontFamily: 'monospace' }}>Regla: {codigoRegla}</div>}
      </div>
    </div>
  );
}

export function DisabledBtn({ children, tooltip, label, reason, className = 'btn-secondary' }: { children?: React.ReactNode; tooltip?: string; label?: string; reason?: string; className?: string }) {
  const tip = tooltip ?? reason ?? '';
  return (
    <button
      className={className}
      disabled
      title={tip}
      aria-label={tip}
      style={{ opacity: 0.45, cursor: 'not-allowed' }}
    >
      {children ?? label}
    </button>
  );
}
