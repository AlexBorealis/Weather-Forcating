import argparse

parser = argparse.ArgumentParser(description="Download data")
parser.add_argument(
    "--start_year", type=str, default="2025", help="Start year (default: 2025)"
)
parser.add_argument(
    "--end_year", type=str, default="2025", help="End year (default: 2025)"
)
parser.add_argument(
    "--start_month", type=str, default="1", help="Start month (default: 1)"
)
parser.add_argument("--end_month", type=str, default=12, help="End month (default: 12)")
parser.add_argument(
    "--north", type=str, default="40", help="North Latitude (default: 40)"
)
parser.add_argument(
    "--south", type=str, default="20", help="South Latitude (default: 20)"
)
parser.add_argument(
    "--east", type=str, default="-20", help="East Longitude (default: -20)"
)
parser.add_argument(
    "--west", type=str, default="20", help="West Longitude (default: 20)"
)
parse_args = parser.parse_args()
