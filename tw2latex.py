#!/usr/bin/env python
#    run python as determined from the environment.
#    For example, this could be under linux, macintosh or cygwin environments
#!/usr/bin/env win32python.sh
#    run a script that starts a Windows version of Python from cygwin
#
# For example, add the following to your path (in bash):
#    export PATH=/home/user/tw2latex:$PATH
# 
###

###############################################################################
# tw2latex - export to LaTeX from TaskWarrior
#
# Copyright 2012,2013 by Aikido Guy.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the
#
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor,
# Boston, MA
# 02110-1301
# USA
#
import json      # See http://json.org/
import os
import platform
import string
import sys
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import time
import pytz      # See http://pytz.sourceforge.net/
                 # Tested with: pytz-2012c-py2.7.egg
###############################################################################
# default configuration (you should change these to suit your needs)
TASK_PROG      = "task"           # command to run TaskWarrior
LOCAL_TIMEZONE = 'Canada/Eastern' # your location in the world
if(LOCAL_TIMEZONE not in pytz.all_timezones):
   raise RuntimeError("Did NOT find timezone '" + LOCAL_TIMEZONE + "'")
theLocalTimeZone = pytz.timezone(LOCAL_TIMEZONE)
#
UTC_FORMAT                = "%Y%m%dT%H%M%SZ"  # Zulu time zone used by TaskWarrior
PRINT_COMMANDLINE_OPTIONS = True
PRINT_DATE_TIME_FORMAT    = "%Y/%m/%d %H:%M"
###
def getNowInUTCandLocalTime():
   nowInUTC = datetime.datetime.utcnow()
   # make the naive datetime into a UTC aware datetime
   nowInUTC = pytz.utc.localize(nowInUTC)
   # convert to local time zone
   nowInLocalTimeZone = nowInUTC.astimezone(theLocalTimeZone)
   return (nowInUTC, nowInLocalTimeZone)

def getNowStringInLocalTime():
   now = getNowInUTCandLocalTime()
   return now[1].strftime(PRINT_DATE_TIME_FORMAT)

def getNowStringInUTCTime():
   now = getNowInUTCandLocalTime()
   return now[0].strftime(UTC_FORMAT)

###
DEFAULT_ANONYMIZE                 = "false"
DEFAULT_TASKS_PAGE                = "{6cm}{1.5cm}"
DEFAULT_TASKS_COLUMNS             = "long"
DEFAULT_TASKS_SUMMARY             = "count"
DEFAULT_TASKS_BOOKLET             = "{?cm}{?cm}"
DEFAULT_TASKS_WIDTH_PAGE          = "{\\paperwidth-9cm}" # "{\\paperwidth-5mm-1cm}"
DEFAULT_TASKS_WIDTH_BOOKLET       = "{?cm}"
DEFAULT_CALENDAR_PAGE             = "{0cm}{1.5cm}"
DEFAULT_CALENDAR_BOOKLET          = "{?cm}{?cm}"
DEFAULT_CALENDAR_NUMWEEKS_PAGE    = "48"
DEFAULT_CALENDAR_NUMWEEKS_BOOKLET = "35"
DEFAULT_CALENDAR_MONTH            = "weekWithFirst"
DEFAULT_DATE_PAGE                 = "{16cm}{1.0cm}"
DEFAULT_TIMELINE_PAGE             = "{0cm}{0.5cm}"
DEFAULT_TIMELINE_ZERODATE         = datetime.datetime.utcnow().strftime("%Y") + "0101T000000Z"
DEFAULT_TIMELINE_ENDDATE          = getNowStringInUTCTime()
TAGS_SEPARATOR                    = ","
###

def testPrintNowInUTCandLocalTime():
   now = getNowInUTCandLocalTime()
   print "Testing to see results of 'now'"
   print "   " + now[0].strftime(PRINT_DATE_TIME_FORMAT) + " is 'now' in UTC"
   print "   " + now[1].strftime(PRINT_DATE_TIME_FORMAT) + " is 'now' in local time zone (" + LOCAL_TIMEZONE + ")"
   print "   done."
   return

