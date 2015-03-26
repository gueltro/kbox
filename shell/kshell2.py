import subprocess


while 1:
	
	sp = subprocess.Popen("/bin/zsh",stdin=subprocess.PIPE,shell=True,env=dict(ENV='/home/gueltro/.zshrc'))
	x = raw_input('<k>')

	sp.communicate(x)
