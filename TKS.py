import argparse
import tks_functions
import infog_functions

# Set up argparse
parser = argparse.ArgumentParser(description="--> How to throw a kitchen sink..")

# Define command-line arguments
parser.add_argument("-u", "--url", action="store", type=str, metavar="URL", help="Define the URL to work with.")
parser.add_argument("-g", "--grep", action="store", type=str, metavar="DIRECTORY", help="Will grep through files and folders looking for CTF related keywords")
parser.add_argument("-s", "--static", action="store_true", help="Will conduct a static code source analysis")
parser.add_argument("-e", "--enumerate", action="store_true", help="Will enumerate a domain/URL")
parser.add_argument("-x", "--xss", action="store_true", help="Test URL for interactable inputs")
parser.add_argument("-f", "--fingerprint", action="store_true", help="Determine the version and type of a running web server to enable further discovery of any known vulnerabilities.")

# Parse the command-line arguments
args = parser.parse_args()

# Check if a URL was provided
if args.url:
    print(tks_functions.banner())
    print(f"--> URL entered: {args.url}")

    # If the --static flag is used, conduct static analysis on the URL
    if args.static:
        print(f"\n--> Starting static source code analysis..")
        tks_functions.static_analysis(args.url)
        print("\nFinished throwing the kitchen sink ✓✓\n")

    if args.xss:
        print(f"--> Counting number of interactable inputs in URL..")
        tks_functions.interact_and_check_response(args.url)

    # If the --root flag is used, conduct room domain analysis on the URL
    if args.enumerate:
        print(f"\n--> Starting root domain enumeration..")
        tks_functions.enumerate_root_domain(args.url, 'paths.txt')

    if args.fingerprint:
        print("\n--> Fingerprinting WebServer..")
        infog_functions.banner_grab(args.url)

if args.grep:
    print(tks_functions.banner())
    print(f"--> CTF Grepping..\n")
    tks_functions.grep_files(args.grep, tks_functions.load_patterns())




if not any([args.static, args.enumerate, args.grep, args.xss, args.fingerprint]):
    print("No action specified. Try appending an argument like -s, -r, -xss or -g to your command.\n")




