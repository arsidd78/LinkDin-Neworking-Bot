<h1>Documentation for LinkedIn Networking Bot<h1>
<h2>Project Overview</h2>
<p>The LinkedIn Networking Bot is a Python-based automation tool designed to automate the process of connecting with people on LinkedIn. It uses playwright.async_api to control a web browser and perform operations like logging in, searching for specific keywords, and sending connection requests to multiple people. The bot is designed to run asynchronously using Python's asyncio library.
</p>
<h2>Requirements</h2>
<p>To run this project, ensure you have the following installed:</p>
<ul>
  <li>Python 3.7 or higher</li>
  <li>playwright</li>
  <li>asyncio</li>
</ul>
<h4>Install the required dependencies with:</h4>
<p>
pip install asyncio playwright
Before you start, initialize the Playwright browsers by running:
</p><hr>
<p>
playwright install
</p><hr>
  
<h2>Class Overview: Networking_Bot
__init__(self, username, password, search, maximum_pages=5, headless=True, sign_in_time=30000)</h2><br><hr>

<h4>The constructor initializes the bot with the following parameters:</h4>
<ol>
  <li>username: LinkedIn username/email.</li>
  <li>password: LinkedIn password.</li>
  <li>search: Search query to find people.</li>
  <li>maximum_pages: The maximum number of pages to navigate (default is 5).</li>
  <li>headless: Whether to run in headless mode (default is True).</li>
  <li>sign_in_time: Time in milliseconds for sign-in operations (default is 30,000).</li>
  <li>The constructor also sets up a logging configuration to log actions and errors.</li>
</ol>
<h3>authenticate_linkedin(self)</h4>
<h4><p><strong>The main method that controls the bot's workflow:</strong></p></h4>
<p>
Browser Setup: Initializes the Playwright context and opens a new page.
LinkedIn Login: Navigates to the LinkedIn login page and performs sign-in operations.
Search and Connect: Searches for the given keyword and connects with users over multiple pages, adhering to the maximum_pages limit.
Logging: Logs important steps, errors, and exceptions for debugging and tracking purposes.
Error Handling
The bot includes error handling mechanisms for various steps:

Logs errors in case of incorrect login credentials or timeouts.
Captures exceptions during searching and connecting operations, providing meaningful log messages.
Attempts to recover from common errors like non-clickable elements.
Logging
Logs are stored in networkinglogs.log with the following information:

Timestamp
Logger name
Log level (INFO, ERROR, etc.)
Log message
Using the Bot
Input Credentials: The bot requires user input for LinkedIn credentials and search query.
Adjust Parameters: You can adjust maximum_pages, headless, and sign_in_time as needed.
Run the Bot: Execute the main() function to start the bot.
Check Logs: If errors occur, refer to networkinglogs.log for details.
</p>

<h2>Example Usage</h2>
<article>
<h3> python code: </h3>
<p>  
async def main():
    username = input('Type your email or username : ')
    password = input('Type password : ')
    search = input('Search : ')
    
    bot = Networking_Bot(
        username=username,
        password=password,
        search=search,
        maximum_pages=5,
        headless=True,
        sign_in_time=30000
    )
    await bot.authenticate_linkedin()

asyncio.run(main())
</p>
</article>
<h1>Considerations and Tips</h1>
<h4>Use with Caution:</h4>
<p></p>LinkedIn may have limits on connection requests. Avoid excessive automation to prevent account restrictions or bans.
Time Settings: Adjust sign_in_time for slower connections or if encountering frequent timeouts.
Headless Mode: Running in non-headless mode (headless=False) can help diagnose issues visually.</p>
