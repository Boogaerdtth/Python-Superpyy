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

# week_range = today - one_week_back_in_time
# print(week_range)
# print(one_week_back_in_time)

# base = datetime.datetime.today()
# date_list = [today - one_week_back_in_time for x in range(1)]
# print(date_list)

# if data < today and > one_week_back_in_time:
# print line

# display_date = datetime.strftime(today, "%Y/%m/%d")
# # print(display_date)

# display_yesterday = datetime.strftime(yesterday, "%Y/%m/%d")

# def display_date(date):
#     return datetime.strftime(date, "%Y-%m-%d")

# print(display_date(today))
# print(type(display_date(today)))

# def display_date_string(date):
#     return datetime.strptime(date, "%Y/%m/%d")

# print(display_date_string("2021/02/05"))


"""
ik wil eigenlijk bij argparse lastweek de volledige week naar voren krijgen, en niet alleen maar
de today - 7 dagen
"""


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
    buy_parser.add_argument("-ex", "--expiration_date", type=str)

    # REPORT PARSER
    report_parser = subparser.add_parser("report", help="report command")
    report_parser.add_argument(
        "subcommand",
        choices=["inventory", "revenue", "profit", "sold"],
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
            bought_writer.writerow(new_arr_for_csvfile)
            # print(display_date(args.expiration_date))


def get_report():
    with open("bought.csv", "r") as f:
        bought_report = csv.reader(f)
        args = get_arguments()
        if (
            args.command == "report"
            and args.subcommand == "inventory"
            and args.time == "today"
        ):
            for line in bought_report:
                print(line)
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

        # HIER BEN IK!!!
        if (
            args.command == "report"
            and args.subcommand == "inventory"
            and args.time == "lastweek"
        ):
            next(bought_report)
            display_last_week = datetime.strftime(last_week, "%d/%m/%Y")
            display_today = datetime.strftime(today, "%d/%m/%Y")
            print(display_last_week)
            print(display_today)

            for line in bought_report:
                print(datetime.strptime(line[3], "%d/%m/%Y"))
    # dit lukt bijna!! alleen onderstaande code nog even converteren naar waardes waarmee ie wel kan rekenen
    # maandag weer een dag
    #     if (datetime.strptime(line[3], "%d/%m/%Y")) > display_last_week and (
    #         datetime.strptime(line[3], "%d/%m/%Y")
    #     ) < display_today:
    #         print(line)
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
                # total_revenue = [sum_revenue]
                # print(total_revenue)
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
            elif args.command == "sell" and str(args.id == item[0]):
                sold_writer = csv.writer(sold)

                arr_for_soldfile = [
                    args.id,
                    args.product,
                    args.sell_price,
                    args.sell_date,
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
