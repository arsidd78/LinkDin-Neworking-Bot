import threading
import time
from playwright.sync_api import  sync_playwright
from customtkinter import *
class Auto_NetWorking(CTk):
    def __init__(self):
        super().__init__()
        # Variables
        self.url = r'https://www.linkedin.com/uas/login?'
        self.max_pages=5
        # Interface:
        self.title('AutoNetworking')
        self.geometry('600x700')
        self.resizable()
        self.iconbitmap('Auto_Networking_Bot.ico')
        self._set_appearance_mode('light')
        CTkLabel(self, text='Type your Email:   ', width=250).grid(row=0, column=0)
        self.email_entry = CTkEntry(self, width=250)
        self.email_entry.grid(row=1, column=0)
        CTkLabel(self, text='Type your Password: ', width=250).grid(row=2, column=0)
        self.password_entry = CTkEntry(self, width=250,show='*')
        self.password_entry.grid(row=3, column=0)
        self.signin_btn = CTkButton(self, text='Sign In and Connect ', command=self.SignIn)
        self.signin_btn.grid(row=6, column=0)
        CTkLabel(self, text='Search for your connections:   ', width=250).grid(row=4, column=0)
        self.interest_entry = CTkEntry(self, width=250)
        self.interest_entry.grid(row=5, column=0)

    def SignIn(self):
        self.status = CTkLabel(self, text='Wait the bot is workinggg.......')
        self.status.grid(row=8, column=0)
        thread=threading.Thread(target=self.Connecting)
        thread.start()
    def Connecting(self):
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(self.url)
            page.locator('xpath=//input[@id="username"]').fill(self.email_entry.get())
            page.locator('xpath=//input[@id="password"]').fill(self.password_entry.get())
            page.locator('xpath=//button[@type="submit"]').click()
            search=page.locator('xpath=//input[@class="search-global-typeahead__input"]')
            print('*******Input Field Was located ***********')
            search.fill(self.interest_entry.get())
            search.press(key='Enter')
            print('****** Searching Initiated *********')
            page.locator('xpath=//li[@class="search-reusables__primary-filter"]/button[text()="People"]').click()
            print('******* People Btn was clicked ******')
            total_connects=[]
            def clicking_connect():
                page.wait_for_selector('xpath=//div/button[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]')
                connect_btn_container=page.locator('//div/button[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]').all()
                i=0
                for btn in connect_btn_container:
                    print('***** Connect Btn for loop Initiated ****')
                    if btn.text_content().strip().lower()=='connect':
                        btn.click()
                        print('*******Connect Button was clicked*******')
                        page.wait_for_selector('xpath=//button[@aria-label="Send now"]')
                        page.locator('xpath=//button[@aria-label="Send now"]').click()
                        i+=1
                        print(f'*****Total -->{i} <--Connect Request was sent on this page ***')
                        total_connects.append(i)
                    else:
                        print(f'**** {btn.text_content().strip()} is not a connect btn ******')
            clicking_connect()
            next_page_btn=page.locator('xpath=//button[@aria-label="Next"]')
            page_counter=0
            for pages in range(2,self.max_pages+1):
                print(' Next btn was clicked')
                next_page_btn.click(no_wait_after=True)
                page_counter+=1
                clicking_connect()
            print('Connect Requests are send')
            self.status.configure(text=f'Total {sum(total_connects)} connect requests have been sent !')
            print(f' Total Connect Requests: {sum(total_connects)}')
            print(f'Total Pages : {page_counter}')
            print('-----------------------------------------------------------------------------------------------')

app = Auto_NetWorking()
app.mainloop()
