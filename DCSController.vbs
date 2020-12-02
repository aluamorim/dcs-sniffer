

'Set oShell = CreateObject ("Wscript.Shell") 
'Dim strArgs
'strArgs = "cmd /c .\py\run.bat"
'oShell.Run strArgs, 0, false

Set oShell = CreateObject("Wscript.Shell")
'oShell.CurrentDirectory = "./py"
oShell.CurrentDirectory = "./"
oShell.Run "run.bat", 0, True