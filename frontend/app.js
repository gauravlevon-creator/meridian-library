/* Meridian Library — frontend SPA (vanilla JS, no build step) */

const API = "/api";

const state = {
  user: null,           // {id, name, email} or {id:null, name:'Guest', guest:true}
  stats: null,
  genres: [],
  wizard: { roomId: null, date: todayStr(), slot: null, name: "" },
  catalogue: { q: "", genre: "All Genres", status: "All", aiMode: false, results: [], aiResults: null },
  mobileNavOpen: false,
  loginTab: "signin",
};

function todayStr() {
  return new Date().toISOString().slice(0, 10);
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (state.user && state.user.token) {
    headers["Authorization"] = "Bearer " + state.user.token;
  }
  const res = await fetch(API + path, { ...options, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    let msg = data.detail || "Something went wrong.";
    if (Array.isArray(msg)) msg = msg.map((e) => e.msg || JSON.stringify(e)).join(" ");
    throw new Error(msg);
  }
  return data;
}

function saveSession(user) {
  state.user = user;
  if (user && user.token) {
    localStorage.setItem("meridian_session", JSON.stringify(user));
  } else {
    localStorage.removeItem("meridian_session");
  }
}

function clearSession() {
  state.user = null;
  localStorage.removeItem("meridian_session");
}

function toast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.style.display = "block";
  clearTimeout(toast._t);
  toast._t = setTimeout(() => (el.style.display = "none"), 2600);
}

