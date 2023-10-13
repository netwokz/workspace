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

^+d::
{
    Send A_YYYY A_MM A_DD
}

^+w::
{
    Send "GYR1Admin"
    Send "{Tab down}{Tab up}"
    Send "AmazonGYR1"
    Send "{Enter down} {Enter up}"
}

^+c::
{
    Send "GYR1Admin"
    Send "{Tab down}{Tab up}"
    Send "ControlsGYR1AE"
    Send "{Enter down} {Enter up}"
}

^+e::
{
    Send "DEANEJST"
    Send "{Tab down}{Tab up}"
    Send "EMAGDNIM9#"
    Send "{Enter down} {Enter up}"
}

#h::
{
    win_name := "C:\Users\deanejst\Documents\software\RemoteHMI_IP=[10.79.216.18_8080].exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.216.18_8080].exe"
    if WinExist("GYR1 [10.79.216.18:8080] - Remote HMI (Ver1.2.0.2)")
        WinActivate
    Else 
        {
            Run win_name
            Sleep 2000
            WinActivate("Password")
            WinWaitActive("Password")
            ; Sleep 1000
            Send "User1"
            Send "{Tab down}{Tab up}"
            Send "Moaust"
            Send "{Enter down} {Enter up}"

        }
    Return
}