import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  auth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged
} from '../services/firebase';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check Firebase auth state on initial load
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    // Listen for logoutRequested event from client-side script
    const handleLogoutRequested = async () => {
      await logout();
    };

    window.addEventListener('logoutRequested', handleLogoutRequested);

    // Cleanup subscription on unmount
    return () => {
      unsubscribe();
      window.removeEventListener('logoutRequested', handleLogoutRequested);
    };
  }, []);

  const login = async (email, password) => {
    // Debug logging
    if (process.env.NODE_ENV !== 'production') {
      console.log('Login attempt with email:', email);
      console.log('Auth object available:', !!auth);
      console.log('Email format valid:', /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email));
      console.log('Password length:', password.length);
    }

    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);

      if (process.env.NODE_ENV !== 'production') {
        console.log('Login successful:', userCredential.user.email);
      }

      return { success: true, user: userCredential.user };
    } catch (error) {
      console.error('Login error details:', {
        code: error.code,
        message: error.message,
        email: email,
        passwordLength: password.length
      });

      let errorMessage = 'Login failed';

      switch (error.code) {
        case 'auth/user-not-found':
          errorMessage = 'No account found with this email address';
          break;
        case 'auth/wrong-password':
          errorMessage = 'Incorrect password';
          break;
        case 'auth/invalid-email':
          errorMessage = 'Invalid email address';
          break;
        case 'auth/invalid-credential':
          errorMessage = 'Invalid email or password. Please check your credentials.';
          break;
        case 'auth/too-many-requests':
          errorMessage = 'Too many failed attempts. Please try again later.';
          break;
        case 'auth/user-disabled':
          errorMessage = 'This account has been disabled';
          break;
        default:
          errorMessage = error.message || 'Login failed';
      }

      return { success: false, error: errorMessage };
    }
  };

  const register = async (userData) => {
    try {
      const { email, password, name, ...profileData } = userData;

      if (!email || !password) {
        return { success: false, error: 'Email and password are required' };
      }

      const userCredential = await createUserWithEmailAndPassword(auth, email, password);

      // Update user profile with display name if provided
      if (name) {
        await userCredential.user.updateProfile({
          displayName: name
        });
      }

      return { success: true, user: userCredential.user };
    } catch (error) {
      console.error('Registration error:', error);
      let errorMessage = 'Registration failed';

      switch (error.code) {
        case 'auth/email-already-in-use':
          errorMessage = 'Email address is already in use';
          break;
        case 'auth/invalid-email':
          errorMessage = 'Invalid email address';
          break;
        case 'auth/weak-password':
          errorMessage = 'Password is too weak. Please use at least 6 characters.';
          break;
        default:
          errorMessage = error.message || 'Registration failed';
      }

      return { success: false, error: errorMessage };
    }
  };

  const logout = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error('Logout error:', error);
      // Even if logout fails, clear local state
      setUser(null);
    }
  };

  const updateProfile = async (profileData) => {
    try {
      if (!user) {
        return { success: false, error: 'No user is currently logged in' };
      }

      // In Firebase, profile updates are typically handled through user.updateProfile()
      // For additional profile data, you would typically use Firestore
      if (profileData.displayName) {
        await user.updateProfile({
          displayName: profileData.displayName
        });
      }

      // Update local state
      setUser(prevUser => ({
        ...prevUser,
        ...profileData
      }));

      return { success: true, user: { ...user, ...profileData } };
    } catch (error) {
      console.error('Profile update error:', error);
      return { success: false, error: error.message };
    }
  };

  const value = {
    user,
    login,
    register,
    logout,
    updateProfile,
    loading,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Helper function to get current user
// This is no longer used since we're not making actual API calls
// const getCurrentUser = async (token) => {
//   try {
//     const response = await fetch(`${API_BASE_URL}/auth/me`, {
//       headers: {
//         'Authorization': `Bearer ${token}`,
//       },
//     });

//     if (!response.ok) {
//       throw new Error(`Failed to get user data: ${response.status} ${response.statusText}`);
//     }

//     return await response.json();
//   } catch (error) {
//     console.error('Error fetching user data:', error);
//     throw error;
//   }
// };