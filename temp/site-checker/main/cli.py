import argparse

def read_cli_args():
    parser = argparse.ArgumentParser(prog="site_checker", description="check the availability of websites")
    
    parser.add_argument(
        "-u",
        "--urls",
        metavar="URLs",
        nargs="+",
        type=str,
        default=[],
        help="enter one or more website URLs",
    )

    parser.add_argument(
        "-f",
        "--input-file",
        metavar="FILE",
        type=str,
        default="",
        help="read URLs from a file",
    )

    parser.add_argument(
        "-a",
        "--asynchronous",
        action="store_true",
        help="run the connectivity check asynchronously",
    )

    return parser.parse_args()

def display_check_result(result, url, error=""):
    """Display the result of a connectivity check."""
    print(f"The status of {url} is: ", end=" ")
    if result:
        print("Online")
    else:
        print(f"Offline \n Error: {error}")