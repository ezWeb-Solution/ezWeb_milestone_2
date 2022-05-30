# Milestone 1 Submission

## Team ezWeb

## Motivation
A personal website can be crucial in allowing others to gauge the capability of an individual in their respective field. For example, a real estate agent may benefit from having a personal website that details all of his/her previous transactions. Being able to showcase their portfolios serves as a great way for them to instill confidence in potential clients, which may lead to them onboarding more clients.

However, creating a personal website is not easy. Currently, there are two options available for those who want to make their own site. Option 1 is to design your own website through web builders that claim to provide a no-brainer solution to those in need of a website. However, these web builders often have a steep learning curve and learning how to use them efficiently may require hours of tutorials and practice.
### Examples of what non-technically inclined person may be up against when deciding to create their own website:
![WebDesign_tutorials2](https://user-images.githubusercontent.com/52826683/170931424-61abd339-20c5-4207-b876-d014d9e6ca87.jpg)
![WebDesign_tutorials3](https://user-images.githubusercontent.com/52826683/170931440-da898648-3dce-48f6-956c-f84601e3be83.jpg)
![WebDesign_tutorials4](https://user-images.githubusercontent.com/52826683/170931446-a908d229-46b9-43f0-8118-dde5904b470f.jpg)

Clearly, these web builders aren't as simple to use as they are advertised to be. The average real estate agent would face many hurdles in trying to set up an aesthetically-pleasing website. In addition, maintaining the website and getting their website indexed by search engines will require some technical know-how. These hurdles may seem too daunting and they may end up giving up altogether.

Option 2 would be to seek the help of freelance web designers to help you out. However, their services may be costly and the quality of the websites designed may differ greatly between different freelancers, and there is no guarantee that you will get a satisfactory website after all. Furthermore, when you want to update the website to expand your portfolio in future, it is likely that you will have to pay for the services of freelancers again, which makes a tedious and costly process. 

## Our Solution
Almost every has had experience with messaging apps such as Telegram and Whatsapp. Hence, our solution will offer users with a user-friendly way to set up their site. Users will only have to interact with our Telegram bot to set up their personal websites, and will also be able to update the content through the bot. This allows for a very efficient and simple way for individuals to manage and update their sites. A few beautiful and thoughtfully-designed templates will be offered for users to pick from. Given that our target audience will be from the same industry (Real Estate), we will be able to tailor these templates to their needs, thus ensuring that they will be able to build relevant websites that benefits their careers. 

Most real estate agents are currently registered under PropertyGuru, and as such, they have a personal page created on PropertyGuru. The process of managing one’s personal page is not simple, and users have to pay a high fee to keep their personal pages up ($3,000 per 12 months for the Advance plan). In addition, users do not get their own domain name, such as perrysiow.com, and instead have their website registered as a subdomain of PropertyGuru.com, such as https://www.propertyguru.com.sg/agent/timothy-tan-431805.

We also hope to provide users with real-time traffic analytics, which can allow them to accurately determine if the site is effective in helping them convert visitors into paying clients. This will then allow them to develop better personal branding strategies that will provide them with a valuable edge over competing agents.


## User Story

As a real estate agent who has just started, I want to have a cheap and easy way to create a personal website as it will make me seem like a more credible agent. I would also like to have my past successful transactions displayed to instill confidence in my clients that I am able to service their needs effectively. As I execute more transactions, I would also like to be able to periodically update my portfolio with just a few simple clicks, without needing to reach out to a tech professional to help me out.


As someone who is looking to purchase a property, I want to know more about my agent. In the event that my agent would like to direct me to their page, I would like it to be easily navigable and aesthetically pleasing. More importantly, I want to be able to quickly assess the skill set of my prospective agent through viewing his/her portfolios.

## Features
The features of our solution can be separated into three main components - the Telegram bot, our database, and our backend site-generator.

### Telegram bot
Our Telegram bot will be designed in a manner such that it offers a fool-proof way for clients to set up, design, upload information, and manage their site through the form of automated conversation. 

![workflow](https://user-images.githubusercontent.com/52826683/170936274-f5ce2617-193f-41f0-a192-33469920eedf.jpg)
#### Workflow of the Telegram bot
1. The bot will first allow the client to choose whether he/she would like to create a new site, or manage their current websites.
2. Upon choosing to create a new site, the bot will then take in the desired url of the user.
3. The url will be checked for its availability. Upon confirming its availability, its respective hosting costs will be presented to the user for confirmation.
4. After the url has been confirmed, the user is prompted to input their desired website description, upload their desired profile picture, and upload an excel file that contains information about their past transactions.
5. The user will then be provided with a list of templates that they can choose from for their site.
6. Once the relevant details has been confirmed, the user will be prompted to make a payment for the web hosting costs.
7. After payment capture, the details will then be sent to our database, where our backend site-generator will retrieve these information to be used in the process of generating the site.
8. The site will be expected to be generated in about 15-20 minutes, upon which the site will go live.
9. Users can then interact with the bot whenever they want to manage and update the information on their websites through a simple conversation with the bot.

#### Content Modification
1. The user instructs the Telegram bot to delete or update existing content, or to upload new content to the site.
2. The Telegram bot receives the request and the new content, then passes it to our database.
3. Our backend then processes this data and updates the site accordingly.

#### Website analytics
1. The user instructs the Telegram bot to retrieve traffic information of the web page.
2. The Telegram bot receives the request and forwards the request to our backend.
3. The backend then retrieves the traffic information and sends it back to the Telegram bot, after which, the analytics data will be displayed to the user for their perusal.

#### Full workflow
![Workflow2](https://user-images.githubusercontent.com/52826683/170938710-5419e72c-cbbf-4113-b394-90356ea8d6f7.jpg)

### Timeline
#### Milestone 1 - Ideation (30 May) (Completed)
Task  | Description | Handled by | Complete by
------------- | ------------- | -- | ---
System Design   | Create a workable system and workflow | Chengyue, Sean | 15 May
Familiarisation | Complete courses on JavaScript, Node.js, React, Python, ExpressJs etc. | Chengyue, Sean | 22 May 
Familiarise with Telegram bot API | Researched on optimal ways to implement Telegram bot | Sean | 22 May
Implement Telegram bot  | Basic prompt/response flow | Sean | 22 May
Familiarise with APIs and choosing proper platforms | Researched on the flow of website creation (Hosting, DNS, Database etc.) | Chengyue | 22 May
Connect bot to database | Set up database and ensure successful connection | Sean | 23 May
Connect ezWeb backend to database | Set up database and ensure successful connection |Chengyue | 23 May
Automate domain and DNS setup | Implement automated domain registering and DNS setup using GoDaddy's APIs | Chengyue | 24 May
Response capture | Capture url and website description into database | Sean | 25 May
Automate simple site generation | Implement standard Wordpress site generation and connect site's server to domain | Chengyue | 26 May
UX improvements | Swap from forward-slash commands to user-friendly inline buttons | Sean | 27 May
Wrapping up of prototype | Connect the bot, the site, and the ezWeb backend. | Chengyue | 29 May
Site-managemenet | Link each entry in database to unique user, allow for updates requests | Sean | 29 May 


#### Milestone 2 - Prototyping (27 Jun) (In Progress)
Task  | Description | Handled by | Date
------------- | ------------- | -- | ---
Base website Design | Decide on base website features | Chengyue, Sean | 10 Jun
Finalize Database | Switch to scalable database | Chengyue, Sean | 10 Jun
One-page Template | Create a deployable one-page template | Chengyue | 12 Jun
User Authentication | Authenticate users and link user data to their id | Sean |13 Jun
URL Availability Check | Confirm URL availability with hosting platform | Sean | 15 Jun
Update Requests | Ensure backend receives update requests and enact changes promptly | Chengyue | 16 Jun
Integrate Relevant APIs | CrazyDomain domain set-up & Cloudways hosting API | Chengyue | 17 Jun
Payment Capture | Prompt for payment to be made for website to be hosted | Sean | 21 Jun
File Uploads | Allow for user to upload files via Telegram bot | Sean | 23 Jun
Process Files | Backend to process uploaded files, followed by enacting updates | Chengyue | 25 Jun
Documentation | All features implemented to be documented comprehensively | Chengyue, Sean | 27 Jun

#### Milestone 3 - Extension (25 Jul) (To Be Confirmed)
Task  | Description | Handled by | Date
------------- | ------------- | -- | ---
Website Analytics Tracking | Implement website backend system to capture web traffic | Chengyue | 5 Jul
Website Analytics Display | Provide analytics to users in an easy-to-digest manner on Telegram | Chengyue, Sean | 8 Jul
More Templates | Deploy more templates for users to pick from | Chengyue, Sean | 15 Jul
Insurance Agents Templates | Expand target audience to insurance agents | Chengyue, Sean | 20 Jul
Expand Customizability | Allow users greater customizability to their site | Chengyue, Sean | 22 Jul
User Testing | Allow selected real estate agents to build their websites using ezWeb | Chengyue, Sean | 24 Jul



### Proof of Concept
Our Telegram bot has been set up to receive website creation requests, and capture url/description data which is sent to our database. On the backend, we will be able to retrive this data and generate a simple website on the given url.

#### Website Creation
To start, navigate to @ezWebTest_bot to start the bot.


<img src="https://user-images.githubusercontent.com/52826683/170946015-acc9b552-d9af-4001-817e-14578df2d96c.jpg" width="210" height="450">

Inline message options will then be provided to the user to create a website or manage their current websites.

<img src="https://user-images.githubusercontent.com/52826683/170946029-9b0f39e6-c5bd-4e71-b218-8bd0bfef70b5.jpg" width="210" height="450">

After clicking on create a website, the user will be prompted for a desired url as well as a description for the website.

<img src="https://user-images.githubusercontent.com/52826683/170946053-261ceb20-7a87-4fcb-bcb5-68e75df4f461.jpg" width="210" height="450">

Following which, the user will be prompted to confirm the description and url. Upon confirmation, the data will be sent to our database, where the data will then be retrived for their site to be generated.

<img src="https://user-images.githubusercontent.com/52826683/170946061-678cab1c-9e28-4129-8832-ada21b081767.jpg" width="210" height="450">

#### Managing/Update Websites
Users who want to update their websites can simply run a /start command on the bot to start the process.

<img src="https://user-images.githubusercontent.com/52826683/170946073-4c6a7eaf-cf64-4396-b9bc-de97fd2846f2.jpg" width="210" height="450">

**Manage my websites** option is chosen, and data is retrieved from the database to display all websites registered to the user.

<img src="https://user-images.githubusercontent.com/52826683/170946082-c5ff5f8b-a3d3-4a64-964b-bc7aada60dda.jpg" width="210" height="450">

After picking the website to be updated, the current information of the site will be retrieved and shown to the user. The user will then be prompted on what changes they would like to make to the site. The user will then be asked to confirm their changes.

<img src="https://user-images.githubusercontent.com/52826683/170946092-6c879864-c05b-4172-845f-314009062493.jpg" width="210" height="450">

Upon confirmation, the new data will be sent to the database and updated. 

<img src="https://user-images.githubusercontent.com/52826683/170946106-dbc3ab40-f97f-46a3-982d-89b3925feb9d.jpg" width="210" height="450">

