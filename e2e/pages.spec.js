const { test, expect } = require("@playwright/test");

test.describe("Pages", () => {
  test("serves the home page", async ({ request }) => {
    const response = await request.get("/index.html");
    expect(response.ok()).toBeTruthy();
  });

  test("serves the order form", async ({ request }) => {
    const response = await request.get("/order.html");
    expect(await response.text()).toContain('id="order"');
  });

  test("answers 404 for a page that does not exist", async ({ request }) => {
    const response = await request.get("/no-such-page.html");
    expect(response.status()).toBe(404);
  });
});
