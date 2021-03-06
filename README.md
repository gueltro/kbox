# `kbox`
##### an encrypted file system

## What is `kbox`?
`kbox` is a system that allows you to securely store your files on an untrusted server. Users can remain confident that anyone with access the server cannot decrypt any of your files, including both the filenames and content, without access to your cryptographically secure private key which is stored on your local computer. Additionally, files are stored securely along with a signature of their content so `kbox` users will always know if someone has tampered with their encrypted files.
For more details on the design, please refer to:
[this paper] (http://css.csail.mit.edu/6.858/2014/projects/gueltro-klaverty-npaggi-vrama.pdf)

## Usage:
`kbox <command> [<argument>]`

## Commands:
- `setup`: setup a username, generate a key, enter the information for the server, and create a root directory
- `show-roots`: Show the list of current root knodes
- `show <knode_name>`: Visualize remote folder rooted at knode with name <knode_name>
- `push <local_file_name>`: Upload a local file located in a kbox directory in the remote directory (recursively if file is a folder)
- `pull <remote_file_name>`: Download a remote file in your local kbox folder

## Getting Started:
1. Download/clone the kbox source. (Do not put it at the path `$HOME/kbox`. See notes for more information.)
2. Set an alias for the string `'kbox'` to the command that runs the `commands.py` file. You can use a command such as: 

 ```bash
echo 'alias kbox="python <PATH-TO-THE-KBOX-CODE>/commands.py"' >> ~/.bashrc
```

3. Source the changes to your bashrc. You can use a command such as:

  ```bash
  source ~/.bashrc
  ```
(or restart your shell)

4. Run `kbox setup` to setup your first username, generate a key, enter the information for the server, and create a root directory.

5. Navigate to your `kbox` directory:

  ```bash
cd ~/kbox/
``` 
If you look at its contents, you should see a folder that corresponds to your root directory. From here you can add files to your root, push them to the server, pull files from the server, switch users, create new roots, etc. See **Sample Usage** for more ideas.

## Sample Usage
This user has initialized his or her kbox with the username `user1` and a single root `myroot`.

 ```bash
    $ cd ~/kbox/
    $ ls
    myroot
    $ cd myroot/
    $ touch mytestfile
    $ echo "this is a test" >> mytestfile
    $ ls
    mytestfile
    $ kbox push mytestfile
    $ cd ..
    $ rm -r myroot
    $ kbox show-roots
    myroot
    $ ls
    $ kbox show myroot
    $ ls
    myroot
    $ cd myroot
    $ ls
    mytestfile.rem
    $ kbox pull mytestfile.rem
    $ ls
    mytestfile
    $ cat mytestfile
    this is a test
    $
```

## Notes
* The kbox system uses a folder called `kbox` in your home directory for all of your interactions with the files stored on the server. Do **not** put the kbox source code into this directory.
* If the account on the server that you are using is password protected, you may quickly grow tired of typing in your password for that account. You can avoid this by adding your ssh keys to the list of authorized keys on the server. You can use the command:

  ```bash
cat .ssh/id_rsa.pub | ssh <USERNAME@SERVER> 'cat >> .ssh/authorized_keys'
```
For more information or troubleshooting for this process, see [this website] (http://www.linuxproblem.org/art_9.html).
* The current implementation of `kbox` only works for Linux/UNIX systems.
