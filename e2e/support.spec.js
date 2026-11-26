const { test, expect } = require("@playwright/test");
const { answer } = require("./helpers");

test.describe("Help", () => {
  test("asks for a question before sending", async ({ page }) => {
    await page.goto("/support.html");
    await page.click("text=Send question");
    await expect(page.locator("#support-message")).toHaveText("Write your question first.");
  });

  test("counts the characters left", async ({ page }) => {
    await page.goto("/support.html");
    await page.fill("#question", "Where is my order?");
    await expect(page.locator("#left")).toHaveText("482");
  });

  test("opens a ticket", async ({ page }) => {
    await answer(page, "support", 200, { id: 55 });
    await page.goto("/support.html");
    await page.fill("#support-email", "sam@example.com");
    await page.fill("#question", "My bread was late.");
    await page.click("text=Send question");
    await expect(page.locator("#support-message")).toHaveText("Ticket 55 opened. We answer within a day.");
  });
});
