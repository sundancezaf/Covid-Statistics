#COVID-19 Project
'''
This project was modified from the original to now include other functions.

This project includes data from the NYTimes Github.
This file includes NEW cases and NEW deaths for each state, for each day that an event occurs.
We will want to develop python programs to help us analyze this information.
For this project, we will be working with data in two separate files.  The first file is named us-states.csv,
and contains the number of CUMULATIVE COVID-19 cases and deaths for each day, starting from 1/21/20.  So, the number
of events should be increasing with time.  The data is sorted by date.

You will need to reformat the date to match Python date. Notice that each field is separated by a comma, so when you
read each line in the file, you will want to separate the contents of the file by a comma, and also remove
the "new line" character.

Not allowed to use established functions that help with list comprehension, sorting, reversal, slicing, readlines,
or any other functions that do not explicitly appear in the handouts or in sample code. Functions that you are allowed
to use are: split(), strip(), date(), open(), close(), max(), min().
'''


from datetime import date, timedelta

# Changes dates format from MM/DD/YY or MM/DD/YYYY to YYYY-MM-DD Python format.
def paranthesisDate(dateString):
    # Split at the "/"
    x = dateString.split("/")
    # First split value is the month, then day, then year
    month = x[0]
    day = x[1]
    year = x[2]
    # The requirement asks to solve for a date in the MM/DD/YY format but if it is given
    # a date in MM/DD/YYYY format this will accept it and
    if len(year) == 2:
        year = "20" + str(year)
    else:
        year = year
    # Need ints to convert to Python date
    month = int(month)
    day = int(day)
    year = int(year)
    # Final Conversion
    finalDate = date(year, month, day)
    return finalDate


# Just need to convert it to Python date
def hyphensDate(aDate):
    # Split at the "/"
    x = aDate.split("-")
    # First split value is the month, then day, then year
    month = x[1]
    day = x[2]
    year = x[0]
    # Need ints to convert to Python date
    month = int(month)
    day = int(day)
    year = int(year)
    # Final Conversion
    finalDate = date(year, month, day)
    return finalDate



# Recognize if date is in MM/DD/YY or YYYY-MM-DD and format accordingly
def recognizeDate(mDate):
    hyphens = []
    parantheses = []
    for item in str(mDate):
        if item == "-":
            hyphens.append(item)
        elif item == "/":
            parantheses.append(item)
    if len(hyphens) > 1:
        correctedDate = hyphensDate(mDate)
    else:
        correctedDate = paranthesisDate(mDate)
    return correctedDate


# Get last date in the csv file
def lastDateinCSV():
    f = open("us-states.csv","r")
    lastDateList = []
    for line in f:
        splitValue = line.split(",")
        date = splitValue[0]
        stateFinal = splitValue[1]
        fips = splitValue[2]
        cases = splitValue[3]
        deaths = splitValue[4]
        deaths = deaths.strip("\n")
    f.close()
    return date


# Previous date from last date in CSV file

def previousDate():
    lastDate = recognizeDate(lastDateinCSV())
    dateBefore = lastDate - timedelta(days=1)
    return dateBefore

print(previousDate())




#####################                 isInRange               #########################
#write a function that takes, as an argument, three strings representing dates
#a start date, an end date, and a query date, all three of which are in the format
#MM/DD/YY and returns a Boolean True if the query date is BETWEEN the start and end dates,
#and False if not.

def isInRange(startDate, endDate, queryDate):
    # split the values by "/" this returns a string which will be converted to ints
    splitValue = startDate.split("/")
    startMonth = int(splitValue[0])
    startDay = int(splitValue[1])
    startYear="20"+ splitValue[2]
    startYear = int(startYear)
    # we get the ints for the year, month, and day and convert it to Python Date
    finalStart = date(startYear,startMonth,startDay)

    # Repeat the process for the endDate and queryDate

    endSplitValue = endDate.split("/")
    endMonth = int(endSplitValue[0])
    endDay = int(endSplitValue[1])
    endYear = "20" + endSplitValue[2]
    endYear = int(endYear)
    finalEnd = date(endYear,endMonth,endDay)

    querySplitValue = queryDate.split("/")
    queryMonth = int(querySplitValue[0])
    queryDay = int(querySplitValue[1])
    queryDay = int(queryDay)
    queryYear = "20"+ querySplitValue[2]
    queryYear = int(queryYear)
    finalQuery = date(queryYear,queryMonth,queryDay)

    # This checks that the queryDate is in between the start and end date. Returns a boolean.
    inBetween = finalEnd > finalQuery > finalStart
    return inBetween

