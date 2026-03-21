import { Page } from 'playwright';

export async function extractElements(page: Page) {

  return await page.evaluate(() => {

    const inputs = Array.from(document.querySelectorAll('input')).map(el => ({
      type: el.getAttribute('type'),
      id: el.id,
      name: el.getAttribute('name'),
      placeholder: el.getAttribute('placeholder')
    }));

    const buttons = Array.from(document.querySelectorAll('button')).map(el => ({
      text: el.innerText,
      id: el.id
    }));

    const links = Array.from(document.querySelectorAll('a')).map(el => ({
      text: el.innerText,
      href: el.getAttribute('href')
    }));

    return {
      inputs,
      buttons,
      links
    };

  });

}