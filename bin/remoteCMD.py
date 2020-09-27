#!/usr/bin/python3.7


# remoteCMD.py : easy-to-use tool for system automation
# Version: 1.0
# License: GNU GPLv2

 
# Importing required modules.

from fabric import Connection
import argparse
import os
import sys


# Creating argument parser's variables.

parser = argparse.ArgumentParser(
						prog='remoteCMD.py',
						usage='remoteCMD.py [options]',
						description='Execute command(s) specified in config files on remote host(s).',
						epilog='License: GNU GPLv2',
						add_help=True
						)
							
							
							
parser.add_argument('-u',
					action='store_true',
					help='perform package updates on hosts',
					required=False
					)
						
						
	
parser.add_argument('-a',
					action='store_true',
					help='install AMP stack(Apache MariaDB Php)',
					required=False
					)
						
						
parser.add_argument('-p',
					action='store_true',
					help='install APP stack(Apache PostgreSQL Php)',
					required=False
					)
					
parser.add_argument('-f',
					help='User specified command file',
					required=False
					)
						

						
# Creating path variables and initializing parser's.
						
args = parser.parse_args()
home_path = os.path.expanduser('~')
host_file = f'{home_path}/remoteCMD.py/config/host.cfg'
config_file = f'{home_path}/remoteCMD.py/config/config.cfg'



# Creating program's main function.

def main_func(upDate = args.u, amp = args.a, app = args.p, fil = args.f):
	
	
	
	# Creating function which will execute command(s) via SSH specified in 
	# command_file variable on every host(s) according to host_file variable.
	# From every line in command(s) and host(s) files a newline character is removed
	# to ensure proper parsing. 
	
	def cmd_exec(command_file,host_file):
		
		
		with open(host_file, 'r') as host_file:
			with open(command_file, 'r') as command_file:
				command_file = command_file.readlines()
				for host in host_file:
					host = host.strip('\n')
					for command in command_file:
						command = command.strip('\n')
						print(80 * '-')
						print('Performing command'.center(80))
						print(f'{command} on host:'.center(80))
						print(f'{host}'.center(80))
						print(80 * '-')
						print('')
						try:
							c = Connection(host)
							cmd = c.run(command)
						except:
							print('An error occurred, performing the next command.')
							continue
				
	
	# Creating function which will choose proper file with commands to 
	# execute on remote host(s)	according to flag used by the user.
	
	def path_parser(config_file):
		
	
		with open(config_file,'r') as config_file:
			for line in config_file:
				if upDate:
					if 'Update' in line:
						command_file = line.strip('Update').strip()
				if amp:
					if 'AMP' in line:
						command_file = line.strip('AMP').strip()
				if app:
					if 'APP' in line:
						command_file = line.strip('APP').strip()
				if fil:
					command_file = fil
			
			
			return command_file 
				
						
			
	# Executing function responsible for performing commands(s) 
	# on remote hosts(s).
			
	cmd_exec(path_parser(config_file),host_file)
			

# If program is used without proper flag then an error message is displayed.

if len(sys.argv) == 1:
	print('Positional argument required, use -h option to view help message.')
else:
	main_func(upDate = args.u, amp = args.a, app = args.p, fil = args.f)	
