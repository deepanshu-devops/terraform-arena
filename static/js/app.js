const state = {
  challenges: [],
  current: null,
  files: {},
  activeFile: "main.tf",
  tab: "tests",
  view: "problem",
  result: null,
  jobId: null,
  jobChallengeId: null,
  polling: null,
  search: "",
  difficulty: "",
  level: "",
  tag: "",
  auth: null,
  challengeSeq: 0,
  loadingChallenge: false,
  stats: null,
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

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const text = await response.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch (_) {
    data = null;
  }
  if (!response.ok) {
    const detail =
      data && typeof data.detail === "string"
        ? data.detail
        : text || response.statusText || `HTTP ${response.status}`;
    const error = new Error(detail);
    error.status = response.status;
    throw error;
  }
  return data;
}

function toast(message) {
  const el = $("toast");
  el.textContent = message;
  el.classList.add("show");
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => el.classList.remove("show"), 3200);
}

function escapeHtml(text) {
  return String(text ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeAttr(text) {
  return escapeHtml(text).replaceAll('"', "&quot;");
}

function initials(name) {
  const words = String(name || "?").trim().split(/\s+/).filter(Boolean);
  const value = words.slice(0, 2).map((word) => word[0]).join("");
  return (value || "?").toUpperCase();
}

function avatarHtml(name, url, extraClass = "") {
  const cls = extraClass ? ` ${extraClass}` : "";
  if (url) {
    return `<img class="avatar-img${cls}" src="${escapeAttr(url)}" alt="" loading="lazy" referrerpolicy="no-referrer" />`;
  }
  return `<span class="avatar-fallback${cls}" aria-hidden="true">${escapeHtml(initials(name))}</span>`;
}

function setProfileAvatarElement(img, fallback, name, url) {
  if (url) {
    img.src = url;
    img.hidden = false;
    fallback.hidden = true;
  } else {
    img.removeAttribute("src");
    img.hidden = true;
    fallback.hidden = false;
    fallback.textContent = initials(name);
  }
}

function clearAuthErrorFromUrl() {
  const params = new URLSearchParams(window.location.search);
  const error = params.get("auth_error");
  if (!error) return;
  toast(`Google sign-in failed: ${error}`);
  params.delete("auth_error");
  const query = params.toString();
  const next = window.location.pathname + (query ? `?${query}` : "") + window.location.hash;
  window.history.replaceState({}, document.title, next);
}

/* --------------------------------- auth ---------------------------------- */
function renderAuth(me) {
  state.auth = me;
  const login = $("login-btn");
  const chip = $("profile-btn");
  if (!login || !chip) return;

  const user = me && me.user;
  if (user) {
    login.hidden = true;
    chip.hidden = false;
    const display = user.display_name || "Profile";
    $("profile-name").textContent = display;
    setProfileAvatarElement($("profile-avatar"), $("profile-initial"), display, user.avatar_url);
    chip.title = me.auth_enabled
      ? `Signed in with Google as ${display}`
      : "Local profile (Google sign-in is not configured)";
  } else {
    login.hidden = !(me && me.auth_enabled);
    chip.hidden = true;
  }
}

async function loadAuth() {
  try {
    const me = await api("/api/auth/me");
    renderAuth(me);
    return me;
  } catch (error) {
    renderAuth({ auth_enabled: false, authenticated: false, user: null, mode: "local" });
    return state.auth;
  }
}

function openProfiles() {
  $("profiles-drawer").classList.add("open");
  $("profiles-drawer").setAttribute("aria-hidden", "false");
  $("profiles-backdrop").classList.add("open");
  $("profiles-backdrop").setAttribute("aria-hidden", "false");
  refreshProfiles();
}

function closeProfiles() {
  $("profiles-drawer").classList.remove("open");
  $("profiles-drawer").setAttribute("aria-hidden", "true");
  $("profiles-backdrop").classList.remove("open");
  $("profiles-backdrop").setAttribute("aria-hidden", "true");
}

function renderProfileSelf(me, stats) {
  const panel = $("profile-self");
  const user = me && me.user;
  if (!user) {
    panel.innerHTML = `
      <div class="signin-card">
        <div class="signin-title">Sign in to keep your progress</div>
        <p>Use your Google account to save solved challenges, scores and submission history
        across visits. Other learners only see your display name, avatar and progress.</p>
        <a class="google-btn" href="/auth/google/login">Sign in with Google</a>
      </div>`;
    return;
  }

  const s = stats || state.stats || {};
  const byDifficulty = (s.by_difficulty || [])
    .map(
      (row) => `
      <div class="diff-progress-row">
        <span class="diff ${escapeAttr(row.difficulty)}">${escapeHtml(row.difficulty)}</span>
        <span class="diff-progress-track"><span style="width:${row.total ? Math.round((row.solved / row.total) * 100) : 0}%"></span></span>
        <span class="diff-progress-value">${row.solved || 0}/${row.total || 0}</span>
      </div>`,
    )
    .join("");

  const signOut = me.auth_enabled
    ? '<a class="ghost-btn signout-btn" href="/auth/logout">Sign out</a>'
    : '<span class="local-badge">Local profile</span>';

  panel.innerHTML = `
    <div class="profile-self-card">
      <div class="profile-self-head">
        ${avatarHtml(user.display_name, user.avatar_url, "avatar-lg")}
        <div class="profile-self-main">
          <div class="profile-self-name">${escapeHtml(user.display_name || "Learner")}</div>
          ${user.email ? `<div class="profile-self-email">${escapeHtml(user.email)}</div>` : ""}
          <div class="profile-self-provider">${
            me.auth_enabled ? "Google account" : "Google sign-in is not configured on this deployment"
          }</div>
        </div>
        ${signOut}
      </div>
      <div class="profile-stat-grid">
        <div><strong>${s.solved || 0}</strong><small>solved</small></div>
        <div><strong>${s.attempted || 0}</strong><small>attempted</small></div>
        <div><strong>${s.average_score || 0}</strong><small>avg score</small></div>
        <div><strong>${s.submissions || 0}</strong><small>submissions</small></div>
      </div>
      ${byDifficulty ? `<div class="section-title">Progress by difficulty</div><div class="diff-progress">${byDifficulty}</div>` : ""}
    </div>`;
}

function renderProfileList(data) {
  const list = $("profile-list");
  const note = $("profiles-note");
  const items = (data && data.items) || [];
  if (!items.length) {
    list.innerHTML = '<div class="empty-state small">No profiles yet. Be the first to solve a challenge.</div>';
  } else {
    list.innerHTML = items
      .map(
        (profile, index) => `
        <div class="profile-row${profile.is_self ? " self" : ""}">
          <div class="profile-rank">${index + 1}</div>
          ${avatarHtml(profile.display_name, profile.avatar_url)}
          <div class="profile-row-main">
            <div class="profile-row-name">
              ${escapeHtml(profile.display_name)}
              ${profile.is_self ? '<span class="you-tag">you</span>' : ""}
            </div>
            <div class="profile-row-meta">
              ${profile.email ? `${escapeHtml(profile.email)} · ` : ""}
              ${profile.solved || 0} solved · ${profile.attempted || 0} attempted · ${profile.submissions || 0} submissions
            </div>
          </div>
          <div class="profile-row-score"><strong>${profile.solved || 0}</strong><small>solved</small></div>
        </div>`,
      )
      .join("");
  }
  note.textContent =
    "Only display names, avatars and progress are shared. Email addresses are visible only to the signed-in owner.";
}

async function refreshProfiles() {
  const me = await loadAuth();
  const self = $("profile-self");
  self.innerHTML = '<div class="empty-state small">Loading your profile...</div>';
  $("profile-list").innerHTML = '<div class="empty-state small">Loading profiles...</div>';
  $("profiles-note").textContent = "";

  if (!me || !me.authenticated) {
    renderProfileSelf(me, null);
    $("profile-list").innerHTML =
      '<div class="empty-state small">Sign in with Google to compare progress with every learner.</div>';
    $("profiles-note").textContent = me && me.auth_enabled
      ? "Google sign-in is enabled on this deployment."
      : "Google sign-in is not configured. The local profile is used when credentials are absent.";
    return;
  }

  try {
    const stats = await api("/api/stats");
    state.stats = stats;
    renderProfileSelf(me, stats);
  } catch (error) {
    renderProfileSelf(me, null);
  }

  try {
    const data = await api("/api/profiles?limit=200");
    renderProfileList(data);
  } catch (error) {
    $("profile-list").innerHTML = `<div class="empty-state small">Could not load profiles: ${escapeHtml(
      error.message,
    )}</div>`;
    $("profiles-note").textContent = "";
  }
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
  const count = data.total || state.challenges.length;
  const brandSub = document.querySelector(".brand-sub");
  if (brandSub) brandSub.textContent = `${count} hands-on IaC challenges, level 0 to 5`;
  $("search").placeholder = `Search ${count} challenges...`;

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
  if (!state.current && !state.loadingChallenge && state.challenges.length) {
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
  const seq = ++state.challengeSeq;

  // Flush edits into the *old* challenge before detaching it.  Every file
  // write below is guarded by state.current, so an event that arrives while
  // the next request is in flight cannot leak old code into the new editor.
  if (state.current) saveActiveFile();

  // Detach the previous challenge completely: stop its poll loop and ignore
  // any in-flight result, so old code/results cannot appear in the new editor.
  clearTimeout(state.polling);
  state.polling = null;
  state.jobId = null;
  state.current = null;
  state.files = {};
  state.activeFile = "main.tf";
  state.result = null;
  state.jobChallengeId = null;
  state.loadingChallenge = true;
  closeResults();
  $("code").value = "";
  $("file-tabs").innerHTML = "";
  $("file-name").textContent = "loading...";
  $("submit-btn").disabled = true;
  $("submit-btn").textContent = "Run tests";
  refreshEditor();

  if (fromList) closeCatalog();
  if (isMobile()) setView("problem");

  try {
    const challenge = await api(`/api/challenges/${encodeURIComponent(key)}`);
    if (seq !== state.challengeSeq) return; // a newer selection won the race
    state.loadingChallenge = false;
    state.current = challenge;
    state.result = null;
    state.jobChallengeId = null;
    renderStatement(challenge);
    setupFiles(challenge);
    renderList();
    $("submit-btn").disabled = false;
  } catch (error) {
    if (seq !== state.challengeSeq) return;
    state.loadingChallenge = false;
    $("file-name").textContent = "main.tf";
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
  let saved = {};
  try {
    const raw = localStorage.getItem(storageKey(challenge));
    if (raw) saved = JSON.parse(raw);
  } catch (_) {
    saved = {};
  }
  if (!saved || typeof saved !== "object") saved = {};

  // Build from the starter allowlist only.  This drops stale files from a
  // previous challenge as well as anything malformed in localStorage.
  const files = {};
  for (const [name, content] of Object.entries(challenge.starter || {})) {
    files[name] = typeof saved[name] === "string" ? saved[name] : content;
  }
  state.files = files;
  state.activeFile = Object.keys(files)[0] || "main.tf";
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
  // Guard every write: while a challenge switch is in flight state.current is
  // null, and an input event from the old editor must be a no-op.
  if (!state.current) return;
  if (!(state.activeFile in state.files)) return;
  state.files[state.activeFile] = $("code").value;
  localStorage.setItem(storageKey(state.current), JSON.stringify(state.files));
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
  if (state.auth && state.auth.auth_enabled && !state.auth.authenticated) {
    openProfiles();
    toast("Sign in with Google to submit and save your progress.");
    return;
  }
  persistAll();

  const challenge = state.current;
  const seq = state.challengeSeq;
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
        challenge: String(challenge.number),
        files: state.files,
      }),
    });
    if (seq !== state.challengeSeq) {
      // The learner moved to another challenge while this request was queued.
      // The submission is still recorded, but its result must not touch the
      // new challenge's editor or verdict panel.
      toast("Previous submission queued. Reopen that challenge to see its result.");
      refreshStats();
      loadCatalog();
      finishSubmit();
      return;
    }
    state.jobId = response.job_id;
    state.jobChallengeId = response.challenge_id;
    pollJob(response.job_id, response.challenge_id);
  } catch (error) {
    if (seq !== state.challengeSeq) {
      finishSubmit();
      return;
    }
    button.disabled = false;
    button.textContent = "Run tests";
    if (error.status === 401) {
      openProfiles();
      toast("Sign in with Google to submit and save your progress.");
    } else {
      toast(`Submission failed: ${error.message}`);
    }
  }
}

