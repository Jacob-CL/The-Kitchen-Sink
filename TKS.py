import argparse
import tks_functions
import tks_functions

def perform_static_analysis(url):
    print(f"\n--> Starting static analysis..")
    tks_functions.search_for_HTML_inputs(url)
    tks_functions.search_for_HTML_comments(url)
    tks_functions.search_for_javascript_tags(url)
    tks_functions.search_for_frontend_filtering(url)
    tks_functions.search_for_databases(url)
    print("\nFinished throwing the kitchen sink ✓✓\n")

def perform_root_domain_analysis(url):
    print(f"\n--> Starting root domain analysis..")
    tks_functions.enumerate_root_domain(url, 'paths.txt')

def perform_grep(directory):
    print(f"\n--> CTF Grepping..\n")
    search_patterns = tks_functions.load_patterns()
    tks_functions.grep_files(directory, search_patterns)

def main():
    parser = argparse.ArgumentParser(description="--> How to throw a kitchen sink..")
    parser.add_argument("-u", "--url", type=str, metavar="URL", help="Define the URL to analyze.")
    parser.add_argument("-g", "--grep", type=str, metavar="DIRECTORY", help="Will grep through files and folders looking for CTF vulnerabilities")
    parser.add_argument("-s", "--static", action="store_true", help="Will do a static analysis on a URL's page source.")
    parser.add_argument("-r", "--root", action="store_true", help="Will do an root domain analysis.")

    args = parser.parse_args()

    if args.url:
        print(tks_functions.banner())
        print(f"--> URL entered: {args.url}")
        if args.static:
            perform_static_analysis(args.url)
        if args.root:
            perform_root_domain_analysis(args.url)

    if args.grep:
        perform_grep(args.grep)

    if not any([args.static, args.root, args.grep]):
        print("No action specified. Try appending an argument like -s, -r, or -g to your command.\n")

if __name__ == "__main__":
    main()
