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
parser.add_argument("-t", "--test", action="store_true", help="TEST")
parser.add_argument("-tks","--throw", action="store_true", help="Throw the god dam kitchen sink at a URL")

# Parse the command-line arguments
args = parser.parse_args()

# Create the HTML file and keep the file handle
file = infog_functions.make_file()

# Check if a URL was provided
if args.url:
    print(tks_functions.banner())
    print(f"--> URL entered: {args.url}")

    if args.static:
        print(f"\n--> Starting static source code analysis..")
        tks_functions.static_analysis(args.url)
        print("\nFinished throwing the kitchen sink ✓✓\n")

    if args.xss:
        print(f"--> Counting number of interactable inputs in URL..")
        tks_functions.interact_and_check_response(args.url)

    if args.enumerate:
        print(f"\n--> Starting root domain enumeration..")
        tks_functions.enumerate_root_domain(args.url, 'paths.txt')

    if args.fingerprint:
        infog_functions.make_file()
        infog_functions.banner_grab(args.url)
        infog_functions.close_file()
        print(f"\n--> InformationGathering.html created.")

    if args.throw:
        print(f"--> Throwing the kitchen sink at {args.url}")
        infog_functions.make_file()
        infog_functions.banner_grab(args.url)
        infog_functions.close_file()
        print(f"✓✓ Kitchen sink thrown at {args.url}")

    if args.test:
        print(f"\n--> Test argument..")
        infog_functions.make_file()
        infog_functions.testfunction(args.url)
        infog_functions.close_file()
    



if args.grep:
    print(tks_functions.banner())
    print(f"--> CTF Grepping..\n")
    tks_functions.grep_files(args.grep, tks_functions.load_patterns())


if not any([args.static, args.enumerate, args.grep, args.xss, args.fingerprint, args.test, args.throw]):
    print("No action specified. Try appending an argument like -s, -r, -xss or -g to your command.\n")




