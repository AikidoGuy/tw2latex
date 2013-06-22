tw2latex
========

Taskwarrior to LaTeX python utility. A little rough around the edges... but smoothing things out slowly :)

Usage
-----
Further information and discussion is available at: http://taskwarrior.org/boards/6/topics/2084

    $ vi tw2latex.py           # and modify settings near top of file to suit your needs
    $ chmod 700 tw2latex.py
    $ ./tw2latex.py            # to get a list of all options
    $ cd examples
    $ vi createReport.sh       # and modify to suit your needs (e.g. change filter, etc.)
    $ ./createReport.sh        # to create *.tex and *.pdf based on your settings
                               # uses chronology.sty if a timeline is selected

Dependencies
------------
    python
    python package pytz                 # See: http://pytz.sourceforge.net/
    python package dateutil             # On Ubuntu: sudo apt-get install python-dateutil
    LaTeX                               # See: http://www.latex-project.org/guides/
    chronology.sty                      # See: http://www.ctan.org/pkg/chronology

Chronology.sty is a LaTeX 'sty'le file and should be placed in the same directory as the generated LaTeX file \*.tex
if it is not already installed as a package in your LaTeX system so that LaTeX will be able to find it. On Ubuntu, if
you follow the directions below for installing LaTeX, then the chronology.sty package will already be installed and available
for use... so you do not need to download or directly do anything yourself.

List of Things to Improve
-------------------------
- [X] 2013/05/03: make simple filter usage work; use filter overrides for more complex cases
- [X] 2013/03/24: placed first version on github
- [X] 2013/03/24: added 'createReport.sh' to show example usage for inclusion of filters. This occured because
      during development of this code I needed to have one filter for the set of tasks and one filter
      for the timeline. Anyway, this is how the current code works... slightly unexpectedly, I presume! :)
- [X] 2013/03/24: learn how to use LaTeX on Ubuntu https://help.ubuntu.com/community/LaTeX (I originally developed this code using MikTex on Windows).
- [X] 2013/03/24: test with newest Taskwarrior (works with 2.1.2 on Ubuntu)

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
    #    http://tex.stackexchange.com/questions/28627/how-to-install-the-algorithms-package
    $ sudo tlmgr update --all
    #
    # And according to TUG, "the timing and content of updates is entirely up to your operating system provider"
    # So... I start to install a native TeX Live side-by-side with the Ubuntu version.
    #    http://www.tug.org/texlive/acquire-netinstall.html
    #    It will take up quite a bit of hard disk space... I am installing 2,436 packages.
    $ sudo ./install-tl
    #    It failed five times, but it was very easy to restart the installation
    $ sudo ./install-tl --profile installation.profile
    #    TEXDIR (the main TeX directory):                        /usr/local/texlive/2012
    #    TEXMFLOCAL (directory for site-wide local files):       /usr/local/texlive/texmf-local
    #    TEXMFSYSVAR (dir for variable and auto generated data): /usr/local/texlive/2012/texmf-var
    #    TEXMFSYSCONFIG (directory for local config):            /usr/local/texlive/2012/texmf-config
    #    TEXMFVAR (personal dir for variable and auto gen data): ~/.texlive2012/texmf-var
    #    TEXMFCONFIG (personal directory for local config):      ~/.texlive2012/texmf-config
    #    TEXMFHOME (directory for user-specific files):          ~/texmf
    # Success!
    $ vi ~/.bashrc
    $ PATH="$PATH:/usr/local/texlive/2012/bin/x86_64-linux"
    #
    # Remove the old texlive that was installed in Ubuntu
    $ sudo apt-get remove texlive
    #
    # Swap the order of the path in .bashrc to make sure I get my new latex
    $ PATH="/usr/local/texlive/2012/bin/x86_64-linux:$PATH"
    $ source ~/.bashrc
    #
    $ latex --version
    # pdfTeX 3.1415926-2.4-1.40.13 (TeX Live 2012)
    # kpathsea version 6.1.0
    # Copyright 2012 Peter Breitenlohner (eTeX)/Han The Thanh (pdfTeX).
    # There is NO warranty.  Redistribution of this software is
    # covered by the terms of both the pdfTeX copyright and
    # the Lesser GNU General Public License.
    # For more information about these matters, see the file
    # named COPYING and the pdfTeX source.
    # Primary author of pdfTeX: Peter Breitenlohner (eTeX)/Han The Thanh (pdfTeX).
    # Compiled with libpng 1.5.10; using libpng 1.5.10
    # Compiled with zlib 1.2.7; using zlib 1.2.7
    # Compiled with xpdf version 3.03
    #
    # One LaTeX editor is Kile, installable by:
    $ sudo apt-get install kile
    #
    # I have now run the 'createReport.sh' using my new latex environment on Ubuntu and everything works