######################             getFirstEvent             ########################
# write a function that takes, as arguments, a file name, a state, and an event which is either 'cases' or 'deaths'.
# If the event is 'cases', return the STRING date of the first case, and if the event is 'deaths', return the STRING
# date of the first death.  If no event has occurred, return the STRING 'None'.
# Function name: getFirstEvent(fileName, state, event).

def getFirstEvent(fileName,state,event):
    f = open(fileName,"r")
    i = 0
    masterList = []
    for line in f:
        splitValue = line.split(",")
        date = splitValue[0]
        stateFinal = splitValue[1]
        fips = splitValue[2]
        cases = splitValue[3]
        deaths = splitValue[4]
        deaths = deaths.strip("\n")

        if stateFinal == state:
            if event == "cases":
                if cases >= "1":
                    masterList.append(date)
                    masterList.append(cases)
                    result = masterList[0]
                else:
                    result = "None"

            elif event == "deaths":
                if deaths >= "1":
                    masterList.append(date)
                    masterList.append(deaths)
                    result = masterList[0]
                else:
                    result = "None"

    f.close()
    return str(result)


####################                 caseToDeath                     ####################
# write a function that takes, as arguments, a file name and a state, and returns the number of days between the
# first case for the state and the first death reported.  If either no case or no death has been reported return the
# string 'None'.  Name this function caseToDeath(filename, state).
# Use helper functions getDateFromString(dateString) and getFirstEvent(fileName, state, event)
# as part of this function.

def caseToDeath(fileName, state):
    # Need to get the dates for first case and first death reported
    firstCase = getFirstEvent(fileName, state, "cases")
    firstDeath = getFirstEvent(fileName, state, "deaths")

    if firstCase == "None" or firstDeath == "None":
        result = "None"
    else:
        # convert the date to Python date
        finalCaseDate = recognizeDate(str(firstCase))
        finalDeathDate = recognizeDate(str(firstDeath))
        # returns the difference between first case and first death reported in Delta time
        deltaTimeDifference = finalCaseDate - finalDeathDate
        # need to convert delta time into just an int or return "None" if no case or death reported
        newList = []
        finalString = ''
        # Need to copy Delta time into a string that we can iterate over and change
        convertFromDelta = str(deltaTimeDifference)
        # Splitting at the comma
        finalConvert = convertFromDelta.split(",")

        # As we have split at the comma, we only need the first item in that list
        result = finalConvert[0]

        # We need to iterate between the items to extract the number we need
        for item in result:
            isDigit = item.isdigit()
            if isDigit:
                newList.append(item)
        for num in newList:
            finalString = finalString + str(num)
        finalNumber = int(finalString)
        finalDate = finalNumber
    return finalDate



####################                maxDaysCaseDeath               #############
# Write a function that takes, as arguments, the name of the file containing case/death data and the name of a file
# containing population data, and returns the state whose time between the first case and
# the first death is a MAXIMUM value. For example, if the state were Washington and the number of days was 55,
# your function should return the string 'Washington: 55 days'.

def maxDaysCaseDeath(caseFile, populationFile):
    f = open(populationFile,"r")
    maximumValue = 0

    for line in f:
        # Split the values by ","
        nameSplit = line.split(",")
        # First value is the state name
        state = nameSplit[0]
        # Days between the first case and the first death
        daysBetweenCaseDeath = caseToDeath(caseFile,state)

        typo = type(daysBetweenCaseDeath)
        # Have to make sure the result is integer otherwise it won't compare
        if typo == int:
            if daysBetweenCaseDeath > maximumValue:
                maximumValue = daysBetweenCaseDeath
                # Final statistic containing state name, days between first case and first death
                finalStat = str(state) + ":" + " " + str(daysBetweenCaseDeath)
    return finalStat


