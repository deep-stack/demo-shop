// The shop front's browser tests: a static server for web/, and the API answered by each test.
const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "e2e",
  use: { baseURL: "http://127.0.0.1:4173", headless: true },
  webServer: {
    command: "python3 -m http.server 4173 --bind 127.0.0.1 -d web",
    url: "http://127.0.0.1:4173/index.html",
    reuseExistingServer: !process.env.CI,
  },
});
