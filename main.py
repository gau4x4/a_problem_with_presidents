import csv
import pandas
import datetime as dt
import numpy as NaN
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from operator import itemgetter
from IPython.display import display
from statistics import mode

headerIndexDict = {}

# Reading CSV file of U.S. Presidents Birth and Death Information
def readCSVDataFile():
    rows = []
    with open("U.S. Presidents Birth and Death Information - Sheet.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    rows = rows[:-1]
    return header, rows

def csvDateAdjustment(rows):
    dobIndex = headerIndexDict['BIRTH DATE']
    dodIndex = headerIndexDict['DEATH DATE']

    for row in rows:
        dobDateStr = row[dobIndex]
        dobDateStrArr = dobDateStr.split(' ')

        dobDateStr = '{} {} {}'.format(dobDateStrArr[0][:3], dobDateStrArr[1], dobDateStrArr[2])
        row[dobIndex] = dobDateStr

        dodDateStr = row[dodIndex]
        if (dodDateStr != ''):
            dodDateStrArr = dodDateStr.split(' ')

            dodDateStr = '{} {} {}'.format(dodDateStrArr[0][:3], dodDateStrArr[1], dodDateStrArr[2])
            row[dodIndex] = dodDateStr

# Creating data with no death date.
# Helper methods
# Graph Plotter
# Printing Lists
def createData(header, rows):
    birthDateIndex = headerIndexDict['BIRTH DATE']
    deathDateIndex = headerIndexDict['DEATH DATE']
    livedYearsIndex = headerIndexDict['lived_years']

    for row in rows:
        dob = row[birthDateIndex]
        dob_dt_obj = dt.datetime.strptime(dob, '%b %d, %Y')
        if dob == NaN:
            continue

        dod = row[deathDateIndex]
        dod_dt_obj = ''
        if dod != '':
            dod_dt_obj = dt.datetime.strptime(dod, '%b %d, %Y')


        row.append(getBirthYear(dob_dt_obj))
        row.append(getLivedYears(dob_dt_obj, dod_dt_obj))
        row.append(getLivedMonths(dob_dt_obj, dod_dt_obj, row[livedYearsIndex]))
        row.append(getLivedDays(dob_dt_obj, dod_dt_obj))
    
    return rows

def printDataList(header, list,fileName):
    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    list.insert(0, header)
    df = pandas.DataFrame(list[1:11], columns=header)

    ax.table(cellText=df.values, colLabels=df.columns, colColours=(['BurlyWood'] * len(header)))

    fig.tight_layout()
    plt.savefig(fileName, dpi=400)
    plt.show()

def statsListPrinting(mean, weighted_avg, median, mode, max, min, standard_deviation):
    list = []
    list.append(['Mean', mean])
    list.append(['Weighted Avg', weighted_avg])
    list.append(['Median', median])
    list.append(['Mode', mode])
    list.append(['Max', max])
    list.append(['Min', min])
    list.append(['Standard Deviation', standard_deviation])


    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    list.insert(0, ['Type', 'Value'])
    df = pandas.DataFrame(list[1:], columns=list[0])

    ax.table(cellText=df.values, colLabels=df.columns, colColours=(['BurlyWood'] * 2))
    fig.tight_layout()
    plt.savefig('stats.png', dpi=400)
    plt.show()

def graphPlotter(rows):
    tlist = list(zip(*rows))
    xaxis = tlist[0]
    yaxis = tlist[8]

    num_rows = len(rows)
    mean_value = getMeanFromList(rows)
    median_value = getMedianFromList(rows)
    mode_value = getModeFromList(rows)
    max_value = getMaxFromList(rows)
    min_value = getMinFromList(rows)
    sd_value = getStdFromList(rows)

    y_mean = [mean_value] * num_rows
    y_median = [median_value] * num_rows
    y_mode = [mode_value] * num_rows
    y_max = [max_value] * num_rows
    y_min = [min_value] * num_rows
    y_sd_max = [mean_value + sd_value] * num_rows
    y_sd_min = [mean_value - sd_value] * num_rows

    ax = plt.gca()
    
    ax.tick_params(axis='x', labelrotation = 90)

    mean_line = ax.plot(xaxis, y_mean, label='Mean - ' + str(format(mean_value, ".3f")), linestyle='--')
    median_line = ax.plot(xaxis, y_median, label='Median - ' + str(median_value), linestyle=':')
    mode_line = ax.plot(xaxis, y_mode, label='Mode - ' + str(mode_value), linestyle='-')
    max_line = ax.plot(xaxis, y_max, label='Max - ' + str(max_value), linestyle='dotted')
    min_line = ax.plot(xaxis, y_min, label='Min - ' + str(min_value), linestyle='dotted')

    ax.fill_between(xaxis, y_sd_min, y_sd_max, color='blue', alpha=0.15, label='Standard Deviation')

    legend = ax.legend(loc='lower left')

    plt.plot(xaxis, yaxis)
    plt.savefig('graph.png', dpi=400)
    plt.show()

# Mathematical Calculations Mean/Median/Mode/Min/Max/WMean/Standard Deviation
def getMeanFromList(list):
    count=0
    total=0
    livedDaysIndex = headerIndexDict['lived_days']

    for row in list:
        total = total + row[livedDaysIndex]
        count = count + 1

    return (total/count)

def getWAvgFromList(list):
    count = 0
    total = 0
    weight = (1/len(list))
    livedDaysIndex = headerIndexDict['lived_days']

    for row in list:
        total = total + (row[livedDaysIndex] * weight)
        count = count + (weight)

    return (total/count)

def getMedianFromList(list):
    display(pandas.DataFrame(list))

    list2 = sorted(list, key=itemgetter(headerIndexDict['lived_days']))
    length = len(list2)

    medianEl1 = 0
    medianEl2 = 0
    if length % 2 == 1:
        medianEl1 = (int)((length + 1) / 2)
        medianEl2 = (int)((length + 1) / 2)
    else:
        medianEl1 = ((int)(length/2))
        medianEl2 = (((int)(length/2) + 1))

    val1 = list2[medianEl1][headerIndexDict['lived_days']]
    val2 = list2[medianEl2][headerIndexDict['lived_days']]

    median = (val1 + val2) / 2
    return median

def getModeFromList(list):
    listDays = []
    for row in list:
        listDays.append(row[headerIndexDict['lived_days']])

    modeVal = mode(listDays)
    return modeVal
    
def getStdFromList(list):
    livedDaysIndex = headerIndexDict['lived_days']
    mean = getMeanFromList(list)

    sigmaVal = 0;
    for row in list:
        sigmaVal = sigmaVal + ((row[livedDaysIndex] - mean) ** 2)
    
    before_root_val = sigmaVal / (len(list) - 1)
    standard_deviation = (before_root_val ** 0.5)
    return standard_deviation

def getMaxFromList(list):
    livedDaysIndex = headerIndexDict['lived_days']
    max = list[0][livedDaysIndex]
    for row in list:
        livedDays = row[livedDaysIndex]
        if (livedDays > max) :
            max = livedDays
    return max

def getMinFromList(list):
    livedDaysIndex = headerIndexDict['lived_days']
    min = list[0][livedDaysIndex]
    for row in list:
        livedDays = row[livedDaysIndex]
        if (livedDays < min) :
            min = livedDays
    return min

def getBirthYear(dob_dt_obj):
    dob_year = dob_dt_obj.year
    return dob_year

def getLivedYears(dob_obj, dod_obj):
    effective_dod_obj = dod_obj

    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), '%b %d, %Y')
        effective_dod_obj = dt.datetime.strptime(today_str, '%b %d, %Y')
    
    return (relativedelta(effective_dod_obj, dob_obj).years)

