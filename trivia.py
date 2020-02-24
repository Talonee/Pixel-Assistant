# This class handles miscellaneous commands such as 
# math operations, exchange conversations, etc


# Write note
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    vsc = "C:/Users/Cakee/AppData/Local/Programs/Microsoft VS Code/Code.exe"
    notepad = "C:/WINDOWS/system32/notepad.exe"
    subprocess.Popen([notepad, file_name])