#############              minDaysCaseDeath             ######################
#write a function that takes, as arguments, the name of the file containing case/death
#data and the name of a file containing population data, and returns the state whose
#time between the first case any the first death is a minimum value. Hint: use the
#population.csv file to get the name of each state...as you read through that file,
#get the name of each state and use the caseToDeath(fileName, state) helper function to get the number of days
#between the first case and the first death for that state.  keep track of this date
#as well as the corresponding state as you determine the smallest of these dates
#your function should return a string containing the name of the state and the number of
#days between the first case and the first death.  For example, if the state were Washington
#and the number of days was 12, your function should return the string 'Washington: 12 days'
#make sure your string is grammatically correct.  if it is 1 day, it should be singular.
#name this function minDaysCaseDeath(caseFile, populationFile).

def minDaysCaseDeath(caseFile, populationFile):
    f = open(populationFile,"r")
    minimumValue = 15
    numList = []
    for line in f:

        # Split the values by ","
        nameSplit = line.split(",")
        # First value is the state name
        state = nameSplit[0]
        # Days between the first case and the first death
        daysBetweenCaseDeath = caseToDeath(caseFile,state)

        typo = type(daysBetweenCaseDeath)
    # Have to make sure the result is integer otherwise it won't compare
        if typo == int:
            if daysBetweenCaseDeath < minimumValue:
                minimumValue = daysBetweenCaseDeath
                # Final statistic containing state name, days between first case and first death
                finalStat = str(state) + ":" + " " + str(daysBetweenCaseDeath)

    f.close()
    return finalStat

#############                  eventsOnDate              #########################
#write a function that takes, as arguments, the name of the file containing case/death
#data, a state, a date and an event type.  if the event is 'cases' your function should
#return the number of cases reported on that date, and if the event is 'deaths' your
#function should return the number of deaths on that date.  Name this function
#eventsOnDate(fileName, state, date, event).

def eventsOnDate(fileName, state, date, event):

    f = open(fileName, "r")
    originalDate = str(recognizeDate(date))
    eventsList = []
    casesMatch = event == "cases"
    deathMatch = event == "deaths"

    if casesMatch:
        for line in f:
            # Read the values in each line, splitting them into their own values
            splitValue = line.split(",")
            dateFinal = splitValue[0]
            stateFinal = splitValue[1]
            fips = splitValue[2]
            cases = splitValue[3]
            deaths = splitValue[4]
            deaths = deaths.strip("\n")

            dateMatch = dateFinal == originalDate
            stateMatch = state == stateFinal

            if dateMatch and stateMatch:
                eventsList.append(cases)
                finalStat = eventsList[0]
    elif deathMatch:
        for line in f:
            # Read the values in each line, splitting them into their own values
            splitValue = line.split(",")
            dateFinal = splitValue[0]
            stateFinal = splitValue[1]
            fips = splitValue[2]
            cases = splitValue[3]
            deaths = splitValue[4]
            deaths = deaths.strip("\n")

            dateMatch = dateFinal == originalDate
            stateMatch = state == stateFinal

            if dateMatch and stateMatch:
                eventsList.append(deaths)
                finalStat = int(eventsList[0])

    f.close()
    return finalStat







#####################        casesBetweenDates       #############################
#write a function that takes, as an argument, the name of a file that contains case/death data,
#a state, a start date, an end date, and an event type,  if the event is 'cases', your
#function should returns the number of NEW cases between those two dates, and if the
#event type is 'deaths', your function should return the number of NEW deaths between those
#two dates.  You must use the helper function eventsOnDate(fileName, state, date, event)
#that you created previously. Even if you are unable to write that function, you should
#assume that the function exists and that you can use it.  
#Name this function casesBetweenDates(fileName, state, start, end, event).


def casesBetweenDates(fileName, state, start,event):

    startEvent = eventsOnDate(fileName,state,start,event)
    startEvent = int(startEvent)
    endDate = lastDateinCSV()
    endEvent = eventsOnDate(fileName,state,endDate,event)
    endEvent = int(endEvent)
    finalStat = int(endEvent - startEvent)
    return finalStat



