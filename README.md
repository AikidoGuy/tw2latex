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
- [ ] learn how to use LaTeX on Ubuntu https://help.ubuntu.com/community/LaTeX (I originally developed this code using MikTex on Windows).
- [ ] test with newest TaskWarrior release

LaTeX on Ubuntu
---------------
    $ latex --version
    # pdfTeX 3.1415926-1.40.10-2.2 (TeX Live 2009/Debian)
    # kpathsea version 5.0.0
    # Copyright 2009 Peter Breitenlohner (eTeX)/Han The Thanh (pdfTeX).
    # There is NO warranty.  Redistribution of this software is
    # covered by the terms of both the pdfTeX copyright and
    # the Lesser GNU General Public License.
    # For more information about these matters, see the file
    # named COPYING and the pdfTeX source.
    # Primary author of pdfTeX: Peter Breitenlohner (eTeX)/Han The Thanh (pdfTeX).
    # Compiled with libpng 1.2.46; using libpng 1.2.46
    # Compiled with zlib 1.2.3.4; using zlib 1.2.3.4
    # Compiled with poppler version 0.18.2
    # I have a latex installed... but what is it?
    $ apt-cache search latex
    $ apt-cache search texlive | grep latex
    $ apt-cache show texlive-latex3
    # It is Tex Live.
    #    See: /usr/share/texmf
    #    See: /usr/share/texmf-texlive/tex/latex/base/article.cls
    #    See: http://www.tug.org/texlive/
    #
    # There are Ubuntu packages and there is a native TeX Live that can be installed directly from TUG.
    # It was suggested that this way you can get (nearly) all of the packages that are currently available on CTAN and
    # you do not need to install anything by hand. Also this lets you always get current package versions by running
    $ sudo tlmgr update --all
    #
    # And according to TUG, "the timing and content of updates is entirely up to your operating system provider"
    # So... I start to install a native TeX Live side-by-side with the Ubuntu version.
    # It will take up quite a bit of hard disk space... I am installing 2,436 packages.
    #    http://www.tug.org/texlive/acquire-netinstall.html
    $ sudo ./install-tl
    # TEXDIR (the main TeX directory):                        /usr/local/texlive/2012
    # TEXMFLOCAL (directory for site-wide local files):       /usr/local/texlive/texmf-local
    # TEXMFSYSVAR (dir for variable and auto generated data): /usr/local/texlive/2012/texmf-var
    # TEXMFSYSCONFIG (directory for local config):            /usr/local/texlive/2012/texmf-config
    # TEXMFVAR (personal dir for variable and auto gen data): ~/.texlive2012/texmf-var
    # TEXMFCONFIG (personal directory for local config):      ~/.texlive2012/texmf-config
    # TEXMFHOME (directory for user-specific files):          ~/texmf
    #
    # One LaTeX editor is Kile, installable by:
    $ sudo apt-get install kile

Suggestions for improvement are welcome.

Aikido Guy
