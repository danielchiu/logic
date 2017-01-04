random notes:

app.run(debug = True) => set debug mode

remember to ctrl-shift-R to reset cache

can find a game at /game/<some string>

html 4 requires action tag so look into that
(html 5 defaults to just the same page)

pickling might not work with mod_wsgi watch out

things to keep in mind:
1. watch .pyc files (esp ones that web server can't access)
2. logging works now
3. when do we need to restart apache
   internal caching

process to add column to database:
1. copy app.db to app.db.bak (or something) in case of a later mistake
2. > sqlite3 app.db
3. > alter table Game add column chat BLOB;
   (replace Game with the model name, replace chat with column name, replace BLOB with the type)
4. done, so just update code (in particular Game constructor if necessary)
5. if the column can't be None, run updateDatabase() to change all existing entries

TODO list:
- make timestamps show seconds on hover
- port to own domain (not catlin.edu)
- lobbies
- timed games?
- perhaps flip passed cards on declare
- autosave notes
- store times server side
- add secret nonrandom hands game maker
- add accounts
