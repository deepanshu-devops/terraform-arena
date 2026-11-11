const state = {
  challenges: [],
  current: null,
  files: {},
  activeFile: "main.tf",
  tab: "tests",
  view: "problem",
  result: null,
  jobId: null,
  polling: null,
  search: "",
  difficulty: "",
  level: "",
  tag: "",
};

const $ = (id) => document.getElementById(id);
const MOBILE_QUERY = window.matchMedia("(max-width: 900px)");
const isMobile = () => MOBILE_QUERY.matches;

function setView(view, focus = false) {
  state.view = view;
  const workspace = $("workspace");
  workspace.classList.toggle("view-problem", view === "problem");
  workspace.classList.toggle("view-code", view === "code");
  document.querySelectorAll(".view-btn").forEach((button) => {
    const active = button.dataset.view === view;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", active ? "true" : "false");
  });
  if (view === "code" && focus) {
    requestAnimationFrame(() => $("code").focus());
  }
}

function openCatalog() {
  $("sidebar").classList.add("open");
  $("sidebar-backdrop").classList.add("open");
  $("catalog-toggle").setAttribute("aria-expanded", "true");
  $("sidebar-backdrop").setAttribute("aria-hidden", "false");
}

function closeCatalog() {
  $("sidebar").classList.remove("open");
  $("sidebar-backdrop").classList.remove("open");
  $("catalog-toggle").setAttribute("aria-expanded", "false");
  $("sidebar-backdrop").setAttribute("aria-hidden", "true");
}

async function api(path, options) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  return response.json();
}

function toast(message) {
  const el = $("toast");
  el.textContent = message;
  el.classList.add("show");
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => el.classList.remove("show"), 2600);
}

function escapeHtml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

const KEYWORDS =
  "resource|data|variable|output|module|provider|terraform|locals|required_providers|backend|validation|lifecycle|dynamic|for_each|count|depends_on|source|version|moved|import|true|false|null";

function highlight(code) {
  let html = escapeHtml(code);
  const stash = [];
  const put = (value) => {
    stash.push(value);
    // Private-use sentinel so later token passes (digits, keywords, attrs)
    // cannot corrupt the placeholder.
    return `\u0000${String.fromCharCode(0xe000 + stash.length - 1)}\u0000`;
  };

  // strings first (escapeHtml leaves double quotes intact)
  html = html.replace(/"(?:[^"\\]|\\.)*"/g, (match) => {
    const body = match.replace(/\$\{[^}]*\}/g, (expr) => `<span class="tok-interp">${expr}</span>`);
    return put(`<span class="tok-string">${body}</span>`);
  });
  // comments
  html = html.replace(/(#[^\n]*|\/\/[^\n]*)/g, (match) => put(`<span class="tok-comment">${match}</span>`));
  // resource types
  html = html.replace(/\b(aws_[a-z0-9_]+|docker_[a-z0-9_]+)\b/g, '<span class="tok-type">$1</span>');
  // keywords / booleans
  html = html.replace(new RegExp(`\\b(${KEYWORDS})\\b`, "g"), '<span class="tok-keyword">$1</span>');
  // numbers
  html = html.replace(/\b\d+(?:\.\d+)?\b/g, '<span class="tok-number">$&</span>');
  // attribute names at the start of a line
  html = html.replace(/^(\s*)([A-Za-z_][\w-]*)(\s*=)/gm, '$1<span class="tok-attr">$2</span>$3');

  return html.replace(/\u0000([\ue000-\uf8ff])\u0000/g, (_, sentinel) =>
    stash[sentinel.charCodeAt(0) - 0xe000],
  );
}

/* ------------------------------- catalog -------------------------------- */
async function loadCatalog() {
  const data = await api("/api/challenges?limit=500");
  state.challenges = data.items;

  const levels = new Map();
  state.challenges.forEach((c) => {
    if (c.level !== undefined && c.level !== null) {
      levels.set(String(c.level), c.level_name || `Level ${c.level}`);
    }
  });
  const levelSelect = $("level-filter");
  const previousLevel = state.level || levelSelect.value;
  levelSelect.innerHTML = '<option value="">All levels</option>';
  [...levels.entries()]
    .sort((a, b) => Number(a[0]) - Number(b[0]))
    .forEach(([value, label]) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = `L${value} · ${label}`;
      levelSelect.appendChild(option);
    });
  if (previousLevel && levels.has(previousLevel)) {
    levelSelect.value = previousLevel;
    state.level = previousLevel;
  } else {
    levelSelect.value = "";
    state.level = "";
  }

  const tags = new Set();
  state.challenges.forEach((c) => c.tags.forEach((t) => tags.add(t)));
  const select = $("tag-filter");
  const previousTag = state.tag || select.value;
  select.innerHTML = '<option value="">All tags</option>';
  [...tags].sort().forEach((tag) => {
    const option = document.createElement("option");
    option.value = tag;
    option.textContent = tag;
    select.appendChild(option);
  });
  if (previousTag && tags.has(previousTag)) {
    select.value = previousTag;
    state.tag = previousTag;
  } else {
    select.value = "";
    state.tag = "";
  }

  renderList();
  if (!state.current && state.challenges.length) {
    selectChallenge(state.challenges[0].number);
  }
}

