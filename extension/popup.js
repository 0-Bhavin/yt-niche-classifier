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
  chrome.storage.local.get(["videos"], (data) => {
    let videos = data.videos || [];

    let csv = "video_url\n" + videos.join("\n");

    let blob = new Blob([csv], {type: "text/csv"});
    let url = URL.createObjectURL(blob);

    chrome.downloads.download({
      url: url,
      filename: "yt_videos.csv"
    });
  });
});

updateUI();