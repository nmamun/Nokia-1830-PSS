# Nokia-1830-PSS
This repository contains Python scripts for 1830 PSS Optical nodes from Nokia.

Tools & library used - Python 3.10.4, Paramiko 2.11.0.
  

Description of different scripts as summary - 

1. basic (pss_login_basic_ne.py)- connects to single 1830PSS Node using Paramiko, execute few commands and display terminal output.
2. basic with exceptions (pss_login_class_exception.py) - uses class, handles exceptions, connects to single 1830 PSS Node, execute few commands and display terminal output.
3. multiple node, log files (pss_login_multiple_log.py) - read list of nodes, connect, execute multiple commands, displays status of execution, writes output to log file