def createUTCawareDateTimeFromUTCstring(utcTimeAsString):
   # create naive datetime from string
   parsedUTC = datetime.datetime.strptime(utcTimeAsString, UTC_FORMAT)
   # make the naive datetime into a UTC aware datetime
   parsedUTC = pytz.utc.localize(parsedUTC)
   return parsedUTC

def createLocalTimeStringFromUTCawareDateTime(parsedUTC):
   # convert UTC time into local time zone
   parsedUTC = parsedUTC.astimezone(theLocalTimeZone)
   # convert to string format
   localTimeAsString = parsedUTC.strftime(PRINT_DATE_TIME_FORMAT)
   return localTimeAsString

def convertUTCTimeStringToLocalTimeString(utcTimeAsString):
   parsedUTC = createUTCawareDateTimeFromUTCstring(utcTimeAsString)
   return createLocalTimeStringFromUTCawareDateTime(parsedUTC)

# See http://stackoverflow.com/questions/396913/in-python-how-do-i-find-the-date-of-the-first-monday-of-a-given-week
def getDateForISOWeekStartDate(year, week):
   d = date(year, 1, 1)    
   delta_days = d.isoweekday() - 1
   delta_weeks = week
   if year == d.isocalendar()[0]:
      delta_weeks -= 1
   delta = timedelta(days=-delta_days, weeks=delta_weeks)
   return d + delta

def runTaskWarriorCommand(cmd):
   cmd = TASK_PROG + " rc.verbose=nothing " + cmd
   # Debugging
   sys.stderr.write("running: '" + cmd + "'\n")
   ###
   os.system(cmd)

def runTaskWarriorCommandAndCollectJSON(cmd):
   cmd = TASK_PROG + " rc.verbose=nothing rc.json.array=yes " + cmd
   # Debugging
   sys.stderr.write("running: '" + cmd + "'\n")
   ###
   fin,fout = os.popen4(cmd)
   result   = fout.read()
   if( (result==None) or (result=="") ):
      raise RuntimeError("No matching tasks for: " + cmd)
   jsonObj = json.loads(result)
   return jsonObj

