/*Test KOD Baş*/
// background.js

chrome.runtime.onInstalled.addListener(() => {
  console.log("✅ OBS Sniffer: Hazır! Trafik dinleniyor...");
});

// Trafik dinleyici (Request Headers)
chrome.webRequest.onBeforeSendHeaders.addListener(
  function (details) {
    // Sadece not listesi veya ana ekran isteklerinde çalış
    if (
      details.url.includes("not_listesi") ||
      details.url.includes("index.aspx")
    ) {
      console.log("🎯 Hedef URL yakalandı:", details.url);

      // Headerların içinde "Cookie" var mı diye bak
      if (details.requestHeaders) {
        for (let i = 0; i < details.requestHeaders.length; ++i) {
          if (details.requestHeaders[i].name === "Cookie") {
            const cookieValue = details.requestHeaders[i].value;
            console.log("🔥 COOKIE YAKALANDI! (Header Yöntemi)");

            // Python'a gönder
            sendToPython(cookieValue);
            break; // Bulduk, döngüden çık
          }
        }
      }
    }
  },
  { urls: ["*://*.dpu.edu.tr/*"] },
  ["requestHeaders", "extraHeaders"] // Bu izin headerları okumamızı sağlar
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
      console.log("✅ BAŞARILI: Cookie Python'a teslim edildi!");
      chrome.storage.local.set({
        status: "success",
        lastSent: new Date().toISOString(),
      });
    } else {
      console.error("❌ Sunucu hatası:", response.status);
    }
  } catch (error) {
    console.error("❌ Python Sunucusuna Ulaşılamadı:", error);
  }
}
/*Test KOD Son*/

// // OBS sitesine istek atıldığında tetiklenir
// chrome.webRequest.onCompleted.addListener(
//   function (details) {
//     // URL kontrolü (Hem not listesini hem de ana girişi kontrol et)
//     if (details.url.includes("not_listesi_op.aspx")) {
//       console.log("Not listesi isteği yakalandı:", details.url);
//       getCookiesAndSend();
//     }
//   },
//   {
//     urls: ["https://obs.dpu.edu.tr/*"],
//     //url değişmediği için alt istekleri görmeliyiz.
//     types: ["main_frame", "sub_frame", "xmlhttprequest"],
//   }
// );

// // Cookie'leri al ve Python'a gönder
// async function getCookiesAndSend() {
//   try {
//     // OBS'den tüm cookie'leri al
//     const cookies = await chrome.cookies.getAll({
//       domain: "obs.dpu.edu.tr",
//     });

//     if (cookies.length === 0) {
//       console.log("Cookie bulunamadı.");
//       return;
//     }

//     // Cookie'leri "key=value; key2=value2" formatına çevir
//     let cookieString = cookies
//       .map((cookie) => `${cookie.name}=${cookie.value}`)
//       .join("; ");

//     console.log("Cookie Python'a gönderiliyor...");

//     // Python sunucusuna gönder
//     const response = await fetch("http://localhost:5000/receive_cookie", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({
//         cookie: cookieString,
//         timestamp: new Date().toISOString(),
//       }),
//     });

//     if (response.ok) {
//       console.log("Cookie başarıyla gönderildi!");
//       chrome.storage.local.set({
//         lastSent: new Date().toISOString(),
//         status: "success",
//       });
//     } else {
//       console.error("Cookie gönderilemedi sunucu hatası:", response.status);
//       chrome.storage.local.set({ status: "error" });
//     }
//   } catch (error) {
//     console.error("Hata:", error);
//     chrome.storage.local.set({ status: "error" });
//   }
// }

// // Extension yüklendiğinde
// chrome.runtime.onInstalled.addListener(() => {
//   console.log("OBS Cookie Helper yüklendi!");
// });
