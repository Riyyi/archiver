# archiver
archiver is a simple 4chan archiver / browser

## Requirements:

- BASC-py4chan
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- humanize

## About the archiver:

The archiver is written in a way where the scraping from the API and the browsing of the contents is separated.<br>
The file `que.py` does the actual scraping, this is a stand alone python file should always be running in the background.<br>
Threads can be added to the Que via the /que page of the application, or by running the command:<br>
`./que.py -A https://boards.4chan.org/b/thread/[THREAD_NUMBER]` or<br>
`./que.py --add https://boards.4chan.org/b/thread/[THREAD_NUMBER]`

## Todo:

- Configure the application to be a proper Flask app (config.cfg)
- Make the application compatible with setuptoools
- Browsing on a board (board.html):
    - Move more template html into macros (Information that is in an OP vs regular thread post)
    - Add stickied thread functionality
    - Display the threads in a time-based order (the one with the newest post comes first)
    - Add country flags to posts in boards that have this enabled (ex: /pol/)
      - Add setting to boards to enable/disable this functionality
- Browsing a thread:
  - Create this page
- Implement catalog:
  - Searching inside the catalog
- If an image already exists: return ID, in 'Add thread' and in the 'Que' < ??
- Mobile version of the page:
  - Thread title
  - Update / double check html
- Look into:
  - Updating comments:
    - Banned/removed, image removed from the post.
  - Defining what is what: 
    - Closed / archived threads and when to display them.
      <br>(Can you pull closed thread that are archived from the API?)
  - Create a way to post as a certain rank
    - Login system?
  - Reseach native extension
    - Should we try to convert the original to work with this apllication?
      - If yes, should we archive the extension version or get the latest each time?
    - Should we create our own extension?
