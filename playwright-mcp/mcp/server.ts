import { chromium, Page, Browser } from 'playwright';
import { extractElements } from '../agent/domParser.js';

let browser: Browser;
let page: Page;

// Open browser + page
export async function openPage(url: string) {
  browser = await chromium.launch({ headless: false });
  page = await browser.newPage();
  await page.goto(url);
  return "Page opened";
}

// Extract DOM (raw)
export async function getSmartDOM() {
  return await extractElements(page);
}

// Click
export async function click(selector: string) {
  await page.click(selector);
  return `Clicked ${selector}`;
}

// Fill input
export async function fill(selector: string, value: string) {
  await page.fill(selector, value);
  return `Filled ${selector}`;
}

// Screenshot
export async function screenshot() {
  await page.screenshot({ path: 'screen.png' });
  return "Screenshot taken";
}

export async function getText(selector: string) {
  try {
    const exists = await page.locator(selector).count();
    if (exists === 0) return null;

    return await page.locator(selector).textContent();
  } catch {
    return null;
  }
}

export async function isVisible(selector: string) {
  try {
    const exists = await page.locator(selector).count();
    if (exists === 0) return false;

    return await page.locator(selector).isVisible();
  } catch {
    return false;
  }
}

export async function waitForSelector(selector: string, timeout = 3000) {
  try {
    await page.waitForSelector(selector, { timeout });
    return true;
  } catch {
    return false;
  }
}