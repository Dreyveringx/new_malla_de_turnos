import { useState, useCallback } from 'react';
import Shell from './Shell';
import type { Rol } from './data';
import { EMPRESA_SCOPE, submoduloDePantalla, SUBMODULOS_MALLA } from './data';
import S00Hub from './screens/S00Hub';
import SA from './screens/SA';
import SB from './screens/SB';
import SC from './screens/SC';
import SD from './screens/SD';
import SE from './screens/SE';
import SF from './screens/SF';

// ─── Toast ────────────────────────────────────────────────────────────────────

interface Toast { id: number; msg: string; desc: string; type: 'success' | 'error' | 'warning'; }
let toastSeq = 0;

// ─── App ──────────────────────────────────────────────────────────────────────

export default function App() {
  const [screen, setScreen] = useState('S00');
  const [params, setParams] = useState<any>(null);
  const [role, setRole] = useState<Rol>('coordinadora_cc');
  const [toasts, setToasts] = useState<Toast[]>([]);
  /** null = dashboard; EMPRESA_SCOPE = catálogos empresa; id de frente = contexto operativo */
  const [frenteCtx, setFrenteCtx] = useState<string | null>(null);

  const navigate = useCallback((s: string, p?: any) => {
    setScreen(s);
    const nextParams = p === undefined ? null : p;
    setParams(nextParams);
    if (s === 'S0D' || s === 'S00') {
      setFrenteCtx(null);
    } else if (nextParams?.frenteId) {
      setFrenteCtx(nextParams.frenteId);
    }
  }, []);

  const enterEmpresa = useCallback(() => {
    setFrenteCtx(EMPRESA_SCOPE);
    navigate('S0P');
  }, [navigate]);

  const enterFrente = useCallback((frenteId: string) => {
    setFrenteCtx(frenteId);
    navigate('S02', { frenteId });
  }, [navigate]);

  const clearFrenteCtx = useCallback(() => {
    setFrenteCtx(null);
  }, []);

  const goSubmodulo = useCallback((entryScreen: string) => {
    setFrenteCtx(null);
    setScreen(entryScreen);
    setParams(null);
  }, []);

  const showToast = useCallback((msg: string, desc: string, type: Toast['type']) => {
    const id = ++toastSeq;
    setToasts(t => [...t, { id, msg, desc, type }]);
    setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), 4500);
  }, []);

  const screenProps = {
    screen,
    navigate,
    params,
    onToast: showToast,
    role,
    frenteCtx,
    enterFrente,
    enterEmpresa,
    clearFrenteCtx,
  };
  const num = parseInt(screen.replace('S', ''), 10);
  const isParam = screen === 'S0P' || screen === 'S0D' || (num >= 1 && num <= 15);

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <Shell
        currentScreen={screen}
        navigate={navigate}
        role={role}
        onRoleChange={setRole}
        frenteCtx={frenteCtx}
        onClearFrenteCtx={() => {
          clearFrenteCtx();
          const sm = submoduloDePantalla(screen);
          const entry = SUBMODULOS_MALLA.find(s => s.id === sm)?.entryScreen ?? 'S0D';
          navigate(entry);
        }}
        onGoSubmodulo={goSubmodulo}
      >
        {screen === 'S00' && <S00Hub navigate={navigate} role={role} />}
        {screen === 'home' && <HomeRedirect navigate={navigate} />}
        {isParam && <SA {...screenProps} />}
        {num >= 16 && num <= 24 && <SB {...screenProps} />}
        {num >= 25 && num <= 29 && <SC {...screenProps} />}
        {num >= 30 && num <= 32 && <SD {...screenProps} />}
        {num >= 33 && num <= 37 && <SE {...screenProps} />}
        {num >= 38 && num <= 43 && <SF {...screenProps} />}
      </Shell>

      <div className="toast-container" role="region" aria-live="polite" aria-label="Notificaciones">
        {toasts.map(t => (
          <div key={t.id} className={`toast toast-${t.type}`} role="alert">
            <span className="toast-icon">{t.type === 'success' ? '✅' : t.type === 'error' ? '❌' : '⚠️'}</span>
            <div>
              <div className="toast-title">{t.msg}</div>
              {t.desc && <div className="toast-desc">{t.desc}</div>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function HomeRedirect({ navigate }: { navigate: (s: string) => void }) {
  return (
    <div style={{ padding: '40px 28px', textAlign: 'center' }}>
      <div style={{ fontSize: 40, marginBottom: 16 }}>🏢</div>
      <div style={{ fontSize: 18, fontWeight: 600, color: 'var(--clr-primary)', marginBottom: 8 }}>GRH — Gestión de Recursos Humanos</div>
      <div style={{ fontSize: 14, color: 'var(--clr-text-muted)', marginBottom: 24 }}>Este prototipo muestra el módulo <strong>Malla de turnos</strong>. Los demás módulos GRH están fuera del alcance de esta demo.</div>
      <button className="btn-primary" onClick={() => navigate('S00')}>Ir a Malla de turnos →</button>
    </div>
  );
}
