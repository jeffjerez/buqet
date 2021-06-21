from argparse import ArgumentParser
from datetime import date
from calendar import Calendar
from csv import reader

class color:
       HEADER = '\033[95m'
       OKBLUE = '\033[94m'
       OKCYAN = '\033[96m'
       OKGREEN = '\033[92m'
       OKGREENBG = '\033[1;92m'
       WARNING = '\033[93m'
       FAIL = '\033[91m'
       ENDC = '\033[0m'
       BOLD = '\033[1m'
       UNDERLINE = '\033[4m'

parser = ArgumentParser(description='Starting amount.')
parser.add_argument('start_amt', metavar="<Starting Amount>", type=int, default=0, nargs=1, help='starting amount')
parser.add_argument('paycheck_amt', metavar="<Paycheck Amount>", type=int, default=0, nargs=1, help='paycheck amount')
args = parser.parse_args()


with open('bill_dates.csv', 'r') as read_obj:
   csv_read = reader(read_obj)
   bills = list(csv_read)


total_bills = 0
for bill in bills:
   total_bills += int(float(bill[2]))


starting_amount = args.start_amt[0]
paycheck_amount = args.paycheck_amt[0]
total_income = starting_amount

# parsing date and storing values
c = Calendar()
today = date.today().strftime('%d %A')
this_month = int(date.today().strftime('%m'))
this_year = int(date.today().strftime('%y'))
after_today = False

for date in c.itermonthdates(this_year,this_month):
   bill_text = ""
   iter_date = date.strftime('%d %A')
   iter_day = date.strftime('%A')
   # only process dates from today onward
   if (iter_date == today):
      after_today = True

   # add paycheck amount on payday 
   if (after_today):
      if iter_day == "Friday":
         total_income += paycheck_amount
         bill_text += color.OKGREEN + " PAYDAY! (+$" + str(paycheck_amount) + ")" + color.ENDC
      # if today is a bill today, subtract from current balance
      # if today is a bill today, subtract from total bills remaining
      for bill in bills:
         if int(bill[0]) == int(date.strftime('%d')):
            total_income -= int(float(bill[2]))
            total_bills -= int(float(bill[2]))
            bill_text += color.FAIL + " -- " + bill[1].upper() + " (-$" + bill[2] + ")" + color.ENDC
      # Day MM/DD: $<balance>, remaining bills: $<remaining bill total>
      print(color.HEADER + date.strftime('%A %m/%d') \
            + color.ENDC + ': Balance ' + color.OKGREENBG + '$' + str(total_income) + color.ENDC \
            + ", Remaining upcoming bills: " + color.WARNING + "$" + str(total_bills))
      print("\t" + bill_text  + color.ENDC)
   
#def main():
#   print("yo")


#if __name__ == "__main__":
#   main()
