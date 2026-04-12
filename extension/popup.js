function updateUI() {
  chrome.storage.local.get(["videos"], (data) => {
    let videos = data.videos || [];
    document.getElementById("count").innerText = "Total: " + videos.length;

    let list = document.getElementById("list");
    list.innerHTML = "";
    videos.forEach((v, i) => {
      let div = document.createElement("div");
      div.innerText = (i+1) + ". " + v;
      list.appendChild(div);
    });
  });
}

document.getElementById("addBtn").addEventListener("click", () => {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    let url = tabs[0].url;

    if (!url.includes("youtube.com/watch")) {
      alert("Not a YouTube video");
      return;
    }

    chrome.storage.local.get(["videos"], (data) => {
      let videos = data.videos || [];

      if (!videos.includes(url)) {
        videos.push(url);
      }

      chrome.storage.local.set({videos}, updateUI);
    });
  });
});

document.getElementById("clearBtn").addEventListener("click", () => {
  chrome.storage.local.set({videos: []}, updateUI);
});

document.getElementById("exportBtn").addEventListener("click", () => {
  let statusEl = document.getElementById("status");
  statusEl.innerText = "Saving...";
  statusEl.style.color = "#666";

  chrome.storage.local.get(["videos"], (data) => {
    let videos = data.videos || [];

    fetch("http://localhost:5000/save-videos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({videos: videos})
    })
    .then(response => response.json())
    .then(result => {
      if (result.status === "success") {
        statusEl.innerText = "✓ Saved to: data/extension_videos.json";
        statusEl.style.color = "green";
      } else {
        statusEl.innerText = "✗ Error: " + result.message;
        statusEl.style.color = "red";
      }
    })
    .catch(error => {
      statusEl.innerText = "✗ Cannot connect to server. Make sure server.py is running!";
      statusEl.style.color = "red";
      console.error("Error:", error);
    });
  });
});

updateUI();