class CmdLineOptions(object):
   def printUsage(self, argv):
      sys.stderr.write("tw2latex - export to LaTeX from TaskWarrior\n")
      sys.stderr.write("\n")
      sys.stderr.write("Usage:\n")
      sys.stderr.write("\n")
      sys.stderr.write("tw2latex export [options]\n")
      sys.stderr.write("  -collect the tasks from TaskWarrior\n")
      sys.stderr.write("  [options] may be:\n")
      sys.stderr.write("     anonymize:X         # X=true or X=false\n")
      sys.stderr.write("                         # default is anonymize:" + DEFAULT_ANONYMIZE + "\n")
      sys.stderr.write("     page:X              # X=latex\n")
      sys.stderr.write("                         # X=text  (not supported yet)\n")
      sys.stderr.write("     booklet:X           # X=latex (not supported yet)\n")
      sys.stderr.write("                         # X=text  (not supported yet)\n")
      sys.stderr.write("     tasks:{Xcm}{Ycm}    # create a list of tasks at location X,Y\n")
      sys.stderr.write("                         # default is page:X    tasks:" + DEFAULT_TASKS_PAGE + "\n")
      sys.stderr.write("                         #            booklet:X tasks:" + DEFAULT_TASKS_BOOKLET + "\n")
      sys.stderr.write("     tasksFilter:X       # filter for tasks creation\n")
      sys.stderr.write("     tasksWidth:{Xcm}    # width to use for tasks\n")
      sys.stderr.write("                         # default is page:X    tasksWidth:" + DEFAULT_TASKS_WIDTH_PAGE + "\n")
      sys.stderr.write("                         # default is booklet:X tasksWidth:" + DEFAULT_TASKS_WIDTH_BOOKLET + "\n")
      sys.stderr.write("     tasksColumns:X      # X=short|X=long\n")
      sys.stderr.write("                         # default is tasksColumns:" + DEFAULT_TASKS_COLUMNS + "\n")
      sys.stderr.write("     tasksSummary:X      # will include a summary at the bottom of task list\n")
      sys.stderr.write("                         # X may be 'none', 'filter' or 'count'\n")
      sys.stderr.write("                         # default is tasksSummary:" + DEFAULT_TASKS_SUMMARY + "\n")
      sys.stderr.write("     calendar:{Xcm}{Ycm} # create a calendar at location X,Y\n")
      sys.stderr.write("                         # default is page:X    calendar:" + DEFAULT_CALENDAR_PAGE + "\n")
      sys.stderr.write("                         #            booklet:X calendar:" + DEFAULT_CALENDAR_BOOKLET + "\n")
      sys.stderr.write("     calendarNumWeeks:X  # use X weeks in the calendar\n")
      sys.stderr.write("                         # default is page:X     calendarNumWeeks:" + DEFAULT_CALENDAR_NUMWEEKS_PAGE + "\n")
      sys.stderr.write("                         #            booklet:X  calendarNumWeeks:" + DEFAULT_CALENDAR_NUMWEEKS_BOOKLET + "\n")
      sys.stderr.write("     calendarMonth:X     # X=everyWeek     (print month name for each week)\n")
      sys.stderr.write("                         # X=weekWithFirst (print month name if week has 1st in it)\n")
      sys.stderr.write("                         # default is calendarMonth:" + DEFAULT_CALENDAR_MONTH + "\n")
      sys.stderr.write("     date:{Xcm}{Ycm}     # create a date at location X,Y\n")
      sys.stderr.write("                         # default is page:X    tasks:" + DEFAULT_DATE_PAGE + "\n")
      sys.stderr.write("     timeline:{Xcm}{Ycm} # create a timeline at location X,Y\n")
      sys.stderr.write("                         # default is timeline:" + DEFAULT_TIMELINE_PAGE + "\n")
      sys.stderr.write("     timelineFilter:X    # filter for timeline creation\n")
      sys.stderr.write("     timelineZeroDate:X  # 0 on timeline has this date\n")
      sys.stderr.write("                         # default is timelineZeroDate:" + DEFAULT_TIMELINE_ZERODATE + "\n")
      sys.stderr.write("     timelineStartDate:X # smallest value on timeline has this date\n")
      sys.stderr.write("                         # default is timelineStartDate:" + DEFAULT_TIMELINE_ZERODATE + "\n")
      sys.stderr.write("     timelineEndDate:X   # largest value on timeline has this date\n")
      sys.stderr.write("                         # default is timelineEndDate:" + DEFAULT_TIMELINE_ENDDATE + "\n")
      sys.stderr.write("\n")
      raise RuntimeError("") # break out of the program
   def __init__(self, argv):
      self.startTime = getNowInUTCandLocalTime()
      self.cmd         = ""
      self.cmdIdx      = -1
      self.options     = {}
      #for arg in argv:
      #   sys.stderr.write("arg " + arg + "\n")
      if 'export' in argv:
         self.cmd    = "export"
         self.cmdIdx = argv.index(self.cmd)
         # get the filter for the command
         #self.taskfilter = string.join(argv[0:self.cmdIdx])
         ## print len(argv)-1 
         ## print self.cmdIdx+2
         ## print "blah"
         if(len(argv)-1 >= self.cmdIdx+1):
            # get the rest of the options
            #print argv[self.cmdIdx+1:len(argv)] # end index is not included
            for option in argv[self.cmdIdx+1:len(argv)]:
               idx = option.find(":")
               if(idx<0): # not found
                  # 'option' was given on the command line
                  if(option in self.options):
                     raise RuntimeError("'" + option + "' is specified more than once")
                  self.options[option] = ""
               else: # found
                  if(idx<len(option)-1):
                     # 'option:value' was given on the command line
                     #print option[0:idx] + "=" + option[idx+1:len(option)]
                     if(option[0:idx] in self.options):
                        raise RuntimeError("'" + option[0:idx] + "' is specified more than once")
                     self.options[option[0:idx]] = option[idx+1:len(option)]
                  else:
                     # 'option:' was given on the command line
                     if(option[0:idx] in self.options):
                        raise RuntimeError("'" + option[0:idx] + "' is specified more than once")
                     self.options[option[0:idx]] = ""
         if(PRINT_COMMANDLINE_OPTIONS==True):
            sys.stderr.write("Options explicit on command line:\n")
            for key, val in sorted(self.options.items()):
               sys.stderr.write("   " + key + ":" + val + "\n")

      # if no cmd, then some kind of error
      if(self.cmd == ""):
         self.printUsage(argv)

