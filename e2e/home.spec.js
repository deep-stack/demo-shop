const { test, expect } = require("@playwright/test");

test.describe("Home", () => {
  test("shows the shop's name", async ({ page }) => {
    await page.goto("/index.html");
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("Demo shop");
  });

  test("starts with an empty basket", async ({ page }) => {
    await page.goto("/index.html");
    await expect(page.locator("#basket-empty")).toBeVisible();
    await expect(page.locator("#basket-total")).toHaveText("£0.00");
  });

  test("adds an item to the basket", async ({ page }) => {
    await page.goto("/index.html");
    await page.click("text=Add apples");
    await expect(page.locator("#basket-count")).toHaveText("1");
    await expect(page.locator("#basket-items")).toContainText("apples");
  });

  test("adds up the basket's total", async ({ page }) => {
    await page.goto("/index.html");
    await page.click("text=Add bread");
    await page.click("text=Add milk");
    await expect(page.locator("#basket-total")).toHaveText("£3.90");
  });

  test("removes an item from the basket", async ({ page }) => {
    await page.goto("/index.html");
    await page.click("text=Add apples");
    await page.getByRole("button", { name: "Remove" }).click();
    await expect(page.locator("#basket-empty")).toBeVisible();
  });

  test("names the shop as a store (fails on purpose)", async ({ page }) => {
    await page.goto("/index.html");
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("Demo store", { timeout: 1000 });
  });
});
