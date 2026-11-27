import pytest
from playwright.sync_api import Page, expect


class TestBasket:
    def test_adds_apples(self, page: Page):
        page.goto("/index.html")
        page.get_by_role(
            "button", name="Add apples"
        ).click()
        expect(page.locator("#basket-count")).to_have_text("1")

    @pytest.mark.parametrize("item, total", [("bread", "£2.50"), ("milk", "£1.40")])
    def test_prices_one_item(self, page: Page, item, total):
        page.goto("/index.html")
        page.click(f"text=Add {item}")
        expect(page.locator("#basket-total")).to_have_text(total)


class TestSignUp:
    def test_asks_for_a_valid_email(self, page: Page):
        page.goto("/signup.html")
        page.fill("#email", "not-an-email")
        page.click("text=Open account")
        expect(page.locator("#signup-message")).to_have_text("Enter a valid email address.")


def test_counts_the_characters_left(page: Page):
    page.goto("/support.html")
    page.fill("#question", "Where is my order?")
    expect(page.locator("#left")).to_have_text("482")


def test_names_the_shop_as_a_store_fails_on_purpose(page: Page):
    page.goto("/index.html")
    expect(page.get_by_role("heading", level=1)).to_have_text("Demo store", timeout=1000)
