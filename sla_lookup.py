#splunk scripted lookup for downtime, based on splunk's example external_lookup.py
import csv,sys

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

        # Read the result
        result = {}
        i = 0
        while i < len(header):
            if i < len(line):
                result[header[i]] = line[i]
            else:
                result[header[i]] = ''
            i += 1

        # Perform the lookup or reverse lookup if necessary
        if len(result[hostf]) and len(result[ipf]):
            writer.writerow(result)

        elif len(result[hostf]):
            ips = lookup(result[hostf])
            for ip in ips:
                result[ipf] = ip
                writer.writerow(result)

        elif len(result[ipf]):
            result[hostf] = rlookup(result[ipf])
            if len(result[hostf]):
                writer.writerow(result)

main()