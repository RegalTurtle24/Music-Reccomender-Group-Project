############################################################
# Name: Thys Vanderschoot, Dominic Catena, Isabelle Villanueva
# Pledge: I pledge my honor that I have abided by the Stevens Honor System.
# CS115 Group Project
# 
############################################################

from functools import reduce
import os.path
data = {}

def readFile(filepath):
    """
    Input: the file name to be opened and read
    Output: loads the file into global dictionary data
    Takes a file and unloads the information in the file out into dictionary data. If no file exists, 
        create an empty file and close it
    Writer: Thys
    """
    global data

    if(os.path.exists(filepath)):
        with open(filepath, "r") as f:
            for line in f:
                username, artist = line.strip().split((":"))
                artistlist = artist.split(",")
                artistlist = list(map(lambda s: s.title(), artistlist))
                while('' in artistlist):#removes any empty elements
                    artistlist.remove('')
                data[username] = sorted(artistlist)
    else:
        myfile = open("musicrecplus.txt", "w")
        myfile.close()

def writeFile(fileName, dictionary):
    """
    Input: A file name to write into and a dictionary with the data to right
    Output: Writes the data from the dictionary into the file in accordance with the format "username:Artist1,Artist2,Artist3"
    Writes from a given dictionary into the given file
    Writer: Thys
    """
    file = open(fileName, "w")
    
    for person in dictionary:
        artists = dictionary[person]
        prefix = person + ":"
        userString = prefix
        if(len(artists) == 1):
            userString = prefix + artists[0]
        if(len(artists) > 1):
            userString = prefix + reduce(lambda str1, str2: str1 + "," + str2, artists)
        file.write(userString + "\n")

    file.close()

def getInput():
    """
    Input: From user get a letter to indicate what the program should do
    Output: Returns the letter to indicate what the program should do
    Prompts the user for a choice after printing the options, and continues to ask until the user
        has submitted a proper choice
    Writer: Isabelle
    """
    correctinputs = ["e", "r", "p", "h", "m", "q", "s", "d"]
    while True:
        selection = input("Enter a letter to choose an option:"
                          "\ne - Enter preferences"
                          "\nr - Get recommendations"
                          "\np - Show most popular artists"
                          "\nh - How popular is the most popular"
                          "\nm - Which user has the most likes"
                          "\ns - Show preferences"
                          "\nd - Delete preferences"
                          "\nq - Save and quit\n")
        if(selection not in correctinputs):
            continue
        else:
            break
    return selection

def checkUser():
    """
    Input: username from user using input()
    Output: returns the username the person input
    Prompts the user for an input, and if the user is new also calls for them to enter their preferences
    Writer: Dominic
    """
    username = input("Enter your name (put a $ symbol after your name if you wish your preferences to remain private):\n")
    if(username in data):
        pass
    else:
        enterPreferences(username)
    return username

def enterPreferences(username):
    """
    Input: The username of the current user
    Output: Adds the liked artists to the data dictionary in a sorted and correctly capitilized manner
    Takes in the username and repeatedly asks the user for artists they like until they do not
        enter an artist, then adds the list of artists to their index in the dictionary sorted and in 
        title case
    Writer: Dominic
    """
    global data

    artists = []
    while(True):
        artist = input("Enter an artist that you like (Enter to finish):\n")
        if(artist == ""):
            data[username] = sorted(artists)
            break
        else:
            artists.append(artist.title())
            continue

def deletePreferences(username):
    """
    Input: username for the current user and inputs from user
    Output: changes data to remove indicated artists
    Prompts the user to delete artists until the user presses enter, then removes all of those artists from
        data
    Writer: Isabelle
    """
    preferences = data[username]
    while(True): 
        print("These are your current artists: " , data[username])
        delete= input("Enter the name of the artist you want to delete.\n")
        if(delete== ""):
            data[username] = preferences
            break
        else:
            if(delete in preferences):
                preferences.remove(delete)

def similarprefs(randuser, currentuser):
    """
    Input: 2 different usernames
    Output: Returns the number of artists in common between the users
    Returns the number of shared artists between 2 users, or 0 if the two users have the exact same lists
    Writer: Dominic
    """
    count = 0
    randuserartist = data[randuser]#creates a list of artists from the random user
    curruserartist = data[currentuser]
    if(randuserartist >= curruserartist):#cant have the same artists
        return 0
    for artist in randuserartist:#counts similar artists
        if(artist in curruserartist):
            count += 1
    return count

