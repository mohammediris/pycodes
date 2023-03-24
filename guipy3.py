import csv
import os
import subprocess
import PySimpleGUI as sg


# import re


def printRoute():
    # os.system('route print')
    output = subprocess.check_output('dir', shell=True,stderr=subprocess.STDOUT, text=True)
    # add new function to refine the output
    #output = subprocess.check_output('dir',text=True)
    print(output)
    # output = subprocess.run('dir',shell=True)
    # text1 = output.find('Persistent Routes:') # find() outputs -1 value if the string is not found
    # text2 = output.find('=', text1)
    # # text1 = output.index("Persistent Routes:")  # index() throw error if the string is not found
    # # text2 = output.index("=", text1)
    # # # print(output.count("Routes"))
    # print(output[text1: text2])
    # print(str(output))
    # if 'Persistent Routes:' in output:
    #    print("string is present")


def createRoute(IP, site):
    routeCommand = 'route -p add ' + IP + '.0.0 mask 255.255.0.0 ' + IP + '.40.254'
    # os.system(routeCommand) # this will simply send the string as command to cmd prompt
    # output = subprocess.check_output(routeCommand, shell=True)
    output = subprocess.check_output(routeCommand, stderr=subprocess.STDOUT, text=True)
    # text=True will make the output into string format
    # print(output)
    if output.find("OK!") != -1:
        # print("Persistent Route for {} is created!".format(site))
        print(f"Persistent Route for {site} is created!")  # this method is using fstring, add f infront of
        # quotes
    elif output.find("The route addition failed") != -1:
        # print("Persistent Route for {} already exist!".format(site))
        print(f"Persistent Route for {site} already exist!")


def deleteRoute(IP, site):
    routeCommand = 'route -p delete ' + IP + '.0.0 mask 255.255.0.0 ' + IP + '.40.254'
    # os.system(routeCommand)
    # output = subprocess.check_output(routeCommand, shell=True)
    output = subprocess.check_output(routeCommand, stderr=subprocess.STDOUT, text=True)
    # print(output)
    if output.find("OK!") != -1:
        print("Persistent Route for {} is deleted!".format(site))
    elif output.find("The route deletion failed") != -1:
        print("Persistent Route for {} doesn't exist!".format(site))


def clearAllRoute():
    output = subprocess.check_output('route print', stderr=subprocess.STDOUT, text=True)
    text1 = output.find('Default')
    text2 = output.find('=', text1)
    Proutes = output[text1 + 9:text2]
    Sroute = Proutes.split()
    Qroute = Sroute[::4]  # leave start index and stop index blank and give step size of 4
    # print(Proutes)
    # print(Qroute)
    for q in Qroute:
        routeCommand = 'route -p delete ' + str(q)
        subprocess.run(routeCommand)
    print("All additional routes cleared!")


# IPscheme = [['ZAK','76.80'],['UAD','75.16']]
file_dir = os.path.dirname(os.path.realpath('__file__'))
# file_name = file_dir + '/routes.csv'
# print (file_name)
file = open(file_dir + '/routes.csv')
# type(file)
csvreader = csv.reader(file)
header = next(csvreader)
IPscheme = []
for row in csvreader:
    IPscheme.append(row)
# print(IPscheme)
# sg.theme('Default1')  # Add a touch of color
# # All the stuff inside your window.
# layout = [
#     [sg.Text('Select Site Name'), sg.DropDown([l[0] for l in IPscheme], key='-SITE-', default_value=IPscheme[0][0])],
#     [sg.Button('Create Route'), sg.Button('Delete Route'), sg.Button('Print Route')],
#     [sg.Button('Clear All Route'), sg.Button('Cancel')],
#     [sg.Multiline("", size=(80, 20), autoscroll=True, reroute_stdout=True, reroute_stderr=True, key='-OUTPUT-')]
# ]
#
# # Create the Window
# window = sg.Window('Static Route', layout)
# # Event Loop to process "events" and get the "values" of the inputs
print(IPscheme)
while True:
    siteName = input("Enter the Site Code: ")
    eventOpt = input("Enter 1 to create\nEnter 2 to delete\nEnter 3 to print\nEnter 4 to clear all\n")
    for i in IPscheme:
        if i[1] == siteName:
            prefix = i[2]
    if eventOpt == '1':
        createRoute(prefix, siteName)
    elif eventOpt == '2':
        deleteRoute(prefix, siteName)
    elif eventOpt == '3':
        printRoute()
    elif eventOpt == '4':
        clearAllRoute()

#window.close()
