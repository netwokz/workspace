#Requires AutoHotkey v2.0

#t::
{
	if WinExist("Windows PowerShell")
		WinActivate
	Else Run "C:\Users\deanejst\AppData\Local\Microsoft\WindowsApps\wt.exe"
	Return
}

#s::
{
    win_name := "C:\Program Files\Google\Chrome\Application\chrome.exe"
    win_prog := "ahk_exe chrome.exe"
    if WinExist(win_prog)
        {
        WinActivate
        Run "https://portal.ez.na.rme.logistics.a2z.com/work-orders/new"
        }
    Else Run win_prog
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

^+c::
{
    Send "GYR1Admin"
    Send "{Tab down}{Tab up}"
    Send "ControlsGYR1AE"
    Send "{Enter down} {Enter up}"
}

#h::
{
    win_name := "C:\Users\deanejst\Documents\software\RemoteHMI_IP=[10.79.216.18_8080].exe"
    login := "ahk_class #32770"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.216.18_8080].exe"
    if WinExist("GYR1 [10.79.216.18:8080] - Remote HMI (Ver1.2.0.2)")
        WinActivate
        if WinExist(login)
            {
                WinActivate
                Send "User1"
                Send "{Tab down}{Tab up}"
                Send "Moaust"
                Send "{Enter down} {Enter up}"    
            }
    Else 
        {
            Run win_name
            Sleep 2000
            WinActivate("Password")
            WinWaitActive("Password")
            Send "User1"
            Send "{Tab down}{Tab up}"
            Send "Moaust"
            Send "{Enter down} {Enter up}"

        }
    Return
}

+F1::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.230_8080] SLAM101.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.230_8080] SLAM101.exe"
    Run win_name
    WinWait("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}
+F2::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.231_8080] SLAM302.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.231_8080] SLAM302.exe"
    Run win_name
    WinWait("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}
+F3::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.232_8080] SLAM103.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.232_8080] SLAM103.exe"
    Run win_name
    WinWait("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}
+F4::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.233_8080] SLAM304.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.233_8080] SLAM304.exe"
    Run win_name
    WinWait("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}
+F5::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.234_8080] SLAM305.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.234_8080] SLAM305.exe"
    Run win_name
    WinWait("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}
+F6::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.235_8080] SLAM206.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.235_8080] SLAM206.exe"
    Run win_name
    WinWait("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}
+F7::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.236_8080] SLAM207.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.236_8080] SLAM207.exe"
    Run win_name
    WinWait("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}
+F8::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.237_8080] SLAM208.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.237_8080] SLAM208.exe"
    Run win_name
    WinWait("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}
+F9::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.238_8080] SLAM109.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.238_8080] SLAM109.exe"
    Run win_name
    WinWait("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}
+F10::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.239_8080] SLAM210.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.239_8080] SLAM210.exe"
    Run win_name
    WinWait("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}
+F11::
{
    win_name := "C:\Users\deanejst\Desktop\HMIs\RemoteHMI_IP=[10.79.218.240_8080] SLAM111.exe"
    win_prog := "ahk_exe RemoteHMI_IP=[10.79.218.240_8080] SLAM111.exe"
    Run win_name
    WinWaitActive("Password")
    Send "User1"
    Send "{Enter down} {Enter up}"
}