import React, { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import LoginModal from './LoginModal';
import SignupModal from './SignupModal';
import { BrowserOnly } from '@docusaurus/router';

const AuthGuard = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const [showRobot, setShowRobot] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setShowRobot(prev => !prev);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)',
        color: '#ffd700',
        fontSize: '1.5rem',
        flexDirection: 'column',
        gap: '20px'
      }}>
        <div style={{
          fontSize: '3rem',
          animation: 'bounce 1s infinite alternate',
          filter: 'drop-shadow(0 0 10px rgba(255, 215, 0, 0.5))'
        }}>
          🤖
        </div>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <span>Authenticating</span>
          <div style={{ display: 'flex', gap: '5px' }}>
            {[0, 1, 2].map(i => (
              <div
                key={i}
                style={{
                  width: '8px',
                  height: '8px',
                  background: '#ffd700',
                  borderRadius: '50%',
                  animation: `pulse 1.5s infinite ${i * 0.2}s`
                }}
              />
            ))}
          </div>
        </div>
        <style jsx>{`
          @keyframes bounce {
            from { transform: translateY(0px); }
            to { transform: translateY(-20px); }
          }
          @keyframes pulse {
            0%, 100% { opacity: 0.3; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1.2); }
          }
        `}</style>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <BrowserOnly>
        {() => (
          <div style={{
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            padding: '20px',
            background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)',
            position: 'relative',
            overflow: 'hidden'
          }}>
            {/* Animated Background Elements */}
            <div style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              width: '400px',
              height: '400px',
              background: 'radial-gradient(circle, rgba(255, 215, 0, 0.1) 0%, transparent 70%)',
              transform: 'translate(-50%, -50%)',
              animation: 'pulse-glow 4s infinite alternate'
            }} />
            
            <div style={{
              textAlign: 'center',
              marginBottom: '40px',
              zIndex: 1
            }}>
              <h1 style={{
                color: '#ffd700',
                fontSize: '2.5rem',
                marginBottom: '20px',
                textShadow: '0 0 20px rgba(255, 215, 0, 0.5)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '15px',
                animation: 'float 3s ease-in-out infinite'
              }}>
                <span>🤖</span>
                Physical AI & Humanoid Robotics Textbook
                <span style={{
                  transform: showRobot ? 'scale(1)' : 'scale(0)',
                  transition: 'transform 0.5s ease',
                  display: 'inline-block'
                }}>
                  🚀
                </span>
              </h1>
              <p style={{
                color: '#ffed4e',
                fontSize: '1.2rem',
                maxWidth: '600px',
                margin: '0 auto 30px',
                lineHeight: '1.6'
              }}>
                Unlock the future of robotics 🤖✨. Login to access exclusive content about AI-powered humanoids, neural networks, and cutting-edge robotics technology! 🔥
              </p>
            </div>

            <div style={{
              display: 'flex',
              gap: '20px',
              marginBottom: '40px',
              zIndex: 1
            }}>
              <button
                onClick={() => window.dispatchEvent(new CustomEvent('showLoginModal'))}
                style={{
                  background: 'linear-gradient(135deg, #ffd700 0%, #ffed4e 100%)',
                  color: '#1a1a1a',
                  border: 'none',
                  padding: '15px 30px',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  fontSize: '1.1rem',
                  fontWeight: '700',
                  textTransform: 'uppercase',
                  letterSpacing: '1px',
                  transition: 'all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
                  position: 'relative',
                  overflow: 'hidden',
                  boxShadow: '0 5px 20px rgba(255, 215, 0, 0.3)'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-5px) scale(1.05)';
                  e.currentTarget.style.boxShadow = '0 10px 30px rgba(255, 215, 0, 0.5)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0) scale(1)';
                  e.currentTarget.style.boxShadow = '0 5px 20px rgba(255, 215, 0, 0.3)';
                }}
              >
                <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  🔓 Login
                </span>
              </button>

              <button
                onClick={() => window.dispatchEvent(new CustomEvent('showSignupModal'))}
                style={{
                  background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)',
                  color: '#ffd700',
                  border: '2px solid #ffd700',
                  padding: '15px 30px',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  fontSize: '1.1rem',
                  fontWeight: '700',
                  textTransform: 'uppercase',
                  letterSpacing: '1px',
                  transition: 'all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
                  position: 'relative',
                  overflow: 'hidden',
                  boxShadow: '0 5px 20px rgba(255, 215, 0, 0.2)'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-5px) scale(1.05)';
                  e.currentTarget.style.background = 'linear-gradient(135deg, #ffd700 0%, #ffed4e 100%)';
                  e.currentTarget.style.color = '#1a1a1a';
                  e.currentTarget.style.boxShadow = '0 10px 30px rgba(255, 215, 0, 0.5)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0) scale(1)';
                  e.currentTarget.style.background = 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)';
                  e.currentTarget.style.color = '#ffd700';
                  e.currentTarget.style.boxShadow = '0 5px 20px rgba(255, 215, 0, 0.2)';
                }}
              >
                <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  🚀 Sign Up
                </span>
              </button>
            </div>

            {/* Animated Robot Elements */}
            <div style={{
              position: 'absolute',
              bottom: '50px',
              right: '50px',
              fontSize: '3rem',
              animation: 'float 6s ease-in-out infinite',
              filter: 'drop-shadow(0 0 15px rgba(255, 215, 0, 0.5))',
              transform: 'rotate(-15deg)'
            }}>
              🤖
            </div>

            <div style={{
              position: 'absolute',
              top: '50px',
              left: '50px',
              fontSize: '2rem',
              animation: 'float 8s ease-in-out infinite 1s',
              filter: 'drop-shadow(0 0 10px rgba(255, 215, 0, 0.4))'
            }}>
              ⚡
            </div>

            <LoginModal isOpen={false} onClose={() => {}} onSwitchToSignup={() => {}} />
            <SignupModal isOpen={false} onClose={() => {}} onSwitchToLogin={() => {}} />

            <style jsx>{`
              @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
              }
              @keyframes pulse-glow {
                0% { opacity: 0.5; transform: translate(-50%, -50%) scale(0.8); }
                100% { opacity: 0.8; transform: translate(-50%, -50%) scale(1.2); }
              }
            `}</style>
          </div>
        )}
      </BrowserOnly>
    );
  }

  // If authenticated, render the protected content
  return children;
};

export default AuthGuard;