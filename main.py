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
display_today = datetime.strftime(today, "%d-%m-%Y")
subtract_one_day = timedelta(days=1)
subtract_two_days = timedelta(days=2)
one_week_back_in_time = timedelta(days=7)

yesterday = today - subtract_one_day
display_yesterday = datetime.strftime(yesterday, "%d-%m-%Y")
day_before_yesterday = today - subtract_two_days
last_week = today - one_week_back_in_time


def main():
    args = get_arguments()
    if args.command == "report":
        get_report()
    elif args.command == "buy":
        buy_product()
    elif args.command == "sell":
        sell_product()


def get_arguments():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    # BUY PARSER
    buy_parser = subparser.add_parser("buy", help="add products that you bought")
    buy_parser.add_argument(
        "-p", "--product", type=str.lower, help="provide name of the product"
    )
    buy_parser.add_argument(
        "-a", "--amount", type=int, help="how many items did you bought"
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
        choices=["today", "yesterday", "lastweek", "date"],
        help="if you want to see a report from different days",
    )
    report_parser.add_argument("-d", "--date", type=str, help="provide date for report")
    report_parser.add_argument(
        "-f", "--file", type=str, help="export report to new file"
    )

    # SELL PARSER
    sell_parser = subparser.add_parser("sell", help="add products that you sold")
    sell_parser.add_argument(
        "-p", "--product", type=str.lower, help="name of the product you sold"
    )
    sell_parser.add_argument("-a", "--amount", type=int, help="amount of product")
    sell_parser.add_argument(
        "-spr", "--sell_price", type=float, help="provide the price of the product"
    )

    args = parser.parse_args()
    return args


# BUY STOCK
def buy_product():
    with open("bought.csv", "r") as inp, open("bought_edit.csv", "a") as out:
        reader = csv.reader(inp)
        writer = csv.writer(out)
        args = get_arguments()
        id_buy = id(1)

        isAdded = False
        for line in reader:
            if args.product == line[2]:
                new_amount = int(args.amount) + int(line[4])
                new_amount_arr_for_csvfile = [
                    id_buy,
                    display_today,
                    args.product,
                    args.buy_price,
                    new_amount,
                    args.expiration_date,
                ]
                isAdded = True
                writer.writerow(new_amount_arr_for_csvfile)
                try:
                    os.rename("bought_edit.csv", "bought.csv")
                except:
                    None

            else:
                writer.writerow(line)
                try:
                    os.rename("bought_edit.csv", "bought.csv")
                except:
                    None

        if not isAdded:
            new_arr_for_csvfile = [
                id_buy,
                display_today,
                args.product,
                args.buy_price,
                args.amount,
                args.expiration_date,
            ]
            writer.writerow(new_arr_for_csvfile)
            try:
                os.rename("bought_edit.csv", "bought.csv")
            except:
                None


# SELL PRODUCTS
def sell_product():
    with open("bought.csv", "r") as inp, open("bought_edit.csv", "w") as out, open(
        "sold.csv", "a"
    ) as sold:
        reader = csv.reader(inp)
        writer = csv.writer(out)
        sold_writer = csv.writer(sold)
        args = get_arguments()
        isAdded = False

        for line in reader:
            id_buy = line[0]

            if args.product == line[2]:
                print(args.amount)
                if int(line[4]) >= args.amount:
                    new_amount = int(line[4]) - int(args.amount)
                    profit_product = (args.sell_price - float(line[3])) * int(
                        args.amount
                    )

                    new_amount_arr_for_csvfile = [
                        line[0],
                        line[1],
                        line[2],
                        line[3],
                        new_amount,
                        line[5],
                    ]
                    isAdded = True

                    if new_amount == 0:
                        None
                    else:
                        writer.writerow(new_amount_arr_for_csvfile)

                    arr_for_soldfile = [
                        id_buy,
                        display_today,
                        args.product,
                        args.amount,
                        args.sell_price,
                        profit_product,
                    ]
                    sold_writer.writerow(arr_for_soldfile)
                    try:
                        os.rename("bought_edit.csv", "bought.csv")
                    except:
                        None
                else:
                    print("Amount is more than we have in stock")
            elif args.product != line[2]:
                writer.writerow(line)

        if not isAdded:
            writer.writerow(line)
            try:
                os.rename("bought_edit.csv", "bought.csv")
            except:
                None


# GET REPORT
def get_report():
    with open("bought.csv", "r") as f, open("report.csv", "w") as file_writer:
        bought_report = csv.reader(f)
        new_csv_file = csv.writer(file_writer)
        args = get_arguments()

        # GET INVENTORY TODAY
        if args.subcommand == "inventory" and args.time == "today":
            for line in bought_report:
                if args.file == "true":
                    new_csv_file.writerow(line)
                else:
                    print(line)

        # GET INVENTORY YESTERDAY
        if args.subcommand == "inventory" and args.time == "yesterday":
            next(bought_report)
            for line in bought_report:
                if (datetime.strptime(line[1], "%d-%m-%Y")) < datetime.strptime(
                    display_yesterday, "%d-%m-%Y"
                ):
                    if args.file == "true":
                        new_csv_file.writerow(line)
                    else:
                        print(line)

        # GET INVENTORY FROM LAST WEEK
        if args.subcommand == "inventory" and args.time == "lastweek":
            next(bought_report)
            display_last_week = datetime.strftime(last_week, "%d-%m-%Y")

            for line in bought_report:
                if (
                    datetime.strptime(display_last_week, "%d-%m-%Y")
                    < datetime.strptime(line[1], "%d-%m-%Y")
                    < datetime.strptime(display_today, "%d-%m-%Y")
                ):
                    if args.file == "true":
                        new_csv_file.writerow(line)
                    else:
                        print(line)

        # GET INVENTORY ON SPECIFIC DATES
        if args.subcommand == "inventory" and args.time == "date":
            next(bought_report)
            display_date = datetime.strptime(args.date, "%d-%m-%Y")

            for line in bought_report:
                if (datetime.strptime(line[1], "%d-%m-%Y")) < display_date:
                    if args.file == "true":
                        new_csv_file.writerow(line)
                    else:
                        print(line)

        # GET REPORT WITH EXPIRATION DATES
        if args.subcommand == "exdates" and args.time == "today":
            next(bought_report)
            for line in bought_report:
                if (datetime.strptime(line[5], "%d-%m-%Y")) < datetime.strptime(
                    display_yesterday, "%d-%m-%Y"
                ):
                    if args.file == "true":
                        new_csv_file.writerow(line)
                    else:
                        print(line)

    with open("sold.csv", "r") as sold_file:
        sold_report = csv.reader(sold_file)

        # GET REPORT WITH SOLD PRODUCTS
        if args.subcommand == "sold":
            for line in sold_report:
                if args.file == "true":
                    new_csv_file.writerow(line)
                else:
                    print(line)

        # GET REPORT WITH REVENUE
        if args.subcommand == "revenue":
            next(sold_report)
            sum_revenue = 0
            for line in sold_report:
                sum_revenue += float(line[2])
            print(sum_revenue)

        # GET REPORT WITH PROFIT
        if args.subcommand == "profit":
            next(sold_report)
            sum_profit = 0
            for line in sold_report:
                sum_profit += float(line[4])
            print(sum_profit)


if __name__ == "__main__":
    main()

    args = get_arguments()
    myconsole = Console()
    myconsole.print("*" * 30)
    myconsole.print("# Arguments", args)
    myconsole.print("*" * 30)
