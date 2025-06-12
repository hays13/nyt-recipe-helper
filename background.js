chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "FETCH_ALLERGENS") {
      fetch("http://127.0.0.1:5000/detect_allergens", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients: message.ingredients })
      })
      .then(res => res.json())
      .then(data => sendResponse(data))
      .catch(error => {
        console.error("Backend fetch failed (allergens):", error);
        sendResponse({ error: "Backend request failed" });
      });
  
      // Important for async responses
      return true;
    }

    if (message.type === "FETCH_EQUIPMENT") {
      fetch("http://127.0.0.1:5000/detect_equipment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: message.text })
      })
      .then(res => res.json())
      .then(data => sendResponse(data))
      .catch(error => {
        console.error("Backend fetch failed (equipment):", error);
        sendResponse({error: "Backend request failed "});
      });

      // Important for async responses
      return true;
    }
  });
  