def printTextPage(opts,jsonObjForTasks):
   for task in jsonObjForTasks:
      if("due" in task):
         due = convertUTCTimeStringToLocalTimeString(task["due"])
      else:
         due = "xxxx/xx/xx xx:xx"
      fulldesc = task["description"]
      sys.stdout.write(due + " " + fulldesc + "\n")
   return

def weekHasTheFirstInIt(dt):
   for ii in range(7):
      if(dt.day==1):
         return True
      dt = dt + relativedelta(days = +1)
   return False

def writeLatexStringInParModeToStdOut(stringToWrite,opts):
   if("anonymize" not in opts.options):
      opts.options["anonymize"]=DEFAULT_ANONYMIZE

   for ii in range(len(stringToWrite)): # +1 because range doesn't include the end value
      if(opts.options["anonymize"]=="false"):
         if(stringToWrite[ii]=='%'):  # LaTeX needs to have percents escaped
            sys.stdout.write('\\')
         if(stringToWrite[ii]=='_'):  # LaTeX needs to have underscores escaped unless in math mode (which we're not)
            sys.stdout.write('\\')
         sys.stdout.write(stringToWrite[ii])
      if(opts.options["anonymize"]=="true"):
         if(stringToWrite[ii]==" "): # keep spaces so that correct wrapping will still occur
            sys.stdout.write(" ")
         else:
            sys.stdout.write("x")
   return

