// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";

// Your Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyCYW3AxavIoamXcve-CUoGB0tDlLwmSpRs",
  authDomain: "collage-porject-final.firebaseapp.com",
  databaseURL: "https://collage-porject-final-default-rtdb.firebaseio.com",
  projectId: "collage-porject-final",
  storageBucket: "collage-porject-final.firebasestorage.app",
  messagingSenderId: "220400167688",
  appId: "1:220400167688:web:a6474ac58691259e2c9abd",
  measurementId: "G-9NJ6QQ4X8G"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Session configuration (15 minutes = 900,000 ms)
const SESSION_DURATION = 15 * 60 * 1000; // 15 minutes

// ----- Helper: SHA256 hashing (Web Crypto API) -----
async function sha256(message) {
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
}

// Helper: show messages
function showMessage(message, divId, isError = false) {
  const messageDiv = document.getElementById(divId);
  if (!messageDiv) return;
  messageDiv.style.display = "block";
  messageDiv.innerHTML = message;
  messageDiv.style.opacity = "1";
  if (isError) {
    messageDiv.style.background = "#FEE2E2";
    messageDiv.style.color = "#991B1B";
    messageDiv.style.borderLeftColor = "#EF4444";
  } else {
    messageDiv.style.background = "#DCFCE7";
    messageDiv.style.color = "#166534";
    messageDiv.style.borderLeftColor = "#22C55E";
  }
  setTimeout(() => {
    messageDiv.style.opacity = "0";
    setTimeout(() => {
      messageDiv.style.display = "none";
      messageDiv.style.opacity = "1";
    }, 300);
  }, 4000);
}

// ----- Session Management Functions -----

// Initialize session after successful login
function initializeSession(userId) {
  const now = Date.now();
  const sessionExpiry = now + SESSION_DURATION;
  localStorage.setItem('loggedInUserId', userId);
  localStorage.setItem('sessionExpiry', sessionExpiry);
  localStorage.setItem('lastActivityTime', now);
}

// Clear session data and sign out from Firebase
async function clearSessionAndLogout(redirectToLogin = true) {
  // Clear localStorage
  localStorage.removeItem('loggedInUserId');
  localStorage.removeItem('sessionExpiry');
  localStorage.removeItem('lastActivityTime');
  
  // Sign out from Firebase
  try {
    await signOut(auth);
  } catch (error) {
    console.error("Logout error:", error);
  }
  
  // Redirect to login page if needed
  if (redirectToLogin && !window.location.pathname.includes('index.html') && window.location.pathname !== '/') {
    window.location.href = 'index.html';
  }
}

// Check if current session is valid
function isSessionValid() {
  const userId = localStorage.getItem('loggedInUserId');
  const sessionExpiry = localStorage.getItem('sessionExpiry');
  const lastActivity = localStorage.getItem('lastActivityTime');
  
  if (!userId || !sessionExpiry) {
    return false;
  }
  
  const now = Date.now();
  const expiryTime = parseInt(sessionExpiry, 10);
  const lastActivityTime = parseInt(lastActivity, 10);
  
  // Check absolute expiry
  if (now > expiryTime) {
    console.log("Session expired (absolute timeout)");
    return false;
  }
  
  // Check inactivity timeout (15 minutes)
  if (lastActivityTime && (now - lastActivityTime) > SESSION_DURATION) {
    console.log("Session expired (inactivity timeout)");
    return false;
  }
  
  return true;
}

// Update last activity timestamp (for idle tracking)
function updateActivity() {
  if (localStorage.getItem('loggedInUserId')) {
    localStorage.setItem('lastActivityTime', Date.now());
  }
}

// Setup activity listeners on current page
function setupActivityListeners() {
  const events = ['mousedown', 'keydown', 'touchstart', 'scroll', 'click'];
  events.forEach(event => {
    document.addEventListener(event, updateActivity);
  });
}

