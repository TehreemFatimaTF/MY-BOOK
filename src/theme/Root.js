import ChatWidget from '../components/Chat/ChatbotWidget';
import { TranslationProvider } from '../contexts/TranslationContext';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import LoginModal from '../components/Auth/LoginModal';
import SignupModal from '../components/Auth/SignupModal';
import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

// ================= Auth Modals =================
const AuthModals = () => {
  return (
    <>
      <LoginModal
        onSwitchToSignup={() => {
          window.dispatchEvent(new CustomEvent('showSignupModal'));
        }}
      />
      <SignupModal
        onSwitchToLogin={() => {
          window.dispatchEvent(new CustomEvent('showLoginModal'));
        }}
      />
    </>
  );
};

// ================= Auth Guard =================
const AuthGuard = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        background: 'radial-gradient(circle at top, #1a1a1a, #000)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        color: '#FFD700',
        fontSize: '22px',
        fontWeight: '600',
        letterSpacing: '1px'
      }}>
        Loading Intelligence…
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #000000, #111111)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        perspective: '1200px'
      }}>
        <div style={{
          background: 'linear-gradient(145deg, #0d0d0d, #000)',
          padding: '60px 70px',
          borderRadius: '20px',
          boxShadow: `
            0 40px 80px rgba(0,0,0,0.9),
            inset 0 0 0 1px rgba(255,215,0,0.15)
          `,
          transform: 'rotateX(6deg)',
          textAlign: 'center',
          animation: 'float 6s ease-in-out infinite'
        }}>
          <h1 style={{
            color: '#FFD700',
            fontSize: '34px',
            marginBottom: '14px',
            textShadow: '0 4px 20px rgba(255,215,0,0.35)'
          }}>
            Physical AI & Humanoid Robotics
          </h1>

          <p style={{
            color: '#cccccc',
            fontSize: '16px',
            marginBottom: '40px',
            letterSpacing: '0.5px'
          }}>
            Secure access required to continue
          </p>

          <div style={{
            display: 'flex',
            gap: '22px',
            justifyContent: 'center'
          }}>
            <button
              onClick={() =>
                window.dispatchEvent(new CustomEvent('showLoginModal'))
              }
              style={{
                background: 'linear-gradient(145deg, #FFD700, #ffbf00)',
                color: '#000',
                border: 'none',
                padding: '14px 32px',
                borderRadius: '10px',
                fontSize: '16px',
                fontWeight: '700',
                cursor: 'pointer',
                boxShadow: `
                  0 12px 30px rgba(255,215,0,0.35),
                  inset 0 -2px 0 rgba(0,0,0,0.25)
                `,
                transition: 'all 0.25s ease',
              }}
              onMouseEnter={e => e.target.style.transform = 'translateY(-4px) scale(1.03)'}
              onMouseLeave={e => e.target.style.transform = 'none'}
            >
              Login
            </button>

            <button
              onClick={() =>
                window.dispatchEvent(new CustomEvent('showSignupModal'))
              }
              style={{
                background: 'transparent',
                color: '#FFD700',
                border: '2px solid #FFD700',
                padding: '14px 32px',
                borderRadius: '10px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer',
                boxShadow: '0 10px 25px rgba(255,215,0,0.15)',
                transition: 'all 0.25s ease',
              }}
              onMouseEnter={e => {
                e.target.style.background = '#FFD700';
                e.target.style.color = '#000';
                e.target.style.transform = 'translateY(-4px)';
              }}
              onMouseLeave={e => {
                e.target.style.background = 'transparent';
                e.target.style.color = '#FFD700';
                e.target.style.transform = 'none';
              }}
            >
              Sign Up
            </button>
          </div>
        </div>
      </div>
    );
  }

  return children;
};

// ================= GLOBAL LOGOUT HANDLER =================
const GlobalLogoutHandler = () => {
  const { logout } = useAuth();

  React.useEffect(() => {
    window.handleLogoutClick = async () => {
      await logout();
      window.location.href = '/';
    };
  }, [logout]);

  return null;
};

// ================= ROOT =================
export default function Root({ children }) {
  return (
    <AuthProvider>
      <TranslationProvider>
        <BrowserOnly>
          {() => (
            <>
              <GlobalLogoutHandler />
              <AuthGuard>{children}</AuthGuard>
            </>
          )}
        </BrowserOnly>

        <ChatWidget />
        <AuthModals />
      </TranslationProvider>
    </AuthProvider>
  );
}
