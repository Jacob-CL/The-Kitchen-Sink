import argparse
import tks_functions
import tks_functions

# Set up argparse
parser = argparse.ArgumentParser(description="--> How to throw a kitchen sink..")

# Define command-line arguments
parser.add_argument("-u", "--url", action="store", type=str, metavar="URL", help="Define the URL to analyze.")
parser.add_argument("-g", "--grep", action="store", type=str, metavar="DIRECTORY", help="Will grep through files and folders looking for CTF vulnerabilities")
parser.add_argument("-s", "--static", action="store_true", help="Will do a static analysis on a URL's page source - scans for HTML comments, HTML inputs, JavaScript tags, and evidence of databases or frontend filtering.")
parser.add_argument("-r", "--root", action="store_true", help="Will do an root domain analysis - looks for common URL paths and returns response codes")

# Parse the command-line arguments
args = parser.parse_args()

# Check if a URL was provided
if args.url:
    print(tks_functions.banner())
    print(f"--> URL entered: {args.url}")

    # If the --static flag is used, conduct static analysis on the URL
    if args.static:
        print(f"\n--> Starting static analysis..")
        tks_functions.search_for_HTML_inputs(args.url)
        tks_functions.search_for_HTML_comments(args.url)
        tks_functions.search_for_javascript_tags(args.url)
        tks_functions.search_for_frontend_filtering(args.url)
        tks_functions.search_for_databases(args.url)
        print("\nFinished throwing the kitchen sink ✓✓\n")

    # If the --root flag is used, conduct room domain analysis on the URL
    if args.root:
        print(f"\n--> Starting root domain analysis..")
        tks_functions.enumerate_root_domain(args.url, 'paths.txt')

if args.grep:
    print(f"\n--> CTF Grepping..\n")
    tks_functions.grep_files(args.grep, tks_functions.load_patterns())

if not any([args.static, args.root, args.grep]):
    print("No action specified. Try appending an argument like -s, -r, or -g to your command.\n")


    