// Start session monitoring (call this on protected pages)
function startSessionMonitoring() {
  if (!isSessionValid()) {
    clearSessionAndLogout(true);
    return false;
  }
  
  setupActivityListeners();
  
  // Check session every 30 seconds
  const intervalId = setInterval(() => {
    if (!isSessionValid()) {
      clearInterval(intervalId);
      clearSessionAndLogout(true);
    }
  }, 30000);
  
  return true;
}

// Check for existing valid session on login page and auto-redirect
async function checkAndRedirectToLove() {
  if (isSessionValid()) {
    const userId = localStorage.getItem('loggedInUserId');
    const secret = "MocoSecretLove2025";
    const rawToken = userId + secret;
    const hash = await sha256(rawToken);
    window.location.href = `love.html?uid=${encodeURIComponent(userId)}&hash=${hash}`;
    return true;
  }
  return false;
}

// ------------------- SIGN UP -------------------
const signUpButton = document.getElementById('submitSignUp');
if (signUpButton) {
  signUpButton.addEventListener('click', (event) => {
    event.preventDefault();
    const email = document.getElementById('rEmail').value.trim();
    const password = document.getElementById('rPassword').value;
    const firstName = document.getElementById('fName').value.trim();
    const lastName = document.getElementById('lName').value.trim();

    if (!email || !password || !firstName || !lastName) {
      showMessage('Please fill in all fields', 'signUpMessage', true);
      return;
    }
    if (password.length < 6) {
      showMessage('Password must be at least 6 characters', 'signUpMessage', true);
      return;
    }

    createUserWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        showMessage(`✨ Account created successfully! Welcome ${firstName}!`, 'signUpMessage', false);
        // Clear form
        document.getElementById('fName').value = '';
        document.getElementById('lName').value = '';
        document.getElementById('rEmail').value = '';
        document.getElementById('rPassword').value = '';
        // Switch to login view after 1.5s
        setTimeout(() => {
          const signUpDiv = document.getElementById('signup');
          const signInDiv = document.getElementById('signIn');
          if (signUpDiv && signInDiv) {
            signUpDiv.style.display = 'none';
            signInDiv.style.display = 'block';
          }
        }, 1500);
      })
      .catch((error) => {
        if (error.code === 'auth/email-already-in-use') {
          showMessage('❌ Email already exists. Try logging in.', 'signUpMessage', true);
        } else {
          showMessage('Unable to create account. ' + error.message, 'signUpMessage', true);
        }
      });
  });
}

// ------------------- SIGN IN (with SHA256 redirect + Session) -------------------
const signInButton = document.getElementById('submitSignIn');
if (signInButton) {
  signInButton.addEventListener('click', async (event) => {
    event.preventDefault();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email || !password) {
      showMessage('Please enter both email and password', 'signInMessage', true);
      return;
    }

    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      
      // Initialize session with current timestamp
      initializeSession(user.uid);

      // Generate SHA256 token for love.html
      const secret = "MocoSecretLove2025";
      const rawToken = user.uid + secret;
      const hash = await sha256(rawToken);
      
      // Redirect to love.html with uid and hash
      window.location.href = `love.html?uid=${encodeURIComponent(user.uid)}&hash=${hash}`;
    } catch (error) {
      if (error.code === 'auth/invalid-credential') {
        showMessage('❌ Incorrect email or password', 'signInMessage', true);
      } else {
        showMessage('Login failed: ' + error.message, 'signInMessage', true);
      }
    }
  });
}

// Check for active session when login page loads
window.addEventListener('DOMContentLoaded', () => {
  // If user already has valid session, redirect to love.html
  checkAndRedirectToLove();
});

// "Enter" key support
document.querySelectorAll('#email, #password, #rEmail, #rPassword, #fName, #lName').forEach(input => {
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      const isLoginForm = input.closest('#signIn');
      if (isLoginForm && signInButton) signInButton.click();
      else if (signUpButton) signUpButton.click();
    }
  });
});