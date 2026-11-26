// What several tests share: answering the shop's API, and filling in an order.
async function answer(page, path, status, body) {
  await page.route("**/api/" + path, (route) => route.fulfill({ status, json: body }));
}

async function openOrder(page) {
  await page.goto("/order.html");
}

async function chooseItems(page, items) {
  for (const item of items) await page.getByLabel(item, { exact: true }).check();
}

module.exports = { answer, openOrder, chooseItems };
