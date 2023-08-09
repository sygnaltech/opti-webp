

'MsgBox "Execution paused. Press OK to continue."

Set WshShell = CreateObject("WScript.Shell") 
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.Run Chr(34) & scriptDir & "\opti-webp.exe" & Chr(34) & " -a -w " & WScript.Arguments(0), 0
Set WshShell = Nothing
