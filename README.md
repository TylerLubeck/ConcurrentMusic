ConcurrentMusic
===============

To run conductor: python conductor.py --song [song file] --port [port to listen
on]

To run musician: python musician.py --ip [ip address of conductor] --port [port
conductor is listening on]

Default ip is localhost, and default port is 8123.

To parse a song file: python parse.py [song file]

To compile the LaTeX report:
* Make sure you are in the report subdirectory
* pdflatex project-final-report.tex

