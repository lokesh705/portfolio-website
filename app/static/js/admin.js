const SCHEMAS = {
  projects: {
    label: "Project",
    fields: [
      { name: "title", label: "Title" },
      { name: "tagline", label: "Tagline" },
      { name: "description", label: "Description", type: "textarea", full: true },
      { name: "tech_stack", label: "Tech stack (comma separated)", full: true },
      { name: "github_url", label: "GitHub URL" },
      { name: "demo_url", label: "Demo URL" },
      { name: "image_url", label: "Image URL" },
      { name: "position", label: "Order", type: "number" },
      { name: "featured", label: "Featured", type: "checkbox" },
    ],
    columns: (item) => [item.title, item.tech_stack.join(", "), item.featured ? "Yes" : "No", item.position],
  },
  certificates: {
    label: "Certificate",
    fields: [
      { name: "name", label: "Name", full: true },
      { name: "issuer", label: "Issuer" },
      { name: "issue_date", label: "Issue date" },
      { name: "credential_url", label: "Credential URL", full: true },
      { name: "position", label: "Order", type: "number" },
    ],
    columns: (item) => [item.name, item.issuer, item.issue_date, item.position],
  },
  skills: {
    label: "Skill",
    fields: [
      { name: "name", label: "Name" },
      { name: "category", label: "Category" },
      { name: "level", label: "Level (0-100)", type: "number" },
      { name: "position", label: "Order", type: "number" },
    ],
    columns: (item) => [item.name, item.category, `${item.level}%`, item.position],
  },
  education: {
    label: "Education",
    fields: [
      { name: "institution", label: "Institution", full: true },
      { name: "degree", label: "Degree" },
      { name: "field", label: "Field" },
      { name: "start_year", label: "Start year" },
      { name: "end_year", label: "End year" },
      { name: "score", label: "Score / GPA" },
      { name: "position", label: "Order", type: "number" },
    ],
    columns: (item) => [item.institution, item.degree, `${item.start_year} - ${item.end_year}`, item.position],
  },
};

const editor = document.getElementById("editor");
const editorForm = document.getElementById("editor-form");
const editorFields = document.getElementById("editor-fields");
const editorTitle = document.getElementById("editor-title");
let editing = { resource: null, id: null };

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(`panel-${tab.dataset.panel}`).classList.add("active");
  });
});

async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.error || `Request failed (${response.status})`);
  }
  return response.json();
}

function renderRows(resource, items) {
  const schema = SCHEMAS[resource];
  const tbody = document.getElementById(`rows-${resource}`);
  tbody.innerHTML = "";
  if (!items.length) {
    tbody.innerHTML = `<tr><td colspan="5" class="empty">No entries yet.</td></tr>`;
    return;
  }
  items.forEach((item) => {
    const row = document.createElement("tr");
    schema.columns(item).forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = value ?? "";
      row.appendChild(cell);
    });
    const actions = document.createElement("td");
    actions.innerHTML = `<div class="row-actions"><button data-edit>Edit</button><button class="danger" data-delete>Delete</button></div>`;
    actions.querySelector("[data-edit]").addEventListener("click", () => openEditor(resource, item));
    actions.querySelector("[data-delete]").addEventListener("click", async () => {
      if (!confirm(`Delete "${schema.columns(item)[0]}"?`)) return;
      await request(`/api/${resource}/${item.id}`, { method: "DELETE" });
      load(resource);
    });
    row.appendChild(actions);
    tbody.appendChild(row);
  });
}

async function load(resource) {
  renderRows(resource, await request(`/api/${resource}`));
}

function openEditor(resource, item) {
  const schema = SCHEMAS[resource];
  editing = { resource, id: item ? item.id : null };
  editorTitle.textContent = `${item ? "Edit" : "New"} ${schema.label.toLowerCase()}`;
  editorFields.innerHTML = "";
  schema.fields.forEach((field) => {
    let value = item ? item[field.name] : "";
    if (Array.isArray(value)) value = value.join(", ");
    const label = document.createElement("label");
    if (field.full || field.type === "textarea") label.classList.add("full");
    if (field.type === "checkbox") {
      label.classList.add("checkbox");
      label.innerHTML = `<input type="checkbox" name="${field.name}" ${value ? "checked" : ""}> ${field.label}`;
    } else if (field.type === "textarea") {
      label.innerHTML = `${field.label}<textarea name="${field.name}" rows="4"></textarea>`;
      label.querySelector("textarea").value = value ?? "";
    } else {
      label.innerHTML = `${field.label}<input name="${field.name}" type="${field.type || "text"}">`;
      label.querySelector("input").value = value ?? "";
    }
    editorFields.appendChild(label);
  });
  editor.showModal();
}

document.querySelectorAll("[data-new]").forEach((button) => {
  button.addEventListener("click", () => openEditor(button.dataset.new, null));
});

document.getElementById("editor-cancel").addEventListener("click", () => editor.close());

editorForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const { resource, id } = editing;
  const payload = {};
  SCHEMAS[resource].fields.forEach((field) => {
    const input = editorForm.querySelector(`[name="${field.name}"]`);
    if (field.type === "checkbox") payload[field.name] = input.checked;
    else if (field.type === "number") payload[field.name] = Number(input.value || 0);
    else payload[field.name] = input.value;
  });
  await request(id ? `/api/${resource}/${id}` : `/api/${resource}`, {
    method: id ? "PUT" : "POST",
    body: JSON.stringify(payload),
  });
  editor.close();
  load(resource);
});

const aboutForm = document.getElementById("about-form");
aboutForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const status = document.getElementById("about-status");
  const payload = Object.fromEntries(new FormData(aboutForm).entries());
  try {
    await request("/api/about", { method: "PUT", body: JSON.stringify(payload) });
    status.textContent = "Saved";
    status.className = "status ok";
  } catch (error) {
    status.textContent = error.message;
    status.className = "status err";
  }
});

Object.keys(SCHEMAS).forEach(load);
