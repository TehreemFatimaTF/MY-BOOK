import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './AuthModal.css';

const SignupModal = ({ onSwitchToLogin }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Hardware background state
  const [hardwareType, setHardwareType] = useState('');
  const [jetsonModel, setJetsonModel] = useState('');
  const [components, setComponents] = useState('');

  // Software background state
  const [softwareStack, setSoftwareStack] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('');

  const { register } = useAuth();

  useEffect(() => {
    const handleOpenSignupModal = () => {
      setIsOpen(true);
      setError('');
      setName('');
      setEmail('');
      setPassword('');
      setConfirmPassword('');
    };

    window.addEventListener('showSignupModal', handleOpenSignupModal);

    return () => {
      window.removeEventListener('showSignupModal', handleOpenSignupModal);
    };
  }, []);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    // Prepare profile data
    const profileData = {
      name,
      email,
      password,
      // Hardware background
      hardware_type: hardwareType,
      jetson_model: jetsonModel,
      components: components ? components.split(',').map(item => item.trim()).filter(item => item) : [],
      // Software background
      software_stack: softwareStack ? softwareStack.split(',').map(item => item.trim()).filter(item => item) : [],
      experience_level: experienceLevel,
    };

    const result = await register(profileData);

    if (result.success) {
      setIsOpen(false);
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  return (
    <div className="auth-modal-overlay" onClick={handleClose}>
      <div className="auth-modal" onClick={(e) => e.stopPropagation()}>
        <div className="auth-modal-header">
          <h2>Sign Up</h2>
          <button className="auth-modal-close" onClick={handleClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="auth-error">{error}</div>}

          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              placeholder="John Doe"
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="your@email.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              placeholder="••••••••"
            />
          </div>


        

          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        <div className="auth-switch">
          Already have an account?{' '}
          <button onClick={onSwitchToLogin} className="auth-switch-link">
            Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default SignupModal;