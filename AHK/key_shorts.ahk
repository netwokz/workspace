#Requires AutoHotkey v2.0

#t::
{
	if WinExist("Windows PowerShell")
		WinActivate
	Else Run "C:\Users\deanejst\AppData\Local\Microsoft\WindowsApps\wt.exe"
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

#n::
{
    if WinExist("Network Connections")
        WinActivate
    Else Run "ncpa.cpl"
    Return
}