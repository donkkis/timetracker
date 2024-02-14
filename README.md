# Time Tracker

CLI based time tracker for people needing to track their daily spent time with various projects/
clients/etc.

## Building the app

Just run `make` and place the resulting executable `dist/tt` in a directory listed in your `PATH`,
e.g.:

`cp dist/tt /home/panu/.local/bin`

Then, you'll be able to run commands like `tt workon`, `tt status` and `tt today`. For a full list 
of options, just run `tt`

## Database solution

`SQLite` is used as a backend solution. Upon first run, a file is created in 
your `~/.time-tracker/time-tracker.db`. Subsequent runs of `make` will _not_ overwrite this file,
but you'll be able to access your old time entries and projects even if install a new version. That
is, of course, provided the code itself does not contain any breaking changes towards the DB schema