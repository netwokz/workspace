#Requires AutoHotkey v2.0

#t::
{
	if WinExist("Windows PowerShell") or WinExist("Ubuntu")
		WinActivate
	Else Run 'C:\Users\netwokz\AppData\Local\Microsoft\WindowsApps\wt.exe -p `"Ubuntu`"'
	Return
}

#t::
{
	if WinExist("Windows PowerShell") or WinExist("Ubuntu")
		WinActivate
	Else Run 'C:\Users\netwokz\AppData\Local\Microsoft\WindowsApps\wt.exe -p `"Ubuntu`"'
	Return
}

#c::
{
    win_name := "C:\Program Files\Google\Chrome\Application\chrome.exe"
    win_prog := "ahk_exe chrome.exe"
    if WinExist(win_prog)
        WinActivate
    Else Run win_prog
    Return
}