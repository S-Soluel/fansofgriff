# Fans of Griff - Griff Tracker (CS 191 Capstone Project)

Joe Barnard, Maddie Backhaus, Maddie McEarlean, Sam Solheim


## Project Description:

Using Python, AWS, JavaScript, and HTML, our group has created a website to hypothetically track our live mascot, Griff II, when he visits Drake University's campus. We are currently using a Tile Mate tracker on ourselves rather than on Griff II for location data.

## Methodology & Scope:

-   Using the pytile API, we built a Flask app hosted by Amazon Web Services to call a Tile Mate tracker’s coordinates.
    
-   The website has an embedded Open Street Maps view of Drake University’s campus with the location of Griff II drawn on top.
    
-   Our system is self-sufficient and should not require any interaction by Griff II's handler once it is set up, except for updating the Google Calendar with Griff’s events.
    
-   We ignore the location data coming from pytile as soon as the tracker leaves Drake’s campus and surrounding area, noted by boundary coordinates we set in our code.
    

## Deliverables:

-   We launched a web page with four pages - one containing a map of Drake University’s campus and an Agenda overview of Griff’s events, one containing a full Calendar page of Griff’s events, one containing an email subscription system, and one containing an unsubscribe page.
    
-   When Griff II is on campus, his location will be displayed on the map, updating periodically to keep up-to-date on his location. When he is off campus, location data will not be available.
    
-   Users can subscribe and unsubscribe from email notifications when Griff is found to be on campus.
    

## Tools & Technologies:

-   Tile Mate Bluetooth LE Tracker
-   Github
-   Flask
-   Python
-   HTML
-   pytile API   
-   AWS
-   Amazon EC2
-   Amazon Simple Email Service
-   Google Calendar Customization and Editing
-   Other AWS Services as needed for website visuals
