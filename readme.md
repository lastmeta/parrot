# Parrot

Simple backup system on home lan

## how it works

if you have many computers on a home lan you can install parrot on one of them, the one with the most room.

Fill out the config file which specifies what folders (and sub fodlers) should be saved to what locations.

Now you have a backup of all your important data.

Parrot will constantly run, pinging the computers to see if they're up. If it finds that they are it will constantly watch the folders that belong to that computer and if any new files show up it will get copied to the backup location. If any files change they will replace the existing files at the backup location.