def getLivedMonths(dob_obj, dod_obj, total_years):
    effective_dod_obj = dod_obj

    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), '%b %d, %Y')
        effective_dod_obj = dt.datetime.strptime(today_str, '%b %d, %Y')
    
    return (relativedelta(effective_dod_obj, dob_obj).months + (total_years * 12))

def getLivedDays(dob_obj, dod_obj):
    effective_dod_obj = dod_obj
    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), '%b %d, %Y')
        effective_dod_obj = dt.datetime.strptime(today_str, '%b %d, %Y')

    date_format = '%m/%d/%Y'
    a = dt.datetime.strftime(effective_dod_obj, date_format)
    a = dt.datetime.strptime(a, date_format).date()
    b = dt.datetime.strftime(dob_obj, date_format)
    b = dt.datetime.strptime(b, date_format).date()

    return ((a-b).days)

# Main Helper Method
def main():

    header, rows = readCSVDataFile()

    header.append('year_of_birth')
    header.append('lived_years')
    header.append('lived_months')
    header.append('lived_days')

    i=0
    for val in header:
        headerIndexDict[val] = i
        i = i + 1

    csvDateAdjustment(rows)

    rows = createData(header, rows)

    leastLivedPresident = sorted(rows, key=itemgetter(headerIndexDict['lived_days']))
    printDataList(header, leastLivedPresident,'leastLivedPresident.png')
    
    mostLivedPresident = sorted(rows, key=itemgetter(headerIndexDict['lived_days']), reverse=True)
    printDataList(header, mostLivedPresident,'mostLivedPresident.png')

    # Calculating Mathematical values to print in the console
    mean = getMeanFromList(rows)
    weightedAverage = getWAvgFromList(rows)
    median = getMedianFromList(rows)
    mode = getModeFromList(rows)
    max = getMaxFromList(rows)
    min = getMinFromList(rows)
    standardDeviation = getStdFromList(rows)

    # list = []
    # list.append(['Mean', mean])
    # list.append(['Weighted Average', weightedAverage])
    # list.append(['Median', median])
    # list.append(['Mode', mode])
    # list.append(['Max', max])
    # list.append(['Min', min])
    # list.append(['Standard Deviation', standardDeviation])

    # printDataList(header, list,'stats.png')
    # Printing Data in the console
    statsListPrinting(mean, weightedAverage, median, mode, max, min, standardDeviation)
    
    graphPlotter(rows)

main()
