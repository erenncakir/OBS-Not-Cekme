chrome.runtime.onInstalled.addListener(() => {
  console.log("OBS Sniffer: Hazır! Trafik dinleniyor...");
});

// Trafik dinleyici (Request Headers)
chrome.webRequest.onBeforeSendHeaders.addListener(
  function (details) {
    // Sadece not listesi veya ana ekran isteklerinde çalış
    if (
      details.url.includes("not_listesi") ||
      details.url.includes("index.aspx")
    ) {
      console.log("Hedef URL yakalandı:", details.url);

      // Headerların içinde "Cookie" var mı diye bak
      if (details.requestHeaders) {
        for (let i = 0; i < details.requestHeaders.length; ++i) {
          if (details.requestHeaders[i].name === "Cookie") {
            const cookieValue = details.requestHeaders[i].value;
            console.log("COOKIE YAKALANDI! (Header Yöntemi)");

            // Python'a gönder
            sendToPython(cookieValue);
            break; // Bulduk, döngüden çık
          }
        }
      }
    }
  },
  { urls: ["*://*.dpu.edu.tr/*"] },
  ["requestHeaders", "extraHeaders"]
);

// Python'a gönderme fonksiyonu
async function sendToPython(cookieString) {
  try {
    const response = await fetch("http://localhost:5000/receive_cookie", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cookie: cookieString,
        timestamp: new Date().toISOString(),
      }),
    });

    if (response.ok) {
      console.log("BAŞARILI: Cookie Python'a teslim edildi!");
      chrome.storage.local.set({
        status: "success",
        lastSent: new Date().toISOString(),
      });
    } else {
      console.error("Sunucu hatası:", response.status);
    }
  } catch (error) {
    console.error("Python Sunucusuna Ulaşılamadı:", error);
  }
}
