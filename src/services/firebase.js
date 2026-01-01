import { initializeApp } from 'firebase/app';
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged } from 'firebase/auth';

// For Docusaurus, we'll access the Firebase config from the themeConfig
// The config values will be injected at build time via docusaurus.config.js
let firebaseConfig;

// Check if we're in the browser environment and if the config is available from Docusaurus
if (typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig) {
  firebaseConfig = window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig;

  // Log the loaded config for debugging (only in development)
  if (typeof process !== 'undefined' && process.env && process.env.NODE_ENV !== 'production') {
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
      : "my-docusaurus-site.firebaseapp.com",
    projectId: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.projectId
      : "my-docusaurus-site",
    storageBucket: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.storageBucket
      : "my-docusaurus-site.firebasestorage.app",
    messagingSenderId: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.messagingSenderId
      : "812534412214",
    appId: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.appId
      : "1:812534412214:web:9eaacd21ead0afae8d8717",
    measurementId: typeof window !== 'undefined' && window.DOCUSAURUS_CONFIG && window.DOCUSAURUS_CONFIG.themeConfig && window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig
      ? window.DOCUSAURUS_CONFIG.themeConfig.firebaseConfig.measurementId
      : "G-KGJ96XLC0G"
  };

  // Log the fallback config for debugging (only in development)
  if (typeof process !== 'undefined' && process.env && process.env.NODE_ENV !== 'production') {
    console.log('Firebase config loaded from hardcoded fallback values');
  }
}

// Initialize Firebase app with better error handling
let app;
try {
  // Check if Firebase app already exists to avoid multiple initialization error
  app = initializeApp(firebaseConfig);
} catch (error) {
  // If app already exists, get the default app
  app = initializeApp();
  console.warn('Firebase app already initialized, using existing app');
}

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);

// Log the Firebase configuration to help with debugging
if (typeof process !== 'undefined' && process.env && process.env.NODE_ENV !== 'production') {
  console.log('Firebase initialized with config:', {
    apiKey: firebaseConfig.apiKey ? '***HIDDEN***' : 'MISSING',
    authDomain: firebaseConfig.authDomain,
    projectId: firebaseConfig.projectId
  });

  console.log('Firebase auth object created:', auth ? 'SUCCESS' : 'FAILED');
}

// Export Firebase auth methods
export {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged
};