function visibleChallenges() {
  const q = state.search.toLowerCase();
  return state.challenges.filter((c) => {
    if (state.difficulty && c.difficulty !== state.difficulty) return false;
    if (state.level && String(c.level) !== state.level) return false;
    if (state.tag && !c.tags.includes(state.tag)) return false;
    if (!q) return true;
    return (
      c.title.toLowerCase().includes(q) ||
      c.id.toLowerCase().includes(q) ||
      String(c.number) === q ||
      (c.level_name || "").toLowerCase().includes(q)
    );
  });
}

function renderList() {
  const list = $("challenge-list");
  const items = visibleChallenges();
  list.innerHTML = "";
  if (!items.length) {
    list.innerHTML = '<div class="empty-state small">No challenges match the filters.</div>';
    return;
  }
  items.forEach((c) => {
    const row = document.createElement("div");
    row.className = "challenge-item" + (state.current && state.current.id === c.id ? " active" : "");
    const solved = c.progress && c.progress.status === "PASS";
    row.innerHTML = `
      <div class="ci-num">${String(c.number).padStart(3, "0")}</div>
      <div class="ci-main">
        <div class="ci-title">${escapeHtml(c.title)}</div>
        <div class="ci-meta">
          <span class="ci-level">L${c.level}</span>
          <span class="diff ${c.difficulty}">${c.difficulty}</span>
          <span>${c.points} pts</span>
          <span>${c.test_count} tests</span>
        </div>
      </div>
      <div class="ci-dot ${solved ? "solved" : ""}" title="${solved ? "Solved" : "Unsolved"}"></div>
    `;
    row.addEventListener("click", () => selectChallenge(c.number, true));
    list.appendChild(row);
  });
}

/* ------------------------------ challenge ------------------------------- */
async function selectChallenge(key, fromList = false) {
  try {
    const challenge = await api(`/api/challenges/${encodeURIComponent(key)}`);
    state.current = challenge;
    state.result = null;
    closeResults();
    if (fromList) closeCatalog();
    if (isMobile()) setView("problem");
    renderStatement(challenge);
    setupFiles(challenge);
    renderList();
    $("submit-btn").disabled = false;
  } catch (error) {
    toast(`Could not load challenge: ${error.message}`);
  }
}

