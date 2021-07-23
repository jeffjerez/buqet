class Bill {
   constructor(day, total) {
      this.day = day;
      this.total = total;
   }
}

function reset_month() {
   carry = false;
   carryAmount = 0;
   today = new Date();
   currentMonth = today.getMonth();
   currentYear = today.getFullYear();
   showCalendar(currentMonth, currentYear);
}

let csv="day,name,amount\n" +
        "1,rent,840\n" +
        "8,internet,109\n" +
        "12,dukenrg,100\n" +
        "12,d+,15\n" +
        "14,audible,25\n" +
        "14,wdw,55\n" +
        "17,apple,15.99\n" +
        "18,amazon,6.50\n" +
        "20,apple,15\n" +
        "20,twitch,10\n" +
        "23,spotify,10\n" +
        "25,car insurance,220\n" +
        "27,car,541\n" +
        "28,life insurance,900\n" +
        "29,at&t,190";

my_bills = $.csv.toObjects(csv);

paydayAmount = document.getElementById("payday_amount");
startAmount = document.getElementById("starting_amount");
selectPayday = document.getElementById("payday");
carry = false;
carryAmount = 0;
amt = 0;

selectDay = 0;
var myFocus = "";

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

monthAndYear = document.getElementById("monthAndYear");
reset_month();

function set_check(){
   carry = !carry;
}

function next_month() {
   myFocus = ""; 
   selectDay = 0;
   currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
   currentMonth = (currentMonth + 1) % 12;
   showCalendar(currentMonth, currentYear);

}

function previous_month() {
   myFocus = ""; 
   selectDay = 0;
   carry = false;
   carryAmount = 0;
   currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
   currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
   showCalendar(currentMonth, currentYear);
}

function get_paydays() {
   showCalendar(currentMonth, currentYear);
}

function select_date(e) {
   if (myFocus.id == e.id) {
      selectDay = 0;
      myFocus = "";
   }
   else {
      selectDay = parseInt(e.innerText.split("\n")[0]);
      if (isNaN(selectDay)) {
         selectDay = 0;
      }
      myFocus = e;
   }
   get_paydays();
}

function showCalendar(month, year) {

   let firstDay = (new Date(year, month)).getDay();

   tbl = document.getElementById("calendar-body"); // body of the calendar

   // clearing all previous cells
   tbl.innerHTML = "";

   // filing data about month and in the page via DOM.
   monthAndYear.innerHTML = months[month] + " " + year;

   // creating all cells
   let date = 1;
   setStart = false;
   if (carry == true) {
      carryAmount = amt;
   }
   else {
      amt = 0;
   }

   for (let i = 0; i < 6; i++) {
      // creates a table row
      let row = document.createElement("tr");

      //creating individual cells, filing them up with data.
      for (let j = 0; j < 7; j++) {
         todays_bills = ""
            if (selectDay != 0 && date >= selectDay && !setStart) {
               sa = parseInt(startAmount.value);
               if (isNaN(sa)) {
                  sa = 0;
               }
               amt = sa;
               setStart = true;
            }
         if (i === 0 && j < firstDay) {
            cell = document.createElement("td");
            cellText = document.createTextNode("");
            cell.appendChild(cellText);
            row.appendChild(cell);
         } else if (date > daysInMonth(month, year)) {
            break;
         } else {
            cell = document.createElement("td");
            cell.setAttribute("onclick", "select_date(this)");
            cell.setAttribute("id", date);
            for (bill in my_bills) {
               b = my_bills[bill];
               if (b.day == date) {
                  amt -= parseInt(b.amount);
                  todays_bills += b.name + " (-$" + b.amount + ")\n";
               } 
            }
            cell.setAttribute("data-toggle","tooltip");
            cell.setAttribute("data-placement","top");
            cell.setAttribute("title",todays_bills);

            cellText = document.createTextNode(date);
            if (!isNaN(parseInt(selectPayday.value)) && j == selectPayday.value) {
               amt += parseInt(paydayAmount.value);
            }
            amtText = document.createTextNode("$" + amt);
            if (date === today.getDate() && year === today.getFullYear()
                  && month === today.getMonth()) {
               cell.classList.add("table-info");
            } // color today's date
            cell.appendChild(cellText);
            cell.appendChild(document.createElement('br'));
            cell.appendChild(amtText);
            row.appendChild(cell);
            date++;
         }
      }
      tbl.appendChild(row); // appending each row into calendar body
   }
   tbl = document.getElementById("calendar"); // body of the calendar
   ths = tbl.getElementsByTagName("th");
   let i = 0;
   for (let th of ths) {
      if (!isNaN(parseInt(selectPayday.value)) && i == selectPayday.value) {
         th.classList.add("table-success");
         break;
      }
      else {
         th.classList.remove("table-success");
      }
      i++;
   }
   tds = tbl.getElementsByTagName("td");
   for (let td of tds) {
      for (let bill of my_bills) {
         if (bill.day == td.id && today.getDate() != td.id) {
            td.classList.remove("table-warning");
            td.classList.add("table-danger");
            break;
         }
         else {
            td.classList.remove("table-danger");
         }
      }
   }
   for (let td of tds) {
      if (myFocus != "" && myFocus.id == td.id && td.id != "") {
         td.classList.remove("table-danger");
         td.classList.remove("table-info");
         td.classList.add('table-warning');
      } else {
         td.classList.remove('table-warning');
      }
   }
}


// check how many days in a month code from https://dzone.com/articles/determining-number-days-month
function daysInMonth(iMonth, iYear) {
   return 32 - new Date(iYear, iMonth, 32).getDate();
}

