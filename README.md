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
1. Download/clone the kbox source. (Do not put it at the path $HOME/kbox. See notes for more information.)
2. Set an alias for the string 'kbox' to the command that runs the commands.py file. You can use a command such as: `echo 'alias kbox="python <PATH-TO-THE-KBOX-CODE>/commands.py"' >> ~/.bashrc`
3. Source the changes to your bashrc. You can use a command such as: `source ~/.bashrc` (or restart your shell)
4. Run `kbox setup` to setup your first username, generate a key, enter the information for the server, and create a root directory.

## Notes
* The kBox system uses a folder called kbox in your home directory for all of your interactions with the files stored on the server. Do **not** put the kBox source code into this directory.
* If the account on the server that you are using is password protected, you may quickly grow tired of typing in your password for that account. You can avoid this by adding your ssh keys to the list of authorized keys on the server. You can use the command: `cat .ssh/id_rsa.pub | ssh <username@server> 'cat >> .ssh/authorized_keys'`. For more information or troubleshooting for this process, see [this website] (http://www.linuxproblem.org/art_9.html).