#write a program that takes, as arguments, the name of a file containing case/death data,
#the name of a state, and an event, and returns the latest number of events reported.  if the
#event is 'cases' your function should return the highest number of cases reported for that
#state, and if the event is 'deaths' your function should return the highest number of deaths
#reported for that state.  Name this function totalEventsRecorded(fileName, state, event).


def totalEventsRecorded(fileName, state, event):
    f = open(fileName, "r")
    # Will need to have a master list with all the event numbers for the state
    masterList = []

    for line in f:
        splitValue = line.split(",")
        finalDate = splitValue[0]
        stateFinal = splitValue[1]
        fips = splitValue[2]
        numOfcases = splitValue[3]
        deaths = splitValue[4]
        deaths = deaths.strip("\n")

        # Some booleans to compare if state is the same state or event same event reading on the line

        sameState = state == stateFinal
        needCases = event == "cases"
        needDeaths = event == "deaths"
        # if line has state name and event == "cases"
        if sameState and needCases:
            masterList.append(state)
            masterList.append(numOfcases)
            lenghtOfList = len(masterList)
            # Get the last number for cases
            finalCasesNumber = masterList[lenghtOfList - 1]
            result = int(finalCasesNumber)

        # if line has state name and event == "deaths"
        if sameState and needDeaths:
            masterList.append(state)
            masterList.append(deaths)
            lenghtOfList = len(masterList)
            # Get the last number for cases
            finalDeathNumber = masterList[lenghtOfList - 1]
            result = int(finalDeathNumber)
    f.close()
    return result


#write a function that takes, as arguments, the name of a file containing case/death data,
#a file containing population data, and an event type, and returns the name of the state
#with the highest number of events in the form of a STRING: 'State: events'  For example,
#if Washington had 45 cases, and it was the highest number of cases of all states, your
#function should return the string 'Washington: 45'  there should be one space between the colon
#and the number of events.  You must use the helper function totalEventsRecorded(fileName, state, event)
#in this function. Name this function mostEvents(caseFile, populationFile, event).


def mostEvents(caseFile, populationFile, event):
    f = open(populationFile, "r")
    maximumValue = 0
    finalStat = []
    for line in f:
        # Split the values by ","
        nameSplit = line.split(",")
        # First value is the state name
        state = nameSplit[0]
        numberOfEvents = totalEventsRecorded(caseFile, state, event)
        numberOfEvents = int(numberOfEvents)
        if numberOfEvents > maximumValue:
            maximumValue = numberOfEvents
            finalStat = str(state) + ": " + str(maximumValue)
    f.close()
    return finalStat


#write a function that takes, as arguments, the name of a file containing case/death data,
#a file containing population data, and an event type (either 'cases' or 'deaths'), 
#and returns total number of events in the US.  Name this function 
#totalUSEvents(caseFile, populationFile, event).  You must use the helper function 
#totalEventsRecorded(caseFile, myState, event) in this function.

def totalUSEvents(caseFile, populationFile, event):
    f = open(populationFile, "r")
    maximumValue = 0
    totalNumList = []
    for line in f:
        # Split the values by ","
        nameSplit = line.split(",")
        # First value is the state name
        state = nameSplit[0]
        # Need the max # of events for that state
        numberOfEvents = totalEventsRecorded(caseFile, state, event)
        # Add the integer form to a list to sum later
        totalNumList.append(int(numberOfEvents))
    f.close()
    # return the sum of the list that has all the maximum
    return sum(totalNumList)


#write a program that takes, as arguments, the name of a file containing case/death data,
#the name of a state, the population of the state, and an event, and returns the latest 
#number of events per 100,000 people reported.
#if the event is 'cases' your function should return the highest number of cases reported per 100,000 for that
#state, and if the event is 'deaths' your function should return the highest number of deaths per 100,000
#reported for that state.  Your answer should be rounded to a WHOLE NUMBER (no decimal point). 
#You must use the helper function that determines the maximum number of events for the state, 
#totalEventsRecorded(fileName, state, event) in this function.  
#Your answer must be a WHOLE number, not a float...no decimal point!  Name this function 
#eventsPerCapita(fileName, state, population, event).  (5 points)