def getRec(data, currentuser):
    """
    Input: dictionary and the current user
    Output: A list of reccomendations for the current user
    Taking the dictionary of song preferences, returns recommendations for the current user. If
        there are no other users, returns an empty list
    Writer: Dominic
    """
    userlist = list(data.keys())#creates a list of users from the database
    userlist.remove(currentuser)
    
    """
    Extra credit part 3
    Writer: thys
    """
    if (len(userlist) == 0):
        print("There are no other users to recommend from")
        return []
    
    mostsim = 0
    mostsimuser = ""

    for user in userlist:#iterates through the list of users to find the most simliar user to the currentuser
        if("$" in user):
            continue
        numsim = similarprefs(user, currentuser)
        if(numsim==mostsim):
            continue
        elif(numsim>mostsim):
            mostsim = numsim
            mostsimuser = user

    if (mostsimuser == ""):
        print("No recommendations available at this time.")
        return []

    reclist = []

    for artist in list(data[mostsimuser]):#returns a list of recommended artists not including the ones in the current users prefences
        if(artist in list(data[currentuser])):
            continue
        else:
            reclist.append(artist)
    return reclist

def popularArtist():
    """
    Input: none
    Output: List of 3 most popular artists
    Finds and returns a list of the 3 most popular artists
    Writer: Dominic
    """
    listofartists = []
    for user in data.keys():#removes the privated users from the pool
        if("$" in user):
            continue
        else:
            listofartists += data[user]
    allartists = set(listofartists)#turns list into a set to remove duplicates
    artistslikes = []
    def likecounter(currartists, listofartists):
        """
        Counts the artists number of likes
        """
        likes = 0
        for i in listofartists:
            if(i==currartists):
                likes+=1
        return [currartists, likes]
    for artist in allartists:#creates a list of artists and their likes
        artistslikes += [likecounter(artist, listofartists)]
    mostpopular = []
    def getmostpopular(artistslikes, mostlikes):
        """
        Gets the most popular artists out of a list of lists
        """
        person = ""
        index = 0
        for i in range(len(artistslikes)):
            if (artistslikes[i][1] > mostlikes):
                person = artistslikes[i][0]
                index = i
                mostlikes = artistslikes[i][1]
        return [person, index]

    while(len(mostpopular)!=3 and len(artistslikes) != 0):#gets a list of three most popular artists
        person = getmostpopular(artistslikes, 0)[0]
        index = getmostpopular(artistslikes, 0)[1]
        mostpopular.append(person)
        artistslikes.pop(index)

    while('' in mostpopular):#removes any empty elements
        mostpopular.remove('')
    
    if(len(mostpopular) == 0):
        print("Sorry, no artists found")

    return mostpopular

def howPopular():
    """
    Input: Nothing, but takes into account of all the data. 
    Output: The number of likes the most popular artist received. 
    Returns the number of users that like the most popular artist
    Writer: Isabelle
    """
    listOfArtists= [] #will have all the user's artists, excluding the private users 
    for user in data.keys(): 
        if ("$" in user):
            continue
        else:
            listOfArtists += data[user]
    if data == {}:
        print("Sorry, no artists found") #if there are no artists in data
        return
    mostPopularArtists = popularArtist() #will create a variable list that has the top three artists using the popularArtist function
    if(len(mostPopularArtists) == 0): 
        return
    mostPopular = mostPopularArtists[0] #creates a variable (string) that has the most popular artist
    likes = 0 
    for artist in listOfArtists: #iterates through all the artists and checks to see how many times that artist appears to tally the likes. 
        if artist == mostPopular:
            likes += 1
    print(likes)

def userwithmostlikes():
    """
    Input: none
    Output: gives a list of users with the greatest number of liked artists
    Returns a list of users that had the greatest number of liked artists
    Writer: Isabelle
    """
    person = []
    mostlikes = 0
    for user in data.keys():  # removes the privated users from the pool
        if ("$" in user):
            continue
        else:
            if(len(data[user]) > mostlikes):#finds user with most likes
                mostlikes = len(data[user])
                person = [user]
            elif(len(data[user]) == mostlikes):
                person += [user]
    return person

"""
Run the ongoing part of the program
Writer: Thys
"""

readFile("musicrecplus.txt")
username = checkUser()

while(True):
    selection = getInput()
    if(selection == "e"):
        enterPreferences(username)
    elif(selection == "r"):
        recs = getRec(data, username)
        if(len(recs) != 0):
            print( reduce (lambda s1, s2: s1 + "\n" + s2, recs) )
    elif(selection == "p"):
        popular = popularArtist()
        for artist in popular:
            print(artist)
    elif(selection == "h"):
        howPopular()
    elif(selection == "m"):
        users = userwithmostlikes()
        if(len(users) == 0):
            print("There are no public accounts")
        else:
            for user in users:
                print(user)
    elif(selection == "s"):
        prefs = data[username]
        if(prefs == []):
            print("You have no preferences")
        else:
            print(prefs)
    elif(selection == "d"):
        deletePreferences(username)
    elif(selection == "q"):
        writeFile("musicrecplus.txt", data)
        break
