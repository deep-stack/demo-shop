// The shop front: a basket on the home page, and forms that post to the shop's API.
const PRICES = { apples: 3.2, bread: 2.5, "peanut-butter": 4.75, milk: 1.4 };
const CONTAINS = { apples: [], bread: ["gluten"], "peanut-butter": ["peanuts"], milk: ["milk"] };

function money(value) {
  return "£" + value.toFixed(2);
}

async function post(path, body) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return { status: response.status, body: await response.json().catch(() => ({})) };
}

function say(element, text, kind) {
  element.textContent = text;
  element.className = "message " + kind;
  element.hidden = false;
}

function basket() {
  const list = document.querySelector("#basket-items");
  if (!list) return;
  const items = [];
  const draw = () => {
    list.innerHTML = "";
    for (const [index, item] of items.entries()) {
      const row = document.createElement("li");
      row.textContent = item + " ";
      const remove = document.createElement("button");
      remove.textContent = "Remove";
      remove.dataset.index = String(index);
      remove.addEventListener("click", () => {
        items.splice(index, 1);
        draw();
      });
      row.append(remove);
      list.append(row);
    }
    document.querySelector("#basket-count").textContent = String(items.length);
    document.querySelector("#basket-total").textContent = money(items.reduce((sum, item) => sum + PRICES[item], 0));
    document.querySelector("#basket-empty").hidden = items.length > 0;
  };
  for (const button of document.querySelectorAll("[data-add]")) {
    button.addEventListener("click", () => {
      items.push(button.dataset.add);
      draw();
    });
  }
  draw();
}

function signup() {
  const form = document.querySelector("#signup");
  if (!form) return;
  const message = document.querySelector("#signup-message");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    if (!data.email.includes("@")) return say(message, "Enter a valid email address.", "error");
    if (!/^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$/i.test(data.postcode)) return say(message, "Enter a valid postcode.", "error");
    const answer = await post("/api/signup", data);
    if (answer.status !== 200) return say(message, "We could not open your account. Try again later.", "error");
    say(message, `Welcome, ${data.full_name}! Your customer number is ${answer.body.id}.`, "ok");
    form.hidden = true;
  });
}

function order() {
  const form = document.querySelector("#order");
  if (!form) return;
  const message = document.querySelector("#order-message");
  const total = () =>
    [...form.querySelectorAll("input[name=item]:checked")].reduce((sum, box) => sum + PRICES[box.value], 0);
  form.addEventListener("change", () => {
    document.querySelector("#order-total").textContent = money(total());
  });
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const chosen = [...form.querySelectorAll("input[name=item]:checked")].map((box) => box.value);
    if (!chosen.length) return say(message, "Choose at least one item.", "error");
    const card = form.querySelector("#card").value;
    if (!/^\d{4}$/.test(card)) return say(message, "Enter the last 4 digits of your card.", "error");
    const answer = await post("/api/orders", {
      customer_id: Number(form.querySelector("#customer").value),
      total: total(),
      contains: chosen.flatMap((item) => CONTAINS[item]),
      card_last4: card,
    });
    if (answer.status === 409) return say(message, answer.body.error + ": remove it to order.", "warning");
    if (answer.status !== 200) return say(message, "Your order did not go through. Try again later.", "error");
    say(message, `Order ${answer.body.id} placed. We sent your receipt by email.`, "ok");
  });
}

function support() {
  const form = document.querySelector("#support");
  if (!form) return;
  const message = document.querySelector("#support-message");
  const text = form.querySelector("#question");
  text.addEventListener("input", () => {
    document.querySelector("#left").textContent = String(500 - text.value.length);
  });
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!text.value.trim()) return say(message, "Write your question first.", "error");
    const answer = await post("/api/support", {
      customer_email: form.querySelector("#support-email").value,
      message: text.value,
    });
    say(message, `Ticket ${answer.body.id} opened. We answer within a day.`, "ok");
    form.reset();
  });
}

basket();
signup();
order();
support();
