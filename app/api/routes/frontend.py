from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def frontend() -> str:
    return """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ScamShield AI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
    <style>
      :root {
        --bg: #f5f7fa;
        --card: #ffffff;
        --text: #102a43;
        --muted: #486581;
        --primary: #005fcc;
        --danger: #b42318;
        --safe: #027a48;
        --border: #d9e2ec;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: "Atkinson Hyperlegible", sans-serif;
        background: var(--bg);
        color: var(--text);
        line-height: 1.5;
      }
      .container {
        max-width: 860px;
        margin: 0 auto;
        padding: 24px 16px 36px;
      }
      .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
      }
      h1 {
        font-size: 2rem;
        margin: 0 0 8px;
      }
      .subtitle {
        font-size: 1.1rem;
        color: var(--muted);
        margin: 0;
      }
      label {
        display: block;
        font-size: 1.1rem;
        margin: 10px 0 8px;
        font-weight: 700;
      }
      textarea, select {
        width: 100%;
        font-size: 1.15rem;
        padding: 14px;
        border: 2px solid var(--border);
        border-radius: 10px;
        background: #fff;
      }
      textarea { min-height: 180px; resize: vertical; }
      button {
        margin-top: 14px;
        width: 100%;
        border: none;
        border-radius: 10px;
        background: var(--primary);
        color: #fff;
        font-size: 1.25rem;
        font-weight: 700;
        padding: 14px 18px;
        cursor: pointer;
      }
      button:disabled { opacity: 0.7; cursor: wait; }
      .result h2 {
        margin-top: 0;
        font-size: 1.6rem;
      }
      .pill {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        color: #fff;
        font-weight: 700;
        margin-bottom: 8px;
      }
      .pill.scam { background: var(--danger); }
      .pill.safe { background: var(--safe); }
      .score {
        font-size: 1.3rem;
        font-weight: 700;
      }
      ul {
        margin: 8px 0 0 18px;
        font-size: 1.1rem;
      }
      .help {
        color: var(--muted);
        font-size: 1rem;
      }
      .error {
        color: var(--danger);
        font-weight: 700;
      }
      .nav-link {
        display: inline-block;
        margin-top: 10px;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--primary);
        text-decoration: none;
      }
    </style>
  </head>
  <body>
    <main class="container">
      <section class="card">
        <h1>ScamShield AI</h1>
        <p class="subtitle">Input a suspicious message or email. We will explain if it looks like a scam.</p>
        <a class="nav-link" href="/history">View Past Results</a>
      </section>

      <section class="card">
        <label for="text">Suspicious message or email</label>
        <textarea id="text" placeholder="Example: Your bank account is locked. Click here now to verify your password."></textarea>

        <label for="channel">Where did you receive this?</label>
        <select id="channel">
          <option value="">Not sure</option>
          <option value="email">Email</option>
          <option value="sms">Text message</option>
          <option value="chat">Chat app</option>
          <option value="call_transcript">Phone call transcript</option>
        </select>

        <button id="checkBtn">Check Message</button>
        <p class="help">Tip: Do not enter private data like passwords or account numbers.</p>
        <p id="status" class="help"></p>
      </section>

      <section class="card result" id="resultCard" style="display:none;">
        <h2>Result</h2>
        <div id="riskPill" class="pill">Risk</div>
        <p class="score">Risk Score: <span id="score"></span></p>
        <p><strong>Scam Type:</strong> <span id="scamType"></span></p>
        <p><strong>Recommended Next Step:</strong> <span id="nextStep"></span></p>
        <p><strong>Why this was flagged:</strong></p>
        <ul id="reasons"></ul>
      </section>
    </main>

    <script>
      const btn = document.getElementById("checkBtn");
      const statusEl = document.getElementById("status");
      const resultCard = document.getElementById("resultCard");
      const riskPill = document.getElementById("riskPill");
      const score = document.getElementById("score");
      const scamType = document.getElementById("scamType");
      const nextStep = document.getElementById("nextStep");
      const reasons = document.getElementById("reasons");

      function showError(message) {
        statusEl.className = "error";
        statusEl.textContent = message;
      }

      btn.addEventListener("click", async () => {
        const text = document.getElementById("text").value.trim();
        const channel = document.getElementById("channel").value;

        if (!text) {
          showError("Please input a message first.");
          return;
        }

        btn.disabled = true;
        statusEl.className = "help";
        statusEl.textContent = "Checking message...";

        try {
          const res = await fetch("/detect", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, channel: channel || null })
          });
          if (!res.ok) {
            throw new Error("Request failed. Please try again.");
          }
          const data = await res.json();

          const percent = Math.round((data.confidence || 0) * 100);
          score.textContent = `${percent}%`;
          scamType.textContent = data.scam_type || "unknown";
          nextStep.textContent = data.recommended_action || "Be careful and verify through official channels.";

          riskPill.textContent = data.is_scam ? "Likely Scam" : "Likely Safe";
          riskPill.className = `pill ${data.is_scam ? "scam" : "safe"}`;

          reasons.innerHTML = "";
          (data.reasons || []).forEach((r) => {
            const li = document.createElement("li");
            li.textContent = r;
            reasons.appendChild(li);
          });

          resultCard.style.display = "block";
          statusEl.className = "help";
          statusEl.textContent = "";
        } catch (err) {
          showError(err.message || "Something went wrong.");
        } finally {
          btn.disabled = false;
        }
      });
    </script>
  </body>
</html>
"""