function renderStatement(challenge) {
  const statement = $("statement");
  const variablesRows = challenge.variables.length
    ? challenge.variables
        .map(
          (v) =>
            `<tr><td><code>${escapeHtml(v.name)}</code></td><td><code>${escapeHtml(
              v.type || "string",
            )}</code></td><td>${
              v.default === undefined ? "<em>required</em>" : `<code>${escapeHtml(JSON.stringify(v.default))}</code>`
            }</td></tr>`,
        )
        .join("")
    : '<tr><td colspan="3">No input variables.</td></tr>';

  const resources = challenge.expected_resources.length
    ? challenge.expected_resources.map((r) => `<span class="resource-chip">${escapeHtml(r)}</span>`).join("")
    : '<span class="resource-chip">see constraints</span>';

  const outputs = challenge.expected_outputs.length
    ? challenge.expected_outputs.map((o) => `<span class="resource-chip">${escapeHtml(o)}</span>`).join("")
    : '<span class="resource-chip">none</span>';

  const progress = challenge.progress
    ? `<div class="hidden-note">Your best: ${challenge.progress.best_score}/100 · ${
        challenge.progress.status === "PASS" ? "solved" : "not solved yet"
      } · ${challenge.progress.attempts} attempt(s)</div>`
    : "";

  const focus = challenge.focus || {};
  const focusHtml = focus.title
    ? `
    <div class="focus-card">
      <div class="section-title">What to complete</div>
      <div class="focus-file"><code>${escapeHtml(focus.file || "main.tf")}</code></div>
      <div class="focus-title">${escapeHtml(focus.title)}</div>
      ${focus.todo ? `<div class="focus-todo">${escapeHtml(focus.todo)}</div>` : ""}
    </div>`
    : "";

  statement.innerHTML = `
    <div class="statement-meta">
      <span class="badge level">${escapeHtml(challenge.level_name || `Level ${challenge.level}`)}</span>
      <span class="badge ${challenge.difficulty}">${challenge.difficulty}</span>
      <span class="badge">${challenge.points} pts</span>
      <span class="badge">Challenge ${String(challenge.number).padStart(3, "0")}</span>
      ${challenge.tags.map((t) => `<span class="badge">${escapeHtml(t)}</span>`).join("")}
    </div>
    <h1>${escapeHtml(challenge.title)}</h1>
    <div class="scenario">${escapeHtml(challenge.scenario)}</div>
    ${focusHtml}

    <div class="section-title">Constraints</div>
    <ul class="constraints">
      ${challenge.constraints.map((c) => `<li>${escapeHtml(c)}</li>`).join("")}
    </ul>

    <div class="section-title">Input variables</div>
    <div class="table-scroll">
      <table class="data-table">
        <thead><tr><th>Name</th><th>Type</th><th>Default</th></tr></thead>
        <tbody>${variablesRows}</tbody>
      </table>
    </div>

    <div class="section-title">Expected resources</div>
    <div class="resource-list">${resources}</div>

    <div class="section-title">Expected outputs</div>
    <div class="resource-list">${outputs}</div>

    <div class="section-title">Evaluation</div>
    <div class="hidden-note">
      ${challenge.test_count} hidden tests · architecture drift detection · formatting and
      variable-compliance grading. Test details are revealed only after you run the tests.
    </div>
    ${progress}
  `;
}

/* -------------------------------- files --------------------------------- */
function storageKey(challenge) {
  return `arena:files:${challenge.id}`;
}

function setupFiles(challenge) {
  let files = {};
  try {
    const saved = localStorage.getItem(storageKey(challenge));
    if (saved) files = JSON.parse(saved);
  } catch (_) {
    files = {};
  }
  for (const [name, content] of Object.entries(challenge.starter)) {
    if (!(name in files)) files[name] = content;
  }
  state.files = files;
  state.activeFile = Object.keys(challenge.starter)[0] || Object.keys(files)[0] || "main.tf";
  renderTabs();
  loadActiveFile();
}

