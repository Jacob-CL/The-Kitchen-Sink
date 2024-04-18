import argparse
import tks_functions

# Set up argparse
parser = argparse.ArgumentParser(description="--> How to throw a kitchen sink..")

# Define command-line arguments
parser.add_argument("-te", "--test", action="store_true", help="TEST")
parser.add_argument("-ur", "--url", action="store", type=str, metavar="URL", help="Define the URL to work with.")
parser.add_argument("-st", "--static", action="store_true", help="Will conduct a static code source analysis")
parser.add_argument("-bg", "--bannergrab", action="store_true", help="Send normal and  malformed requests to URL to trigger something")
parser.add_argument("-dw", "--directorywalk", action="store_true", help="Will enumerate a domain/URL for extra paths")
parser.add_argument("-dns", "--dnslookup", action="store_true", help="Will attempt to find IP of URL. Uses record types A, NS, MX")
parser.add_argument("-ps", "--portscan", action="store_true", help="Port scan common, well known ports")
parser.add_argument("-ps1024", "--portscan1024", action="store_true", help="Port scans the first 1024 ports")
parser.add_argument("-ip", "--findip", action="store_true", help="Find IP address of URL")
parser.add_argument("-gr", "--grep", action="store", type=str, metavar="DIRECTORY", help="Will grep through files and folders looking for CTF related keywords")
parser.add_argument("-so", "--sources", action="store_true", help="Will search a page for Javascript sources.")

parser.add_argument("-x", "--xss", action="store_true", help="Test URL for interactable inputs")

# Parse the command-line arguments
args = parser.parse_args()

# Check if a URL was provided
if args.url:
    print(tks_functions.banner())
    print(f"--> URL entered: {args.url}")

    if args.static:
        tks_functions.static_analysis(args.url)

    if args.bannergrab:
        tks_functions.banner_grab(args.url)

    if args.directorywalk:
        tks_functions.directorywalk(args.url, 'paths.txt')

    if args.dnslookup:
        tks_functions.dns_lookup(args.url)

    if args.portscan:
        tks_functions.common_port_scan(args.url)
    
    if args.portscan1024:
        tks_functions.port_scan_1024(args.url)
    
    if args.findip:
        tks_functions.get_ip(args.url)
    
    if args.sources:
        tks_functions.find_sources(args.url)

    if args.xss:
        tks_functions.interact_and_check_response(args.url)

if args.grep:
    print(tks_functions.banner())
    tks_functions.grep_files(args.grep, tks_functions.load_patterns())


if not any([args.static, args.directorywalk, args.grep, args.xss, args.test, args.findip, args.sources,
            args.bannergrab,args.dnslookup, args.portscan, args.portscan1024]):
    print("No action specified. Try appending an argument like -ip, -dns, or -g to your command.\n")




