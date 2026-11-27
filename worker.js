const MODULES = {
  altitude: "altitude_curve"
  // TODO: gnss_comparison
};
const FILES = ["bounded_utilities", ...Object.values(MODULES)];

let pyodide;

async function init() {
  try {
    const base = "https://cdn." + "jsdelivr.net/pyodide/v314.0.8/full";
    const { loadPyodide } = await import(base + "pyodide.mjs");
    pyodide = await loadPyodide({ indexURL: base });
    await pyodide.loadPackage(["numpy", "matplotlib"])

    for (const name of FILES) {
      const responce = await fetch(`py/${name}.py`);
      if (!responce.ok) throw new Error(`Failed to fetch py/${name}.py`)
      const text = await responce.text();
      pyodide.FS.writeFile(`/home/pyodide/${name}.py`, text);
    }

    pyodide.runPython("import sys; sys.path.append('/home/pyodide')");
    postMessage({ type: "ready" });
  } catch (e) {
    postMessage({ type: "error", message: String(e) });
  }
}

const ready = init();

self.onmessage = async (ev) => {
  await ready;
  const { cmd, csv } = ev.data;
  const name = MODULES[cmd];

  if (!name) {
    postMessage({ type: "error", message: `Unbekannter Befehl: ${cmd}` });
    return;
  }

  try {
    const mod = pyodide.pyimport(name);
    const pyBytes = mod.make_plot(csv);
    const png = pyBytes.toJs();
    pyBytes.destroy();
    mod.destroy();
    postMessage({ type: "plot", cmd, png });
  } catch (e) {
    postMessage({ type: "error", message: String(e) });
  }
};
