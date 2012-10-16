import csv,sys

def main():
    if len(sys.argv) != 4:
        print "Usage: python sla_lookup.py [event time field] [monitor name field] [is during maintenance field]"
        sys.exit(0)

main()