@router.get("/history", response_class=HTMLResponse, include_in_schema=False)
def history_page() -> str:
    return """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ScamShield AI - History</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
    <style>
      :root {
        --bg: #f5f7fa;
        --card: #ffffff;
        --text: #102a43;
        --muted: #486581;
        --primary: #005fcc;
        --danger: #b42318;
        --safe: #027a48;
        --border: #d9e2ec;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: "Atkinson Hyperlegible", sans-serif;
        background: var(--bg);
        color: var(--text);
        line-height: 1.5;
      }
      .container {
        max-width: 900px;
        margin: 0 auto;
        padding: 24px 16px 36px;
      }
      .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
      }
      h1 {
        font-size: 2rem;
        margin: 0 0 6px;
      }
      .subtitle {
        font-size: 1.1rem;
        color: var(--muted);
        margin: 0;
      }
      .nav {
        display: flex;
        gap: 10px;
        margin: 14px 0 16px;
      }
      .link-btn {
        display: inline-block;
        text-decoration: none;
        background: var(--primary);
        color: #fff;
        font-weight: 700;
        font-size: 1rem;
        padding: 10px 14px;
        border-radius: 10px;
      }
      .pill {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        color: #fff;
        font-weight: 700;
        font-size: 0.95rem;
      }
      .scam { background: var(--danger); }
      .safe { background: var(--safe); }
      .meta, .help { color: var(--muted); }
      .meta { font-size: 0.95rem; margin: 6px 0; }
      .text {
        margin: 10px 0 0;
        font-size: 1.08rem;
        background: #f8fbff;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 10px;
      }
      .help { font-size: 1rem; }
      .error {
        color: var(--danger);
        font-weight: 700;
      }
      .top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
      }
    </style>
  </head>
  <body>
    <main class="container">
      <section class="card">
        <h1>Scan History</h1>
        <p class="subtitle">All previously checked messages are listed below.</p>
        <div class="nav">
          <a class="link-btn" href="/">Back to Detector</a>
          <a class="link-btn" href="/docs">Open API Docs</a>
        </div>
        <p id="status" class="help">Loading history...</p>
      </section>

      <section id="list"></section>
    </main>

    <script>
      const statusEl = document.getElementById("status");
      const listEl = document.getElementById("list");

      function renderItem(item) {
        const card = document.createElement("section");
        card.className = "card";
        const score = Math.round((item.confidence || 0) * 100);
        const isScam = item.is_scam;
        card.innerHTML = `
          <div class="top-row">
            <span class="pill ${isScam ? "scam" : "safe"}">${isScam ? "Likely Scam" : "Likely Safe"}</span>
            <strong>Score: ${score}%</strong>
          </div>
          <p class="meta">Message ID: ${item.message_id} | Channel: ${item.channel || "unknown"} | Type: ${item.scam_type}</p>
          <p class="text">${item.raw_text}</p>
        `;
        listEl.appendChild(card);
      }

      async function loadHistory() {
        try {
          const res = await fetch("/messages");
          if (!res.ok) throw new Error("Could not load message history.");
          const data = await res.json();
          if (!Array.isArray(data) || data.length === 0) {
            statusEl.textContent = "No scans yet. Go back and check a message first.";
            return;
          }
          statusEl.textContent = `Loaded ${data.length} saved scan(s).`;
          data.forEach(renderItem);
        } catch (err) {
          statusEl.className = "error";
          statusEl.textContent = err.message || "Something went wrong.";
        }
      }

      loadHistory();
    </script>
  </body>
</html>
"""
