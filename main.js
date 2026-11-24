const statusEl = document.getElementById("status");
const runBtn = document.getElementById("run");
const outImg = document.getElementById("out");

let currentUrl = null;
const worker = new Worker("worker.js", { type: "module" });


worker.onmessage = (ev) => {
  const { type, png, message } = ev.data;

  if (type === "ready") {
    statusEl.textContent = "Bereit";
    runBtn.disabled = false;
  } else if (type === "altitude") {
    if (currentUrl) {
      URL.revokeObjectURL(currentUrl);
    }
    const blob = new Blob([png], { type: "image/png" });
    currentUrl = URL.createObjectURL(blob);
    outImg.src = currentUrl;
    statusEl.textContent = "Bereit";
    runBtn.disabled = false;
  } else if (type === "error") {
    statusEl.textContent = `Fehler: ${message}`;
    runBtn.disabled = false;
  }
};

runBtn.addEventListener("click", async () => {
  try {
    runBtn.disabled = true;
    statusEl.textContent = "Berechne Höhenkurve …";
    const response = await fetch("data/gnss_orbital_parameters.csv");
    if (!response.ok) throw new Error("CSV konnte nicht geladen werden.");
    const csv = await response.text();
    worker.postMessage({ cmd: "altitude", csv });
  } catch (e) {
    statusEl.textContent = `Fehler: ${String(e)}`;
    runBtn.disabled = false;
  }
});
