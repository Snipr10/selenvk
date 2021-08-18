from pyppeteer import launch


class BrowserManager:

    def __init__(self, proxy, width, height, **kargs):
        self.browser = None
        self.params = kargs
        self.proxy = proxy
        self.width = width
        self.height = height

    async def __aenter__(self):
        self.browser = await launch(headless=False,
                                    handleSIGINT=False,
                                    handleSIGTERM=False,
                                    handleSIGHUP=False,
                                    args=['--no-sandbox',
                                          f'--proxy-server={self.proxy}',
                                          f'--window-size=${self.width},${self.height}']
                                    )
        return self

    async def __aexit__(self, type, value, traceback):
        if self.browser:
            await self.browser.close()
