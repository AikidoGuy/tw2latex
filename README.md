tw2latex
========

Task Warrior to LaTeX python utility.

This is being made available sooner that I was planning because I received an email request
for it. Please be aware that it is a work in progress.

Usage
-----
Further information and discussion is available at: http://taskwarrior.org/boards/6/topics/2084

    $ vi tw2latex.py           # and modify settings near top of file to suit your needs
    $ chmod 700 tw2latex.py
    $ ./tw2latex.py            # to get a list of all options

Dependencies
------------
- python
- python package pytz available from: http://pytz.sourceforge.net/
- LaTeX (http://www.latex-project.org/guides/)
- chronology.sty available from: http://www.ctan.org/pkg/chronology

List of Things to Improve
-------------------------
- [x] 2013/03/24: placed first version on github
- [x] 2013/03/24: added 'createReport.sh' to show example usage for inclusion of filters. This occured because
      during development of this code I needed to have one filter for the set of tasks and one filter
      for the timeline. Anyway, this is how the current code works... slightly unexpectedly, I presume! :)
- [ ] learn how to use LaTeX on Ubuntu https://help.ubuntu.com/community/LaTeX. I originally developed this code using MikTex on Windows.
- [ ] test with newest TaskWarrior release

Suggestions for improvement are welcome.

Aikido Guy