/* ---------------- icons ---------------- */
const icon = {
  book: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5v-17Z"/><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/></svg>`,
  scroll: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 21h8a3 3 0 0 0 3-3V7a2 2 0 0 0-2-2H9"/><path d="M8 21a3 3 0 0 1-3-3V5a2 2 0 0 1 2-2h7v3"/></svg>`,
  newspaper: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="13" height="14" rx="1"/><path d="M19 9h2v9a2 2 0 0 1-2 2H6"/><path d="M6.5 9h6M6.5 12.5h6M6.5 16h3.5"/></svg>`,
  map: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2Z"/><path d="M9 4v14M15 6v14"/></svg>`,
  calendar: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>`,
  stamp: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="6" y="3" width="12" height="9" rx="1"/><path d="M4 21h16M9 12v4h6v-4"/></svg>`,
  search: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>`,
  user: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="4"/><path d="M4 20c1.5-4 5-6 8-6s6.5 2 8 6"/></svg>`,
  check: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="20 6 9 17 4 12"/></svg>`,
  chevron: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="9 18 15 12 9 6"/></svg>`,
  menu: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`,
  close: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>`,
  sparkle: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/></svg>`,
};

function initials(name) {
  if (!name) return "?";
  return name.split(" ").map((p) => p[0]).slice(0, 2).join("").toUpperCase();
}

/* ---------------- router ---------------- */
window.addEventListener("hashchange", render);
window.addEventListener("DOMContentLoaded", boot);

async function boot() {
  try {
    state.stats = await api("/stats");
  } catch (e) {}

  const saved = localStorage.getItem("meridian_session");
  if (saved) {
    try {
      state.user = JSON.parse(saved);
      // verify the token is still valid; if not, fall back to the login screen
      await api("/me");
    } catch (e) {
      clearSession();
    }
  }
  render();
}

function navigate(hash) {
  window.location.hash = hash;
}

function render() {
  const root = document.getElementById("app");
  if (!state.user) {
    root.innerHTML = "";
    root.appendChild(renderLogin());
    return;
  }
  const route = (window.location.hash || "#/home").replace("#", "");
  root.innerHTML = "";
  root.appendChild(renderShell(route));
}

/* ---------------- shell ---------------- */
function renderShell(route) {
  const wrap = el("div");
  wrap.appendChild(renderTopnav(route));
  const main = el("main");
  main.appendChild(renderRoute(route));
  wrap.appendChild(main);
  return wrap;
}

function renderRoute(route) {
  if (route.startsWith("/rooms")) return renderRooms();
  if (route.startsWith("/book")) return renderBookWizard();
  if (route.startsWith("/catalogue")) return renderCatalogue();
  if (route.startsWith("/events")) return renderEvents();
  if (route.startsWith("/account")) return renderAccount();
  return renderHome();
}

function renderTopnav(route) {
  const nav = el("header", "topnav");
  const inner = el("div", "topnav-inner");

  const brand = el("a", "brand");
  brand.href = "#/home";
  brand.innerHTML = `<span class="brand-mark">M</span><span class="brand-name">Meridian Library</span>`;
  inner.appendChild(brand);

  const links = [
    ["Home", "/home"], ["Rooms", "/rooms"], ["Book Slot", "/book"],
    ["My Stamps", "/account"], ["Catalogue", "/catalogue"], ["Events", "/events"],
  ];
  const navLinks = el("nav", "nav-links");
  links.forEach(([label, href]) => {
    const a = el("a");
    a.href = "#" + href;
    a.textContent = label;
    if (route === href || (href !== "/home" && route.startsWith(href))) a.className = "active";
    navLinks.appendChild(a);
  });
  inner.appendChild(navLinks);

  const right = el("div", "nav-right");
  if (state.user.guest) {
    const chip = el("a", "btn btn-dark");
    chip.href = "#/account";
    chip.textContent = "Sign in";
    chip.onclick = (e) => { e.preventDefault(); clearSession(); render(); };
    right.appendChild(chip);
  } else {
    const chip = el("div", "user-chip");
    chip.innerHTML = `<span class="avatar">${initials(state.user.name)}</span><span>${state.user.name}</span>`;
    right.appendChild(chip);
    const signout = el("button", "signout");
    signout.textContent = "Sign out";
    signout.onclick = async () => {
      try { await api("/auth/logout", { method: "POST" }); } catch (e) {}
      clearSession();
      navigate("#/home");
      render();
    };
    right.appendChild(signout);
  }

  const toggleWrap = el("div", "mobile-toggle-wrap");
  const toggleBtn = el("button", "mobile-toggle");
  toggleBtn.innerHTML = state.mobileNavOpen ? icon.close : icon.menu;
  toggleBtn.style.display = "none";
  toggleBtn.onclick = () => { state.mobileNavOpen = !state.mobileNavOpen; render(); };
  toggleWrap.appendChild(toggleBtn);
  right.appendChild(toggleWrap);

  inner.appendChild(right);
  nav.appendChild(inner);

  if (state.mobileNavOpen) {
    const panel = el("div", "mobile-panel");
    links.forEach(([label, href]) => {
      const a = el("a");
      a.href = "#" + href;
      a.textContent = label;
      a.onclick = () => { state.mobileNavOpen = false; };
      panel.appendChild(a);
    });
    nav.appendChild(panel);
  }

  return nav;
}

/* ---------------- login ---------------- */
function renderLogin() {
  const wrap = el("div", "login-wrap");

  const left = el("div", "login-left");
  left.innerHTML = `
    <div class="brand" style="color:#fff">
      <span class="brand-mark">M</span><span class="brand-name">Meridian Library</span>
    </div>
    <div class="quote">
      "A library is not a luxury but one of the necessities of life."
      <div class="quote-attr">— Henry Ward Beecher</div>
    </div>
    <div class="stat-row"></div>
  `;
  const statRow = left.querySelector(".stat-row");
  const s = state.stats || { total_books: 0, reading_rooms: 0, members: 0 };
  [[s.total_books.toLocaleString(), "Books"], [s.reading_rooms, "Reading Rooms"], [s.members.toLocaleString(), "Members"]]
    .forEach(([n, l]) => {
      const d = el("div", "stat");
      d.innerHTML = `<div class="n">${n}</div><div class="l">${l}</div>`;
      statRow.appendChild(d);
    });
  wrap.appendChild(left);

  const right = el("div", "login-right");
  const card = el("div", "login-card");

  const isSignIn = state.loginTab === "signin";
  card.innerHTML = `
    <h1>${isSignIn ? "Welcome back" : "Create your account"}</h1>
    <p class="login-sub">${isSignIn ? "Sign in to access your library account." : "Register for a Meridian Library membership."}</p>
    <div class="tabrow">
      <button class="${isSignIn ? "active" : ""}" data-tab="signin">Sign In</button>
      <button class="${!isSignIn ? "active" : ""}" data-tab="register">Register</button>
    </div>
    <div id="login-error"></div>
    <form id="login-form"></form>
  `;
  right.appendChild(card);
  wrap.appendChild(right);

  card.querySelectorAll(".tabrow button").forEach((b) => {
    b.onclick = () => { state.loginTab = b.dataset.tab; render(); };
  });

  const form = card.querySelector("#login-form");
  if (isSignIn) {
    form.innerHTML = `
      <div class="field"><label>Email Address</label><input type="email" name="email" value="gaurav@gmail.com" required></div>
      <div class="field"><label>Password</label><input type="password" name="password" value="demo1234" required></div>
      <div class="forgot">Forgot password?</div>
      <button type="submit" class="btn btn-dark btn-block">Sign In</button>
      <div class="divider">or continue as guest</div>
    `;
    const guestBtn = el("button", "btn btn-outline btn-block");
    guestBtn.type = "button";
    guestBtn.textContent = "Browse as Guest";
    guestBtn.onclick = async () => {
      const guest = await api("/auth/guest", { method: "POST" });
      saveSession(guest);
      navigate("#/home");
      render();
    };
    form.appendChild(guestBtn);
  } else {
    form.innerHTML = `
      <div class="field"><label>Full Name</label><input type="text" name="name" placeholder="e.g. Priya Raman" required></div>
      <div class="field"><label>Email Address</label><input type="email" name="email" placeholder="you@email.com" required></div>
      <div class="field"><label>Password</label><input type="password" name="password" placeholder="At least 8 characters" required></div>
      <button type="submit" class="btn btn-dark btn-block">Create Account</button>
    `;
  }

  form.onsubmit = async (e) => {
    e.preventDefault();
    const errEl = card.querySelector("#login-error");
    errEl.innerHTML = "";
    const data = Object.fromEntries(new FormData(form).entries());
    try {
      let user;
      if (isSignIn) {
        user = await api("/auth/login", { method: "POST", body: JSON.stringify(data) });
      } else {
        user = await api("/auth/register", { method: "POST", body: JSON.stringify(data) });
        toast("Account created — welcome to Meridian Library.");
      }
      saveSession(user);
      navigate("#/home");
      render();
    } catch (err) {
      errEl.innerHTML = `<div class="login-error">${err.message}</div>`;
    }
  };

  const foot = el("div", "login-foot");
  foot.textContent = "Meridian Public Library · Est. 1892 · Open Mon–Sat 08:00–20:00";
  right.appendChild(foot);

  return wrap;
}

/* ---------------- home ---------------- */
function renderHome() {
  const frag = el("div");

  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";

  const hero = el("section", "hero");
  const s = state.stats || { total_books: 0, reading_rooms: 0, members: 0 };
  hero.innerHTML = `
    <div class="hero-inner">
      <div class="eyebrow">MERIDIAN PUBLIC LIBRARY · EST. 1892</div>
      <h1>${greeting},<br><span class="accent">${state.user.name}</span>.</h1>
      <p>Explore our reading rooms, reserve your slot, or browse ${s.total_books.toLocaleString()}+ books across all disciplines.</p>
      <div class="hero-actions">
        <a class="btn btn-gold" href="#/book">Book a Room</a>
        <a class="btn btn-outline-light" href="#/catalogue">Browse Catalogue</a>
      </div>
      <div class="hero-stats"></div>
    </div>
  `;
  const statsRow = hero.querySelector(".hero-stats");
  [["4", "Reading Rooms"], [s.total_books.toLocaleString(), "Books"], [s.members.toLocaleString(), "Members"], ["5", "Upcoming Events"]]
    .forEach(([n, l]) => {
      const d = el("div", "stat");
      d.innerHTML = `<div class="n">${n}</div><div class="l">${l}</div>`;
      statsRow.appendChild(d);
    });
  frag.appendChild(hero);

  const section = el("section", "section");
  section.innerHTML = `<h2>What would you like to do?</h2><p class="lead">Access all library services from one place.</p>`;
  const grid = el("div", "card-grid");
  const actions = [
    [icon.book, "4 Rooms", "Find a Room", "Browse all four reading rooms, check availability, and view time slots.", "#/rooms"],
    [icon.calendar, "Online", "Book a Slot", "Reserve your preferred room and time up to 7 days in advance.", "#/book"],
    [icon.stamp, `${state.user.guest ? "—" : ""} Earned`, "Get Your Stamp", "Collect stamps for library activities and unlock exclusive rewards.", "#/account"],
    [icon.search, "84k+ Items", "Search Catalogue", "Discover books, journals, maps, and digital collections.", "#/catalogue"],
    [icon.newspaper, "5 Upcoming", "Upcoming Events", "Workshops, reading circles, seminars — register your place.", "#/events"],
    [icon.user, state.user.guest ? "Guest" : "Active", "My Account", "View borrowed books, due dates, membership info, and history.", "#/account"],
  ];
  actions.forEach(([ic, pill, title, desc, href]) => {
    const card = el("button", "action-card");
    card.innerHTML = `
      <div class="top-row"><div class="action-icon">${ic}</div><span class="pill">${pill}</span></div>
      <h3>${title}</h3><p>${desc}</p>
    `;
    card.onclick = () => { navigate(href); render(); };
    grid.appendChild(card);
  });
  section.appendChild(grid);
  frag.appendChild(section);

  return frag;
}

/* ---------------- rooms ---------------- */
function renderRooms() {
  const section = el("section", "section");
  section.innerHTML = `<h2>Reading Rooms</h2><p class="lead">Four rooms, each suited to a different kind of visit.</p>`;
  const grid = el("div", "room-grid");
  section.appendChild(grid);

  api(`/rooms?for_date=${state.wizard.date}`).then((rooms) => {
    grid.innerHTML = "";
    rooms.forEach((room) => {
      const card = el("div", "room-card");
      const isOpen = room.status === "Open";
      card.innerHTML = `
        <div class="room-media" style="color:#6b5a30">
          ${icon[room.icon] || icon.book}
          <div class="status-badge ${isOpen ? "open" : "closed"}"><span class="dot"></span>${room.status}</div>
        </div>
        <div class="room-body">
          <div class="room-cat">${room.category.toUpperCase()}</div>
          <h3>${room.name}</h3>
          <p class="desc">${room.description}</p>
          <div class="room-meta">
            <span>Level ${room.level} · Cap. ${room.capacity} · ${isOpen ? room.free_slots + " free" : "Closed"}</span>
            <a class="view" href="#/book">View →</a>
          </div>
        </div>
      `;
      card.querySelector(".view").onclick = (e) => {
        e.preventDefault();
        state.wizard = { roomId: room.id, date: todayStr(), slot: null, name: state.user.name || "" };
        navigate("#/book");
        render();
      };
      grid.appendChild(card);
    });
  });

  return section;
}

/* ---------------- book wizard ---------------- */
function renderBookWizard() {
  const section = el("section", "section");
  const w = state.wizard;
  const step = !w.roomId ? 1 : !w.slot ? 2 : 3;

  const stepper = el("div", "stepper");
  [["1", "Select Room"], ["2", "Choose Time"], ["3", "Your Details"]].forEach(([n, label], i) => {
    if (i > 0) stepper.appendChild(el("div", "step-line"));
    const s = el("div", `step ${step === i + 1 ? "active" : ""}`);
    s.innerHTML = `<span class="circle">${n}</span><span>${label}</span>`;
    stepper.appendChild(s);
  });
  section.appendChild(stepper);

  const card = el("div", "wizard-card");
  section.appendChild(card);

  if (step === 1) renderWizardStep1(card);
  else if (step === 2) renderWizardStep2(card);
  else renderWizardStep3(card);

  return section;
}

function renderWizardStep1(card) {
  card.innerHTML = `<h3>Which room would you like?</h3>`;
  const list = el("div");
  card.appendChild(list);

  api("/rooms").then((rooms) => {
    list.innerHTML = "";
    rooms.forEach((room) => {
      const opt = el("div", `room-option ${state.wizard.roomId === room.id ? "selected" : ""}`);
      const disabled = room.status !== "Open";
      opt.style.opacity = disabled ? "0.5" : "1";
      opt.style.cursor = disabled ? "not-allowed" : "pointer";
      opt.innerHTML = `
        <div class="thumb"></div>
        <div class="meta"><div class="name">${room.name}</div><div class="sub">Level ${room.level} · Cap. ${room.capacity} · ${disabled ? "Closed" : room.free_slots + " slots free"}</div></div>
        ${state.wizard.roomId === room.id ? `<span class="check">${icon.check}</span>` : ""}
      `;
      if (!disabled) {
        opt.onclick = () => { state.wizard.roomId = room.id; render(); };
      }
      list.appendChild(opt);
    });

    const dateField = el("div", "field");
    dateField.style.marginTop = "18px";
    dateField.innerHTML = `<label>Preferred Date</label>`;
    const input = el("input");
    input.type = "date";
    input.value = state.wizard.date;
    input.min = todayStr();
    input.onchange = () => { state.wizard.date = input.value; };
    dateField.appendChild(input);
    list.appendChild(dateField);

    const actions = el("div", "wizard-actions");
    const cont = el("button", "btn btn-dark");
    cont.textContent = "Continue →";
    cont.disabled = !state.wizard.roomId;
    cont.onclick = () => { render(); };
    actions.appendChild(el("span"));
    actions.appendChild(cont);
    list.appendChild(actions);
  });
}

function renderWizardStep2(card) {
  card.innerHTML = `<h3>Pick an open time</h3>`;
  const body = el("div");
  card.appendChild(body);

  api(`/rooms/${state.wizard.roomId}/slots?for_date=${state.wizard.date}`).then((slots) => {
    const grid = el("div", "slot-grid");
    slots.forEach((s) => {
      const btn = el("button", "slot-btn");
      btn.textContent = formatTime(s.time);
      if (!s.available) btn.disabled = true;
      if (state.wizard.slot === s.time) btn.classList.add("selected");
      btn.onclick = () => { state.wizard.slot = s.time; render(); };
      grid.appendChild(btn);
    });
    body.appendChild(grid);

    const actions = el("div", "wizard-actions");
    const back = el("button", "btn btn-outline");
    back.textContent = "← Back";
    back.onclick = () => { state.wizard.roomId = null; render(); };
    const cont = el("button", "btn btn-dark");
    cont.textContent = "Continue →";
    cont.disabled = !state.wizard.slot;
    cont.onclick = () => { render(); };
    actions.appendChild(back);
    actions.appendChild(cont);
    body.appendChild(actions);
  });
}

function renderWizardStep3(card) {
  card.innerHTML = `<h3>Confirm your details</h3>`;
  const nameField = el("div", "field");
  nameField.innerHTML = `<label>Your Name</label>`;
  const nameInput = el("input");
  nameInput.type = "text";
  nameInput.value = state.wizard.name || state.user.name || "";
  nameInput.placeholder = "e.g. Priya Raman";
  nameInput.oninput = () => { state.wizard.name = nameInput.value; };
  nameField.appendChild(nameInput);
  card.appendChild(nameField);

  const summary = el("p", "lead");
  summary.style.margin = "0 0 18px";
  summary.textContent = `${state.wizard.date} · ${formatTime(state.wizard.slot)} — 1 hour`;
  card.appendChild(summary);

  const actions = el("div", "wizard-actions");
  const back = el("button", "btn btn-outline");
  back.textContent = "← Back";
  back.onclick = () => { state.wizard.slot = null; render(); };
  const confirm = el("button", "btn btn-gold");
  confirm.textContent = "Confirm Booking";
  confirm.onclick = async () => {
    if (!nameInput.value.trim()) { toast("Add your name to confirm."); return; }
    try {
      const payload = {
        room_id: state.wizard.roomId,
        date: state.wizard.date,
        time: state.wizard.slot,
        guest_name: state.user.guest ? nameInput.value.trim() : null,
      };
      await api("/bookings", { method: "POST", body: JSON.stringify(payload) });
      toast("Room booked. You'll find it under My Stamps.");
      state.wizard = { roomId: null, date: todayStr(), slot: null, name: "" };
      navigate(state.user.guest ? "#/home" : "#/account");
      render();
    } catch (err) {
      toast(err.message);
    }
  };
  actions.appendChild(back);
  actions.appendChild(confirm);
  card.appendChild(actions);
}

function formatTime(t) {
  if (!t) return "";
  const [h, m] = t.split(":").map(Number);
  const period = h >= 12 ? "PM" : "AM";
  const h12 = h % 12 === 0 ? 12 : h % 12;
  return `${h12}:${String(m).padStart(2, "0")} ${period}`;
}

/* ---------------- catalogue ---------------- */
function renderCatalogue() {
  const section = el("section", "section");
  section.innerHTML = `<h2>Catalogue</h2><p class="lead">Search 84,000+ books, journals, maps, and digital collections.</p>`;

  const toolbar = el("div", "cat-toolbar");
  const searchInput = el("input");
  searchInput.type = "text";
  searchInput.placeholder = state.catalogue.aiMode
    ? "Ask in plain language, e.g. “a book about building good habits”"
    : "Search by title, author, or call number";
  searchInput.value = state.catalogue.q;
  toolbar.appendChild(searchInput);

  const genreSelect = el("select");
  toolbar.appendChild(genreSelect);

  const statusSelect = el("select");
  ["All", "Available", "Borrowed", "Reserved"].forEach((s) => {
    const o = el("option");
    o.value = s; o.textContent = s;
    if (s === state.catalogue.status) o.selected = true;
    statusSelect.appendChild(o);
  });
  toolbar.appendChild(statusSelect);

  const aiBtn = el("button", "ai-toggle");
  aiBtn.innerHTML = `${icon.sparkle} ${state.catalogue.aiMode ? "Ask the Librarian: On" : "Ask the Librarian"}`;
  toolbar.appendChild(aiBtn);

  section.appendChild(toolbar);

  const note = el("p", "ai-note");
  note.textContent = state.catalogue.aiMode
    ? "Natural-language search powered by a lightweight local text-similarity model — no exact keyword match needed."
    : "";
  section.appendChild(note);

  const tableWrap = el("div");
  section.appendChild(tableWrap);

  api("/genres").then((genres) => {
    state.genres = genres;
    const allOpt = el("option"); allOpt.textContent = "All Genres"; allOpt.value = "All Genres";
    genreSelect.appendChild(allOpt);
    genres.forEach((g) => {
      const o = el("option"); o.value = g; o.textContent = g;
      if (g === state.catalogue.genre) o.selected = true;
      genreSelect.appendChild(o);
    });
  });

  async function runSearch() {
    if (state.catalogue.aiMode && state.catalogue.q.trim()) {
      const data = await api(`/assistant/search?q=${encodeURIComponent(state.catalogue.q)}`);
      renderCatTable(tableWrap, data.results, true);
    } else {
      const params = new URLSearchParams();
      if (state.catalogue.q) params.set("q", state.catalogue.q);
      if (state.catalogue.genre) params.set("genre", state.catalogue.genre);
      if (state.catalogue.status) params.set("status", state.catalogue.status);
      const data = await api(`/catalogue?${params.toString()}`);
      renderCatTable(tableWrap, data, false);
    }
  }

  let debounce;
  searchInput.oninput = () => {
    state.catalogue.q = searchInput.value;
    clearTimeout(debounce);
    debounce = setTimeout(runSearch, 280);
  };
  genreSelect.onchange = () => { state.catalogue.genre = genreSelect.value; runSearch(); };
  statusSelect.onchange = () => { state.catalogue.status = statusSelect.value; runSearch(); };
  aiBtn.onclick = () => { state.catalogue.aiMode = !state.catalogue.aiMode; render(); };

  runSearch();
  return section;
}

function renderCatTable(wrap, books, showScore) {
  wrap.innerHTML = "";
  const table = el("table", "cat-table");
  table.innerHTML = `
    <thead><tr><th>Call No.</th><th>Title & Author</th><th>Year</th><th>Status</th></tr></thead>
    <tbody></tbody>
  `;
  const tbody = table.querySelector("tbody");
  if (!books.length) {
    const tr = el("tr");
    tr.innerHTML = `<td colspan="4" class="empty-note">No matches. Try a different search.</td>`;
    tbody.appendChild(tr);
  }
  books.forEach((b) => {
    const tr = el("tr");
    tr.innerHTML = `
      <td>${b.call_no}</td>
      <td><div class="book-title">${b.title}</div><div class="book-author">${b.author} · <span class="genre-tag">${b.genre}</span></div>${showScore ? `<div class="match-score">match ${(b.match_score * 100).toFixed(0)}%</div>` : ""}</td>
      <td>${b.year}</td>
      <td><span class="status-text ${b.status}">${b.status}</span>${b.due_date ? `<div class="match-score">due ${b.due_date}</div>` : ""}</td>
    `;
    tbody.appendChild(tr);
  });
  wrap.appendChild(table);
}

/* ---------------- events ---------------- */
function renderEvents() {
  const section = el("section", "section");
  section.innerHTML = `<h2>Upcoming Events</h2><p class="lead">Workshops, reading circles, and seminars at Meridian Library.</p>`;
  const list = el("div");
  section.appendChild(list);

  api("/events").then((events) => {
    list.innerHTML = "";
    events.forEach((ev) => {
      const d = new Date(ev.event_date + "T00:00:00");
      const card = el("div", "event-card");
      const full = ev.registered_count >= ev.capacity;
      card.innerHTML = `
        <div class="event-date-block"><div class="d">${d.getDate()}</div><div class="m">${d.toLocaleString("en", { month: "short" }).toUpperCase()}</div></div>
        <div class="event-info">
          <h3>${ev.title}</h3>
          <p>${ev.description}</p>
          <div class="event-meta">${formatTime(ev.event_time)} · ${ev.type} · ${ev.registered_count}/${ev.capacity} registered</div>
        </div>
      `;
      const btn = el("button", "btn " + (full ? "btn-outline" : "btn-dark"));
      btn.textContent = full ? "Full" : "Register";
      btn.disabled = full || state.user.guest;
      btn.title = state.user.guest ? "Sign in to register" : "";
      btn.onclick = async () => {
        try {
          await api(`/events/${ev.id}/register`, { method: "POST", body: "{}" });
          toast("You're registered — see you there.");
          render();
        } catch (err) { toast(err.message); }
      };
      card.appendChild(btn);
      list.appendChild(card);
    });
  });

  return section;
}

/* ---------------- account ---------------- */
function renderAccount() {
  const section = el("section", "section");
  section.innerHTML = `<h2>My Account</h2><p class="lead">Your stamps, bookings, and membership details.</p>`;

  if (state.user.guest) {
    const p = el("div", "panel");
    p.innerHTML = `<h3>You're browsing as a guest</h3><p class="empty-note">Sign in or register to collect stamps and manage bookings.</p>`;
    const btn = el("button", "btn btn-dark");
    btn.textContent = "Sign In";
    btn.onclick = () => { clearSession(); render(); };
    p.appendChild(btn);
    section.appendChild(p);
    return section;
  }

  const grid = el("div", "account-grid");
  section.appendChild(grid);

  const bookingsPanel = el("div", "panel");
  bookingsPanel.innerHTML = `<h3>Your Bookings</h3>`;
  grid.appendChild(bookingsPanel);

  const stampsPanel = el("div", "panel");
  stampsPanel.innerHTML = `<h3>My Stamps</h3>`;
  grid.appendChild(stampsPanel);

  api(`/bookings`).then((bookings) => {
    if (!bookings.length) {
      bookingsPanel.appendChild(elHTML(`<div class="empty-note">No bookings yet — reserve a room to see it here.</div>`));
      return;
    }
    bookings.forEach((b) => {
      const row = el("div", "booking-row");
      row.innerHTML = `<span>${b.room_name} — ${b.booking_date} · ${formatTime(b.booking_time)}</span>`;
      const cancel = el("button", "cancel-link");
      cancel.textContent = "Cancel";
      cancel.onclick = async () => {
        await api(`/bookings/${b.id}`, { method: "DELETE" });
        toast("Booking cancelled.");
        render();
      };
      row.appendChild(cancel);
      bookingsPanel.appendChild(row);
    });
  });

  api(`/me`).then((member) => {
    if (!member.stamps.length) {
      stampsPanel.appendChild(elHTML(`<div class="empty-note">No stamps yet.</div>`));
      return;
    }
    member.stamps.forEach((s) => {
      const row = el("div", "stamp-row");
      row.innerHTML = `<span class="stamp-dot"></span><span>${s.label}</span>`;
      stampsPanel.appendChild(row);
    });
  });

  return section;
}

/* ---------------- dom helpers ---------------- */
function el(tag, className) {
  const e = document.createElement(tag);
  if (className) e.className = className;
  return e;
}
function elHTML(html) {
  const d = document.createElement("div");
  d.innerHTML = html.trim();
  return d.firstChild;
}
