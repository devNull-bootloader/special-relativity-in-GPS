let pyodide;

async function init() {
  try {
    const base = "https://cdn." + "jsdelivr.net/pyodide/v314.0.8/full/";
    const { loadPyodide } = await import(base + "pyodide.mjs");
    pyodide = await loadPyodide({ indexURL: base });
    await pyodide.loadPackage(["numpy", "matplotlib"]);


    for (const name of ["bounded_utilities", "altitude_curve"]) {
      const response = await fetch(`py/${name}.py`);
      if (!response.ok) throw new Error(`Failed to fetch py/${name}.py`);
      const text = await response.text();
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
  if (ev.data.cmd === "altitude") {
    try {
      const mod = pyodide.pyimport("altitude_curve");
      const pyBytes = mod.make_plot(ev.data.csv);
      const png = pyBytes.toJs();
      pyBytes.destroy();
      mod.destroy();
      postMessage({ type: "altitude", png });
    } catch (e) {
      postMessage({ type: "error", message: String(e) });
    }
  }
};
