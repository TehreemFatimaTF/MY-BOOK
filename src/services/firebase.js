import { initializeApp } from 'firebase/app';
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged } from 'firebase/auth';

// For Docusaurus, we'll access the Firebase config from the themeConfig
// The config values will be injected at build time via docusaurus.config.js
let firebaseConfig;

// Check if we're in the browser environment and if the config is available from Docusaurus
if (typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig) {
  firebaseConfig = window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig;

  // Log the loaded config for debugging (only in development)
  if (typeof window !== 'undefined' && window.location && window.location.hostname !== 'localhost') {
    console.log('Firebase config loaded from Docusaurus config:', {
      apiKey: firebaseConfig.apiKey ? '***HIDDEN***' : 'MISSING',
      authDomain: firebaseConfig.authDomain || 'MISSING',
      projectId: firebaseConfig.projectId || 'MISSING'
    });
  }
} else {
  // Fallback configuration - this ensures that even if Docusaurus config isn't available,
  // we still have the proper values from the environment
  firebaseConfig = {
    apiKey: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.apiKey
      : "",
    authDomain: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.authDomain
      : "",
    projectId: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.projectId
      : "",
    storageBucket: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.storageBucket
      : "",
    messagingSenderId: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.messagingSenderId
      : "",
    appId: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.appId
      : "",
    measurementId: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.measurementId
      : ""
  };

  // Log the fallback config for debugging (only in development)
  if (typeof window !== 'undefined' && window.location && window.location.hostname !== 'localhost') {
    console.log('Firebase config loaded from fallback values');
  }
}

// Initialize Firebase app with better error handling
let app;
if (firebaseConfig.apiKey) {
  try {
    // Check if Firebase app already exists to avoid multiple initialization error
    app = initializeApp(firebaseConfig);
  } catch (error) {
    // If app already exists, get the default app
    app = initializeApp();
    console.warn('Firebase app already initialized, using existing app');
  }
} else {
  console.warn('Firebase not initialized: API key is missing. Please set up environment variables.');
  // Create a mock app object to prevent errors when Firebase is not configured
  app = null;
}

// Initialize Firebase Authentication and get a reference to the service
let auth;
if (app) {
  auth = getAuth(app);
} else {
  // Create a mock auth object to prevent errors when Firebase is not configured
  auth = null;
  console.warn('Firebase Auth not initialized due to missing configuration.');
}

export { auth };

// Log the Firebase configuration to help with debugging
if (typeof window !== 'undefined' && window.location && window.location.hostname !== 'localhost') {
  console.log('Firebase initialized with config:', {
    apiKey: firebaseConfig.apiKey ? '***HIDDEN***' : 'MISSING',
    authDomain: firebaseConfig.authDomain,
    projectId: firebaseConfig.projectId
  });

  console.log('Firebase auth object created:', auth ? 'SUCCESS' : 'FAILED');
}

// Export Firebase auth methods with safety checks
const safeCreateUserWithEmailAndPassword = auth ? createUserWithEmailAndPassword : () => Promise.reject(new Error('Firebase not initialized'));
const safeSignInWithEmailAndPassword = auth ? signInWithEmailAndPassword : () => Promise.reject(new Error('Firebase not initialized'));
const safeSignOut = auth ? signOut : () => Promise.reject(new Error('Firebase not initialized'));
const safeOnAuthStateChanged = auth ? onAuthStateChanged : () => { console.warn('Firebase not initialized'); };

// Export Firebase auth methods
export {
  safeCreateUserWithEmailAndPassword as createUserWithEmailAndPassword,
  safeSignInWithEmailAndPassword as signInWithEmailAndPassword,
  safeSignOut as signOut,
  safeOnAuthStateChanged as onAuthStateChanged
};