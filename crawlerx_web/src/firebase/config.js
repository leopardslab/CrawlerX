//Import the required methods
import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'

//The config we copied from firebase(Replace with your config)
const firebaseConfig = {
  apiKey: process.env.VUE_APP_FIREBASE_API_KEY,
  authDomain: process.env.VUE_APP_FIREBASE_AUTH_DOMAIN,
  databaseURL: process.env.VUE_APP_FIREBASE_DB_DOMAIN,
  projectId: process.env.VUE_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.VUE_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.VUE_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.VUE_APP_FIREBASE_APP_ID,
  measurementId: process.env.VUE_APP_FIREBASE_MEASURMENT_ID,
};

//initialize the firebase app
initializeApp(firebaseConfig)

//initialize firebase auth
const auth = getAuth()

//export the auth object
export { auth }