def printLatexTasks(opts,jsonObjForTasks):
   if(opts.options["tasks"]==""): # use a default location
      opts.options["tasks"]=DEFAULT_TASKS_PAGE
   if("tasksColumns" not in opts.options):
      opts.options["tasksColumns"]=DEFAULT_TASKS_COLUMNS
   if("tasksSummary" not in opts.options):
      opts.options["tasksSummary"]=DEFAULT_TASKS_SUMMARY

   print ""
   print "\\TWstandardPageBox" + opts.options["tasks"] + opts.options["tasksWidth"] + "{white}{%"
   print "\\setlength{\\tabcolsep}{0.5mm}    % specify a more compact table column separator"
   print "\\noindent\\resizebox" + opts.options["tasksWidth"] + "{!}{%"
   if(opts.options["tasksColumns"]=="long"):
      print "\\begin{tabularx}" + opts.options["tasksWidth"] + "{cccccX}"
      print "\\TWhighlightMedium{1}{c}{A}  & \\TWhighlightMedium{1}{c}{ID}  & \\TWhighlightMedium{1}{c}{Tags} & \\TWhighlightMedium{1}{c}{Due}  & \\TWhighlightMedium{1}{c}{Project} & \\TWhighlightMedium{1}{c}{Description} \\tabularnewline"
   if(opts.options["tasksColumns"]=="short"):
      print "\\begin{tabularx}" + opts.options["tasksWidth"] + "{ccX}"
      print "\\TWhighlightMedium{1}{c}{ID}  & \\TWhighlightMedium{1}{c}{Due}  & \\TWhighlightMedium{1}{c}{Description} \\tabularnewline"

   #print "\\multicolumn{7}{c}{\\TWdarkText{next 10} \\hfill \\TWdarkText{Project foo, tags:bar} \\hfill \\TWdarkText{42 of 174}} \\tabularnewline"
   #print "\\multicolumn{7}{l}{\\TWdarkText{" + opts.taskfilter + "}} \\tabularnewline"
   #print "\\TWhighlightMedium{1}{c}{A}  & \\TWhighlightMedium{1}{c}{ID}  & \\TWhighlightMedium{1}{c}{Tags} & \\TWhighlightMedium{1}{c}{Due}  & \\TWhighlightMedium{1}{c}{Countdown} & \\TWhighlightMedium{1}{c}{Project} & \\TWhighlightMedium{1}{c}{Description} \\tabularnewline"

   for task in jsonObjForTasks:
      # A
      if(opts.options["tasksColumns"]=="long"):
         if("start" in task):
            sys.stdout.write("\\TWmediumText{*}")
         sys.stdout.write(" & ")

      # ID
      sys.stdout.write("\\TWmediumText{" + str(task["id"]) + "}")

      # Tags
      if(opts.options["tasksColumns"]=="long"):
         sys.stdout.write(" & ")
         sys.stdout.write("\\TWmediumText{" + string.join(task["tags"],TAGS_SEPARATOR) + "}")

      # Due
      sys.stdout.write(" & ")
      if("due" in task):
         due = convertUTCTimeStringToLocalTimeString(task["due"])
         sys.stdout.write("\\TWmediumText{" + due + "}")

      # Project
      if(opts.options["tasksColumns"]=="long"):
         sys.stdout.write(" & ")
         sys.stdout.write("\\TWmediumText{")
         writeLatexStringInParModeToStdOut(task["project"],opts)
         sys.stdout.write("}")

      # Description
      sys.stdout.write(" & ")
      sys.stdout.write("\\TWmediumText{")
      writeLatexStringInParModeToStdOut(task["description"],opts)
      sys.stdout.write("}")

      # How deal with annotations?
      sys.stdout.write(" \\tabularnewline \n")

   #print "\\TWhighlightMedium{7}{c}{since 20/09/11 - 17 done - 7 deleted - 4 waiting - 42 pending} \\tabularnewline"
   #print "\\TWhighlightMedium{7}{c}{" + opts.taskfilter + "} \\tabularnewline"

   # Print the footer with or without the filter
   if(opts.options["tasksColumns"]=="long"):
      print "\\TWhighlightMedium{6}{c}{" 
   if(opts.options["tasksColumns"]=="short"):
      print "\\TWhighlightMedium{3}{c}{"
   #if(opts.options["tasksSummary"]=="none"):
   #  do nothing
   if(opts.options["tasksSummary"]=="filter"):
      #print opts.taskfilter 2013/03/24: old way using items before "export"
      # print opts.options["tasksFilter"]
      before = opts.options["anonymize"]
      opts.options["anonymize"] = "false"
      writeLatexStringInParModeToStdOut(opts.options["tasksFilter"],opts)
      opts.options["anonymize"] = before
   if(opts.options["tasksSummary"]=="count"):
      print str(len(jsonObjForTasks)) + " tasks"
   print "} \\tabularnewline"

   print "\\end{tabularx}%"
   print "}%resizebox"
   print "}% end box location and/or rotation"
   return

