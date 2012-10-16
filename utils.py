__all__ = [
	'get_monitis_options', 
	'get_sla_options',
	'get_xlist',
	'get_maintenance_windows',
	'split_interval',
	'bound_interval',
	'is_in_xlist',
	'get_appcode',
	'teamcity_message',
	'teamcity_error',
	'teamcity_warning',
	'TeamcityBlock',
]

from optparse import OptionParser
from datetime import datetime
import re

def get_sla_options():
	parser = OptionParser()
	parser.add_option("-u", "--username", dest="username", help="authenticate with username")
	parser.add_option("-p", "--password", dest="password", help="authenticate with password")
	parser.add_option("-m", "--maintenance-window-filename", dest="maintenance_window_filename", help="file containing maintentance windows", default="maintenance_windows.txt")
	parser.add_option("-e", "--end", dest="end", help="end datetime")
	parser.add_option("-s", "--start", dest="start", help="start datetime")
	(options, args) = parser.parse_args()
	return options
	
def get_monitis_options():
	parser = OptionParser()
	parser.add_option("-u", "--username", dest="username", help="authenticate with username")
	parser.add_option("-p", "--password", dest="password", help="authenticate with password")
	parser.add_option("-a", "--monitis-api-key", dest="apikey", help="monitis api key", default="")
	parser.add_option("-s", "--monitis-secret-key", dest="secretkey", help="monitis secret key", default="")
	parser.add_option("-e", "--execute", dest="execute", action="store_true", help="execute monitis operations", default=False)
	(options, args) = parser.parse_args()
	return options
	
def get_file_contents(file_name, columns=3):
	with open(file_name) as f:
		return [line.split()[0:columns] for line in f]

def get_datetime(date, time):
	return datetime.strptime("{0} {1}".format(date, time), "%m/%d/%Y %H:%M:%S")
		
def get_maintenance_windows(file_name):
	contents = filter(lambda line: len(line) > 0 and not line[0].startswith("#"), get_file_contents(file_name, columns=4))
	windows = [[get_datetime(start_date, start_time), get_datetime(end_date, end_time)] for start_date, start_time, end_date, end_time in contents]
	
	for window in windows:
		if window[0] >= window[1]:
			raise ValueError("Start {0} is greater than or equal to end {1}".format(window[0], window[1]))
	return windows

def split_interval(interval, maintenance_window):
	if interval[0] > maintenance_window[1] or interval[1] < maintenance_window[0]:
		return [interval]
	if interval[1] <= maintenance_window[1] and interval[0] >= maintenance_window[0]:		
		return []
	result = []
	if interval[0] < maintenance_window[0]:
		result.append([interval[0], maintenance_window[0]])
	if  interval[1] > maintenance_window[1]:
		result.append([maintenance_window[1], interval[1]])
	return result
	
def bound_interval(interval, boundary):
	return [max(interval[0], boundary[0]), min(interval[1], boundary[1])]

def get_xlist(file_name):
	contents = filter(lambda line: len(line) > 0 and not line[0].startswith("#"), get_file_contents(file_name))
	for line in contents:		
		if len(line) == 0:
			continue
		if len(line) == 1:
			line.insert(0, "*")
		if len(line) == 2:
			line.append("*")		
	return contents	

def is_in_xlist(row, xlist):
	first_three = row[0:3]
	return any(map(lambda xrow: is_in_xrow(first_three, xrow), xlist))
	
def is_in_xrow(row, xrow):
	patterns = map(lambda pair: pair[0].format(re.escape(pair[1]).replace("\*", ".*")), zip(("^{0}$", "^{0}", "^{0}$"), xrow))	
	return all(map(lambda pair: re.search(pair[0], pair[1], flags=re.IGNORECASE), zip(patterns, row)))
	
def get_app_code(app_instance):
	code = app_instance[0:4]
	if code.lower() == "iden":
		code = "IDM"
	return code.upper()
	
def teamcity_message(message, status='NORMAL'):
	print "##teamcity[message text='{0}' status='{1}']".format(message, status)
	
def teamcity_error(message):
	teamcity_message(message, 'ERROR')

def teamcity_warning(message):
	teamcity_message(message, 'WARNING')
	
class TeamcityBlock:
	
	def __init__(self, name):
		self.name = name
	
	def __enter__(self):
		print "##teamcity[blockOpened name='{0}']".format(self.name)
	
	def __exit__(self, type, value, traceback):
		print "##teamcity[blockClosed name='{0}']".format(self.name)