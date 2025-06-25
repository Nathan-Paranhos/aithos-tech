// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";
import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyC9d3V4KWpGiSl5vzKZ16ycwoZqldLo2zI",
  authDomain: "hackaton-anchieta.firebaseapp.com",
  projectId: "hackaton-anchieta",
  storageBucket: "hackaton-anchieta.firebasestorage.app",
  messagingSenderId: "585293268662",
  appId: "1:585293268662:web:5a15c69ba1347b2d404817",
  measurementId: "G-MEPT9NZS7B"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Firebase services
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);

export { auth, db, storage, analytics };
export default app;