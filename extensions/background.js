// OBS sitesine istek atıldığında tetiklenir
chrome.webRequest.onCompleted.addListener(
  function (details) {
    // Sadece not listesi sayfasında çalış
    if (details.url.includes("not_listesi_op.aspx")) {
      getCookiesAndSend();
    }
  },
  { urls: ["https://obs.dpu.edu.tr/*"] }
);

// Cookie'leri al ve Python'a gönder
async function getCookiesAndSend() {
  try {
    // OBS'den tüm cookie'leri al
    const cookies = await chrome.cookies.getAll({
      domain: "obs.dpu.edu.tr",
    });

    // Cookie'leri "key=value; key2=value2" formatına çevir
    let cookieString = cookies
      .map((cookie) => `${cookie.name}=${cookie.value}`)
      .join("; ");

    // Python sunucusuna gönder
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
      console.log("Cookie başarıyla gönderildi!");
      // Başarı durumunu kaydet (popup'ta göstermek için)
      chrome.storage.local.set({
        lastSent: new Date().toISOString(),
        status: "success",
      });
    } else {
      console.error("Cookie gönderilemedi:", response.status);
      chrome.storage.local.set({ status: "error" });
    }
  } catch (error) {
    console.error("Hata:", error);
    chrome.storage.local.set({ status: "error" });
  }
}

// Extension yüklendiğinde bir kez kontrol et
chrome.runtime.onInstalled.addListener(() => {
  console.log("OBS Cookie Helper yüklendi!");
});
