import webbrowser 

# Windows
chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe %s'

# getting path 
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# First registers the new browser 
webbrowser.register('chrome', None,  
                    webbrowser.BackgroundBrowser(chrome_path)) 

for i in range(201,232):
    ip = "10.79.217."
    webbrowser.get('chrome').open(ip + str(i))