function pollJob(jobId, challengeId) {
  clearTimeout(state.polling);
  state.polling = setTimeout(async () => {
    if (state.jobId !== jobId) return;
    try {
      const job = await api(`/api/jobs/${jobId}`);
      if (state.jobId !== jobId) return;
      if (job.state === "done" && job.result) {
        const stillCurrent = state.current && state.current.id === challengeId;
        if (stillCurrent) {
          renderResults(job.result);
          state.current.progress = job.result.progress || state.current.progress;
        } else {
          toast("Submission finished. Reopen that challenge to see the result.");
        }
        refreshStats();
        loadCatalog();
        finishSubmit();
      } else if (job.state === "error") {
        toast(`Evaluation error: ${job.error}`);
        finishSubmit();
      } else {
        $("verdict-sub").textContent =
          job.state === "running" ? "Evaluating submission..." : "Queued...";
        pollJob(jobId, challengeId);
      }
    } catch (error) {
      if (state.jobId !== jobId) return;
      toast(`Polling failed: ${error.message}`);
      finishSubmit();
    }
  }, 500);
}

function finishSubmit() {
  const button = $("submit-btn");
  button.disabled = !state.current;
  button.textContent = "Run tests";
}

async function refreshStats() {
  try {
    const stats = await api("/api/stats");
    state.stats = stats;
    $("stat-solved").textContent = stats.solved;
    $("stat-total").textContent = stats.total_challenges;
    $("stat-avg").textContent = stats.average_score;
    $("stat-subs").textContent = stats.submissions;
    return stats;
  } catch (_) {
    return null;
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
$("profiles-btn").addEventListener("click", openProfiles);
$("profile-btn").addEventListener("click", openProfiles);
$("close-profiles").addEventListener("click", closeProfiles);
$("profiles-backdrop").addEventListener("click", closeProfiles);
$("refresh-profiles").addEventListener("click", refreshProfiles);

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
    closeProfiles();
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
    clearAuthErrorFromUrl();
    await loadAuth();
    await refreshStats();
    await loadTerraformStatus();
    await loadCatalog();
  } catch (error) {
    toast(`Could not reach the API: ${error.message}`);
  }
})();
