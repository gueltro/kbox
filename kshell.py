import os

while 1:
	
	command = raw_input("<<k>>: ")

	words = command.split(' ')

	check=0
	for i in range(len(words)):
			
		if  words[i][-4:] == '.rem':
			check=1
			os.system('python ~/kbox/code/commands.py pull '+words[i])
			words[i] = words[i][:-4]
	
	newcommand = ' '.join(words)
						
	if words[0] == 'cd':
		os.chdir(os.path.realpath(words[1]))

	else:
		os.system(newcommand)
		if check ==1:
			os.system('python ~/kbox/code/commands.py free '+words[i])
			

