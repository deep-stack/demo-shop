const { test, expect } = require("@playwright/test");
const { answer, openOrder, chooseItems } = require("./helpers");

test.describe("Order", () => {
  test("adds up the chosen items", async ({ page }) => {
    await openOrder(page);
    await chooseItems(page, ["Apples", "Peanut butter"]);
    await expect(page.locator("#order-total")).toHaveText("£7.95");
  });

  test("asks for at least one item", async ({ page }) => {
    await openOrder(page);
    await page.click("text=Pay and order");
    await expect(page.locator("#order-message")).toHaveText("Choose at least one item.");
  });

  test("asks for the card's last 4 digits", async ({ page }) => {
    await openOrder(page);
    await chooseItems(page, ["Milk"]);
    await page.fill("#card", "12");
    await page.click("text=Pay and order");
    await expect(page.locator("#order-message")).toHaveText("Enter the last 4 digits of your card.");
  });

  test("warns about an item the customer is allergic to", async ({ page }) => {
    await answer(page, "orders", 409, { error: "Contains peanuts" });
    await openOrder(page);
    await chooseItems(page, ["Peanut butter"]);
    await page.fill("#card", "4242");
    await page.click("text=Pay and order");
    await expect(page.locator("#order-message")).toHaveText("Contains peanuts: remove it to order.");
    await expect(page.locator("#order-message")).toHaveCSS("background-color", "rgb(184, 54, 42)");
  });

  test("places an order and says a receipt was sent", async ({ page }) => {
    await answer(page, "orders", 200, { id: 1001 });
    await openOrder(page);
    await chooseItems(page, ["Apples", "Bread"]);
    await page.fill("#card", "4242");
    await page.click("text=Pay and order");
    await expect(page.locator("#order-message")).toHaveText("Order 1001 placed. We sent your receipt by email.");
  });

  test("charges for milk at half price (fails on purpose)", async ({ page }) => {
    await openOrder(page);
    await chooseItems(page, ["Milk"]);
    await expect(page.locator("#order-total")).toHaveText("£0.70", { timeout: 1000 });
  });
});
