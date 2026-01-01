// Sayfa yüklendiğinde durumu kontrol et
document.addEventListener("DOMContentLoaded", function () {
  checkStatus();

  // Manuel gönder butonuna event listener ekle
  document.getElementById("manualSend").addEventListener("click", manualSend);
});

// Durumu kontrol et ve göster
async function checkStatus() {
  const statusBox = document.getElementById("statusBox");
  const lastSentDiv = document.getElementById("lastSent");

  // Local storage'dan son durumu al
  chrome.storage.local.get(["status", "lastSent"], function (result) {
    if (result.status === "success") {
      statusBox.className = "status success";
      statusBox.textContent = "✓ Cookie başarıyla gönderildi!";

      if (result.lastSent) {
        const date = new Date(result.lastSent);
        lastSentDiv.textContent = `Son gönderim: ${date.toLocaleString(
          "tr-TR"
        )}`;
      }
    } else if (result.status === "error") {
      statusBox.className = "status error";
      statusBox.textContent = "✗ Hata! Python programı çalışmıyor olabilir.";
    } else {
      statusBox.className = "status info";
      statusBox.textContent = "Henüz cookie gönderilmedi.";
    }
  });

  // Python sunucusunun çalışıp çalışmadığını kontrol et
  try {
    const response = await fetch("http://localhost:5000/health");
    if (response.ok) {
      // Sunucu çalışıyor
    } else {
      statusBox.className = "status error";
      statusBox.textContent = "✗ Python programı çalışmıyor!";
    }
  } catch (error) {
    statusBox.className = "status error";
    statusBox.textContent = "✗ Python programı çalışmıyor!";
  }
}

// Manuel olarak cookie gönder
async function manualSend() {
  const statusBox = document.getElementById("statusBox");
  statusBox.className = "status info";
  statusBox.textContent = "⏳ Gönderiliyor...";

  try {
    // Cookie'leri al
    const cookies = await chrome.cookies.getAll({
      domain: "obs.dpu.edu.tr",
    });

    if (cookies.length === 0) {
      statusBox.className = "status error";
      statusBox.textContent = "✗ Cookie bulunamadı! Önce OBS'ye giriş yap.";
      return;
    }

    let cookieString = cookies
      .map((cookie) => `${cookie.name}=${cookie.value}`)
      .join("; ");

    // Python'a gönder
    const response = await fetch("http://localhost:5000/receive_cookie", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        cookie: cookieString,
        timestamp: new Date().toISOString(),
      }),
    });

    if (response.ok) {
      statusBox.className = "status success";
      statusBox.textContent = "✓ Cookie başarıyla gönderildi!";
      chrome.storage.local.set({
        lastSent: new Date().toISOString(),
        status: "success",
      });
      checkStatus(); // Durumu güncelle
    } else {
      statusBox.className = "status error";
      statusBox.textContent = "✗ Gönderim başarısız!";
    }
  } catch (error) {
    statusBox.className = "status error";
    statusBox.textContent = "✗ Hata: " + error.message;
  }
}
