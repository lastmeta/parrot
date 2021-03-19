# Parrot

Simple backup system on home lan

## how it works

if you have many computers on a home lan you can install parrot on one of them, the one with the most room.

Fill out the config file which specifies what folders (and sub folders) should be saved to what locations.

Now you have a backup of all your important data.

Parrot will constantly run, pinging the computers to see if they're up. If it finds that they are it will constantly watch the folders that belong to that computer and if any new files show up it will get copied to the backup location. If any files change they will replace the existing files at the backup location.

What if the same file it backsup already exists in the backup? Parrot will delete the old one so there's no unnecessary redundancy, a feature that can be turned off via the config. That way you can rearrange files in a folder meant to be backedup and the backup location will match your arrangement.

Parrot prints a log of everything it backs up.
