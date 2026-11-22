const STATION = { lat: 53.1, lon: 8.8 };
const REROUTE_M = 25;
const BREMEN_VIEWBOX = "8.6,53.2,9.0,52.95";

const state = {
  system: "GPS",
  mode: "none",
  err: null,
  believed: null,
  dest: null,
  routedFrom: null,
  routing: false,
};

// ---------- map ----------
const map = L.map("map").setView([STATION.lat, STATION.lon], 15);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "© OpenStreetMap contributors",
}).addTo(map);

const truePos = L.latLng(STATION.lat, STATION.lon);
const trueMarker = L.circleMarker(truePos, {
  radius: 7, color: "#fff", weight: 2, fillColor: "#1c1c1c", fillOpacity: 1,
}).addTo(map);
const believedMarker = L.circleMarker(truePos, {
  radius: 7, color: "#fff", weight: 2, fillColor: "#c2331f", fillOpacity: 1,
}).addTo(map);
const destMarker = L.circleMarker([0, 0], {
  radius: 6, color: "#1c1c1c", weight: 2, fillColor: "#fff", fillOpacity: 1,
});
const routeTrue = L.polyline([], { color: "#8d8a82", weight: 4, dashArray: "8 8" }).addTo(map);
const routeShown = L.polyline([], { color: "#c2331f", weight: 5 }).addTo(map);

// ---------- helpers ----------
const $ = (id) => document.getElementById(id);

function setStatus(msg) { $("status").textContent = msg || ""; }

function offsetLatLon(lat, lon, eastM, northM) {
  const dlat = northM / 111320;
  const dlon = eastM / (111320 * Math.cos((lat * Math.PI) / 180));
  return L.latLng(lat + dlat, lon + dlon);
}

function fmtDist(m) {
  const a = Math.abs(m);
  return a < 1000 ? `${m.toFixed(1)} m` : `${(m / 1000).toFixed(2)} km`;
}

function fmtClock(s) {
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
}

// ---------- geocoding and routing ----------
async function geocode(query) {
  const url =
    "https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&countrycodes=de" +
    `&viewbox=${BREMEN_VIEWBOX}&q=${encodeURIComponent(query)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Adresssuche nicht erreichbar");
  const hits = await res.json();
  if (!hits.length) throw new Error("Ziel nicht gefunden");
  return L.latLng(parseFloat(hits[0].lat), parseFloat(hits[0].lon));
}

async function getRoute(from, to) {
  const url =
    "https://router.project-osrm.org/route/v1/driving/" +
    `${from.lng},${from.lat};${to.lng},${to.lat}?overview=full&geometries=geojson`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Routing nicht erreichbar");
  const data = await res.json();
  if (data.code !== "Ok") throw new Error("Keine Route gefunden");
  return data.routes[0].geometry.coordinates.map(([lon, lat]) => [lat, lon]);
}

async function drawRoutes({ both }) {
  if (!state.dest || !state.believed || state.routing) return;
  state.routing = true;
  const from = state.believed;
  try {
    if (both) {
      routeTrue.setLatLngs(await getRoute(truePos, state.dest));
    }
    routeShown.setLatLngs(await getRoute(from, state.dest));
    state.routedFrom = from;
    setStatus("");
  } catch (e) {
    setStatus(e.message);
  } finally {
    state.routing = false;
  }
}

// ---------- live error ----------
async function tick() {
  try {
    const res = await fetch(`/api/error?system=${state.system}&mode=${state.mode}`);
    if (!res.ok) throw new Error();
    state.err = await res.json();
  } catch {
    setStatus("Server nicht erreichbar");
    return;
  }
  const e = state.err;
  const k = $("exag").checked ? 50 : 1;

  state.believed = offsetLatLon(STATION.lat, STATION.lon, e.east_m * k, e.north_m * k);
  believedMarker.setLatLng(state.believed);

  $("h-time").textContent = fmtClock(e.sim_s);
  $("h-sec").textContent = state.mode === "none" ? fmtDist(e.secular_m) : "korrigiert";
  $("h-ecc").textContent = `${e.ecc_ns.toFixed(1)} ns`;
  $("h-sag").textContent = `${e.sagnac_ns.toFixed(1)} ns`;
  $("h-tot").textContent = fmtDist(e.range_m);

  if (state.dest && (!state.routedFrom || state.believed.distanceTo(state.routedFrom) > REROUTE_M)) {
    drawRoutes({ both: false });
  }
}

// ---------- controls ----------
$("search").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const q = $("dest").value.trim();
  if (!q) return;
  setStatus("Suche …");
  try {
    state.dest = await geocode(q);
    destMarker.setLatLng(state.dest).addTo(map);
    state.routedFrom = null;
    await drawRoutes({ both: true });
    map.fitBounds(L.latLngBounds([truePos, state.believed, state.dest]).pad(0.2));
  } catch (e) {
    setStatus(e.message);
  }
});

function bindSegment(id, key) {
  $(id).addEventListener("click", (ev) => {
    const b = ev.target.closest("button");
    if (!b) return;
    state[key] = b.dataset.v;
    for (const x of $(id).children) x.classList.toggle("on", x === b);
    tick();
  });
}
bindSegment("systems", "system");
bindSegment("modes", "mode");

$("exag").addEventListener("change", tick);

$("reset").addEventListener("click", async () => {
  await fetch("/api/reset", { method: "POST" });
  state.routedFrom = null;
  tick();
});

tick();
setInterval(tick, 1000);
