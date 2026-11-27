// The shop front, served for the Puppeteer tests, and the browser they drive.
const { spawn } = require("node:child_process");
const path = require("node:path");
const puppeteer = require("puppeteer-core");
// The Chromium the image has for Playwright, so no other browser is downloaded.
const { chromium } = require("playwright-core");

const PORT = 4175;
const URL = `http://127.0.0.1:${PORT}`;

async function start() {
  const server = spawn("python3", ["-m", "http.server", String(PORT), "--bind", "127.0.0.1", "-d", path.join(__dirname, "..", "web")], {
    stdio: "ignore",
  });
  for (let i = 0; i < 50; i++) {
    try {
      await fetch(`${URL}/index.html`);
      break;
    } catch {
      await new Promise((done) => setTimeout(done, 100));
    }
  }
  const browser = await puppeteer.launch({ executablePath: chromium.executablePath(), args: ["--no-sandbox"] });
  return { server, browser };
}

module.exports = { start, URL };