def eventsPerCapita(fileName, state, population, event):

    population = int(population)
    # Need to get the maximum recorded event for the state
    numberOfEvents = totalEventsRecorded(fileName, state, event)
    # convert the result from string to an int
    numberOfEvents = int(numberOfEvents)

    # Because it's cases per 100K, have to divide the population by 100K
    # Make sure it's cases per 100K
    if population > 100000:
        hundredThouPop = population / 100000
    else:
        hundredThouPop = 1

    # divide the number of events by previous result
    finalNumber = numberOfEvents / hundredThouPop
    finalNumber = round(finalNumber)
    finalNumber = int(finalNumber)

    return finalNumber

#write a function that takes, as arguments, the name of a file containing case/death data,
#a file containing population data, and an event type, and returns the name of the state
#with the highest number of events per 100,000 people in the form of a STRING: 'State: events'  For example,
#if Washington had 45 cases per 100,000, and it was the highest number of cases per 100,000 of all states, your
#function should return the string 'Washington: 45 per 100,000'  there should be one space between the colon
#and the number of events.  You must use the helper function eventsPerCapita(fileName, state, population, event)
#in this function. Name this function mostEventsPerCapita(caseFile, populationFile, event).
#(10 points)

def mostEventsPerCapita(caseFile, populationFile, event):
    f = open(populationFile)
    maximumPerCapitaNumber = 0

    for line in f:
        splitValue = line.split(",")
        stateFinal = splitValue[0]
        populationFinal = splitValue[1]
        perCapitaNumber = eventsPerCapita(caseFile, stateFinal, populationFinal, event)
        perCapitaNumber = int(perCapitaNumber)
        if perCapitaNumber > maximumPerCapitaNumber:
            maximumPerCapitaNumber = perCapitaNumber
            finalPerCapita = str(stateFinal) + ": " + str(maximumPerCapitaNumber) + " per 100,000"
    f.close()
    return finalPerCapita

#write a function that takes, as arguments, the name of a file containing case/death data,
#a file containing population data, and an event type, and returns the name of the state
#with the lowest number of events per 100,000 people in the form of a STRING: 'State: events'  For example,
#if Washington had 45 cases per 100,000, and it was the lowest number of cases per 100,000 of all states, your
#function should return the string 'Washington: 45 per 100,000'  there should be one space between the colon
#and the number of events.  You must use the helper function eventsPerCapita(fileName, state, population, event)
#in this function. Name this function fewestEventsPerCapita(caseFile, populationFile, event).
#(10 points)

def fewestEventsPerCapita(caseFile, populationFile, event):
    f = open(populationFile)
    minimumPerCapita = 100

    for line in f:
        splitValue = line.split(",")
        stateFinal = splitValue[0]
        populationFinal = splitValue[1]
        perCapitaNumber = eventsPerCapita(caseFile, stateFinal, populationFinal, event)
        perCapitaNumber = int(perCapitaNumber)
        if perCapitaNumber < minimumPerCapita:
            minimumPerCapita = perCapitaNumber
            finalPerCapita = str(stateFinal) + ": " + str(minimumPerCapita) + " per 100,000"
    f.close()
    return finalPerCapita


# This is a helper function, if this returns True then the date is greater than the last date in the
# csv file. This means the state hasn't opened yet.
def dateComparison(startDate, endDate):
    # split the values by "/" this returns a string which will be converted to ints

    start = recognizeDate(startDate)
    end = recognizeDate(endDate)

    # This checks that the queryDate is in between the start and end date. Returns a boolean.
    greater = start > end
    return greater


# Additional function. This function writes to a .txt file some statistics. It writes date state will open or has
# open for businesses. The new cases between opening dates and the latest date for data compiled. Finally, it
# writes the total case for the state.