To Update LaTeX Packages on Ubuntu
----------------------------------
Here is an example that I used to update all of my packages to the latest versions today (8th May 2013):

    $ sudo `which tlmgr` update --all
    TeX Live 2012 is frozen forever and will no
    longer be updated.  This happens in preparation for a new release.
    
    If you're interested in helping to pretest the new release (when
    pretests are available), please read http://tug.org/texlive/pretest.html.
    Otherwise, just wait, and the new release will be ready in due time.
    tlmgr: package repository http://ctan.mirror.rafal.ca/systems/texlive/tlnet
    tlmgr: saving backups to /usr/local/texlive/2012/tlpkg/backups
    [ 1/80] auto-remove: macqassign ... done
    [ 2/80, ??:??/??:??] update: abntex2 [3523k] (29221 -> 29502) ... done
    [ 3/80, 00:14/10:26] update: acro [509k] (29073 -> 29681) ... done
    [ 4/80, 00:16/10:26] update: amsaddr [196k] (15878 -> 29630) ... done
    [ 5/80, 00:18/11:11] update: biblatex-caspervector [268k] (28808 -> 29577) ... done
    [ 6/80, 00:20/11:41] update: biblatex-fiwi [522k] (28491 -> 29578) ... done
    [ 7/80, 00:23/12:03] update: biblatex-philosophy [503k] (29411 -> 29571) ... done
    [ 8/80, 00:26/12:23] update: bidi [1130k] (28144 -> 29650) ... done
    [ 9/80, 00:29/11:27] update: chronology [15k] (18994 -> 29682) ... done
    [10/80, 00:31/12:13] update: cleveref [470k] (27807 -> 29503) ... done
    [11/80, 00:34/12:31] update: cm [238k] (24956 -> 29581) ... done
    [12/80, 00:36/12:50] update: crbox [31k] (24414 -> 29701) ... done
    [13/80, 00:37/13:08] update: dashrule [233k] (15878 -> 29579) ... done
    [14/80, 00:39/13:25] update: dowith [1192k] (28401 -> 29501) ... done
    [15/80, 00:43/12:48] update: dvips [581k] (28616 -> 29585) ... done
    [16/80, 00:45/12:34] update: embrac [445k] (29483 -> 29683) ... done
    [17/80, 00:47/12:32] update: endiagram [669k] (27489 -> 29684) ... done
    [18/80, 00:50/12:29] update: enotez [443k] (29422 -> 29696) ... done
    [19/80, 00:52/12:28] update: environ [150k] (15878 -> 29600) ... done
    [20/80, 00:53/12:32] update: etoc [301k] (29289 -> 29697) ... done
    [21/80, 00:56/12:54] update: exsheets [733k] (29334 -> 29685) ... done
    [22/80, 00:58/12:33] update: filedate [559k] (28242 -> 29529) ... done
    [23/80, 01:00/12:25] update: fontawesome [171k] (29485 -> 29498) ... done
    [24/80, 01:02/12:39] update: fouriernc [49k] (15878 -> 29646) ... done
    [25/80, 01:03/12:49] update: ftnxtra [28k] (17317 -> 29652) ... done
    [26/80, 01:04/12:59] update: ghab [29k] (24578 -> 29701) ... done
    [27/80, 01:09/13:58] update: hyph-utf8 [1948k] (29193 -> 29641) ... done
    [28/80, 01:13/12:51] update: iftex [32k] (18833 -> 29654) ... done
    [29/80, 01:15/13:10] update: imakeidx [512k] (28240 -> 29542) ... done
    [30/80, 01:16/12:54] update: imsproc [71k] (26198 -> 29701) ... done
    [31/80, 01:19/13:21] update: media9 [4634k] (29445 -> 29530) ... done
    [32/80, 01:23/10:48] update: mpgraphics [165k] (27230 -> 29655) ... done
    [33/80, 01:25/10:59] update: nameauth [682k] (29359 -> 29632) ... done
    [34/80, 01:27/10:52] update: needspace [158k] (19684 -> 29601) ... done
    [35/80, 01:30/11:10] update: newtx [3869k] (29152 -> 29551) ... done
    [36/80, 01:47/11:13] update: paratype [4788k] (26866 -> 29629) ... done
    [37/80, 01:58/10:23] update: pdftex [2805k] (29349 -> 29585) ... done
    [38/80, 05:25/26:10] update: persian-hm-ftx [32015k] (29146 -> 29700) ... done
    [39/80, 09:06/22:11] update: persian-hm-xbs [31801k] (29147 -> 29616) ... done
    [40/80, 09:45/15:56] update: persian-modern [1950k] (23959 -> 29701) ... done
    [41/80, 09:56/15:55] update: pgfplots [10547k] (29349 -> 29531) ... done
    [42/80, 10:03/14:32] update: pkuthss [385k] (28865 -> 29580) ... done
    [43/80, 10:11/14:41] update: pstricks [7204k] (29482 -> 29678) ... done
    [44/80, 10:21/14:00] update: regexpatch [532k] (27155 -> 29543) ... done
    [45/80, 10:23/13:59] update: roundbox [3k] (17896 -> 29675) ... done
    [46/80, 10:24/14:00] update: sansmathaccent [164k] (26200 -> 29541) ... done
    [47/80, 10:26/14:02] update: smartdiagram [276k] (29329 -> 29680) ... done
    [48/80, 10:28/14:02] update: splitindex.x86_64-linux [1k] (12613 -> 29688) ... done
    [49/80, 10:29/14:04] update: splitindex [456k] (29349 -> 29688) ... done
    [50/80, 10:31/14:03] update: tetex [379k] (29349 -> 29585) ... done
    [51/80, 10:35/14:06] update: texlive-docindex [196k] (29478 -> 29691) ... done
    [52/80, 10:37/14:07] update: texlive-scripts [69k] (29405 -> 29676) ... done
    [53/80, 10:38/14:08] update: tikzscale [541k] (29342 -> 29569) ... done
    [54/80, 10:41/14:08] update: tikzsymbols [550k] (29308 -> 29570) ... done
    [55/80, 10:44/14:08] update: toptesi [2439k] (29321 -> 29550) ... done
    [56/80, 10:50/13:59] update: tram [31k] (24395 -> 29701) ... done
    [57/80, 10:51/14:00] update: unamthesis [546k] (22500 -> 29519) ... done
    [58/80, 10:54/14:00] update: upmethodology [447k] (27896 -> 29615) ... done
    [59/80, 10:55/13:58] auto-install: biblatex-gost (29663) [871k] ... done
    [60/80, 10:57/13:55] auto-install: cjk-ko (29516) [2666k] ... done
    [61/80, 11:00/13:41] auto-install: download (29588) [175k] ... done
    [62/80, 11:00/13:40] auto-install: iitem (29613) [377k] ... done
    [63/80, 11:01/13:39] auto-install: matc3 (29698) [436k] ... done
    [64/80, 11:02/13:37] auto-install: matc3mem (29699) [392k] ... done
    [65/80, 11:03/13:36] auto-install: nanumtype1 (29558) [27664k] ... done
    [66/80, 11:21/11:29] auto-install: newpx (29576) [893k] ... done
    [67/80, 11:23/11:27] auto-install: readarray (29614) [185k] ... done
    [68/80, 11:23/11:26] auto-install: skdoc (29544) [207k] ... done
    [69/80, 11:24/11:27] auto-install: skmath (29607) [220k] ... done
    [70/80, 11:25/11:27] auto-install: skrapport (29608) [184k] ... done
    [71/80, 11:26/11:27] auto-install: xint (29649) [279k] ... done
    [72/80, 11:28/11:28] update: collection-bibtexextra [1k] (28717 -> 29517) ... done
    [73/80, 11:29/11:29] update: collection-fontsextra [2k] (29485 -> 29576) ... done
    [74/80, 11:30/11:30] update: collection-langarabic [1k] (29147 -> 29659) ... done
    [75/80, 11:31/11:31] update: collection-langcjk [1k] (29335 -> 29552) ... done
    [76/80, 11:31/11:31] update: collection-latexextra [5k] (29447 -> 29651) ... done
    [77/80, 11:32/11:32] update: collection-mathextra [1k] (28513 -> 29607) ... done
    [78/80, 11:33/11:33] update: collection-metapost [1k] (29358 -> 29655) ... done
    [79/80, 11:34/11:34] update: collection-pictures [1k] (29264 -> 29595) ... done
    [80/80, 11:34/11:34] update: collection-publishers [1k] (29466 -> 29687) ... done
    tlmgr: package log updated at /usr/local/texlive/2012/texmf-var/web2c/tlmgr.log
    running mktexlsr ...
    done running mktexlsr.
    running updmap-sys ...
    done running updmap-sys.
    regenerating fmtutil.cnf in /usr/local/texlive/2012/texmf-var
    running fmtutil-sys --no-error-if-no-format --byengine pdftex ...
    done running fmtutil-sys --no-error-if-no-format --byengine pdftex.

Suggestions for improvement are welcome.

Aikido Guy
