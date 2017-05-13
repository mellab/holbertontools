Scraper for Holberton Projects

Logs into Holberton's intranet and downloads project pages based on the
project number, and then attempts to generate the required directories
and files.

scrapersetup.py can be used to install the scraper to your PATH
		and moves all templates to /usr/include, necessary
		to use templates for your files.

Usage:

./scraper.py <project number> <operation>

Valid operations:
      touch: Goes through the project page to grab file names and folders
      	     and creates the necessary files, pushing templates to the files
	     where possible.
      name: Prints all file names
      fullname: Prints all file names with the directory
      directories: Prints a list of directories used
      all: Prints a prettified version of the project page source