#!/usr/bin/env sh
#########
# ../tw2latex.py export anonymize:true page:latex tasks:{6cm}{6.5cm} tasksFilter:project:Home_status:pending_-thought_-question tasksColumns:short calendar:{0cm}{6.5cm} calendarNumWeeks:36 date timeline timelineFilter:project:Home_status.not:deleted_status.not:pending_-thought_-question timelineStartDate:20111201T010000Z > `date "+%Y%m%d%H%M%S.tex"`
#
# ../tw2latex.py export page:latex tasks tasksFilter:project:Home_status:pending tasksColumns:short calendar date > `date "+%Y%m%d%H%M%S.tex"`
#
# limit:20 seems to not be working. See: http://taskwarrior.org/issues/1213
#../tw2latex.py export anonymize:true page:latex tasks:{6cm}{1.5cm} tasksFilter:project:Home.Wood_status:pending_limit:20 tasksColumns:short tasksSummary:filter calendar:{0cm}{1.5cm} calendarNumWeeks:40 date > `date "+%Y%m%d%H%M%S.tex"`
#########

# create a unique filename stub
STUB=`date "+%Y%m%d%H%M%S"`

# Copy the style file to the current directory
cp ../taskwarrior.sty .

# create the latex report using the new filter (before export)
../tw2latex.py project:Home.Wood status:pending limit:20 export anonymize:true page:latex tasks:{6cm}{1.5cm} tasksColumns:short tasksSummary:filter calendar:{0cm}{1.5cm} calendarNumWeeks:40 date > "${STUB}.tex"

# create the pdf from the generated latex file
# latex "${STUB}.tex"      # create a *.dvi document
  pdflatex "${STUB}.tex"   # create a *.pdf document

# cleanup
  rm ./taskwarrior.sty
  rm "${STUB}.aux"
# rm "${STUB}.dvi"         # uncomment if needed
  rm "${STUB}.log"

