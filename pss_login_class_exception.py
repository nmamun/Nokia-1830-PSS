#!/usr/bin/python3

# ==============================================================
__author__ = "Nurul Mamun"
__date__ = " 06 February, 2023 "
__version__ = "1.0"
__description__ = "login to PSS node using Paramiko, execute few commands, handles exceptions, uses class"
# ==============================================================

# ========== Imports ===========================================
import paramiko
import getpass                                                                      # getpass to hide user typed password characters
import time
import socket
# ==============================================================

# ========= Variables ==========================================
terminal_output = ''                                                                 # variable to store text output from terminal
terminal_output_list = []                                                            # variable to store text output from terminal as a list
cli_commands_sent = ["show version","alm","show general date","logout"]              # list of cli commands to be sent
# ==============================================================

# ========= Classes & Functions ================================
class SshConnection:                                                                 # 'class' to manage SSH connections and related aspects
    
    session_status = True                                                                                       # variable to flag SSH session status
    
    def __init__(self, ip_address, user_name, pass_word) -> None:

        try:
            self.connection = paramiko.SSHClient()                                                              # setting up SSH session
            self.connection.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
            self.connection.connect(hostname=ip_address, username=user_name, password=pass_word)

        except paramiko.AuthenticationException :                                                               # exception
            print("Authentication error, please check username password and try again. \n")                     # print error message
            self.session_status = False                                                                         # change session status flag
        except paramiko.ssh_exception.NoValidConnectionsError :
            print("Unable to SSH to device, please check IP connectivity to the device and try again. \n")
            self.session_status = False
        except paramiko.ssh_exception.SSHException("No authentication methods available"):
            print("Check initial login credential. \n")
            self.session_status = False
        except socket.error:
            print("Connection reset by device. \n")
            self.session_status = False
        except socket.timeout:
            print("Connection timed out. \n")
            self.session_status = False
    
    def open_shell(self):
        try:
            self.shell = self.connection.invoke_shell()                                                          # function to open shell
            self.shell.settimeout(2)
        except socket.timeout :
            print("Timed out")

    def send_shell(self, command):
        self.shell.send(command + "\n")                                                                         # sending command with a new line character
     
        
    def terminal_out(self) :
        global terminal_output_list
        terminal_output = self.shell.recv(65000).decode()
        terminal_output_list = terminal_output.split(" ")                                                       # a 'list' of words by splitting items at ' '
        print (terminal_output)                                                                                 # print command output
        return terminal_output_list                                                                             # store terminal output as a list for further processing

    def close_connection(self):
        if self.connection != None:
            self.connection.close()

# ==============================================================

# ========== Main Function =====================================
def main():

    print("#" * 80 + "\n")
    ip_address = input("IP Address: ")                                                                          # user inputs
    domain_user_name = input("User Name: ")
    pass_word = getpass.getpass("Password: ")
    print("\n" + "#" * 80)

    pss_connection = SshConnection(ip_address, user_name='BBB', pass_word="")                                   # replace user name with PSS SSH user name

    if (pss_connection.session_status):                                                                         # proceed if ssh connection has been established, 
        pss_connection.open_shell()                                                                             # any exception will set session_status variable set to False
        pss_connection.send_shell(domain_user_name)
        time.sleep(2)
        pss_connection.send_shell(pass_word)

        time.sleep(2)                                                                                           # wait, authentication failure takes time
        pss_connection.terminal_out()                                                                           # processing terminal texts
    
        if 'authentication' in terminal_output_list:                                                            # checking authentication failure
            print(f"Authnetication failed on device {ip_address}. Please check user name & password. \n")
        else:
            pss_connection.send_shell("Y")                                                                      # authentication is successfull
            for commands in cli_commands_sent:                                                                  # send commands one by one
                pss_connection.send_shell(commands)
                time.sleep(1)
                pss_connection.terminal_out()                                                                   # process terminal texts

    else:
        pss_connection.close_connection()                                                                       # close session

# ==============================================================


if __name__ == "__main__":
    main()


