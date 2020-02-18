# main.py
main.py is a program for dealing with a csv file and creating a map of where up to 10 films
were shot,whose location is the closest to the given by the user input location and the year. 

## be careful
The program works pretty fast but no stupid input is recommended to do (like invalid location's coordinates)

# Some HTML basics
### Introduction
HTML is a HyperText-MarkupLanguage, used greatly for creating web-pages. It is often confused with CSS (Cascading Style Sheets), which basically allows styling the web-pages. HTML is the standard language for front-end development. 
## Structure
HTML is written in the form of the tags (e.g `<example_tag>`), some of them are doubled (=go in pairs, 
e.g. `<example_tag>Some text</example_tag>`), some of them are singled. 
### Some of the important tags and their functions
* `<!DOCTYPE>` determines the type of the document.
* `<html>` is the doubled tag, some sort of container for the entire web-page
* `<head>` is the doubled tag, contains the information about the page
* `<body>` is also doubled tag, contains the "body", the visible information of the page.
* `<h1>`-`<h6>` are doubled tags, determine headings and numbers stand for the priority of the headings (=how big they are) from the smallest to the greatest
# WEB-Coclusions
The program basically provides with the icons of the movies on the map
and their names.
# How it looks
## launching
```python
    >>> python main.py
    Please enter a year you would like to have a map for: 2014
    Please enter your location (format: lat, long): 50.411778, 30.469194
    Map is generating...
    Please wait...
    Finished. Please have look at the map2014_movies_map.html```
