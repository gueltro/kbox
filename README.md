# kBox
##### an encrypted file system

For details on the implementation refer to:
[our paper] (http://css.csail.mit.edu/6.858/2014/projects/gueltro-klaverty-npaggi-vrama.pdf)

## Usage:
`kbox <command> [<argument>]`

## Commands:
- `setup`: setup 
- `show-roots`: Show the list of currents knodes
- `show <knode_name>`: Visualize remote folder rooted at knode with name <knode_name>
- `push <local_file_name>`: Upload a local file located in a kbox directory in the remote directory (recursively if file is a folder)
- `pull <remote_file_name>`: Download a remote file in your local kbox folder

## Inital Setup:
1. Download/clone the kbox source.
2. Set an alias for the string 'kbox' to the command that runs the commands.py file. You can use: `echo 'alias kbox="python <PATH-TO-THE-KBOX-CODE>/commands.py"' >> ~/.bashrc`
