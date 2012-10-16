#splunk scripted lookup for downtime, based on splunk's example external_lookup.py
import csv,sys

def lookup():
	return True

def main():
    if len(sys.argv) != 4:
        print "Usage: python sla_lookup.py [event time field] [monitor name field] [is during maintenance field]"
        sys.exit(0)

    time_field = sys.argv[1]
    name_field = sys.argv[2]
    downtime_field = sys.argv[3]

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
        	result[downtime_field] = lookup()
        	writer.writerow(result)

if __name__ == '__main__':
	main()