# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.

# Imports
import argparse
import csv
from datetime import date
import sys


def get_arguments():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    buy_parser = subparser.add_parser("buy", help="add products that you bought")
    buy_parser.add_argument(
        "-p", "--product", type=str, help="provide name of the product"
    )
    buy_parser.add_argument(
        "-a", "--amount", type=int, help="how many items dit you bought"
    )
    buy_parser.add_argument(
        "-pr", "--price", type=float, help="provide bought price per item"
    )
    buy_parser.add_argument("-ex", "--expiration_date")

    sell_parser = subparser.add_parser("sell", help="add products that you sold")
    sell_parser.add_argument(
        "-p", "--product", type=str, help="name of the product you sold"
    )
    sell_parser.add_argument("-a", "--amount", type=int, help="number of products sold")
    sell_parser.add_argument(
        "-pr", "--price", type=float, help="provide the price of the product"
    )

    args = parser.parse_args()
    return args


def main():
    with open("bought.csv", "a") as f:
        bought_writer = csv.writer(f)
        args = get_arguments()
        new_arr_for_csvfile = [
            args.product,
            args.price,
            args.amount,
            args.expiration_date,
        ]
        print(new_arr_for_csvfile)
        bought_writer.writerow(new_arr_for_csvfile)


# array uitbreiden

# with open('sold.csv', 'w') as sold_file:
# sold_writer = csv.writer(sold_file)#, delimiter= '\t'

if __name__ == "__main__":
    main()
    get_arguments()