function renderTabs() {
  const tabs = $("file-tabs");
  tabs.innerHTML = "";
  Object.keys(state.files).forEach((name) => {
    const button = document.createElement("button");
    button.className = "tab" + (name === state.activeFile ? " active" : "");
    button.textContent = name;
    button.addEventListener("click", () => {
      saveActiveFile();
      state.activeFile = name;
      renderTabs();
      loadActiveFile();
    });
    tabs.appendChild(button);
  });
}

function loadActiveFile() {
  const code = $("code");
  code.value = state.files[state.activeFile] ?? "";
  $("file-name").textContent = state.activeFile;
  refreshEditor();
  if (!isMobile() || state.view === "code") code.focus();
}

function saveActiveFile() {
  state.files[state.activeFile] = $("code").value;
  if (state.current) {
    localStorage.setItem(storageKey(state.current), JSON.stringify(state.files));
  }
  const el = $("save-state");
  el.textContent = "autosaved locally";
}

function persistAll() {
  saveActiveFile();
}

function refreshEditor() {
  const code = $("code");
  $("highlight").innerHTML = highlight(code.value) + "\n";
  const lineCount = code.value.split("\n").length;
  $("gutter").textContent = Array.from({ length: lineCount }, (_, i) => i + 1).join("\n");
  syncScroll();
}

function syncScroll() {
  const code = $("code");
  const pre = $("highlight");
  const gutter = $("gutter");
  pre.scrollTop = code.scrollTop;
  pre.scrollLeft = code.scrollLeft;
  gutter.scrollTop = code.scrollTop;
}

function updateCursor() {
  const code = $("code");
  const upto = code.value.slice(0, code.selectionStart);
  const lines = upto.split("\n");
  const line = lines.length;
  const col = lines[lines.length - 1].length + 1;
  $("cursor-pos").textContent = `Ln ${line}, Col ${col}`;
}

/* ------------------------------- results -------------------------------- */
function openResults() {
  $("results-drawer").classList.add("open");
  $("results-drawer").setAttribute("aria-hidden", "false");
}
function closeResults() {
  $("results-drawer").classList.remove("open");
  $("results-drawer").setAttribute("aria-hidden", "true");
}

function renderResults(result) {
  state.result = result;
  const verdict = $("verdict");
  verdict.textContent = `[${result.status}]`;
  verdict.className = "verdict " + (result.status === "PASS" ? "pass" : "fail");
  $("verdict-sub").textContent =
    `${result.score}/100 · ${result.passed}/${result.total} tests · ${result.duration_ms} ms · ${result.challenge_title}`;
  state.tab = "tests";
  [...document.querySelectorAll(".rtab")].forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.rtab === "tests");
  });
  renderResultTab("tests");
  openResults();
}

function gradeClass(score) {
  if (score >= 85) return "grade-good";
  if (score >= 60) return "grade-mid";
  return "grade-bad";
}

