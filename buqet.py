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

class Bill:
   def __init__(self, day, name, amount):
      self.day = day
      self.name = name
      self.amount = amount
      
   def __repr__(self):
      return "%d, %s, %f" % (self.day,self.name,self.amount)

   def __lt__(self,other):
      return(self.day < other.day)

class Day:
   def __init__(self, day, total):
      self.day = day
      self.total = total
   
   def __repr__(self):
      return "%d: %f" % (self.day, self.total)

   def __lt__(self,other):
      return(self.day < other.day)

parser = ArgumentParser(description='Starting amount.')
parser.add_argument('start_amt', metavar="<Starting Amount>", type=int, default=0, nargs=1, help='starting amount')
parser.add_argument('paycheck_amt', metavar="<Paycheck Amount>", type=int, default=0, nargs=1, help='paycheck amount')
args = parser.parse_args()

bills_list = []
days_list  = []

with open('bill_dates.csv', 'r') as read_obj:
   csv_read = reader(read_obj)
   for row in csv_read:
      b = Bill(int(row[0]),str(row[1]),float(row[2]))
      bills_list.append(b)

bills_list=sorted(bills_list)

total_bills = 0
for bill in bills_list:
   total_bills += int(bill.amount)


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
   total_today = 0
   # only process dates from today onward
   if (iter_date == today):
      after_today = True

   # add paycheck amount on payday 
   # TODO: make payday input
   if (after_today):
      if iter_day == "Friday":
         total_income += paycheck_amount
         bill_text += color.OKGREEN + " PAYDAY! (+$" + str(paycheck_amount) + ")" + color.ENDC
         total_today += paycheck_amount
      # if today is a bill day, subtract from current balance
      # if today is a bill day, subtract from total bills remaining
      for bill in bills_list:
         if bill.day == int(date.strftime('%d')):
            total_income -= int(bill.amount)
            total_bills -= int(bill.amount)
            bill_text += color.FAIL + " -- " + bill.name.upper() + " (-$" + str(bill.amount) + ")" \
            + color.ENDC
            total_today -= bill.amount

      d = Day(int(date.strftime('%d')), float(total_today))
      days_list.append(d)
      # Day MM/DD: $<balance>, remaining bills: $<remaining bill total>
      print(color.HEADER + date.strftime('%A %m/%d') \
            + color.ENDC + ': Balance ' + color.OKGREENBG + '$' + str(total_income) + color.ENDC \
            + ", Remaining upcoming bills: " + color.WARNING + "$" + str(total_bills))
      print("\t" + bill_text  + color.ENDC)
   
print(days_list)

#def main():
#   print("yo")


#if __name__ == "__main__":
#   main()
