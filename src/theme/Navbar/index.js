import React, { useState, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import OriginalNavbar from '@theme-original/Navbar';
import { useAuth } from '@site/src/contexts/AuthContext';
import '../Navbar.css';

const GoldParticles = () => {
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    const createParticles = () => {
      const particlesArray = Array.from({ length: 15 }, (_, i) => ({
        id: i,
        size: Math.random() * 5 + 2,
        left: Math.random() * 100,
        delay: Math.random() * 5,
        duration: Math.random() * 3 + 4,
      }));
      setParticles(particlesArray);
    };

    createParticles();
    const interval = setInterval(createParticles, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="particles-container">
      {particles.map(particle => (
        <div
          key={particle.id}
          className="gold-particle"
          style={{
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            left: `${particle.left}%`,
            animationDelay: `${particle.delay}s`,
            animationDuration: `${particle.duration}s`,
            opacity: Math.random() * 0.6 + 0.4,
          }}
        />
      ))}
    </div>
  );
};

const AuthButton = () => {
  const { user, isAuthenticated, loading, logout } = useAuth();
  const [buttonHover, setButtonHover] = useState(false);

  if (loading) {
    return (
      <div className="golden-auth-container">
        <div className="loading-spinner-golden"></div>
      </div>
    );
  }

  const handleLogout = async () => {
    await logout();
    window.location.href = '/';
  };

  const handleLogin = () => {
    window.dispatchEvent(new CustomEvent('showLoginModal'));
  };

  const handleSignup = () => {
    window.dispatchEvent(new CustomEvent('showSignupModal'));
  };

  const getInitial = () => {
    if (user?.email) {
      return user.email.charAt(0).toUpperCase();
    }
    return 'U';
  };

  return (
    <div className="golden-auth-container">
      {isAuthenticated ? (
        <>
          <div className="user-greeting">
            <div className="user-avatar" style={{ animation: buttonHover ? 'float 0.5s ease-in-out' : 'float 3s ease-in-out infinite' }}>
              {getInitial()}
            </div>
            <span className="username">
              {user?.email?.split('@')[0]}
            </span>
          </div>
          
          <button
            type="button"
            onClick={handleLogout}
            onMouseEnter={() => setButtonHover(true)}
            onMouseLeave={() => setButtonHover(false)}
            className="golden-button logout-btn-golden"
            style={{
              background: buttonHover 
                ? 'linear-gradient(135deg, #ffdf2bff 0%, #ffe341ff 50%, #fff12bff 100%)' 
                : 'linear-gradient(135deg, #ffdc41ff 0%, #ffdf2bff 100%)'
            }}
          >
            <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              Logout
              <span style={{ fontSize: '18px' }}>🚶‍♂️</span>
            </span>
          </button>
        </>
      ) : (
        <>
          <button
            type="button"
            onClick={handleSignup}
            className="golden-button"
            style={{
              background: 'linear-gradient(135deg, #007bff, #6610f2)',
              color: 'white',
              boxShadow: '0 5px 20px rgba(102, 16, 242, 0.4)'
            }}
          >
            <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              Sign Up
              <span style={{ fontSize: '18px' }}>✨</span>
            </span>
          </button>
          
          <button
            type="button"
            onClick={handleLogin}
            onMouseEnter={() => setButtonHover(true)}
            onMouseLeave={() => setButtonHover(false)}
            className="golden-button login-btn-golden"
            style={{
              background: buttonHover 
                ? 'linear-gradient(135deg, #20c997 0%, #28a745 50%, #20c997 100%)' 
                : 'linear-gradient(135deg, #28a745 0%, #20c997 100%)'
            }}
          >
            <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              Login
              <span style={{ fontSize: '18px' }}>🔓</span>
            </span>
          </button>
        </>
      )}
      
      {/* Theme Toggle Button */}
      
    </div>
  );
};

export default function Navbar(props) {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      <OriginalNavbar 
        {...props} 
        style={{
          background: scrolled 
            ? 'linear-gradient(135deg, rgba(0,0,0,0.95) 0%, rgba(10,10,10,0.9) 100%)'
            : 'transparent',
          backdropFilter: scrolled ? 'blur(10px)' : 'none',
          transition: 'all 0.3s ease',
          borderBottom: scrolled ? '2px solid #FFD700' : 'none',
          boxShadow: scrolled ? '0 5px 30px rgba(255, 215, 0, 0.2)' : 'none'
        }}
      />
      
      <BrowserOnly>
        {() => (
          <>
            <AuthButton />
            <GoldParticles />
            
            {/* Glowing Border Effect */}
            <div style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              height: '3px',
              background: 'linear-gradient(90deg, #FFD700, #FFA500, #FFD700)',
              zIndex: 1001,
              animation: 'glow 3s infinite alternate',
            }} />
          </>
        )}
      </BrowserOnly>
      
      {/* Inline Animation Styles */}
      <style jsx>{`
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        :global(.navbar) {
          animation: slideIn 0.5s ease-out;
        }
      `}</style>
    </>
  );
}