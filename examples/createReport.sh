#!/usr/bin/env sh

# ../tw2latex.py export anonymize:true page:latex tasks:{6cm}{6.5cm} tasksFilter:project:Home_status:pending_-thought_-question tasksColumns:short calendar:{0cm}{6.5cm} calendarNumWeeks:36 date timeline timelineFilter:project:Home_status.not:deleted_status.not:pending_-thought_-question timelineStartDate:20111201T010000Z > `date "+%Y%m%d%H%M%S.tex"`

../tw2latex.py export page:latex tasks tasksFilter:project:Home_status:pending tasksColumns:short calendar date > `date "+%Y%m%d%H%M%S.tex"`


