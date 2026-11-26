const { test, expect } = require("@playwright/test");
const { answer } = require("./helpers");

test.describe("Sign up", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/signup.html");
  });

  test("asks for a valid email", async ({ page }) => {
    await page.fill("#email", "not-an-email");
    await page.click("text=Open account");
    await expect(page.locator("#signup-message")).toHaveText("Enter a valid email address.");
  });

  test("asks for a valid postcode", async ({ page }) => {
    await page.fill("#email", "sam@example.com");
    await page.fill("#postcode", "12");
    await page.click("text=Open account");
    await expect(page.locator("#signup-message")).toHaveText("Enter a valid postcode.");
  });

  test("welcomes a new customer with their number", async ({ page }) => {
    await answer(page, "signup", 200, { id: 42 });
    await page.fill("#email", "sam@example.com");
    await page.fill("#full_name", "Sam Green");
    await page.fill("#postcode", "AB1 2CD");
    await page.click("text=Open account");
    await expect(page.locator("#signup-message")).toHaveText("Welcome, Sam Green! Your customer number is 42.");
    await expect(page.locator("#signup")).toBeHidden();
  });

  test("says when the account could not be opened", async ({ page }) => {
    await answer(page, "signup", 500, { error: "Something went wrong" });
    await page.fill("#email", "sam@example.com");
    await page.fill("#postcode", "AB1 2CD");
    await page.click("text=Open account");
    await expect(page.locator("#signup-message")).toHaveText("We could not open your account. Try again later.");
  });

  test("shows the form when the page opens", async ({ page }) => {
    await expect(page.locator("#signup")).toBeVisible();
  });

  test("greets the customer by first name (fails on purpose)", async ({ page }) => {
    await answer(page, "signup", 200, { id: 7 });
    await page.fill("#email", "sam@example.com");
    await page.fill("#full_name", "Sam Green");
    await page.fill("#postcode", "AB1 2CD");
    await page.click("text=Open account");
    await expect(page.locator("#signup-message")).toHaveText("Welcome, Sam!", { timeout: 1000 });
  });
});
