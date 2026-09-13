Name : Kevin Nicholas Santoso

NPM : 2506637041

Class : PBP KKI

### Assignment 1

1. During the design of the HTML5 in tutorial 1 and assignment 1, the semantic element <section>, <main>, and <footer> was used. The section tag especially has helped me tremendously in grouping certain parts of the html and what parts to be targeted by the css file. In my opinion, with only the use of these semantic tags, my website has met my expectations and design needs.

2. When setting up the CSS, I had found complications about the spacing and padding between elements. For example, in the skills section, the boxes that seperate the different skills used to be sticking next to each other unless the mouse cursor is hovering over the box. This css code was old code I had from high school when designing my HTMLs. Generative AI was used in this part to find out how to correctly space the boxes. Furthermore, I also had to use generative AI to find out the correct sizes when each media size would be used and what elements should change (tablet, mobile, small mobile). However, the code for the resizing is according to my own trial and error

3. So far, due to the limited information currently in my website. I currently have felt no limitiations in making my static website. However, as more and more things get added to the website, I feel that dynamic functionality can be implemeneted to make my website more interactive. Currently, I have been thinking about adding a dark mode to my website that only activates during nighttime according to the computer clock. However, this idea is still barebones and I believe that the longer I study more about platform based programming, more creative ideas should appear that would make my website more professional, but also more interactive.

### Assignment 2

1. When a user opens the new portfolio page, the browser sends an HTTP request to the Django server and the project's urls.py receives it first and routes it to the correct application by matching the URL prefix. The application's urls.py then matches the specific path (projects/) and calls the associated view function registered under a name like main:project_list. This acts as the bridge between the database and the response: it queries the model (Project.objects.all()) to retrieve the stored data and packs it into a context dictionary. Django then passes that context to the template (projects.html), which uses the Django Template Language to loop through the objects and generate the final HTML. 

2. Storing the data in a model rather than hard-coding it into the template separates content from presentation. With a model, the data lives in the database and can be edited, added, or deleted without touching any HTML, so updating a project entry requires only changing a record instead of searching through template code. This makes maintenance far easier because there is a single source of truth, and mistakes like inconsistent formatting or duplicated information are avoided.

3. makemigrations scans the models.py files, compares them to the existing migration history, and generates new migration files that describe the changes that need to be applied to the database schema. migrate takes those generated migration files and actually executes them against the database, creating, altering, or dropping tables and columns so the database matches the models. For example, if a new field such as year = models.IntegerField() is added to an existing Project model, we must first run python manage.py makemigrations to create a migration file for that change, then run python manage.py migrate to apply it so the new year column actually exists in the database table. 