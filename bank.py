from ui import UI
import sqlite3 as sql
import os
import datetime
import locale
import requests
from bs4 import BeautifulSoup

class colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
class Bank():
    def __init__(self,db):#db=database.sqlite3
        
        try:
            self.database=sql.connect(db)#db=database.sqlite3
            self.cur=self.database.cursor()
            self.exit = False
            self.mainmenu=False
        except:
            print("Bağlantı sağlanamadı...")

    def Datetime(self):
        # Get the current date and time
        current_datetime = datetime.datetime.now()
        # Format the current date and time with the specified format
        formatted_datetime = current_datetime.strftime("%Y.%m.%d %H:%M:%S")
        return formatted_datetime  
    
    def CreateTables(self,table_name):
        self.table_name=table_name

        account=f"""CREATE TABLE IF NOT EXISTS "ACCOUNTS"(
        "AccountID"	INTEGER NOT NULL UNIQUE,
	    "KimlikNo"	TEXT NOT NULL UNIQUE,
    	"Passwoard"	TEXT NOT NULL,
    	"Type"	TEXT NOT NULL DEFAULT 1,
	    "FirstName"	TEXT NOT NULL,
    	"Lastname"	TEXT NOT NULL,
	    "Email"	TEXT NOT NULL,
    	"Phone"	TEXT NOT NULL,
    	"address"	TEXT NOT NULL,
    	"DateOfBirth"	TEXT NOT NULL,
    	PRIMARY KEY("AccountID"))"""

        balance=f"""CREATE TABLE IF NOT EXISTS "BALANCE" (
	    "CustomerID"	INTEGER,
	    "BalanceID"	INTEGER NOT NULL UNIQUE,
	    "Balance"	TEXT,
	    "Update"	INTEGER,
	    "Status"	TEXT DEFAULT 'True',
	    PRIMARY KEY("BalanceID" AUTOINCREMENT)
        );"""
        Transactions=f"""CREATE TABLE "TRANSACTIONS" (
    	"TransactionID"	INTEGER NOT NULL UNIQUE,
	    "TransactionType"	TEXT DEFAULT 'none',
    	"FromAccountID"	INTEGER,
    	"ToAccountID"	INTEGER,
	    "DateIssued"	TEXT,
    	"Amount"	INTEGER,
    	PRIMARY KEY("TransactionID" AUTOINCREMENT)
        );"""
        self.cur.execute(account)
        self.cur.execute(balance)
        self.database.commit()
    def logo(self):
         print(colors.GREEN +
        """
          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░          
          ░       ░░░░      ░░░   ░░░  ░░  ░░░░  ░
          ▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒    ▒▒  ▒▒  ▒▒▒  ▒▒
          ▓       ▓▓▓  ▓▓▓▓  ▓▓  ▓  ▓  ▓▓     ▓▓▓▓
          █  ████  ██        ██  ██    ██  ███  ██
          █       ███  ████  ██  ███   ██  ████  █
          ████████████████████████████████████████                                        
  
        """+colors.RESET)
         print("to exit enter -> 0")
         print("-"*60,"|{:*^58}|".format(" sign in "),sep="\n")
        
    def sign_in(self):
        def ValidID(ID):
            ID=int(ID)
            if ID == 0:
                self.exit = True
                return False
            
            self.cur.execute("SELECT * FROM ACCOUNTS WHERE AccountID=?",(ID,))
            self.rows =self.cur.fetchall()
            if len(self.rows)>=1:
                return False
            else:
                print(colors.RED+"wrong ID . . ."+colors.RESET)
                input(colors.GREEN+"press enter to continue . . ."+colors.RESET)
                os.system("cls")
                self.logo()
                return True
        def ValidPassword(password):
            if password == "": return True
            if int(password) == 0:
                self.exit = True
                return False
            for row in self.rows:
                if password == row[2]:
                    print("-"*60)
                    print(f"Welcome {row[4]} {row[5]} you are logged in.")
                    input(colors.GREEN+"Please press enter to continue"+colors.RESET)
                    return False
                else:
                    print(colors.RED+"wrong Password . . ."+colors.RESET)
                    input(colors.GREEN+"press enter to continue . . ."+colors.RESET)
                    os.system("cls")
                    self.logo()
                    print("Enter ID: ",self.rows[0][0])
                    return True

        while(ValidID(input("Enter ID : "))):pass
        if self.exit == False:
           while(ValidPassword(input("Enter Password : "))):pass
        if(self.exit == True):
            return 0
        return self.rows
    def ValidFName(self,fname):
        if fname == "0" or self.mainmenu==True:
            self.mainmenu=True
            return False
        try:
            # Check if the name contains only alphabetic characters
            if fname.isalpha():
                self.Fname = fname
                return False
            else:
                print(colors.RED+"wrong name name dont need number on it"+colors.RESET)
                return True
        except AttributeError:
            # Handle the case where name is not a string
            return True
    def ValidLName(self,lname):
        if lname == "0" or self.mainmenu==True:
            self.mainmenu=True
            return False
        try:
            # Check if the lname contains only alphabetic characters
            if lname.isalpha():
                self.Lname = lname
                return False
            else:
                print(colors.RED+"wrong last name dont need number on it"+colors.RESET)
                return True
        except AttributeError:
            # Handle the case where name is not a string
            return True
    def ValidDate(self,date):
        if date == "0" or self.mainmenu==True:
            self.mainmenu=True
            return False
        date_format=[2,2,4]
        split_char="."
        if date!="" and date.count(split_char)==2 and len(date)==10 and date_format== [len(i) for i in date.rsplit(split_char)] and date.replace(split_char,"").isdecimal():
            self.birthday=date
            return False
        else:
            print(colors.RED+"Lütfen dd.mm.yyyy formetında giriniz..."+colors.RESET)
            return True
    def ValidEmail(self,email):
        if email == "0" or self.mainmenu==True:
            self.mainmenu=True
            return False
        
        try:
            if "@" in email:
                username, domain = email.split('@')
                assert username and domain, "Username or domain is empty"
                assert '.' in domain, "Missing dot in domain"
                domain_parts = domain.split('.')
                assert len(domain_parts) >= 2 and all(part.isalnum() for part in domain_parts), "Invalid domain format"
                self.email = email
                return False
            else: 
                print(colors.RED+"Invalid email"+colors.RESET)
                return True
        except AssertionError as e:
                    print(colors.RED+e+colors.RESET)
                    return True
    def ValidPhone(self,phone_number):
        if phone_number == "0" or self.mainmenu==True:
            self.mainmenu=True
            return False
        
        # Remove whitespace and non-numeric characters
        phone_number = ''.join(filter(str.isdigit, phone_number))

        # Check if the number starts with '0' and has 10 digits
        if len(phone_number) == 11 and phone_number.startswith('0'):    
            self.phone = phone_number
            return False
            # Check if the number starts with '+90' and has 12 digits    
        else:
            print(colors.RED+"wrong phone number use this format (05*********)"+colors.RESET)
            return True
    def ValidTC(self,Tc):
        if Tc =="":
            print(colors.RED+"TC can't be empty"+colors.RESET)
            return True
        if int(Tc) == 0 or self.mainmenu==True:
            self.mainmenu=True
            return False
        self.cur.execute("SELECT * FROM ACCOUNTS WHERE KimlikNo=?",(Tc,))
        self.rowsvtc =self.cur.fetchall()
        if len(self.rowsvtc)>=1:
            print(colors.RED+"This Tc is already in use"+colors.RESET)
            return True

        if int(Tc) == 0 or self.mainmenu==True:
            self.mainmenu=True
            return False
        
        Tc = str(Tc)
        
        # 11 hanelidir.
        if not len(Tc) == 11:
            print(colors.RED+"its need to be 11 digits !"+colors.RESET)
            return True
        
        # Sadece rakamlardan olusur.
        if not Tc.isdigit():
            print(colors.RED+"Tc need to be a number !"+colors.RESET)
            return True
        
        # Ilk hanesi 0 olamaz.
        if int(Tc[0]) == 0:
            print(colors.RED+"Tc don't start with 0"+colors.RESET)
            return True
        
        digits = [int(d) for d in str(Tc)]
        
        # 1. 2. 3. 4. 5. 6. 7. 8. 9. ve 10. hanelerin toplamından elde edilen sonucun
        # 10'a bölümünden kalan, yani Mod10'u bize 11. haneyi verir.
        if not sum(digits[:10]) % 10 == digits[10]:
            print(colors.RED+"Invalid Tc !"+colors.RESET)
            return True
        
        # 1. 3. 5. 7. ve 9. hanelerin toplamının 7 katından, 2. 4. 6. ve 8. hanelerin toplamı çıkartıldığında,
        # elde edilen sonucun 10'a bölümünden kalan, yani Mod10'u bize 10. haneyi verir.
        if not (((7 * sum(digits[:9][-1::-2])) - sum(digits[:9][-2::-2])) % 10) == digits[9]:
            print(colors.RED+"Invalid Tc !"+colors.RESET)
            return True
        
        # Butun kontrollerden gecti.
        self.Tc = Tc
        return False
    #def for add costumer
    def ValidID(self,id):
        if id == "0" or self.mainmenu==True:
            self.mainmenu=True
            return False
        self.cur.execute("SELECT * FROM ACCOUNTS WHERE AccountID=?",(id,))
        self.rowsvi =self.cur.fetchall()
        if len(self.rowsvi)>=1:
            self.ID=id
            return False
        else:
            print(colors.RED+"wrong ID . . ."+colors.RESET)
            return True
    def ValidAmount(self,amount):
        if amount == "0" or self.mainmenu==True:
            self.mainmenu=True
            return False
        try:
            self.Amount = float(amount)
            return False
        except ValueError as e:
            print(colors.RED+"Amount must be a number"+colors.RESET)
            return True


    def AddCostumer(self):
        print(colors.BG_GREEN+"press 0 to back to main menu."+colors.RESET)
        while(self.ValidFName(input(colors.BOLD+"Enter First Name : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.Fname
        if self.mainmenu : return False 
        while(self.ValidLName(input(colors.RESET+colors.BOLD+"Enter Last Name : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.Lname
        if self.mainmenu : return False 
        while(self.ValidDate(input(colors.RESET+colors.BOLD+"Enter Date of Birth : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.birthday
        if self.mainmenu : return False 
        while(self.ValidEmail(input(colors.RESET+colors.BOLD+"Enter Email : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.email
        if self.mainmenu : return False 
        while(self.ValidPhone(input(colors.RESET+colors.BOLD+"Enter phone number : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.phone
        if self.mainmenu : return False 
        while(self.ValidTC(input(colors.RESET+colors.BOLD+"Enter Tc : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.Tc
        if self.mainmenu : return False  
        self.type = 2
        self.address=str(input(colors.RESET+colors.BOLD+"Enter address :"+colors.RESET+colors.GREEN+colors.BOLD))

        formatted_date = self.Datetime()

        self.password = str(input(colors.RESET+colors.BOLD+"Enter password :"+colors.RESET+colors.GREEN+colors.BOLD))
        self.cur.execute("""INSERT INTO "ACCOUNTS" ("KimlikNo", "Passwoard", "Type", "FirstName", "LastName", "Email", "Phone", "Address", "DateOfBirth")
                         VALUES (?,?,?,?,?,?,?,?,?)""",(self.Tc,self.password,self.type,self.Fname,self.Lname,self.email,self.phone,self.address,self.birthday))
        self.database.commit()
        self.cur.execute("SELECT AccountID FROM ACCOUNTS WHERE KimlikNo=?",(self.Tc,))
        self.rowsac =self.cur.fetchall()

        self.cur.execute("""INSERT INTO "BALANCE" ("CustomerID", "Balance", "Update")
                         VALUES (?,?,?)""",(self.rowsac[0][0],"0.0",formatted_date))
        self.database.commit()
        print(colors.RESET+colors.BOLD+colors.GREEN+"*"*60)
        print(colors.RESET+colors.BOLD+colors.GREEN+"costumer saved . cusomer id is : "+colors.RESET+colors.BOLD+colors.UNDERLINE,self.rowsac[0][0]," ")
        print(colors.RESET+colors.BOLD+colors.GREEN+"*"*60)
        input(colors.RESET+colors.BOLD+"please press enter to continue . . .")
    

    def AddEmployee(self):
        print(colors.BG_GREEN+"press 0 to back to main menu."+colors.RESET)
        while(self.ValidFName(input(colors.RESET+colors.BOLD+"Enter First Name : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.Fname
        if self.mainmenu : return False 
        while(self.ValidLName(input(colors.RESET+colors.BOLD+"Enter Last Name : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.Lname
        if self.mainmenu : return False 
        while(self.ValidDate(input(colors.RESET+colors.BOLD+"Enter Date of Birth : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.birthday
        if self.mainmenu : return False 
        while(self.ValidEmail(input(colors.RESET+colors.BOLD+"Enter Email : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.email
        if self.mainmenu : return False 
        while(self.ValidPhone(input(colors.RESET+colors.BOLD+"Enter phone number : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.phone
        if self.mainmenu : return False 
        while(self.ValidTC(input(colors.RESET+colors.BOLD+"Enter Tc : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.Tc
        if self.mainmenu : return False  
        self.type = 1
        self.address=str(input(colors.RESET+colors.BOLD+"Enter address :"+colors.RESET+colors.GREEN+colors.BOLD))
        self.password = str(input(colors.RESET+colors.BOLD+"Enter password :"+colors.RESET+colors.GREEN+colors.BOLD))
        self.cur.execute("""INSERT INTO "ACCOUNTS" ("KimlikNo", "Passwoard", "Type", "FirstName", "LastName", "Email", "Phone", "Address", "DateOfBirth")
                         VALUES (?,?,?,?,?,?,?,?,?)""",(self.Tc,self.password,self.type,self.Fname,self.Lname,self.email,self.phone,self.address,self.birthday))
        self.database.commit()
        self.cur.execute("SELECT AccountID FROM ACCOUNTS WHERE KimlikNo=?",(self.Tc,))
        self.rowsae =self.cur.fetchall()
        print(colors.RESET+colors.BOLD+colors.GREEN+"*"*60)
        print(colors.RESET+colors.BOLD+colors.GREEN+"employee saved . employee id is : "+colors.RESET+colors.BOLD+colors.UNDERLINE, self.rowsae[0][0]," ")
        print(colors.RESET+colors.BOLD+colors.GREEN+"*"*60)
        input(colors.RESET+colors.BOLD+"please press enter to continue . . .")

    def change_passwoard(self):
        def ValidId(id):
            if id == "0" or self.mainmenu==True:
                self.mainmenu=True
                return False
            self.cur.execute("SELECT * FROM ACCOUNTS WHERE AccountID=?",(id,))
            self.rowscp =self.cur.fetchall()
            if len(self.rowscp)>=1:
                self.id=id
                return False
            else:
                print(colors.RESET+colors.RED+colors.BOLD+"don't Find Account With Id : "+colors.UNDERLINE, id)
                return True
        def ValidTc(tc):
            if tc == "0" or self.mainmenu==True:
                self.mainmenu=True
                return False
            if tc == self.rowscp[0][1]:
                return False
            else:
                print(colors.RESET+colors.RED+colors.BOLD+"id dosent matche with this kimlik no please try again :")
                return True
        def validpass(password):
            if password == "": 
                print(colors.RESET+colors.RED+colors.BOLD+"please enter password it's not to be empty :")
                return True
            elif password == "0" or self.mainmenu==True:
                self.mainmenu=True
                return False
            else:
                self.newpassword=password
                return False

        print(colors.RESET+colors.BG_GREEN+colors.BOLD+"press 0 to back to main menu."+colors.RESET)
        while(ValidId(input(colors.RESET+colors.BOLD+"please enter id to change password : "+colors.RESET+colors.GREEN+colors.BOLD))):pass
        if self.mainmenu : return False
        while(ValidTc(input(colors.RESET+colors.BOLD+"please enter kimlik number for safety : "+colors.RESET+colors.GREEN+colors.BOLD))):pass
        if self.mainmenu : return False
        while(validpass(input(colors.RESET+colors.BOLD+"Enter your new password"+colors.RESET+colors.GREEN+colors.BOLD))):pass
        if self.mainmenu : return False
        self.cur.execute(""" UPDATE "ACCOUNTS" SET "Passwoard" =? WHERE "AccountID" =?""",(self.newpassword,self.id))
        self.database.commit()
        print(colors.RESET+colors.BOLD+colors.GREEN+"password changed.")
        input(colors.RESET+colors.BOLD+colors.GREEN+"please press enter to continue . . .")
    def edit_customer(self):
        def ValidId(id):
            if id == "": 
                print(colors.RESET+colors.RED+colors.BOLD+"please enter customer id it's not to be empty :")
                return True
                
            if int(id) == 0:
                self.mainmenu=True
                return False
            self.cur.execute("SELECT * FROM ACCOUNTS WHERE AccountID=?",(id,))
            self.rowsvi =self.cur.fetchall()
            if len(self.rowsvi)>=1:
                self.id=id
                return False
            else:
                print(colors.RESET+colors.RED+colors.BOLD+"dont find account with id : "+colors.RESET+colors.BOLD, id ,colors.RESET+colors.BG_GREEN+colors.BOLD+"\n -> try another id or 0 to back to menu.")
                return True
        def ValidEditMenuId(id):
            if id.isdigit():
                if int(id)>=1 and int(id)<=7:
                    self.edit=str(id)
                    return False
                elif int(id)==0:
                    self.edit=0
                    return False
                else:
                    print(colors.RESET+colors.RED+colors.BOLD+"please Enter between [1-7]")
                    return True
            else:
                print(colors.RESET+colors.RED+colors.BOLD+"id need to be a number !")
                return True

        print(colors.RESET+colors.BG_GREEN+colors.BOLD+"press 0 to back to main menu."+colors.RESET)
        while(ValidId(input(colors.RESET+colors.BOLD+"please Enter customer id :"+colors.RESET+colors.GREEN+colors.BOLD))):pass
        if self.mainmenu==False:
            self.Emenu =[]
            if len(self.rowsvi)>=1:
                for i in range(0,len(self.rowsvi[0])):
                    self.Emenu.append(self.rowsvi[0][i])
                print("."*60)
                print(colors.GREEN+colors.BOLD+"1- kimlik no : "+colors.WHITE , self.Emenu[1])
                print(colors.GREEN+"2- first name : "+colors.WHITE , self.Emenu[4])
                print(colors.GREEN+"3- last name : "+colors.WHITE , self.Emenu[5])
                print(colors.GREEN+"4- email : "+colors.WHITE , self.Emenu[6])
                print(colors.GREEN+"5- phone : "+colors.WHITE , self.Emenu[7])
                print(colors.GREEN+"6- adress : "+colors.WHITE , self.Emenu[8])
                print(colors.GREEN+"7- date of birth : "+colors.WHITE , self.Emenu[9])
                
                print(colors.GREEN+"."*60,colors.RESET)
                while(ValidEditMenuId(input(colors.RESET+colors.BOLD+"Please enter field that you want to Edit [1-7] or [0] to back : "+colors.GREEN))):pass
                if self.edit=="1":
                    while(self.ValidTC(input(colors.RESET+colors.BOLD+"please enter kimlik no :"+colors.GREEN))):pass
                    if self.mainmenu : return False 
                    self.cur.execute(""" UPDATE "ACCOUNTS" SET "KimlikNo" =? WHERE "AccountID" =?""",(self.Tc,self.id))
                    self.database.commit()
                    print("kimlik changed.")
                elif self.edit=="2":
                    while(self.ValidFName(input(colors.RESET+colors.BOLD+"please enter first name :"+colors.GREEN))):pass
                    if self.mainmenu : return False 
                    self.cur.execute(""" UPDATE "ACCOUNTS" SET "FirstName" =? WHERE "AccountID" =?""",(self.Fname,self.id))
                    self.database.commit()
                    print("first name changed.")
                elif self.edit=="3":
                    while(self.ValidLName(input(colors.RESET+colors.BOLD+"please enter Last name :"+colors.GREEN))):pass
                    if self.mainmenu : return False 
                    self.cur.execute(""" UPDATE "ACCOUNTS" SET "LastName" =? WHERE "AccountID" =?""",(self.Lname,self.id))
                    self.database.commit()
                    print("last name changed.")
                elif self.edit=="4":
                    while(self.ValidEmail(input(colors.RESET+colors.BOLD+"please enter Email :"+colors.GREEN))):pass
                    if self.mainmenu : return False 
                    self.cur.execute(""" UPDATE "ACCOUNTS" SET "Email" =? WHERE "AccountID" =?""",(self.email,self.id))
                    self.database.commit()
                    print("Email changed.")
                elif self.edit=="5":
                    while(self.ValidPhone(input(colors.RESET+colors.BOLD+"please enter phone :"+colors.GREEN))):pass
                    if self.mainmenu : return False 
                    self.cur.execute(""" UPDATE "ACCOUNTS" SET "Phone" =? WHERE "AccountID" =?""",(self.phone,self.id))
                    self.database.commit()
                    print("phone changed.")
                elif self.edit=="6":
                    self.address=input(colors.RESET+colors.BOLD+"please enter adress :"+colors.GREEN)
                    if self.mainmenu : return False 
                    self.cur.execute(""" UPDATE "ACCOUNTS" SET "address" =? WHERE "AccountID" =?""",(self.address,self.id))
                    self.database.commit()
                    print("address changed.")
                elif self.edit=="7":
                    while(self.ValidDate(input(colors.RESET+colors.BOLD+"please enter date of birth :"+colors.GREEN))):pass
                    if self.mainmenu : return False 
                    self.cur.execute(""" UPDATE "ACCOUNTS" SET "DateOfBirth" =? WHERE "AccountID" =?""",(self.birthday,self.id))
                    self.database.commit()
                    print("date of birth changed.")
                elif self.edit==0:
                    return False
                
                input(colors.RESET+colors.GREEN+colors.BOLD+"please press enter to continue .")
    def show_customer(self):
        def ValidId(id):
            if id == "0" or self.mainmenu==True:
                self.mainmenu=True
                return False
            self.cur.execute("SELECT * FROM ACCOUNTS WHERE AccountID=?",(id,))
            self.rowsc =self.cur.fetchall()
            if len(self.rowsc)>=1:
                self.id=id
                return False
            else:
                print(colors.RESET+colors.RED+colors.BOLD+"dont find account with id : "+colors.UNDERLINE, id," ")
                return True
            
        print(colors.RESET+colors.BG_GREEN+colors.BOLD+"press 0 to back to main menu."+colors.RESET)
        while(ValidId(input(colors.RESET+colors.BOLD+"please Enter customer id :"+colors.GREEN))):pass
        if self.mainmenu==False:
            self.Emenu =[]
            if len(self.rowsc)>=1:
                for i in range(0,len(self.rowsc[0])):
                    self.Emenu.append(self.rowsc[0][i])
                print(colors.GREEN+colors.BOLD+"."*60)
                print("1- kimlik no : "+colors.WHITE , self.Emenu[1])
                print(colors.GREEN+"2- first name : "+colors.WHITE , self.Emenu[4])
                print(colors.GREEN+"3- last name : "+colors.WHITE , self.Emenu[5])
                print(colors.GREEN+"4- email : "+colors.WHITE , self.Emenu[6])
                print(colors.GREEN+"5- phone : "+colors.WHITE , self.Emenu[7])
                print(colors.GREEN+"6- adress : "+colors.WHITE , self.Emenu[8])
                print(colors.GREEN+"7- date of birth : "+colors.WHITE , self.Emenu[9])
                
                print(colors.GREEN+"."*60)
                input(colors.WHITE+"please press enter to continue"+colors.RESET)
    def addBalance(self):
        print(colors.RESET+colors.BG_GREEN+colors.BOLD+"press 0 to back to main menu."+colors.RESET)
        while(self.ValidID(input(colors.WHITE+colors.BOLD+"Please enter Customer ID : "+colors.GREEN))):pass #self.ID
        if self.mainmenu : return False
        while(self.ValidAmount(input(colors.WHITE+colors.BOLD+"Please Enter Amount :"+colors.GREEN))):pass #self.Amount
        if self.mainmenu : return False
        formatted_date = self.Datetime()
        self.cur.execute("""select * from"BALANCE" Where "CustomerID" = ? """,(self.ID,))
        self.rowsab =self.cur.fetchall()
        if len(self.rowsab)>=1:
            self.CurrentBalance=self.rowsab[0][2]
        else:
            print(colors.RED+"someting error please connect to developer.")
        print(colors.BG_CYAN+"current balance : "+colors.RESET+colors.CYAN+colors.BOLD , self.TLFormat(float(self.rowsab[0][2])))
        self.NewBAlance = float(self.CurrentBalance)+float(self.Amount)
        print(colors.BG_MAGENTA+"charged amount :"+colors.RESET+colors.MAGENTA+colors.BOLD,self.TLFormat(float(self.Amount)))
        print(colors.BG_GREEN+"Last balance : "+colors.RESET+colors.GREEN+colors.BOLD , self.TLFormat(float(self.NewBAlance)))
        self.cur.execute(""" UPDATE "BALANCE" SET "Balance" =? , "Update"=? WHERE "CustomerID" =?""",(self.NewBAlance,formatted_date,self.ID))
        self.cur.execute("""INSERT INTO "TRANSACTIONS" (TransactionType, FromAccountID, ToAccountID, DateIssued, Amount) 
                         VALUES (?, ?, ?, ?, ?)""",("BANK ADD BALANCE",self.rows[0][0],self.ID,formatted_date,self.Amount))
        self.database.commit()
        input(colors.RESET+colors.GREEN+colors.BOLD+"Please press enter to continue")
    def TLFormat(self,amount):
        # Set the locale to Turkish (Turkey)
        locale.setlocale(locale.LC_ALL, 'tr_TR')
        # Define the number you want to format
        Amount = amount
        # Format the number as currency
        formatted_amount = locale.currency(Amount, grouping=True)
        return formatted_amount
    
    def ShowBalance(self):
        self.cur.execute("SELECT * FROM BALANCE WHERE CustomerID =?",(str(self.rows[0][0]),))
        self.balance=self.cur.fetchall()
        if len(self.balance)>=1:
            print(colors.RESET+colors.BOLD+"your balance is : "+colors.BG_GREEN,self.TLFormat(float(self.balance[0][2]))," "+colors.RESET)
        
        input(colors.RESET+colors.BOLD+"please press enter to continue"+colors.RESET)
    def TransferMoney(self):
        def ValidTID(id):
            if id =="":
                print(colors.RESET+colors.BOLD+colors.RED+"can't be empty"+colors.RESET)
                return True
            if id == "0" or self.mainmenu==True:
                self.mainmenu=True
                return False
            self.cur.execute("SELECT * FROM ACCOUNTS WHERE AccountID=?",(id,))
            self.transferRows =self.cur.fetchall()
            if int(id) == int(self.rows[0][0]):
                print(colors.RESET+colors.BOLD+colors.RED+"you can not transfer money to yourself ! please select other IDBANK . . ."+colors.RESET)
                return True
            elif len(self.transferRows)>=1:
                if self.transferRows[0][3] == "1":
                    print(colors.RESET+colors.BOLD+colors.RED+"wrong ID . . ."+colors.RESET)
                    return True
                else:    
                    self.ID=id
                    return False
            else:
                print(colors.RESET+colors.BOLD+colors.RED+"wrong ID . . ."+colors.RESET)
                return True
        def transactiontype(type):
            if type == "":
                print(colors.RESET+colors.BOLD+colors.RED+"please select one of the type (not can't be empty)"+colors.RESET)
                return True
            elif not type.isdigit():
                print(colors.RESET+colors.BOLD+colors.RED+"you must enter a number ..."+colors.RESET)
                return True
            elif type=="0":
                self.mainmenu=True
                return False
            else:
                if int(type) >=1 and int(type)<=6:
                    self.SelectedType=type
                    return False
                else:
                    print(colors.RESET+colors.BOLD+colors.RED+"please select between[1-6] "+colors.RESET)
                    return True
                
        def ValidAmount(amount):
            if amount == "0" or self.mainmenu==True:
                self.mainmenu=True
                return False
            try:
                self.Amount = float(amount)
                id=self.rows[0][0]
                self.cur.execute("""select * from"BALANCE" Where "CustomerID" = ? """,(id,))
                self.rowsT =self.cur.fetchall()
                if len(self.rowsT)>=1:
                    Curent_balance=self.rowsT[0][2]
                    if float(self.Amount) > float(Curent_balance):
                        print(colors.RESET+colors.BOLD+colors.RED+"you can not transfer more money than your current balance . . ."+colors.RESET)
                        return True
                    else:return False
            except ValueError as e:
                print(colors.RED+"Amount must be float or digit number"+colors.RESET)
                return True
        print(colors.RESET+colors.BG_GREEN+colors.BOLD+"press 0 to back to main menu."+colors.RESET)    
        while(ValidTID(input(colors.RESET+colors.BOLD+"please enter IDBANK User to transfer money :"+colors.RESET+colors.BOLD+colors.GREEN))):pass #self.ID
        if self.mainmenu : return False
        while(ValidAmount(input(colors.RESET+colors.BOLD+colors.WHITE+"amount to transfer : "+colors.GREEN))):pass #self.Amount
        if self.mainmenu : return False

        self.tTypes=["individual payment","housing rent","workplace rent","other rent","E-commerce payment","other payments"]
        print(colors.RESET+colors.BOLD+"money sending type :")
        for i in range(0,len(self.tTypes)):
            print(f"  {i+1} -> {self.tTypes[i]} ")
        while(transactiontype(input(colors.RESET+colors.BOLD+colors.WHITE+"please select one of the type :"+colors.GREEN))) :pass #self.tType
        if self.mainmenu : return False
        formatted_date = self.Datetime()
        FromID=self.rows[0][0]
        ToID=self.ID
        Amount=self.Amount
        Type=self.tTypes[int(self.SelectedType)-1]

        self.cur.execute("""select * from"BALANCE" Where "CustomerID" = ? """,(FromID,))
        self.rowsT =self.cur.fetchall()
        if len(self.rowsT)>=1:
            self.CBFromID=self.rowsT[0][2]
        self.cur.execute("""select * from"BALANCE" Where "CustomerID" = ? """,(ToID,))
        self.rowsT =self.cur.fetchall()
        if len(self.rowsT)>=1:
            self.CBToID=self.rowsT[0][2]
        AmountFromID=float(self.CBFromID)-float(Amount)
        AmountToID=float(self.CBToID)+float(Amount)
        self.cur.execute("""INSERT INTO "TRANSACTIONS" (TransactionType, FromAccountID, ToAccountID, DateIssued, Amount) 
                         VALUES (?, ?, ?, ?, ?)""",(Type,FromID,ToID,formatted_date,Amount))
        self.cur.execute(""" UPDATE "BALANCE" SET "Balance" =? , "Update"=? WHERE "CustomerID" =?""",(AmountFromID,formatted_date,FromID))
        self.cur.execute(""" UPDATE "BALANCE" SET "Balance" =? , "Update"=? WHERE "CustomerID" =?""",(AmountToID,formatted_date,ToID))
        self.database.commit()
        print(f"{colors.RESET+colors.BG_BLACK+colors.BOLD+colors.GREEN}money was transfered from{colors.BG_GREEN+colors.WHITE} {FromID}:{self.TLFormat(Amount)} {colors.BG_BLACK+colors.GREEN} to -> {colors.BG_GREEN+colors.WHITE} {ToID} {colors.BG_BLACK+colors.GREEN} in {colors.BG_GREEN+colors.WHITE} {formatted_date}"+colors.RESET)
        print(f"{colors.RESET+colors.BLUE+colors.BOLD}your Current Balance is :{colors.BG_BLUE+colors.WHITE} {self.TLFormat(AmountFromID)} {colors.RESET}")

        input(colors.RESET+colors.BOLD+"please press enter to continue")

    def ChangeCustomerPassword(self):
        def validLastPassword(passwoard):
            if passwoard=="0":
                self.mainmenu=True
                return False
            self.cur.execute("""SELECT Passwoard FROM "ACCOUNTS" WHERE AccountID =?""",(str(self.rows[0][0]),))
            lastpasswoard=self.cur.fetchall()[0][0]
            if lastpasswoard==passwoard:
                self.passvalidate = True
                return False
            else:
                print(colors.RESET+colors.BOLD+colors.RED+"wrong Last Password ."+colors.RESET)
                return True
        def ValidNewPassword(passwoard):
            if passwoard=="0":
                self.mainmenu=True
                return False
            else:
                self.newpassword=passwoard
                return False
            



        print(colors.RESET+colors.BG_GREEN+colors.BOLD+"press 0 to back to main menu."+colors.RESET)
        while(validLastPassword(input(colors.RESET+colors.BOLD+"Enter your"+colors.RED+" LAST PASSWORD : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.passvalidate
        if self.mainmenu==True:return False
        
        if self.passvalidate:
            while(ValidNewPassword(input(colors.RESET+colors.BOLD+"Enter your"+colors.GREEN+" NEW PASSWORD"+colors.WHITE+" : "+colors.RESET+colors.GREEN+colors.BOLD))):pass #self.newpassword
            if self.mainmenu==True:return False
            self.cur.execute(""" UPDATE "ACCOUNTS" SET "Passwoard" =? WHERE "AccountID" =?""",(self.newpassword,self.rows[0][0]))
            self.database.commit()
            print(colors.RESET+colors.BOLD+colors.GREEN+"password changed.")
            input(colors.RESET+colors.BOLD+colors.GREEN+"please press enter to continue . . .")
        else:
            print(colors.RESET+colors.BOLD+colors.RED+"password dosn't change")
            return False

       
    def get_foreign_currency_rates(self):
        # URL of the doviz.com website for foreign exchange rates
        url = "https://www.doviz.com/"

        # Sending HTTP GET request to the website
        response = requests.get(url)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parsing HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all span tags with class "value" containing currency rates
            currency_tags = soup.find_all('span', class_='value')

            # Creating a dictionary to store currency names and exchange rates
            currency_dict = {}
            
            for currency_tag in currency_tags:
                # Extract currency name from data-socket-key attribute
                currency_name = currency_tag['data-socket-key']
                # Extract currency rate
                currency_rate = currency_tag.text.strip()
                currency_dict[currency_name] = currency_rate
                
            return currency_dict
        else:
            print(colors.RESET+colors.RED+colors.BOLD+"Failed to retrieve data from doviz.com"+colors.RESET)
            return None
    def ForeignCurrency(self):
        foreign_currency_rates = self.get_foreign_currency_rates()
        if foreign_currency_rates:
            print("")
            for currency, rate in foreign_currency_rates.items():
                if "$" in rate:
                    print(f"{colors.RESET+colors.BG_GREEN+colors.BOLD}{currency}:{colors.RESET+colors.BOLD+colors.GREEN} {rate}{colors.RESET}",end=" - ")
                else:
                    try:
                        rate=rate.replace('.','')
                        rate=rate.replace(',', '.')
                        rate=float(rate)
                    except ValueError:
                        print(colors.red+colors.BOLD+"error to show currency"+colors.RESET)
                    print(f"{colors.RESET+colors.BG_WHITE+colors.BLACK+colors.BOLD}{currency}:{colors.RESET+colors.BOLD+colors.BLUE} {self.TLFormat(rate)}{colors.RESET}",end=" - ")
                    
            input(colors.RESET+colors.BOLD+colors.GREEN+"\n please press enter to continue . . ."+colors.RESET)
    def accountactivities(self):
        
        self.cur.execute("""SELECT *
            FROM "TRANSACTIONS"
            WHERE "ToAccountID" = ?  OR "FromAccountID" = ?
            ORDER BY "DateIssued" DESC;""",(str(self.rows[0][0]),str(self.rows[0][0])))
        
        self.Green=self.cur.fetchall()
        if len(self.Green)>=1:
            self.cur.execute("SELECT * FROM BALANCE WHERE CustomerID =?",(str(self.rows[0][0]),))

            self.tempbalance=self.cur.fetchall()[0][2]

            print("your Current Balance is : " , self.TLFormat(float(self.tempbalance)))
            for rows in self.Green:
                self.cur.execute("""SELECT * FROM ACCOUNTS WHERE AccountID =?""",(str(rows[2]),))
                self.rowsisadmin =self.cur.fetchall()[0][3]
                if self.rowsisadmin=="1":
                    From="BANK"
                else:
                    From=rows[2]
                if str(rows[2]) == str(self.rows[0][0]):
                    self.tempbalance=float(self.tempbalance)+float(rows[5])
                    self.tempequalbalance=float(self.tempbalance)-float(rows[5])
                    print(colors.RESET+colors.RED+colors.BOLD,"   ( ",rows[4]," )",From," -> " ,rows[3], " : ", self.TLFormat(float(self.tempbalance)) ," -", self.TLFormat(float(rows[5])), " = " , self.tempequalbalance)
                    continue
                else:
                    self.tempbalance=float(self.tempbalance)-float(rows[5])
                    self.tempequalbalance=float(self.tempbalance)+float(rows[5])
                    print(colors.RESET+colors.GREEN+colors.BOLD,"   ( ",rows[4]," )",rows[3]," <- " ,From, " : ",  self.TLFormat(float(self.tempbalance))," +", self.TLFormat(float(rows[5])), " = ", self.tempequalbalance)
        else:
            print(colors.RESET+colors.RED+colors.BOLD+"there is no activities on your account ."+colors.RESET)
       
        input(colors.RESET+colors.GREEN+colors.BOLD+"Please Press enter to continue"+colors.RESET)
    
    def log_out(self):
        self.cur.execute("SELECT * FROM ACCOUNTS WHERE AccountID=?",(self.rows[0][0],))
        self.rows =self.cur.fetchall()
        if len(self.rows)>=1:
            self.cur.execute("""""")

    def __del__(self):
        self.database.commit()
        self.database.close()
    


if __name__=="__main__":
    session = False
    Bank=Bank("db.db")
    Bank.CreateTables("ACCOUNTS")
    

    customer_Menu=UI(["Show balance","transfer money","change password","foreign currency","account activities","log out","exit"])
    employee_Menu=UI(["add customer","add balance to customer","edit customer","add employee","change customer password","change employee password","show customer by ID","loge out","exit"])
    while True:
        os.system("cls")
        Bank.mainmenu=False
        if session==False:
            customer_Menu.logo()
            print("to exit enter -> 0")
            print("-"*60,"|{:*^58}|".format(" sign in "),sep="\n")
            session=Bank.sign_in()
            if session==0:
                os.system("cls")
                break
        else:
            customer_Menu.logo()
            print("-"*60)            
            text=" + User : "+ str(session[0][4])+" "+str(session[0][5])
            print("|{: <58}|".format(text))
            text=" + ID : "+ str(session[0][0])
            print("|{: <58}|".format(text))
            if int(session[0][3])==1:
                print("|{: <58}|".format(" + Type : Admin"))
                
                employee_Menu.ShowMenu()
                choise=employee_Menu.GetChoise()
                if choise==1:
                    Bank.AddCostumer()
                elif choise==2:
                    Bank.addBalance()
                elif choise==3:
                    Bank.edit_customer()
                elif choise==4:
                    Bank.AddEmployee()
                elif choise==5:
                    Bank.change_passwoard()
                elif choise==6:
                    Bank.change_passwoard()
                elif choise==7:
                    Bank.show_customer()
                elif choise==8:
                    session=False
                elif choise==9:
                    os.system("cls")
                    break
            elif int(session[0][3])==2:
                print("|{: <58}|".format(" + Type : Customer"))
                
                customer_Menu.ShowMenu()
                choise=customer_Menu.GetChoise()
                if choise==1:
                    Bank.ShowBalance()
                elif choise==2:
                    Bank.TransferMoney()
                elif choise==3:
                    Bank.ChangeCustomerPassword()
                elif choise==4:
                    Bank.ForeignCurrency()
                elif choise==5:
                    Bank.accountactivities()
                elif choise==6:
                    session=False
                elif choise==7:
                    os.system("cls")
                    break
