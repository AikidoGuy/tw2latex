#!/usr/bin/env sh

# ../tw2latex.py export anonymize:true page:latex tasks:{6cm}{6.5cm} tasksFilter:project:Home_status:pending_-thought_-question tasksColumns:short calendar:{0cm}{6.5cm} calendarNumWeeks:36 date timeline timelineFilter:project:Home_status.not:deleted_status.not:pending_-thought_-question timelineStartDate:20111201T010000Z > `date "+%Y%m%d%H%M%S.tex"`

# ../tw2latex.py export page:latex tasks tasksFilter:project:Home_status:pending tasksColumns:short calendar date > `date "+%Y%m%d%H%M%S.tex"`

# limit:20 seems to not be working. See: http://taskwarrior.org/issues/1213
../tw2latex.py export anonymize:true page:latex tasks:{6cm}{1.5cm} tasksFilter:project:Home.Wood_status:pending_limit:20 tasksColumns:short tasksSummary:filter calendar:{0cm}{1.5cm} calendarNumWeeks:40 date > `date "+%Y%m%d%H%M%S.tex"`
