// firebase-config.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Replace these with your actual Firebase project configuration
const firebaseConfig = {
    apiKey: "AIzaSyD6G4nQ-8jyw9ZT-r7FbLwrWh6kUz3u1bI",
    authDomain: "recomm-demo.firebaseapp.com",
    projectId: "recomm-demo",
    storageBucket: "recomm-demo.firebasestorage.app",
    messagingSenderId: "1087260910863",
    appId: "1:1087260910863:web:3668acf6da92178a904a7a"
};


const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);