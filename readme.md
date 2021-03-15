# Parrot

Simple backup system on home lan

## how it works

if you have many computers on a home lan you can install parrot on one of them, the one with the most room.

Fill out the config file which specifies what folders (and sub folders) should be saved to what locations.

Now you have a backup of all your important data.

Parrot will constantly run, pinging the computers to see if they're up. If it finds that they are it will constantly watch the folders that belong to that computer and if any new files show up it will get copied to the backup location. If any files change they will replace the existing files at the backup location.

Parrot does not backup a file if it's already somewhere in the backup (name and hash already exist) even if it's at a different location.

Parrot makes a log of everything it backs up.

Parrot will never purge files, but will overwrite them if there are new files with the same name.

## todo

One feature that might be nice is to make a database with a hash for each file it copies. that way you have the option of avoiding copying any file that is already backed up. that way you don't have to worry about redundant backup files.
