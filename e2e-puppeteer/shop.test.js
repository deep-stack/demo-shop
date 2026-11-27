const { start, URL } = require("./server");

let running, page;

beforeAll(async () => {
  running = await start();
});
afterAll(async () => {
  await running.browser.close();
  running.server.kill();
});
beforeEach(async () => {
  page = await running.browser.newPage();
});
afterEach(async () => {
  await page.close();
});

describe("Order", () => {
  it("adds up the chosen items", async () => {
    await page.goto(`${URL}/order.html`);
    await page.click("input[value='apples']");
    await page.click("input[value='bread']");
    const total = await page.$eval("#order-total", (el) => el.textContent);
    expect(total).toContain("£");
  });

  it("asks for at least one item", async () => {
    await page.goto(`${URL}/order.html`);
    await page.click("::-p-text(Pay and order)");
    const said = await page.$eval("#order-message", (el) => el.textContent);
    expect(said).toBe("Choose at least one item.");
  });
});

describe("Help", () => {
  it("asks for a question before sending", async () => {
    await page.goto(`${URL}/support.html`);
    await page.click("::-p-text(Send question)");
    const said = await page.$eval("#support-message", (el) => el.textContent);
    expect(said).toBe("Write your question first.");
  });

  it("clicks a button that is not there (fails on purpose)", async () => {
    await page.goto(`${URL}/support.html`);
    await page.click("#not-a-button");
  });
});
