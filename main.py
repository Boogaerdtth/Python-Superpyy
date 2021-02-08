# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
import os
import argparse
import csv
import sys
from rich.console import Console
from datetime import date, timedelta, datetime

today = date.today()
subtract_one_day = timedelta(days=1)
subtract_two_days = timedelta(days=2)
one_week_back_in_time = timedelta(days=7)

yesterday = today - subtract_one_day
day_before_yesterday = today - subtract_two_days
last_week = today - one_week_back_in_time


def get_arguments():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    # BUY PARSER
    buy_parser = subparser.add_parser("buy", help="add products that you bought")
    buy_parser.add_argument(
        "-p", "--product", type=str, help="provide name of the product"
    )
    buy_parser.add_argument(
        "-a", "--amount", type=int, help="how many items dit you bought"
    )
    buy_parser.add_argument(
        "-bpr", "--buy_price", type=float, help="provide bought price per item"
    )
    buy_parser.add_argument("-ex", "--expiration_date", type=str)

    # REPORT PARSER
    report_parser = subparser.add_parser("report", help="report command")
    report_parser.add_argument(
        "subcommand",
        choices=["inventory", "revenue", "profit", "sold", "exdates"],
        help="Choose which report you want to see",
    )
    report_parser.add_argument(
        "time",
        choices=["today", "yesterday", "lastweek"],
        help="if you want to see a report from different days",
    )

    # SELL PARSER
    sell_parser = subparser.add_parser("sell", help="add products that you sold")
    sell_parser.add_argument(
        "-p", "--product", type=str, help="name of the product you sold"
    )
    sell_parser.add_argument("-id", type=int, help="id of the bought product")
    sell_parser.add_argument(
        "-spr", "--sell_price", type=float, help="provide the price of the product"
    )

    args = parser.parse_args()
    return args


# BUY STOCK
def main():
    with open("bought.csv", "a") as f:
        bought_writer = csv.writer(f)
        args = get_arguments()

        id_buy = id(1)
        if args.command == "buy":
            new_arr_for_csvfile = [
                id_buy,
                today,
                args.product,
                args.buy_price,
                args.amount,
                args.expiration_date,
            ]
            bought_writer.writerow(new_arr_for_csvfile)


# GET REPORT
def get_report():
    with open("bought.csv", "r") as f:
        bought_report = csv.reader(f)
        args = get_arguments()

        # GET INVENTORY TODAY
        if (
            args.command == "report"
            and args.subcommand == "inventory"
            and args.time == "today"
        ):
            for line in bought_report:
                print(line)

        # GET INVENTORY YESTERDAY
        if (
            args.command == "report"
            and args.subcommand == "inventory"
            and args.time == "yesterday"
        ):
            next(bought_report)
            display_yesterday = datetime.strftime(yesterday, "%d/%m/%Y")
            for line in bought_report:
                if (datetime.strptime(line[3], "%d/%m/%Y")) < datetime.strptime(
                    display_yesterday, "%d/%m/%Y"
                ):
                    print(line)

        # GET INVENTORY FROM LAST WEEK
        if (
            args.command == "report"
            and args.subcommand == "inventory"
            and args.time == "lastweek"
        ):
            next(bought_report)
            display_last_week = datetime.strftime(last_week, "%d/%m/%Y")
            display_today = datetime.strftime(today, "%d/%m/%Y")

            for line in bought_report:
                if (
                    datetime.strptime(display_last_week, "%d/%m/%Y")
                    < datetime.strptime(line[3], "%d/%m/%Y")
                    < datetime.strptime(display_today, "%d/%m/%Y")
                ):
                    print(line)

        # GET REPORT WITH EXPIRATION DATES
        if (
            args.command == "report"
            and args.subcommand == "exdates"
            and args.time == "today"
        ):
            next(bought_report)
            display_yesterday = datetime.strftime(yesterday, "%d-%m-%Y")
            for line in bought_report:
                if (datetime.strptime(line[5], "%d-%m-%Y")) < datetime.strptime(
                    display_yesterday, "%d-%m-%Y"
                ):
                    print(line)

    with open("sold.csv", "r") as sold_file:
        sold_report = csv.reader(sold_file)

        # GET REPORT WITH SOLD PRODUCTS
        if args.command == "report" and args.subcommand == "sold":
            for line in sold_report:
                print(line)

        # GET REPORT WITH REVENUE
        if args.command == "report" and args.subcommand == "revenue":
            next(sold_report)
            sum_revenue = 0
            for line in sold_report:
                sum_revenue += float(line[2])
            print(sum_revenue)

        # GET REPORT WITH PROFIT
        if args.command == "report" and args.subcommand == "profit":
            next(sold_report)
            sum_profit = 0
            for line in sold_report:
                sum_profit += float(line[4])
            print(sum_profit)


"""
Ik wil dat de winst wordt berekend?
Hoe zorg ik er voor dat de buy price van de bought_edit file wordt gekopieerd naar de sold
"""

# SELL PRODUCTS
def sell_products():
    args = get_arguments()

    with open("bought.csv", "r") as inp, open("bought_edit.csv", "w") as out, open(
        "sold.csv", "a"
    ) as sold:
        writer = csv.writer(out)
        for item in csv.reader(inp):
            if args.command == "sell" and str(args.id) != item[0]:
                writer.writerow(item)
            elif args.command == "sell" and str(args.id == item[0]):
                sold_writer = csv.writer(sold)
                print(item[3])
                profit_product = args.sell_price - float(item[3])
                print(profit_product)

                arr_for_soldfile = [
                    args.id,
                    today,
                    args.product,
                    args.sell_price,
                    profit_product,
                ]
                print(arr_for_soldfile)
                sold_writer.writerow(arr_for_soldfile)
                os.remove("bought.csv")
                os.rename("bought_edit.csv", "bought.csv")


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
