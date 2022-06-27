# IMPORTANT!!! PLEASE PM @cylellll ON TELEGRAM IF YOU WISH TO TRY THE BOT, YOU WILL BE ABLE TO CREATE AND MANAGE A BLOG USING THE BOT IN REAL TIME :)

- [Project Info](#project-info)
- [Motivation](#motivation)
  * [Examples of what non-technically inclined person may be up against when deciding to create their own website:](#examples-of-what-non-technically-inclined-person-may-be-up-against-when-deciding-to-create-their-own-website-)
  * [User Story](#user-story)
  * [Our Solution](#our-solution)
- [Features](#features)
  * [Telegram bot](#telegram-bot)
    + [Workflow of the Telegram bot](#workflow-of-the-telegram-bot)
    + [Content Modification](#content-modification)
    + [Website analytics](#website-analytics)
  * [Proposed Website Design Elements](#proposed-website-design-elements)
    + [Hero banners](#hero-banners)
    + [Block displays](#block-displays)
    + ['About me' section](#-about-me--section)
    + [Testimonials](#testimonials)
    + ['Contact me' section](#-contact-me--section)
  * [Upload of New Listings Data](#upload-of-new-listings-data)
  * [Current Workflow](#current-workflow)
- [Mentor Matching - Poster Submission](#mentor-matching---poster-submission)
- [Mentor Matching - Video Submission](#mentor-matching---video-submission)
- [Timeline](#timeline)
  * [Milestone 1 - Ideation (30 May) (Completed)](#milestone-1---ideation--30-may---completed-)
    + [Milestone 1 - Poster Submission](#milestone-1---poster-submission)
    + [Milestone 1 - Project Log](#milestone-1---project-log)
    + [Milestone 1 - Prototype Demo](#milestone-1---prototype-demo)
    + [Post Milestone 1 Reflections](#post-milestone-1-reflections)
      - [Limitations and Struggles](#limitations-and-struggles)
        * [Inline Buttons](#inline-buttons)
        * [Photo Uploads](#photo-uploads)
        * [Integrating Secure Payment Systems](#integrating-secure-payment-systems)
        * [Design of Site](#design-of-site)
      - [Feedback Received](#feedback-received)
        * [Unintuitive Navigation](#unintuitive-navigation)
        * [Unable to Test](#unable-to-test)
  * [Milestone 2 - Prototyping (27 Jun) (Completed)](#milestone-2---prototyping--27-jun---completed-)
    + [Milestone 2 - Poster Submission](#milestone-2---poster-submission)
    + [Milestone 2 - Project Log](#milestone-2---project-log)
    + [Post Milestone 2 Reflections](#post-milestone-2-reflections)
      - [Limitations and Struggles](#limitations-and-struggles-1)
        * [Payment Testing](#payment-testing)
        * [Edit Listings](#edit-listings)
        * [Edit Agent Details](#edit-agent-details)
        * [Agent Interviews](#agent-interviews)
      - [Feedback Received](#feedback-received-1)
  * [Milestone 3 - Extension (25 Jul) (To Be Confirmed)](#milestone-3---extension--25-jul---to-be-confirmed-)
- [Working Prototype](#working-prototype)
  * [Website Creation](#website-creation)
  * [Update Website Description](#update-website-description)
  * [Add Agent Details](#add-agent-details)
  * [Create Posts/Edit Posts/Delete Posts](#create-posts-edit-posts-delete-posts)
  * [Create Listings/Edit Listings/Delete Listings](#create-listings-edit-listings-delete-listings)
- [Website Features (As of Milestone 2)](#website-features--as-of-milestone-2-)
  * [Agent Details](#agent-details)
  * [About Me](#about-me)
  * [Posts](#posts)
  * [Listings](#listings)




# Project Info
Team members: Li Chengyue & Sean Spencer Manik

Proposed level of achievement: Artemis

# Motivation
A personal website can be crucial in allowing others to gauge the capability of an individual in their respective field. For example, a real estate agent may benefit from having a personal website that details all of his/her previous transactions. Being able to showcase their portfolios serves as a great way for them to instill confidence in potential clients, which may lead to them onboarding more clients.

However, creating a personal website is not easy. Currently, there are two options available for those who want to make their own site. Option 1 is to design your own website through web builders that claim to provide a no-brainer solution to those in need of a website. However, these web builders often have a steep learning curve and learning how to use them efficiently may require hours of tutorials and practice.
## Examples of what non-technically inclined person may be up against when deciding to create their own website:
![WebDesign_tutorials2](https://user-images.githubusercontent.com/52826683/170931424-61abd339-20c5-4207-b876-d014d9e6ca87.jpg)
![WebDesign_tutorials3](https://user-images.githubusercontent.com/52826683/170931440-da898648-3dce-48f6-956c-f84601e3be83.jpg)
![WebDesign_tutorials4](https://user-images.githubusercontent.com/52826683/170931446-a908d229-46b9-43f0-8118-dde5904b470f.jpg)

Clearly, these web builders aren't as simple to use as they are advertised to be. The average real estate agent would face many hurdles in trying to set up an aesthetically-pleasing website. In addition, maintaining the website and getting their website indexed by search engines will require some technical know-how. These hurdles may seem too daunting and they may end up giving up altogether.

Option 2 would be to seek the help of freelance web designers to help you out. However, their services may be costly and the quality of the websites designed may differ greatly between different freelancers, and there is no guarantee that you will get a satisfactory website after all. Furthermore, when you want to update the website to expand your portfolio in future, it is likely that you will have to pay for the services of freelancers again, which makes a tedious and costly process. 

## User Story

As a real estate agent who has just started, I want to have a cheap and easy way to create a personal website as it will make me seem like a more credible agent. I would also like to have my past successful transactions displayed to instill confidence in my clients that I am able to service their needs effectively. As I execute more transactions, I would also like to be able to periodically update my portfolio with just a few simple clicks, without needing to reach out to a tech professional to help me out.


As someone who is looking to purchase a property, I want to know more about my agent. In the event that my agent would like to direct me to their page, I would like it to be easily navigable and aesthetically pleasing. More importantly, I want to be able to quickly assess the skill set of my prospective agent through viewing his/her portfolios.

## Our Solution
Almost every has had experience with messaging apps such as Telegram and Whatsapp. Hence, our solution will offer users with a user-friendly way to set up their site. Users will only have to interact with our Telegram bot to set up their personal websites, and will also be able to update the content through the bot. This allows for a very efficient and simple way for individuals to manage and update their sites. A few beautiful and thoughtfully-designed templates will be offered for users to pick from. Given that our target audience will be from the same industry (Real Estate), we will be able to tailor these templates to their needs, thus ensuring that they will be able to build relevant websites that benefits their careers. 

Most real estate agents are currently registered under PropertyGuru, and as such, they have a personal page created on PropertyGuru. The process of managing one’s personal page is not simple, and users have to pay a high fee to keep their personal pages up ($3,000 per 12 months for the Advance plan). In addition, users do not get their own domain name, such as perrysiow.com, and instead have their website registered as a subdomain of PropertyGuru.com, such as https://www.propertyguru.com.sg/agent/timothy-tan-431805.

We also hope to provide users with real-time traffic analytics, which can allow them to accurately determine if the site is effective in helping them convert visitors into paying clients. This will then allow them to develop better personal branding strategies that will provide them with a valuable edge over competing agents.


# Features
The features of our solution can be separated into three main components - the Telegram bot, our database, and our backend site-generator.

## Telegram bot
Our Telegram bot will be designed in a manner such that it offers a fool-proof way for clients to set up, design, upload information, and manage their site through the form of automated conversation. 

![workflow](https://user-images.githubusercontent.com/52826683/170936274-f5ce2617-193f-41f0-a192-33469920eedf.jpg)
### Workflow of the Telegram bot
1. The bot will first allow the client to choose whether he/she would like to create a new site, or manage their current websites.
2. Upon choosing to create a new site, the bot will then take in the desired url of the user.
3. The url will be checked for its availability. Upon confirming its availability, its respective hosting costs will be presented to the user for confirmation.
4. After the url has been confirmed, the user is prompted to input their desired website description, upload their desired profile picture, and upload an excel file that contains information about their past transactions.
5. The user will then be provided with a list of templates that they can choose from for their site.
6. Once the relevant details has been confirmed, the user will be prompted to make a payment for the web hosting costs.
7. After payment capture, the details will then be sent to our database, where our backend site-generator will retrieve these information to be used in the process of generating the site.
8. The site will be expected to be generated in about 15-20 minutes, upon which the site will go live.
9. Users can then interact with the bot whenever they want to manage and update the information on their websites through a simple conversation with the bot.

### Content Modification
1. The user instructs the Telegram bot to delete or update existing content, or to upload new content to the site.
2. The Telegram bot receives the request and the new content, then passes it to our database.
3. Our backend then processes this data and updates the site accordingly.

### Website analytics
1. The user instructs the Telegram bot to retrieve traffic information of the web page.
2. The Telegram bot receives the request and forwards the request to our backend.
3. The backend then retrieves the traffic information and sends it back to the Telegram bot, after which, the analytics data will be displayed to the user for their perusal.

## Proposed Website Design Elements
Since our initial target audience are real estate agents, our site templates will be tailored to their needs. This will allow us to maximize customizability based on what we believe the target audience wants. We plan to interview local real estate agents to get their input on which elements of a website will be the most important to them. Currently, these are our proposed website design elements, which will serve as the skeleton for all our templates.

### Hero banners
To begin, each site will have to be able to display a default hero banner where the user will be able to replace the hero banner with a photo of themselves. This is done in order to create a strong first impression for site visitors. According to web design industry standards, a well-designed hero banner helps to increase engagement and consequently, conversion rates, due to the fact that humans are highly visual in nature. 

Example of a hero banner, taken from Oceana.org.
<img src="https://user-images.githubusercontent.com/52826683/170986452-f5d738e3-8a4f-4c38-9769-4d0de73b0d2d.png" width="1000" height="400">

### Block displays
Block displays should be used to neatly display a list of properties that the agent has successfully transacted. This manner of display will allow for visitors to be able to get a clear idea of the volume of transactions that the agent has processed, as well as the type of property transactions that the agent generally handles. The visual nature of block displays also serves to keep visitors engaged, which may then result in higher lead generation.

### 'About me' section
An 'About me' section will be generated with a generic copywritten paragraph of what the agent strives to achieve and what they stand for. This section will help visitors to get to know the agent better, and will serve as a strong indicator of whether the agent will be suitable for the visitor/potential client.

Example of an engaging 'About me' section design, retrieved from https://www.youtube.com/watch?v=DXSQ2cEVbAI&ab_channel=Onlinewebustaad.
<img src="https://user-images.githubusercontent.com/52826683/170986863-77c88111-34bf-4003-b0a0-fba9605b6fd0.jpg" width="800" height="400">


### Testimonials 
A testimonial section will be generated where agents can include testimonials provided by past clients. Having a testimonial has been shown to increase lead generation rates, and is thus a powerful tool that we will be taking advantage in order to optimize visitor engagement rates.

Example of a well-designed testimonial section, retrieved from kissmetrics.io
<img src="https://user-images.githubusercontent.com/52826683/170987558-05d4d2f1-6d2e-4689-b093-f3ab4c24cd2d.jpg" width="700" height="400">

### 'Contact me' section
This section will arguably be the most important part of the website, where visitors are provided with a call-to-action. Visitors who are interested in consulting the agent can provide their contact details, which will then be sent to the email address of the agent. The agent will then be able to follow up on this new lead, thus potentially converting this lead to a new paying client.

## Upload of New Listings Data
As agents will want to upload information about their past transactions, it will be more efficient for them to perform the upload via an excel sheet, where they will be able to fill in information in an excel file formatted by us. Upon including all relevant data about their portfolio, the excel file can then be submitted to our Telegram bot, which will then send the file to our database, where we will be processing the data to be updated on the website.

We will be providing a formatted excel sheet with pre-defined fields that users just have to fill in.
![Screenshot 2022-05-30 203013](https://user-images.githubusercontent.com/52826683/170992791-518b697d-13e0-4cbd-90ad-470da28e9bbf.jpg)


## Current Workflow
![Workflow2](https://user-images.githubusercontent.com/52826683/170938710-5419e72c-cbbf-4113-b394-90356ea8d6f7.jpg)

# Mentor Matching - Poster Submission
<img src="https://user-images.githubusercontent.com/52826683/171004590-70ddf63f-0125-4f17-a9f4-6d87fa77aa14.png" width="500" height="775">

# Mentor Matching - Video Submission
This video succintly describes why ezWeb is needed, how we plan to implement our solution. It also includes plans for the expansion of our solution to a wider target audience.
https://user-images.githubusercontent.com/52826683/171005905-3aca0b53-4e0e-4094-8b5b-f35c773ad9eb.mp4



# Timeline
## Milestone 1 - Ideation (30 May) (Completed)
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
Site-management | Link each entry in database to unique user, allow for updates requests | Sean | 29 May 


### Milestone 1 - Poster Submission 
<img src="https://user-images.githubusercontent.com/52826683/171003935-5607d0ef-b251-477f-aae3-d7b960da2a98.png" width="500" height="775">

### Milestone 1 - Project Log
<a href="https://docs.google.com/spreadsheets/d/1PExAhXqZ7PFh2cHDoLcatWTSk98zk-yEUatYOD4pTbw/edit?usp=sharing">Milestone 1 Project Log (5 May - 29 May)</a>

### Milestone 1 - Prototype Demo
Click the following link to view our prototype demo. In this demo, we sent a request to create a new website through the telegram bot, which then sends the request's data to our database, where our backend retrieves the data to generate a simple site based on the given url.
<a href="https://drive.google.com/file/d/1AVJie7noZrFCSSrcqmKfIJInRWCDBHRk/view"><img src="https://user-images.githubusercontent.com/52826683/171210891-5a38f92e-99ee-40e8-ae41-cf54c3de57fb.jpg">
</a>

### Post Milestone 1 Reflections
#### Limitations and Struggles
We initially wanted to add more basic features to the bot and the website, but faced numerous limitations in the process to do so, which we will be documenting in this section.
<br/>

##### Inline Buttons
At first, our prompt/response flow was driven by text commands such as '/yes' or '/no', which served as a poor user experience. Fortunately, Telegram has provided well-documented alternative that uses inline buttons as a way to provide users with options to click on. This switch has drastically improved how the bot is interacted with, and we managed to reduce the total number of text commands to just three, with the rest of the bot's prompt/response flow being driven by inline buttons.

Example of inline buttons in use:

![manage_websites](https://user-images.githubusercontent.com/52826683/175877014-92722d43-c545-451b-bee2-9cc766a6e188.jpg)
<br/>

##### Photo Uploads
Telegram bots are generally not designed to receive photo uploads from users, and as such, there were very few examples available online on how this could be done. We were unable to successfully implement a photo capture protocol for the bot in time, and will focus on implementing it as our main priority, due to its importance in our 'create listings' and 'add agent details' function.
<br/>

##### Integrating Secure Payment Systems
Being able to successfully integrate a secure payment system will be crucial for our bot to evolve into a working and sustainable product. However, we lacked the confidence to be able to implement it in time for Milestone 1 as the documentation for it was not too comprehensive, and we needed much more time to experiment with it before implementing it into our bot.
<br/>

##### Design of Site
As we focused on the successful generation of the site, we had little time to design the site. For that reason, the generated site looked amateurish and improving its design will be one of our main priorities moving forward.
<br/>

#### Feedback Received 
We have received feedback from our submission in Milestone 1 and the areas of improvement mentioned will be stated below. We plan to take these feedback into heavy consideration and will integrate the excellent suggestions provided into our prototype.
<br/>

##### Unintuitive Navigation
One of the feedback we received was that every time a user wants to use the bot, they would have to input '/start' in order to begin using the bot. It was suggested that we implemented a menu to improve user experience.
<br/>

##### Unable to Test
Currently, the bot is being run locally on our laptops, and thus we are not able to facilitate testing of the bot. We plan to either run our bot on the cloud, or allow testers to specify a date and time where they would like to test the bot, after which we will keep the bot running on our end. 
<br/>

## Milestone 2 - Prototyping (27 Jun) (Completed)
Task  | Description | Handled by | Date
------------- | ------------- | -- | ---
Finalize Website Features | Picked out main website feature to add functionality for | Chengyue, Sean | 5 Jun
Integrate Telegram Payments | Integrate Stripe payments to allow users to make payment via bot | Sean | 7 Jun
Enabled Payment Test Mode | Payments are set to test mode, allowing for test payments to be made | Sean | 10 Jun
URL Availability Checker | Allowed availability of urls and price to be checked and returned | Chengyue, Sean | 11 Jun
Added Menu to Telegram Bot | Added menu to Telegram bot for easy navigation | Sean | 12 Jun
Data Structure Optimization | Completed Data Structures and Algorithms Course on Python | Sean | 14 Jun
Added Posts Function | Users are now able to make posts on their site via Telegram bot | Chengyue, Sean | 15 Jun
Enabled Photo Uploads | Telegram bot is now able to capture photo uploads made by users | Sean | 15 June
Added Listings Function | Users are now able to create new listings on their site via Telegram bot | Chengyue, Sean | 20 Jun
Improve User Experience | Prompt/Response flow improved to make interactions more user friendly | Sean | 22 Jun
Added Agent Details | Users are now able to add agent details onto their site via Telegram Bot | Chengyue, Sean | 25 Jun
Bot Testing | Bot testing to be done throughout the entirety of adding new functions | Chengyue, Sean | 27 Jun

### Milestone 2 - Poster Submission
As the poster is A1 sized, there are portions of the poster which you will have to zoom in to see. To download the full version of the poster, please click on the poster below.

<a href="https://drive.google.com/file/d/1e3ISfPmgETlF9_XtLrfvaAnVLYS6M74P/view?usp=sharing">
<img src="https://user-images.githubusercontent.com/52826683/175871671-eba2efe9-6d3d-4ffc-b39f-b40787c4c05a.png" width="500" height="775">
</a>

### Milestone 2 - Project Log
<a href="https://docs.google.com/spreadsheets/d/1Jiu08K7gVhJW_78oDguFb-8-r4jeRqJlmby4ro-4XWc/edit#gid=0">Milestone 2 Project Log (30 May - 27 June)</a>

### Post Milestone 2 Reflections
#### Limitations and Struggles
We were able to add integrate most of the website's features with the Telegram bot, and have extensively tested the bot to fix bugs that appeared along the way. However, there are a few minor features that we have yet to implement as it was either not a priority, or we were unable to confidently implement it as of Milestone 2.

##### Payment Testing
Currently, we are only able to test the payments on a Test Mode. For now, it has worked well as we are able to detect and confirm successful payments on our payments provider, Stripe. However, we were unable to test the bot out of Test Mode as that would require us to make actual payments, of which Stripe would be taking a cut of. We are planning to test the bot once with real payments to ensure that it works well by the end of Milestone 3.

##### Edit Listings
After successfully implementing the create and delete listings function, the next step would have been to add the 'Edit Listings' function. However, there are too many parts of a single listing and we took some time to a concrete conclusion on how we would like the prompt/response flow to look like. There were two possibilities.
1. Upon choosing the 'Edit Listing' option, the user would be prompted to provide a whole new set of details for the listing. This would be the much easier option, but would certainly not be as user friendly as we would have liked it to be.
2. Upon choosing the 'Edit Listing' option, the user would be asked which part of the listing they would like to edit. Currently, there are a total of five fields as seen below that they would be allowed to choose from. However, within each field, there may be multiple subfields/photos which we will have to create separate API calls for updating. 
- Title (Input string)
- Property Details, such as property type, number of rooms, address, tenure, total area, floor, price, and number of storeys (Input string)
- Description (Input string)
- Featured photo (.jpg/.png upload)
- Extra display photos (.jpg/.png upload)
As of now, we are planning to go with option 2, but this will take quite a bit of time to implement and will implementing the 'Edit Listings' function as our top current priority.

##### Edit Agent Details
The 'Edit Agent Details' function suffered from the same problems as mentioned in the 'Edit Listings' section. There were too many fields that would have required an extensive amount of time to include and test, which was why we have decided to implement it at a later stage and direct our atttention to ensuring that key features of the product were able to function properly at this time.

##### Agent Interviews
We intended to interview actual real estate agents to get more feedback on whether our product served as a sufficiently powerful product-market fit. However, we decided against conducting interviews prematurely and have decided to interview real estate agents at a later stage once we have a product that they can test. This would allow us to:
1. Receive feedback on whether our product fulfills their needs.
2. Find out if the design of the website is comparable to industry standards.
3. Receive suggestions on what other key features real estate agents would like to have integrated.

#### Feedback Received
To be added...

## Milestone 3 - Extension (25 Jul) (To Be Confirmed)
Task  | Description | Handled by | Date
------------- | ------------- | -- | ---
Add Edit Listings Function | Allow users to edit listings | Chengyue, Sean | 5 Jul
Interview Real Estate Agents | Find out what the current pain points are, and what we have missed | Chengyue, Sean|10 Jul
Website Analytics Tracking | Implement website backend system to capture web traffic | Chengyue | 10 Jul
Website Analytics Display | Provide analytics to users in an easy-to-digest manner on Telegram | Chengyue, Sean | 12 Jul
More Templates | Deploy more templates for users to pick from | Chengyue, Sean | 15 Jul
Insurance Agents Templates | Expand target audience to insurance agents | Chengyue, Sean | 20 Jul
Expand Customizability | Allow users greater customizability to their site | Chengyue, Sean | 22 Jul
User Testing | Allow selected real estate agents to build their websites using ezWeb | Chengyue, Sean | 24 Jul


# Collaboration Tools
Our project can be split into two main sections, the Telegram bot frontend, and the WordPress backend. Each of us took charge of one main section each and had to find a way to work closely together to ensure smooth collaboration. In order to maintain a strong and consistent level of communication, we used collaborative tools such as Trello to keep track of tasks. We also communicated via messaging platforms to ensure that we were both on the same page when it came to implementing new functions together.

Example of collaborative tool we used:
![Screenshot 2022-06-27 202545](https://user-images.githubusercontent.com/52826683/175942298-98365cb5-8afb-433c-9fe2-a68a1234b781.jpg)


# Working Prototype
Our Telegram bot has been set up to receive website creation requests, and capture url/description data which is sent to our database. On the backend, we will be able to retrive this data and generate a simple website on the given url.

After the site has been created, users can use the Telegram bot to create/edit/delete posts and listings, as well as add agent details to their site. This entire process accommodates photo uploads as well, thus allowing for users to be able to manage their website comfortably within the confines of their Telegram app.

## Website Creation
To start, navigate to @ezWebTest_bot to start the bot.


<img src="https://user-images.githubusercontent.com/52826683/170946015-acc9b552-d9af-4001-817e-14578df2d96c.jpg" width="210" height="450">

Inline message options will then be provided to the user to create a website or manage their current websites.

<img src="https://user-images.githubusercontent.com/52826683/170946029-9b0f39e6-c5bd-4e71-b218-8bd0bfef70b5.jpg" width="210" height="450">

After clicking on create a website, the user will be prompted for a desired url as well as a description for the website.

<img src="https://user-images.githubusercontent.com/52826683/170946053-261ceb20-7a87-4fcb-bcb5-68e75df4f461.jpg" width="210" height="450">

Following which, the user will be prompted to confirm the description and url. Upon confirmation, the data will be sent to our database, where the data will then be retrived for their site to be generated.

<img src="https://user-images.githubusercontent.com/52826683/170946061-678cab1c-9e28-4129-8832-ada21b081767.jpg" width="210" height="450">

Site will then be created. (The following is a placeholder sample site that is created with the desired url of the user)

![Screenshot 2022-06-26 233138](https://user-images.githubusercontent.com/52826683/175821725-bc4c690a-5094-4688-86f9-571d959ace1d.jpg)

## Update Website Description
Users who want to update their website description can simply run a /start command on the bot to start the process.

<img src="https://user-images.githubusercontent.com/52826683/170946073-4c6a7eaf-cf64-4396-b9bc-de97fd2846f2.jpg" width="210" height="450">

**Manage my websites** option is chosen, and data is retrieved from the database to display all websites registered to the user.

<img src="https://user-images.githubusercontent.com/52826683/170946082-c5ff5f8b-a3d3-4a64-964b-bc7aada60dda.jpg" width="210" height="450">

After picking the website to be updated, the current information of the site will be retrieved and shown to the user. The user will then be prompted on what changes they would like to make to the site. The user will then be asked to confirm their changes.

<img src="https://user-images.githubusercontent.com/52826683/170946092-6c879864-c05b-4172-845f-314009062493.jpg" width="210" height="450">

Upon confirmation, the new data will be sent to the database and updated. 

<img src="https://user-images.githubusercontent.com/52826683/170946106-dbc3ab40-f97f-46a3-982d-89b3925feb9d.jpg" width="210" height="450">

## Add Agent Details

## Create Posts/Edit Posts/Delete Posts
Users who want to create new posts or edit their current posts on their website can click on the menu button, and then choose the **Manage Websites** option. 

<img src="https://user-images.githubusercontent.com/52826683/175896599-8149c1f7-358c-482b-ab5b-0a5ebf4fc2b0.jpg" width="275" height="450">
<br/>

Data is then retrieved from our database to display all websites registered to the user. The user can then pick their desired website to create/edit/delete posts.

<img src="https://user-images.githubusercontent.com/52826683/175896926-99e1beda-b416-4300-80c1-1ee64c92e3b2.jpg" width="275" height="450">
<br/>

Following that, the user is presented with a list of actions that they can do to their website.

<img src="https://user-images.githubusercontent.com/52826683/175897122-b2946077-389b-49f3-a47d-fe4e7de12dbf.jpg" width="275" height="450">
<br/>

Upon choosing the 'Create new post' option, the user is then prompted to type in a title for his/her new post, following which, they would be asked if they would like to either confirm the title, change the title, or stop creating a post.

<img src="https://user-images.githubusercontent.com/52826683/175897348-27abe724-c673-4980-ba9b-6ed5a9eb1742.jpg" width="275" height="450">
<br/>

After confirming the title, the user is prompted to type in the content of his/her new post. Following which, they would be asked if they would like to either confirm the content, change the content, or stop creating a post.

<img src="https://user-images.githubusercontent.com/52826683/175897557-7d79a2ff-840a-4a59-9402-e255620e9e47.jpg" width="275" height="450">
<br/>

After confirming the content, the user is asked to confirm the upload of the new post.

<img src="https://user-images.githubusercontent.com/52826683/175897787-cebee6cf-8c8f-4f2d-b79f-51587ff429be.jpg" width="275" height="450">
<br/>

Following the confirmation of upload, the data is captured and processed in our backend, which leads to a post being generated on the user's site. After the post has been generated, a completion message is sent to the user. 

<img src="https://user-images.githubusercontent.com/52826683/175897990-2b780ec4-2a48-4dae-be32-a3d7b698fe5c.jpg" width="275" height="450">
<br/>

The post is generated as seen below.

![8](https://user-images.githubusercontent.com/52826683/175898102-bb163a69-4e84-4290-8ef0-f38b2d602695.jpg)

Link to test-generated listing: https://orbitaltest1.com.ezwebs.xyz/hi-i-am-william/


Post editing and deletion can be done following the bot's prompts after clicking on the 'Edit posts' or 'Delete posts' options instead of 'Create new post'.

## Create Listings/Edit Listings/Delete Listings
Users who want to create new posts or edit their current posts on their website can click on the menu button, and then choose the **Manage Websites** option. Data is then retrieved from our database to display all websites registered to the user. The user can then pick their desired website to create/edit/delete posts.

<img src="https://user-images.githubusercontent.com/52826683/175898629-a9c2ac29-9954-44bf-ac8a-d10125aae5bc.jpg" width="275" height="450">
<br/>

Following that, the user is presented with a list of actions that they can do to their website.

<img src="https://user-images.githubusercontent.com/52826683/175898774-ec7501bc-5898-405d-baca-f7c8b5a60d21.jpg" width="275" height="450">
<br/>

Upon choosing the 'Create new listing' option, the user is then prompted to type in a title description for his/her new listing, following which, they would be asked if they would like to either confirm the title description and proceed with adding the property details, or cancel the process of creating a new post.

<img src="https://user-images.githubusercontent.com/52826683/175899010-ee727aea-a0f7-4492-8bcd-eac4f089b92c.jpg" width="275" height="450">
<br/>

After choosing to proceed with adding the property details, the user is presented with a template that we have prepared for them. 

<img src="https://user-images.githubusercontent.com/52826683/175900148-c407226d-2aa8-48ec-9ae4-b11ae7464b5b.jpg" width="275" height="450">
<br/>

Upon typing in the property details, the bot captures the information and repeats it back to the user for confirmation. The user can now choose whether he is happy with the property details and to proceed to add a description, or choose to change the property details or stop the process of creating a listing.

<img src="https://user-images.githubusercontent.com/52826683/175900417-c3d84b07-5cde-4023-b1d5-67b46e4122b6.jpg" width="275" height="450">
<br/>

After the user types in the property description, the next step would be to upload a featured photo for the listing.

<img src="https://user-images.githubusercontent.com/52826683/175900591-2b4573ab-a0d3-4a2a-970f-8e967e80f91f.jpg" width="275" height="450">
<br/>

The user uploads his/her desired photo, and the bot captures this data and repeats it back to the user for confirmation.

<img src="https://user-images.githubusercontent.com/52826683/175900859-dfc66b1a-87c7-4987-9190-90bc73ddd8bc.jpg" width="275" height="450">
<br/>

Once users are happy with their featured photo, they can proceed with adding extra photos of the listing.

<img src="https://user-images.githubusercontent.com/52826683/175900870-fc461bf7-c70c-4a24-90df-3f2cbb2a2bcb.jpg" width="275" height="450">
<br/>

The bot prompts the user to send up to ten extra photos, with a manual command to signal that the user is done with adding extra photos.

<img src="https://user-images.githubusercontent.com/52826683/175901166-3d497ff5-3065-4a57-8d77-657d6a818d55.jpg" width="275" height="450">
<br/>


The user uploads nine different photos as seen below.

<img src="https://user-images.githubusercontent.com/52826683/175901420-e85ed9e9-b0a4-4f1a-9aa9-df6989548e35.jpg" width="275" height="450">
<br/>

The bot records the number of photos uploaded and reminds the user of the command that he/she can use to signal that they are done with uploading. After uploading nine photos, the tester sends the command.

<img src="https://user-images.githubusercontent.com/52826683/175901712-094006e1-742e-46bb-8282-3130c9ffe780.jpg" width="275" height="450">
<br/>

The bot then repeats the photos sent by the user and is asked for confirmation.

<img src="https://user-images.githubusercontent.com/52826683/175901777-6023f1b9-68b0-4c25-95e5-74b3d1846127.jpg" width="275" height="450">
<br/>

Finally, the user is prompted to confirm that they would like to upload this listing onto their website.

<img src="https://user-images.githubusercontent.com/52826683/175901934-413cc49b-7b9e-4217-af19-622ae6fd41e0.jpg" width="275" height="450">
<br/>

Data is sent to our backend for processing, which then uses the data provided by the user to generate a new listing

![14](https://user-images.githubusercontent.com/52826683/175902183-91fdad3c-20a6-4ee9-9019-614463baa4b0.jpg)

A few seconds after the user has confirmed the upload of the new listing, the new listing has been generated as seen below.

![15](https://user-images.githubusercontent.com/52826683/175902321-a1659418-d0c6-42da-9c8d-f41d13a043eb.jpg)

In addition, the address provided by the user is used to include a Google Maps display of where the property is located at. This feature would help site visitors to understand the surrounding environment of the property, which may influence their interest in the property.

![16](https://user-images.githubusercontent.com/52826683/175902411-c907f9d6-e757-480c-b08d-ac8cc8a53621.jpg)

Link to test-generated listing: https://orbitaltest1.com.ezwebs.xyz/listing/blk-998-street-38/




# Website Features (As of Milestone 2)
As of milestone 2, we have added functionalities for agent details, posts, and listings to be displayed in an aesthetically pleasing and professional manner to site visitors. When visiting the links below, it is recommended for you to use a laptop to view the website as the site is not yet compatible with mobile phone devices.

## Agent Details
Through the Telegram bot, users can click on the 'Manage Websites' option to add their agent details. Currently, the following information is obtained from the user via the Telegram bot.
- Two agent pictures (.jpg/.png upload)
- About Me (Input string)
- Contact Details (Input string)
- Agent Quote (Input string)
- Email Address (Input string)
- Name (Input string)


These agent details are designed to allow for visitors to contact the agent easily if they are interested in paying for the services of the agent. The following is how the generated site will look like after the user has submitted their agent details.
![Agent Details](https://user-images.githubusercontent.com/52826683/175799578-20c1da13-9fef-49bd-81bf-7805e9e3f442.jpg)
Link to test-generated site: https://wordpress-296143-2675827.cloudwaysapps.com/
<br />
<br />
## About Me
Users are able to add their About Me section through providing a string of text to the Telegram bot. Which will serve as a way for visitors to get to know the agents on a more personal level. The following is an how the About Me section will look like.
![About Me](https://user-images.githubusercontent.com/52826683/175799584-414a1afb-5e2f-4097-9b4b-1f39e5b0577f.jpg)
<br />
<br />
## Posts
Through the Telegram bot, users can click on the 'Manage Websites' option to add, delete, or edit their posts. Currently, the following information is obtained from the user via the Telegram bot.
- Title (Input string)
- Content (Input String)

The following is an example of what a post may look like on the home page.


![Posts](https://user-images.githubusercontent.com/52826683/175799588-45a6cead-d4c1-4765-a765-73d0e95622df.jpg)
Upon clicking into the post, the following is what visitors will see.
![Screenshot 2022-06-26 154718](https://user-images.githubusercontent.com/52826683/175804782-863dca83-21f7-4e03-a5bd-318b339f7ae1.jpg)
Link to test-generated listing: https://wordpress-296143-2675827.cloudwaysapps.com/hello-world/
<br />
<br />
## Listings

Through the Telegram bot, users can click on the 'Manage Websites' option to add, delete, or edit(Work in progress) their listings. Currently, the following information is obtained from the user via the Telegram bot.
- Title (Input string)
- Property Details, such as property type, number of rooms, address, tenure, total area, floor, price, and number of storeys (Input string)
- Description (Input string)
- Featured photo (.jpg/.png upload)
- Extra display photos (.jpg/.png upload)


The following is how a listing may look like on the home page.


![Listings](https://user-images.githubusercontent.com/52826683/175799589-3cde12e2-25a8-42a0-bfd2-fe439d9eb435.jpg)
After clicking into the listing, the user will be brought to the listing's page which will provide a much more comprehensive introduction to the property.
![Screenshot 2022-06-26 155204](https://user-images.githubusercontent.com/52826683/175804958-7df66aed-2a5f-45b0-b672-e01181000687.jpg)
![Screenshot 2022-06-26 155212](https://user-images.githubusercontent.com/52826683/175804960-03b8a8c2-139f-4e51-bffa-d467226068ba.jpg)
Link to test-generated listing: https://wordpress-296143-2675827.cloudwaysapps.com/listing/gg/