def printLatexCalendar(opts):
   if(opts.options["calendar"]==""): # use a default location
      opts.options["calendar"]=DEFAULT_CALENDAR_PAGE

   print "\\TWstandardPageBox" + opts.options["calendar"] + "{5cm}{white}{%"

   # See http://stackoverflow.com/questions/2600775/how-to-get-week-number-in-python
   # See http://stackoverflow.com/questions/546321/python-date-time-get-date-6-months-from-now
   # See http://www.staff.science.uu.nl/~gent0113/calendar/isocalendar.htm
   beginDate = opts.startTime[1] # local time
   # year    = dt.isocalendar()[0]
   # weekNum = dt.isocalendar()[1]
   # weekDay = dt.isocalendar()[2]
   
   print "\\setlength{\\tabcolsep}{0.5mm}    % specify a more compact table column separator"
   print "\\noindent\\begin{tabular}{lrccccccc}"
   print "\\TWhighlightMedium{1}{c}{} & \\TWhighlightMedium{1}{c}{\\#} & \\TWhighlightMedium{1}{c}{M} & \\TWhighlightMedium{1}{c}{T} & \\TWhighlightMedium{1}{c}{W} & \\TWhighlightMedium{1}{c}{T} & \\TWhighlightMedium{1}{c}{F} & \\TWhighlightLight{1}{c}{S} & \\TWhighlightLight{1}{c}{S} \\\\"
   print "%"

   for ii in range(int(opts.options["calendarNumWeeks"])+1): # +1 because range doesn't include the end value
      dt = beginDate + relativedelta(weeks = +ii)
      dt = getDateForISOWeekStartDate(dt.year, dt.isocalendar()[1])

      # month
      thisMonthStr = dt.strftime("%B")[0:3]   # first 3 chars of month name
      nextMonthStr = (dt+relativedelta(weeks=+1)).strftime("%B")[0:3]
      yearStr  = "'" + dt.strftime("%Y")[2:5] # quote plus last 2 chars of year
      if(ii==0):
         sys.stdout.write("\\TWdarkText{" + thisMonthStr + "} ")    # first line begins with month
      elif ii==1:
         sys.stdout.write("\\TWdarkText{" + yearStr + "} ")         # second line begins with year
      else:
         if(opts.options["calendarMonth"]=="everyWeek"):
            sys.stdout.write("\\TWdarkText{" + thisMonthStr + "} ")
         elif opts.options["calendarMonth"]=="weekWithFirst":
            if(weekHasTheFirstInIt(dt)==True):
               sys.stdout.write("\\TWdarkText{" + nextMonthStr + "} ")
            elif thisMonthStr=="Jan" and weekHasTheFirstInIt(dt+relativedelta(weeks=-1))==True:
               sys.stdout.write("\\TWdarkText{" + yearStr + "} ")
         else:
            raise RuntimeError("'calendarMonth:" + opts.options["calendarMonth"] + "' is not currently supported")

      # week number
      sys.stdout.write(" & \\TWlightText{" + str(dt.isocalendar()[1]) + "}")
      # dates of the Monday to Sunday in the week
      firstOfMonthInThisWeek = -1
      for ii in range(7):
         # sys.stderr.write("this week " + str(dt.day) + " " + str(ii) + "\n")
         if(dt.day==1):
            sys.stdout.write(" & \\TWhighlightDark{1}{c}{" + str(dt.day) + "}")
         else:
            if(ii>=5): # a weekend
               sys.stdout.write(" & \\TWlightText{" + str(dt.day) + "}")
            else:      # a weekday
               sys.stdout.write(" & \\TWdarkText{" + str(dt.day) + "}")

         if(dt.day==1):
            firstOfMonthInThisWeek = ii
         dt = dt + relativedelta(days = +1)
      sys.stdout.write("\\\\")
      if(firstOfMonthInThisWeek>0):
         sys.stdout.write(" \\cline{3-" + str(3+firstOfMonthInThisWeek-1) + "}")

      # check next week
      firstOfMonthInNextWeek = -1
      for ii in range(7):
         # sys.stderr.write("   next " + str(dt.day) + " " + str(ii) + "\n")
         if(dt.day==1):
            firstOfMonthInNextWeek = ii
         dt = dt + relativedelta(days = +1)
      if(firstOfMonthInNextWeek>=0 and firstOfMonthInNextWeek<6):
         sys.stdout.write(" \\cline{" + str(3+firstOfMonthInNextWeek+1) + "-9}")
      sys.stdout.write("\n")

   print "\\TWhighlightMedium{9}{c}{" + opts.options["calendarNumWeeks"] + " weeks} \\\\"

   print "\\end{tabular}%"
   print "} % end box location and/or rotation"
   return

