#!/usr/bin/python3

# ==============================================================
__author__ = "Nurul Mamun"
__date__ = " 12 January, 2023 "
__version__ = "1.0"
__description__ = "login to PSS node using Paramiko and execute few commands"
# ==============================================================

# ========== Imports ===========================================
import paramiko
import getpass                                                                      # getpass to hide user typed password characters
import time
# ==============================================================

# ========= Variables ==========================================
terminal_output = ''                                                                # variable to keep command outputs
cli_commands_sent = ["show version","alm","show general date","logout"]             # list of cli commands to be sent
pss_pre_login = 'AAA'                                                               # default username for ssh connection (PSS users know)eeee   b
# ==============================================================

# ========= Functions ==========================================


# ==============================================================

# ========== Main Function =====================================
def main():

    print("#" * 80 + "\n")
    ip_address = input("IP Address: ")                                              # user inputs
    domain_user_name = input("User Name: ")
    pass_word = getpass.getpass("Password: ")
    print("\n" + "#" * 80)

    

    session = paramiko.SSHClient()                                                  # define paramiko client
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())                   # host key auto add policy

    session.connect(hostname=ip_address, username=pss_pre_login, password="")       # first connection as default ssh user with no password
    time.sleep(2)
    
    open_shell = session.invoke_shell()                                             # inovking shell to send commands/inputs
    time.sleep(2)
    
    open_shell.send(domain_user_name + "\n")                                        # send user name collected from the prompt
    time.sleep(2)
    open_shell.send(pass_word + "\n")                                               # send password for the user
    time.sleep(1)

    terminal_output = open_shell.recv(65000)
    print(terminal_output.decode()) 
    open_shell.send("Y" + "\n")                                                     # response to prompt 'Do you acknowledge? (Y/N)?'
    time.sleep(1)

    for command in cli_commands_sent:                                               # send commands one by one
        open_shell.send(f'{command}\n')
        time.sleep(1)
        terminal_output = open_shell.recv(65000)
        print(terminal_output.decode())                                             # print command outputs

    session.close()                                                                 # close session


# ==============================================================

if __name__ == "__main__":
    main()
