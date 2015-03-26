import subprocess

sp = subprocess.Popen(["/bin/zsh"])
while 1:
    command = raw_input("$ ")
    stdout,stderr=ps.communicate(command)
    print stdout
