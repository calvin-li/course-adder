# course-adder
Automatically scrapes and adds CS classes from SISWEB into google calendar

Usage:
1. Follow the instructions at https://developers.google.com/google-apps/calendar/overview#quickstarts for the language of your choice
  - Currently, everything is done in Python.

2. Use the SISWEB class search to get a list of the classes you want to add. Save the source to an html file.
  - The scraper might not work for classes without a discussion section. 
  - SISWEB does not return classes that are full.
  - Any webpage that has the classes would work, but SISWEB was the simplest

3. Run scraper.py to generate a json with the class information from the html.
  - The html file path is hard coded
  - Check courses.json for an example json file. It is important to follow the formatting for the dates and recurrence rules exactly.

4. Run adder.py on the json file to add the classes as events on the calendar.
  - The calendar url can be found under calendar settings in the Google Calendar web UI.
  - The calendar url and json file are hard coded.

IMPORTANT: The adder clears the calendar before adding the classes. Either remove the code first, or run on an empty calendar and copy the events over afterwards (recommended).

NOTES:
- The Google Calendar API requires a start date for the first class, and a date to end the recurrence on. These will probably need to be hard coded.
- The scraper will have to be rewritten if the source of the html changes.
