# Good Dive? (goodive.com)

### A simple website where users can rate and review the dive sites of Una-Una, Sulawesi, Indonesia
Good Dive? is a web based application using HTML, CSS, JavaScript, Python and SQL, also utilising the Flask python module and the Lux bootstrap theme.

The website is quite basic: a simple navbar with options to view Una Una information, a dive site map with a list of the sites, a top 5 dive site dropdown, an about Good Dive? page and register & login or logout views depending on if the user is logged in or not.

The core of the program and what I wanted to get out of the project was the website interaction with a SQLite database using Python and Flask, therefore the website design was kept short and sweet.

Each dive site page shows the dive site name and rating above the fold, and follows beneath the fold with a short dive site description, a simple title, comment and rating input box if the user is logged in and finally the respective comments.

> I have detailed many ideas for the future on the about page, but my priority is to to add more detail to the user input such as:
>
> - The ability to upload photos and then display these on each dive site page
> - Species/animals seen
> - Dive time
> - Dive site conditions (visibility, current etc)
> - Dive centre and dive guide
> - Morning/afternoon/night dive


### The Program
I have one main flask application file which most of my website runs from and one additional blueprint for the edit and delete comments functions. The functions/routes in my main application file are as follows: index, register, login, logout, una-una, sites, about, divesite and an error handler.

Alongside this, I have a seperate functions file which the two main flask files detailed above import from to streamline and reduce the amount of code on one page. Most functions consist of SQL SELECT, INSERT, UPDATE or DELETE for users, dive site or comment information, plus a couple of error checking functions.

Last but not least is the database file containg the three SQLite tables: 'users', 'sites' and 'comments'.

I have created two flask template files, one for the main website pages (about.html, sites.html and unauna.html) and one for the dive site pages. In the future I would like to merge these into one file. Currently, both files contain repeated code for the navbar.

The main part of my program is the 'divesite' function contained in application.py. On a 'GET' HTTP request method this function takes a dive site name as an argument from which it query's the database for all information needed such as rating and reviews to load that dive site's page. The href for this would be:

> `href="{{ url_for('divesite', sitename= ###) }}"`

On a 'POST' HTTP request method this function grabs the users review from the page, error checks the input, SQL INSERTS the comment, and loads the dive site page with updated rating and comment information.

The original plan was to create a unique function for each dive site (35 in total!!!). Each function starting by me statically assigning a dive site name variable and then querying from there as above. I actually finished the website with that design. I always realised that I had been copying and pasting a lot for each function, but as CS50 and David Malan have taught me, I knew copying and pasting was bad. However, in the process of learning more deeply about python and flask, I was able to streamline this design by passing the function a sitename argument.

I have added front-end error checking with JavaScript to ensure that the user correctly inputs information, such as 'minlength' and 'required'. I have also added backend error checking using python if the user knows how to get past the JavaScript. Upon any backend errors, an apology page will be loaded with the correct code and a unique error message detailing the issue.

I am sure my program is terribly inefficient or too memory heavy as I pass each render_template/webpage a lot of information. I was part of the 2/3 of people taking CS50 that had never coded anything before so this whole course was a huge learning curve for me. In the first week I got cold sweats thinking about my final project - "how I would manage to build something myself?!?!". It was an extremely compelling moment for me to realise I had been writing my final project in 5 different languages (albeit quite simply for some).

### The story of Good Dive?'s inception
As with many people in the world, due to COVID I have lost my job working as a dive instructor for the next year on the beautiful, little island in which this website is based called Una Una, Sulawesi.
I did my PADI Divemaster training at Pristine Paradise Dive Resort, Una Una in early 2019 and got to know all the dive sites extremely well.
Later on that year I went back to co-manage and run the dive centre, working as a Divemaster alongside my partner Sarina. With each new set of guests, we would be explaining and detailing the best dive sites to visit.
Most people stay on Una Una for somewhere between 3 days and a week, some longer. As you can imagine explaining the dive sites is a huge part of the job.
I had planned to make dive site maps and write descriptions and get it printed out for the guests to read so they could have a resource to enable them to decide which spots they want to go to in their limited time on the island.

Good Dive? is the answer to this problem. Divers coming to Una Una can use it such like Trip Advisor would work, letting them see the top rated dive sites and viewing comments from divers before them.
There are two dive centre's on the island, and during high season these two centres are packed full. Other dive centres from nearby islands visit daily as well, because Una Una hosts some of the best diving in the Archipelago in which it lies.
If just 10% of the divers visiting the dive sites there would leave reviews and ratings, future divers would be able to use Good Dive? alongside the invaluable knowledge that the dive centres and guides could provide to have the best possible Una Una diving experience.