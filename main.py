# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.

# Imports
import argparse
import csv
from datetime import date
import sys
from rich.console import Console


def get_arguments():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    # BUY PARSER
    buy_parser = subparser.add_parser("buy", help="add products that you bought")
    buy_parser.add_argument(
        "-p", "--product", type=str, help="provide name of the product"
    )
    buy_parser.add_argument("-bd", "--buy_date", help="When did you buy it?")
    buy_parser.add_argument(
        "-a", "--amount", type=int, help="how many items dit you bought"
    )
    buy_parser.add_argument(
        "-pr", "--price", type=float, help="provide bought price per item"
    )
    buy_parser.add_argument(
        "-bp",
        "--buy_price",
        type=float,
        help="what was the price that you bought it for",
    )
    buy_parser.add_argument("-ex", "--expiration_date")

    # REPORT PARSER
    report_parser = subparser.add_parser("report", help="report command")
    report_parser.add_argument(
        "subcommand",
        choices=["inventory", "revenue", "profit", "sold"],
        help="Choose which report you want to see",
    )

    # SELL PARSER
    sell_parser = subparser.add_parser("sell", help="add products that you sold")
    sell_parser.add_argument(
        "-p", "--product", type=str, help="name of the product you sold"
    )
    sell_parser.add_argument("-id", type=int, help="id of the bought product")
    sell_parser.add_argument(
        "-pr", "--sell_price", type=float, help="provide the price of the product"
    )
    sell_parser.add_argument(
        "-d", "--sell_date", help="provide the sell date of the product"
    )

    args = parser.parse_args()
    return args


def main():
    with open("bought.csv", "a") as f:
        bought_writer = csv.writer(f)
        args = get_arguments()

        id_buy = id(1)
        if args.command == "buy":
            new_arr_for_csvfile = [
                id_buy,
                args.product,
                args.price,
                args.buy_date,
                args.amount,
                args.expiration_date,
            ]
            print(new_arr_for_csvfile)
            bought_writer.writerow(new_arr_for_csvfile)


def get_report():
    with open("bought.csv", "r") as bought_file:
        bought_report = csv.reader(bought_file)
        args = get_arguments()
        if args.command == "report" and args.subcommand == "inventory":
            for line in bought_report:
                print(line)
    with open("sold.csv", "r") as sold_file:
        sold_report = csv.reader(sold_file)
        if args.command == "report" and args.subcommand == "sold":
            for line in sold_report:
                print(line)


def sell_products():
    with open("bought.csv", "w") as bought_file:
        bought_file_writer = csv.writer(bought_file)
        with open("sold.csv", "a") as sold_file:
            sold_file_writer = csv.writer(sold_file)

            args = get_arguments()
            for line in bought_file_writer:
                if args.command == "sell" and args.id == args.id_buy:
                    line = " "
            if args.command == "sell":
                new_arr_for_sold_csvfile = [
                    args.id,
                    args.product,
                    args.sell_price,
                    args.sell_date,
                ]
                print(new_arr_for_sold_csvfile)
                # sold_file_writer.writerow(new_arr_for_sold_csvfile)


# als ik args sell gebruik, moet het product met de desbetreffende id gewist worden in de bought file
# entoe worden gevoegd aan de sold file

if __name__ == "__main__":
    main()
    get_arguments()
    get_report()
    sell_products()

    args = get_arguments()

    myconsole = Console()
    myconsole.print("*" * 30)
    myconsole.print("# Arguments", args)
    myconsole.print("*" * 30)
