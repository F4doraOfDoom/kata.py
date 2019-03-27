# kata.py
Simple Python script to get a user's CodeWars points in a specific language.

This script catogarizes the points according to the according rule:
White kata - 1 points
Yellow kata - 2 points
Blue kata - 3 points
Purple - 4 points

Usage:
python3 kata.py -u/--user [CodeWar's username] -l/--lang [Programming Language]
Optional flags:
-v/--verbose, if you want the program to be print each challenge as the program acquires it from the CodeWar's API.