def printLatexDate(opts):
   if(opts.options["date"]==""): # use a default location
      opts.options["date"]=DEFAULT_DATE_PAGE

   print ""
   print "\\TWstandardPageBox" + opts.options["date"] + "{2cm}{white}{%"
   print "\TWmediumText{" + getNowStringInLocalTime() + "}"
   print "} % end box location and/or rotation"
   return

def numWeeksDateIsFromBaseDate(dateToDetermine, dateForZeroOnScale):
   td = dateToDetermine - dateForZeroOnScale # produce a timedelta
   #sys.stderr.write("   td    = " + str(td) + "\n")
   #sys.stderr.write("   days  = " + str(td.days) + "\n")
   #sys.stderr.write("   weeks = " + str(td.days / 7.0) + "\n")
   #sys.stderr.write("   weeks = " + ("%.1f"%(td.days / 7.0)) + "\n")
   return  td.days/7.0

def formatWeeksForEvent(weeks):
   return "%.1f" % weeks

def formatWeeksForHeader(weeks):
   return "%.0f" % weeks

# TODO: change TaskWarrior UDA from "timeline" to
# 1) "timeline"                        - which is a single point in time event
# 2) "timelinestart" and "timelineend" - which is an event that happens during an interval
# only (1) or (2) may exist for a task, it is an error to have both
# I think 'duration' is treated by TaskWarrior as a length of time, for example, 2h
#
# I use timeline for major things that have finished and are in the past.
# I use tasks to list things that are detailed and need to be done in the future.
def printLatexTimeline(opts,jsonObjForTimeline):
   if(opts.options["timeline"]==""): # use a default location
      opts.options["timeline"]=DEFAULT_TIMELINE_PAGE
   if("timelineZeroDate" not in opts.options):
      opts.options["timelineZeroDate"]=DEFAULT_TIMELINE_ZERODATE
   if("timelineStartDate" not in opts.options):
      opts.options["timelineStartDate"]=DEFAULT_TIMELINE_ZERODATE
   if("timelineEndDate" not in opts.options):
      opts.options["timelineEndDate"]=DEFAULT_TIMELINE_ENDDATE

   timelineZeroDate = createUTCawareDateTimeFromUTCstring(opts.options["timelineZeroDate"])
   print ""
   print "\\TWstandardPageBox" + opts.options["timeline"] + "{19cm}{white}{%"
   print "% Zero date in UTC format is  : " + opts.options["timelineZeroDate"]
   print "%    and in local time zone is: " + createLocalTimeStringFromUTCawareDateTime(timelineZeroDate)
   sys.stdout.write("\\noindent\\begin{chronology}[4]{")
   startDate = createUTCawareDateTimeFromUTCstring(opts.options["timelineStartDate"])
   numWeeks  = numWeeksDateIsFromBaseDate(startDate, timelineZeroDate)
   sys.stdout.write(formatWeeksForHeader(numWeeks))
   sys.stdout.write("}{")
   endDate   = createUTCawareDateTimeFromUTCstring(opts.options["timelineEndDate"])
   numWeeks  = numWeeksDateIsFromBaseDate(endDate, timelineZeroDate)
   sys.stdout.write(formatWeeksForHeader(numWeeks))
   sys.stdout.write("}{3ex}{19cm}\n")
   for task in jsonObjForTimeline:
      if("timeline" in task):
         # print "\\event[-8]{-2}{Coursework complete}"
         dateToPlace = createUTCawareDateTimeFromUTCstring(task["timeline"])
         if(dateToPlace < startDate):
            sys.stderr.write("task  date: " + createLocalTimeStringFromUTCawareDateTime(dateToPlace) + "\n")
            sys.stderr.write("start date: " + createLocalTimeStringFromUTCawareDateTime(startDate) + "\n")
            raise RuntimeError("a task matching the timeline filter has a date before the timeline start date")
         if(dateToPlace > endDate):
            sys.stderr.write("task date: " + createLocalTimeStringFromUTCawareDateTime(dateToPlace) + "\n")
            sys.stderr.write("end  date: " + createLocalTimeStringFromUTCawareDateTime(endDate) + "\n")
            raise RuntimeError("a task matching the timeline filter has a date after the timeline end date")
         numWeeks    = numWeeksDateIsFromBaseDate(dateToPlace, timelineZeroDate)
         sys.stdout.write("\\event{" + formatWeeksForEvent(numWeeks) + "}{")
         writeLatexStringInParModeToStdOut(task["description"],opts)
         sys.stdout.write("}\n")
   print "\\end{chronology}\n"
   print "} % end box location and/or rotation"
   return