function renderResultTab(tab) {
  const body = $("results-body");
  const result = state.result;
  if (!result) {
    body.innerHTML = '<div class="empty-state small">Run the tests to see the structured verdict.</div>';
    return;
  }

  if (tab === "tests") {
    const tf = result.terraform;
    const tfNote =
      tf && !tf.ran
        ? `<div class="hidden-note" style="margin-bottom:12px">Terraform CLI: ${escapeHtml(
            tf.reason || "not run",
          )}. Static checks passed are authoritative.</div>`
        : "";
    body.innerHTML =
      tfNote +
      result.tests
        .map(
          (t) => `
        <div class="test-row ${t.passed ? "" : "fail"}">
          <span class="test-badge ${t.passed ? "pass" : "fail"}">${t.passed ? "PASS" : "FAIL"}</span>
          <div class="test-main">
            <div class="test-title">${escapeHtml(t.title)}</div>
            <div class="test-cat">${escapeHtml(t.category)}</div>
            ${t.passed ? "" : `<div class="test-detail">${escapeHtml(t.detail)}</div>`}
          </div>
        </div>`,
        )
        .join("");
  } else if (tab === "security") {
    const blocked = result.security.blocked || [];
    const warnings = result.security.warnings || [];
    body.innerHTML = `
      <div class="section-title">Blocked</div>
      ${
        blocked.length
          ? `<ul class="issue-list">${blocked.map((x) => `<li class="bad">${escapeHtml(x)}</li>`).join("")}</ul>`
          : '<div class="hidden-note">No policy violations. Clean.</div>'
      }
      <div class="section-title">Warnings</div>
      ${
        warnings.length
          ? `<ul class="issue-list">${warnings.map((x) => `<li>${escapeHtml(x)}</li>`).join("")}</ul>`
          : "<p>None.</p>"
      }
    `;
  } else if (tab === "formatting") {
    const f = result.formatting;
    body.innerHTML = `
      <div class="grade-line">
        <span class="grade-big ${gradeClass(f.score)}">${f.grade}</span>
        <span>${f.score}/100 formatting score</span>
      </div>
      <div class="meter"><div style="width:${f.score}%"></div></div>
      ${
        f.issues.length
          ? `<ul class="issue-list">${f.issues.map((x) => `<li>${escapeHtml(x)}</li>`).join("")}</ul>`
          : '<div class="hidden-note">terraform fmt-ready. No issues found.</div>'
      }
    `;
  } else if (tab === "variables") {
    const v = result.variables;
    body.innerHTML = `
      <div class="grade-line">
        <span class="grade-big ${gradeClass(v.score)}">${v.grade}</span>
        <span>${v.score}/100 variable compliance</span>
      </div>
      <div class="meter"><div style="width:${v.score}%"></div></div>
      ${v.checks
        .map(
          (c) => `
        <div class="test-row ${c.issues.length ? "fail" : ""}">
          <span class="test-badge ${c.issues.length ? "fail" : "pass"}">${
            c.issues.length ? "FAIL" : "PASS"
          }</span>
          <div class="test-main">
            <div class="test-title">${escapeHtml(c.name)}</div>
            ${
              c.issues.length
                ? `<div class="test-detail">${escapeHtml(c.issues.join("; "))}</div>`
                : ""
            }
          </div>
        </div>`,
        )
        .join("")}
    `;
  } else if (tab === "drift") {
    const drift = result.drift || [];
    body.innerHTML = drift.length
      ? `<ul class="issue-list">${drift
          .map(
            (d) =>
              `<li class="${d.severity === "error" ? "bad" : ""}">[${escapeHtml(
                d.severity,
              )}] ${escapeHtml(d.message)}</li>`,
          )
          .join("")}</ul>`
      : '<div class="hidden-note">No architectural drift detected.</div>';
  }
}

/* -------------------------------- submit -------------------------------- */
async function submit() {
  if (!state.current) return;
  persistAll();

  const button = $("submit-btn");
  button.disabled = true;
  button.textContent = "Running...";
  $("verdict").textContent = "[...]";
  $("verdict").className = "verdict";
  $("verdict-sub").textContent = "Queued for evaluation";
  openResults();

  try {
    const response = await api("/api/submit", {
      method: "POST",
      body: JSON.stringify({
        challenge: String(state.current.number),
        files: state.files,
      }),
    });
    state.jobId = response.job_id;
    pollJob(response.job_id);
  } catch (error) {
    button.disabled = false;
    button.textContent = "Run tests";
    toast(`Submission failed: ${error.message}`);
  }
}

function pollJob(jobId) {
  clearTimeout(state.polling);
  state.polling = setTimeout(async () => {
    try {
      const job = await api(`/api/jobs/${jobId}`);
      if (job.state === "done" && job.result) {
        renderResults(job.result);
        refreshStats();
        loadCatalog();
        finishSubmit();
      } else if (job.state === "error") {
        toast(`Evaluation error: ${job.error}`);
        finishSubmit();
      } else {
        $("verdict-sub").textContent =
          job.state === "running" ? "Evaluating submission..." : "Queued...";
        pollJob(jobId);
      }
    } catch (error) {
      toast(`Polling failed: ${error.message}`);
      finishSubmit();
    }
  }, 500);
}

