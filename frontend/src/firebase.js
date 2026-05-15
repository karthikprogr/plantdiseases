// Firebase Configuration and Initialization
// Replace the config values with your actual Firebase project credentials

import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

// Your web app's Firebase configuration
// Get these values from Firebase Console > Project Settings > Your apps > Web app
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY || "AIzaSyAQMMLGqoditfE-jrB0FDKaOWpygnqwJLk",
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN || "plant-disease-detection-a534c.firebaseapp.com",
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID || "plant-disease-detection-a534c",
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET || "plant-disease-detection-a534c.firebasestorage.app",
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID || "1067017569988",
  appId: process.env.REACT_APP_FIREBASE_APP_ID || "1:1067017569988:web:693b516c0cad1595f9eb91"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);

// Google Auth Provider
export const googleProvider = new GoogleAuthProvider();

// Authentication functions
export const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    return { success: true, user: result.user };
  } catch (error) {
    console.error('Google sign-in error:', error);
    return { success: false, error: error.message };
  }
};

export const signUpWithEmail = async (email, password) => {
  try {
    const result = await createUserWithEmailAndPassword(auth, email, password);
    return { success: true, user: result.user };
  } catch (error) {
    console.error('Sign-up error:', error);
    return { success: false, error: error.message };
  }
};

export const signInWithEmail = async (email, password) => {
  try {
    const result = await signInWithEmailAndPassword(auth, email, password);
    return { success: true, user: result.user };
  } catch (error) {
    console.error('Sign-in error:', error);
    return { success: false, error: error.message };
  }
};

export const logOut = async () => {
  try {
    await signOut(auth);
    return { success: true };
  } catch (error) {
    console.error('Sign-out error:', error);
    return { success: false, error: error.message };
  }
};

export default app;