def printLaTeXPage(opts,jsonObjForTasks,jsonObjForTimeline):
   print "\\documentclass[12pt]{article}"
   print "\\usepackage{taskwarrior}"
   if("timeline" in opts.options):
      print "\\usepackage{chronology}"
   print ""
   print "\\begin{document}"

   if("tasks" in opts.options):
      printLatexTasks(opts,jsonObjForTasks)
   if("calendar" in opts.options):
      printLatexCalendar(opts)
   if("date" in opts.options):
      printLatexDate(opts)
   if("timeline" in opts.options):
      printLatexTimeline(opts,jsonObjForTimeline)

   print "\\end{document}"
   return

def replaceFilterChar(filterStr):
   # replace _ with space. This is a way around spaces not working
   return filterStr.replace('_', ' ')

def main(argv):
   try:
      #testPrintNowInUTCandLocalTime()
      opts = CmdLineOptions(argv)
      jsonObjForTasks    = []
      jsonObjForTimeline = []
      if("tasksFilter" in opts.options):
         jsonObjForTasks = runTaskWarriorCommandAndCollectJSON(replaceFilterChar(opts.options["tasksFilter"]) + " export")
      if("timelineFilter" in opts.options):
         jsonObjForTimeline = runTaskWarriorCommandAndCollectJSON(replaceFilterChar(opts.options["timelineFilter"]) + " export")
      else:
         jsonObjForTimeline = runTaskWarriorCommandAndCollectJSON(" export")
      if(opts.cmd=="export"):
         # set up global defaults
         if("calendarMonth" not in opts.options):
            opts.options["calendarMonth"]=DEFAULT_CALENDAR_MONTH
         # process options
         if("page" in opts.options):
            # set up page defaults
            if("tasksWidth" not in opts.options):
               opts.options["tasksWidth"]=DEFAULT_TASKS_WIDTH_PAGE
            if("calendarNumWeeks" not in opts.options):
               opts.options["calendarNumWeeks"]=DEFAULT_CALENDAR_NUMWEEKS_PAGE
            if(opts.options["page"]=="text"):
               printTextPage(opts,jsonObjForTasks)
            if(opts.options["page"]=="latex"):
               printLaTeXPage(opts,jsonObjForTasks,jsonObjForTimeline)
         elif("booklet" in opts.options):
            # set up booklet defaults
            if("tasksWidth" not in opts.options):
               opts.options["tasksWidth"]=DEFAULT_TASKS_WIDTH_BOOKLET
            if("calendarNumWeeks" not in opts.options):
               opts.options["calendarNumWeeks"]=DEFAULT_CALENDAR_NUMWEEKS_BOOKLET
            raise RuntimeError("'booklet' is not currently supported")
         else:
            raise RuntimeError("'page' or 'booklet' needs to be specified")
      sys.stdout.flush()
      if(PRINT_COMMANDLINE_OPTIONS==True):
         sys.stderr.write("Options at end of program after default values have been determined:\n")
         for key, val in sorted(opts.options.items()):
            sys.stderr.write("   " + key + ":" + val + "\n")
   except RuntimeError as e:
      sys.stderr.write(str(e) + "\n")
      sys.stderr.flush()

main(sys.argv[1:])
 
