import asyncio
import logging
from playwright.async_api import async_playwright
class Networking_Bot:
    def __init__(self, username, password, search, maximum_pages=5, headless= True, sign_in_time=30000,default_time=30000):
        self.url = 'https://www.linkedin.com/login'
        self.username = username
        self.password = password
        self.search = search
        self.maximum_pages = maximum_pages
        self.headless = headless
        self.sign_in_time = sign_in_time
        self.time = default_time
        logging.basicConfig(
            filename='networkinglogs.log',
            filemode='a',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ) # The logging will help you track the program
    async def authenticate_linkedin(self):
        print('Initiated wait .............')
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(self.url,timeout=30000)
            logging.info('LinkedIn site loaded')

            await page.fill('xpath=//input[@id="username"]', self.username,timeout=self.sign_in_time)
            await page.fill('xpath=//input[@id="password"]', self.password,timeout=self.sign_in_time)
            await page.locator('xpath=//button[@data-litms-control-urn="login-submit"]').click(timeout=self.sign_in_time)
            logging.info('Sign in attempt')
            try:
                await page.wait_for_selector('xpath=//div[@class="t-16 t-black t-bold"]', timeout=self.sign_in_time)
                logging.info('Signed in successfully')

            except Exception as e:
                logging.error(f'Invalid username or password. The reason for this exception could be the wrong credential'
                              f' or some sort of human authentication try using window mode and increasing '
                              f'wait so that you can pass authentication.')
                raise e
            try:
                await page.locator('xpath=//input[@class="search-global-typeahead__input"]').click()
                await page.locator('xpath=//input[@class="search-global-typeahead__input"]').fill(self.search)
                await page.locator('xpath=//input[@class="search-global-typeahead__input"]').press(key="Enter")
                logging.info('search query was sent')

                await page.locator('xpath=(//li[@class="search-reusables__primary-filter"]/button)[1]').click(timeout=self.time)

                logging.info(msg="Search Query was redirected to people category")
                i = 0
                number_of_pages = 0
            except Exception as e:
                logging.error(f'There was an error in locating elements Exception: {e}')
                raise e
            try: # mainloop
                for next_click in range(1,self.maximum_pages+1):
                    number_of_pages+=1
                    try:
                        await page.wait_for_selector('xpath=//button[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]')
                        people_container = await page.locator('xpath=//button[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]').all()
                        await page.keyboard.down('End')
                        next_btn = await page.locator('xpath=//button[@aria-label="Next"]').scroll_into_view_if_needed()
                        # Main If:
                        if await page.locator('xpath=//button[@aria-label="Next"]').text_content() == '1':
                            logging.info('At first page')
                            for contact in people_container:
                                connect = await  contact.text_content()
                                if connect.strip().lower() == 'connect':
                                    try:
                                        await contact.click(timeout=self.time)
                                        logging.info('Connect Button was clicked')
                                        await page.locator('xpath=//button[@aria-label="Send without a note"]').click()
                                        i += 1
                                    except:
                                       logging.error('Connect button was not clickable !, this error could occur if the element is not founded.')
                                       continue
                        # Main else:
                        else:
                           for contact in people_container:
                               connect = await  contact.text_content()
                               await page.keyboard.down('End')
                               next_btn = page.locator('xpath=//button[@aria-label="Next"]')
                               if connect.strip().lower() == 'connect':
                                   try:
                                       await contact.click(timeout=self.time)
                                       logging.info('Connect Button was clicked')
                                       await page.locator('xpath=//button[@aria-label="Send without a note"]').click()
                                       i += 1
                                   except:
                                       logging.error(
                                           'Connect button was not clickable !, this error could occur if the element is not founded.')
                                       if page.locator('xpath=//button[@aria-label="Send without a note"]'):
                                           await page.locator('xpath=(//button[@aria-label="Dismiss"])[position()=1]').click()
                                           continue
                                       else:
                                           await next_btn.click()
                                           number_of_pages+=1
                                           continue
                           number_of_pages += 1
                           await next_btn.click()

                    except Exception as e:
                        logging.error(f'Excepion {e} occur in main loop')
                        next_btn = page.locator('xpath=//button[@aria-label="Next"]')
                        await next_btn.click()
                        continue
            except Exception as e:
                logging.error(f'Exception {e} occur when looping through people_containers, restart the bot increase the time'
                              f'if problem persist')
                raise e
            finally:
                logging.info(f'Total connects send were equal to {i}')
                logging.info(f'Total Pages: {number_of_pages} ')
                await browser.close()
                print('Completed .......') # The program code ends here after this a user
                                           # can edit the execution and parameters in anyway.

async def main(): # This function is to run the program this can be changed according to your needs.
    username = input('Type your email or username : ') # This is the username parameter that is required in the bot
    password = input('Type password : ') # Over here you can type your password import it, or just leave it like this
    searh = input('Search : ') # This is the search query parameter in Networking class.
    app = Networking_Bot(
        username=username,
        password=password,
        search=searh,
        maximum_pages=4,
        headless= True,
        sign_in_time=50000,
        default_time= 50000
    )
    await app.authenticate_linkedin()
asyncio.run(main())