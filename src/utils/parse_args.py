import argparse

parser = argparse.ArgumentParser(description="Download data")
parser.add_argument("--start_year", type=str, default="2025")
parser.add_argument("--end_year", type=str, default="2025")
parser.add_argument("--start_month", type=str, default="1")
parser.add_argument("--end_month", type=int, default=12)
parser.add_argument("--start_day", type=str, default="1")
parser.add_argument("--end_day", type=int, default=31)

# Опциональные границы области
parser.add_argument("--north", type=float, default=None)
parser.add_argument("--south", type=float, default=None)
parser.add_argument("--east", type=float, default=None)
parser.add_argument("--west", type=float, default=None)
parse_args = parser.parse_args()