function finishSubmit() {
  const button = $("submit-btn");
  button.disabled = false;
  button.textContent = "Run tests";
}

async function refreshStats() {
  try {
    const stats = await api("/api/stats");
    $("stat-solved").textContent = stats.solved;
    $("stat-total").textContent = stats.total_challenges;
    $("stat-avg").textContent = stats.average_score;
    $("stat-subs").textContent = stats.submissions;
  } catch (_) {
    /* ignore */
  }
}

async function loadTerraformStatus() {
  try {
    const status = await api("/api/terraform/status");
    const pill = $("tf-status");
    if (status.validation_enabled) {
      pill.textContent = "terraform live";
      pill.className = "pill pill-good";
    } else if (status.available) {
      pill.textContent = "tf detected · static";
      pill.className = "pill pill-warn";
    } else {
      pill.textContent = "static engine";
      pill.className = "pill pill-muted";
    }
    pill.title = status.note;
  } catch (_) {
    /* ignore */
  }
}

/* -------------------------------- events -------------------------------- */
$("code").addEventListener("input", () => {
  saveActiveFile();
  refreshEditor();
  updateCursor();
});
$("code").addEventListener("scroll", syncScroll);
$("code").addEventListener("keyup", updateCursor);
$("code").addEventListener("click", updateCursor);
$("code").addEventListener("keydown", (event) => {
  if (event.key === "Tab") {
    event.preventDefault();
    const code = event.target;
    const start = code.selectionStart;
    const end = code.selectionEnd;
    code.value = code.value.slice(0, start) + "  " + code.value.slice(end);
    code.selectionStart = code.selectionEnd = start + 2;
    saveActiveFile();
    refreshEditor();
    updateCursor();
  }
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    event.preventDefault();
    submit();
  }
});

$("submit-btn").addEventListener("click", submit);
$("close-results").addEventListener("click", closeResults);

$("catalog-toggle").addEventListener("click", () => {
  if ($("sidebar").classList.contains("open")) closeCatalog();
  else openCatalog();
});
$("sidebar-backdrop").addEventListener("click", closeCatalog);
document.querySelectorAll(".view-btn").forEach((button) => {
  button.addEventListener("click", () => setView(button.dataset.view, true));
});

const handleViewportChange = (event) => {
  if (!event.matches) closeCatalog();
};
if (MOBILE_QUERY.addEventListener) {
  MOBILE_QUERY.addEventListener("change", handleViewportChange);
} else {
  MOBILE_QUERY.addListener(handleViewportChange);
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeCatalog();
    closeResults();
  }
});

document.querySelectorAll(".rtab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".rtab").forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    renderResultTab(tab.dataset.rtab);
  });
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    document.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
    chip.classList.add("active");
    state.difficulty = chip.dataset.diff;
    renderList();
  });
});

$("search").addEventListener("input", (event) => {
  state.search = event.target.value;
  renderList();
});

$("level-filter").addEventListener("change", (event) => {
  state.level = event.target.value;
  renderList();
});

$("tag-filter").addEventListener("change", (event) => {
  state.tag = event.target.value;
  renderList();
});

$("reset-files").addEventListener("click", () => {
  if (!state.current) return;
  if (!confirm("Reset all files back to the starter scaffold?")) return;
  localStorage.removeItem(storageKey(state.current));
  setupFiles(state.current);
  toast("Starter files restored");
});

window.addEventListener("beforeunload", () => {
  if (state.current) saveActiveFile();
});

/* --------------------------------- boot --------------------------------- */
(async function boot() {
  try {
    setView("problem");
    await refreshStats();
    await loadTerraformStatus();
    await loadCatalog();
  } catch (error) {
    toast(`Could not reach the API: ${error.message}`);
  }
})();
