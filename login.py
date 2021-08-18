import asyncio

from browser import BrowserManager
from keys import USERNAME_GLASSEN, PASSWORD_GLASSEN

NEW_PAGE_TIMEOUT = 20 * 1000
DEFAULT_TIMEOUT = 10 * 1000

LOGIN_URL = "https://api.glassen-it.com/"
VK_BOT_URL = "https://api.glassen-it.com/component/socparser/bot/vkbotstart"

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'


class Login:
    def __init__(self, proxy, bot, user_agent):
        bot_data = bot.split(";")
        proxy_data = proxy.split(":")
        self.proxy_username = proxy_data[2]
        self.proxy_password = proxy_data[3]
        self.proxy = f"{proxy_data[0]}:{proxy_data[1]}"
        self.bot_login = bot_data[0]
        self.bot_password = bot_data[1]
        self.user_agent = user_agent

    async def login_and_add_bots(self):
        async with BrowserManager(self.proxy, self.user_agent['width'], self.user_agent['height']) as browser_manager:
            browser = browser_manager.browser

            page = await browser.newPage()
            await page.setUserAgent(
                self.user_agent['userAgentData']
            )
            await page.authenticate({'username': self.proxy_username, 'password': self.proxy_password})

            await page.goto(LOGIN_URL, timeout=NEW_PAGE_TIMEOUT)
            usernameEl, passwordEl = await asyncio.gather(
                page.waitForSelector("#username", timeout=DEFAULT_TIMEOUT),
                page.waitForSelector("#password", timeout=DEFAULT_TIMEOUT)
            )
            await usernameEl.type(USERNAME_GLASSEN)
            await passwordEl.type(PASSWORD_GLASSEN)

            await asyncio.gather(
                page.waitForNavigation(timeout=NEW_PAGE_TIMEOUT),
                page.click("[class='uk-button uk-button-primary']", timeout=DEFAULT_TIMEOUT),
            )
            page = await browser.newPage()
            await page.goto(VK_BOT_URL, timeout=NEW_PAGE_TIMEOUT)
            bot_usernameEl, bot_passwordEl = await asyncio.gather(
                page.waitForSelector("#login", timeout=DEFAULT_TIMEOUT),
                page.waitForSelector("#password", timeout=DEFAULT_TIMEOUT)
            )

            await bot_usernameEl.type(self.bot_login)
            await bot_passwordEl.type(self.bot_password)
            await asyncio.gather(
                page.waitForNavigation(timeout=NEW_PAGE_TIMEOUT),
                page.click("[class='uk-button']", timeout=DEFAULT_TIMEOUT),
            )

            vk_bot_usernameEl, vk_bot_passwordEl = await asyncio.gather(
                page.waitForSelector("[type='text']", timeout=DEFAULT_TIMEOUT),
                page.waitForSelector("[type='password']", timeout=DEFAULT_TIMEOUT)
            )

            await vk_bot_usernameEl.type(self.bot_login)
            await vk_bot_passwordEl.type(self.bot_password)

            await asyncio.gather(
                page.waitForNavigation(timeout=NEW_PAGE_TIMEOUT),
                page.click("[type='submit']", timeout=DEFAULT_TIMEOUT),
            )
            try:
                await asyncio.gather(
                    page.waitForNavigation(timeout=NEW_PAGE_TIMEOUT),
                    page.click("[class='flat_button fl_r button_indent']", timeout=DEFAULT_TIMEOUT),
                )
            except Exception:
                pass

            print(f"Bot add: {self.bot_login}")
