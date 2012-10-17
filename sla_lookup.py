#splunk scripted lookup for downtime, based on splunk's example external_lookup.py
import csv,sys
from utils import get_maintenance_windows, is_in_xrow
from datetime import datetime


def lookup(test_name, time, windows):	
	return any(map(lambda window: xrow_matches(test_name, window[0]) and window[1] <= datetime.fromtimestamp(time) <= window[2], windows))

"""javelin.staging.zsservices.com/javelindemo03/0002dev/app/web/isalive_https"""
def xrow_matches(test_name, xrow):
	parts = test_name.split("/")[0:3]
	if len(parts) != 3:
		return False
	return is_in_xrow(["Stg" if is_staging(parts[0]) else "Prod", parts[2], parts[1]], xrow)

def is_staging(host_name):
	return host_name.lower().find("staging") != -1

def main(windows):
    if len(sys.argv) != 4:
        print "Usage: python sla_lookup.py [event time field] [monitor name field] [is during maintenance field]"
        sys.exit(0)

    time_field, name_field, downtime_field = sys.argv[1:4]
    reader = csv.reader(sys.stdin)
    writer = None

    header = []
    first = True

    for line in reader:
        if first:
            header = line
            if time_field not in header or name_field not in header or downtime_field not in header:
                print "event time, monitor name, and during maintenance flag need to be columns in the csv"
                sys.exit(0)
            csv.writer(sys.stdout).writerow(header)
            writer = csv.DictWriter(sys.stdout, header)
            first = False
            continue

        line.extend([''] * max(len(header) - len(line), 0))
       	result = { header[i] : line[i] for i in range(len(line)) }
        
        # Perform the lookup or reverse lookup if necessary
        if len(result[downtime_field]):
            writer.writerow(result)

        else:
        	result[downtime_field] = lookup(result[name_field], int(result[time_field]), windows)
        	writer.writerow(result)

if __name__ == '__main__':
	windows = get_maintenance_windows("maintenance_windows.txt")
	main(windows)