def writeToFile(event):
    # open the file containing the accumulated data
    f = open("statesOpening.csv","r")
    # open the file we will write to
    caseFile = open("CovidStatistics.txt", "a")
    for line in f:
        # Here we get the name of the state and the date businesses are openin
        splitValue = line.split(",")
        date = splitValue[0]
        stateFinal = splitValue[1]
        population = splitValue[2]
        twoWeeksAfter = splitValue[3]
        twoWeeksAfter = twoWeeksAfter.strip("\n")

        statsFor = "Statistics for " + str(stateFinal)
        # Get the last compiled date
        endDate = lastDateinCSV()
        startDate = date
        # convert date to match Python format to use later
        beginningDate = recognizeDate(date)

        # if this returns True, the state hasn't opened for businesses yet
        notInRange = dateComparison(date,endDate)

        # change 2Weeks after date
        twoWeeksAfter = recognizeDate(twoWeeksAfter)
        if notInRange:
            # Opening Date
            openingStateDate = "The state will open business as usual on: " + str(beginningDate)
            # Date of first event
            firstEvent = "The first of " + str(event) + " occurred: " + str(
                getFirstEvent("us-states.csv", stateFinal, event))
            # State hasn't opened yet
            casesInBetween = "Currently the state has not declared a business opening date."

            # Write to the file
            caseFile.write(statsFor)
            caseFile.write("\n")
            caseFile.write(openingStateDate)
            caseFile.write("\n")
            caseFile.write(firstEvent)
            caseFile.write("\n")
            caseFile.write(casesInBetween)
            caseFile.write("\n")
            caseFile.write("\n")
        else:
            # population
            populationStat = "1. Population: " + str(population)

            # Opening date
            openingStateDate = "2. The date this state started opening business as usual: " + str(beginningDate)

            # Date that is 2 weeks after opening date
            twoWeeksStat = "3. Two weeks after opening date: " + str(twoWeeksAfter)

            # Track daily changes
            previousDay = previousDate()
            previousDay = str(previousDay)
            previousEvents = eventsOnDate("us-states.csv", stateFinal,previousDay,event)

            # cases on last day
            lastDayEvents = eventsOnDate("us-states.csv",stateFinal,endDate,event)

            # Changes between last day and previous day
            dailyChange = int(lastDayEvents) - int(previousEvents)

            # Date of first event
            firstEvent = "4. The first of " + str(event) + " occurred: " + str(
                getFirstEvent("us-states.csv", stateFinal, event))
            # How many cases in between since opening date and last compiled date
            casesInBetween = "5. The new cases between opening date: " + str(beginningDate) + " and compiled date: " + str(endDate) + " are: " + str(
                casesBetweenDates("us-states.csv", stateFinal, startDate, event))
            # Number of total cases
            totalCases ="6. Total " + str(event) + ": " + str(totalEventsRecorded("us-states.csv",stateFinal,event))
            # Cases per capita
            casesPerCapita = "7. The " + str(event) + " per capita: " + str(eventsPerCapita("us-states.csv",stateFinal,population,event))

            # lastTracked day
            lastDayTracked = "8. Last date that with data: " + str(endDate)
            dayChange = "9. The change in cases between  " +str(previousDay)+ " and " + str(endDate) + ": " + "+"+str(dailyChange)


            maximumInDailyChange = 0

            if dailyChange > maximumInDailyChange:
                maximumInDailyChange = dailyChange
                happenedIn = "10. The highest spike in numbers happened between " + str(endDate) + " and " + str(previousDay) + " with +" + str(dailyChange) + " in new " + str(event)
            else:
                happenedIn = "10. No major change"



            # Write stats to file
            caseFile.write(statsFor)
            caseFile.write("\n")
            caseFile.write(populationStat)
            caseFile.write("\n")
            caseFile.write(firstEvent)
            caseFile.write("\n")
            caseFile.write(lastDayTracked)
            caseFile.write("\n")
            caseFile.write(openingStateDate)
            caseFile.write("\n")
            caseFile.write(twoWeeksStat)
            caseFile.write("\n")
            caseFile.write(casesInBetween)
            caseFile.write("\n")
            caseFile.write(totalCases)
            caseFile.write("\n")
            caseFile.write(casesPerCapita)
            caseFile.write("\n")
            caseFile.write(happenedIn)
            caseFile.write("\n")
            caseFile.write("\n")

    return previousEvents
    f.close()

print(writeToFile("cases"))