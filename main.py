# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.

# Imports
import os
import argparse
import csv
from datetime import date
import sys
from rich.console import Console
import time


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
        # print(f[2])
        # id = 0
        if args.command == "buy":
            # id = id + 1
            new_arr_for_csvfile = [
                id_buy,
                args.product,
                args.price,
                args.buy_date,
                args.amount,
                args.expiration_date,
            ]
            # print(new_arr_for_csvfile)
            bought_writer.writerow(new_arr_for_csvfile)


def get_report():
    with open("bought.csv", "r") as f:
        bought_report = csv.reader(f)
        args = get_arguments()
        if args.command == "report" and args.subcommand == "inventory":
            for line in bought_report:
                print(line)
    with open("sold.csv", "r") as sold_file:
        sold_report = csv.reader(sold_file)
        if args.command == "report" and args.subcommand == "sold":
            for line in sold_report:
                print(line)
        if args.command == "report" and args.subcommand == "revenue":
            next(sold_report)
            sum_revenue = 0
            for line in sold_report:
                sum_revenue += float(line[2])
                print(sum_revenue)


def sell_products():
    args = get_arguments()

    with open("bought.csv", "r") as inp, open("bought_edit.csv", "w") as out, open(
        "sold.csv", "a"
    ) as sold:
        writer = csv.writer(out)
        for item in csv.reader(inp):
            if args.command == "sell" and str(args.id) != item[0]:
                writer.writerow(item)
                # os.rename("bought_edit.csv", "bought.csv")
        sold_writer = csv.writer(sold)
        for item in csv.reader(inp):
            if args.command == "sell" and str(args.id) == item[0]:
                arr_for_soldfile = [
                    args.id,
                    args.product,
                    args.sell_price,
                    args.sell_date,
                ]
                print(arr_for_soldfile)
                sold_writer.writerow(arr_for_soldfile)
        # os.rename("bought_edit.csv", "bought.csv")


# graag wil ik feedback over wa er fout gaat bij sell_products(). en dan geen hints geven over
# wat ik zou moeten doen, maar gewoon zeggen wat ik moet coderen. ik weet het niet meer,
# en ik heb al genoeg vragen gestedl in slack

# als bovenstaande functie uitgevoerd wordt, wordt de bought_edit file overgeschreven.
# wat niet werkt, is dat het oude bought bestand niet wordt bijgewerkt.
# en het bijwerken van de sold file doet t ook niet meer


# def sell_products():
#     args = get_arguments()

#     with open("bought.csv", "r") as inp, open("bought_edit.csv", "w") as out:
#         writer = csv.writer(out)
#         for item in csv.reader(inp):
#             if args.command == "sell" and str(args.id) != item[0]:
#                 writer.writerow(item)
#                 os.rename("bought_edit.csv", "bought.csv")
#                 with open("sold.csv", "a") as sold:
#                     sold_file_writer = csv.writer(sold)
#                     for item in csv.reader(inp):
#                         if args.command == "sell" and str(args.id) == item[0]:
#                             new_arr_for_sold_csvfile = [
#                                 args.id,
#                                 args.product,
#                                 args.sell_price,
#                                 args.sell_date,
#                             ]
#                             # print(new_arr_for_sold_csvfile)
#                             sold_file_writer.writerow(new_arr_for_sold_csvfile)


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
