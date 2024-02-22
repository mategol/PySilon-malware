import webbrowser
spamKey = True
limitKey = 10
while spamKey == True:
    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    if limitKey != 0:
        limitKey -= 1
    elif limitKey == 0:
        spamKey == False
        quit()
    elif limitKey == "Stop":
        print("It is a infinite code. Caution")