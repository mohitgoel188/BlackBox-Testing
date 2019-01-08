from os import system
from datetime import datetime

def clrscr():
    _ = system('cls')

def isLeapYear(year):
    if year%400==0:
        return True
    if year%100==0:
        return False
    if year%4==0:
        return True
    return False

def isRight(pickup,drop,day,month,hour,minutes,m,year,later):
    if pickup>=3 and pickup<=15 and drop>=3 and drop<=15:
        if later==1:
            if m in [0,1]:
                if hour>=1 and hour<=12 and minutes>=1 and minutes<=59:    
                    if year>=datetime.utcnow().year and year<=datetime.utcnow().year+1:
                        if month in [1,3,5,7,8,10,12]:
                            if day>=1 and day<=31:
                                return True
                        if month in [4,6,9,11]:
                            if day>=1 and day<=30:
                                return True
                        if month==2:
                            if isLeapYear(year):
                                if day>=1 and day<=29:
                                    return True
                            else:
                                if day>=1 and day<=28:
                                    return True
        elif later==0:
            return True
    return False

def isLoggedIn(name,email,otp,mob):
    try:
        if len(mob)==10 and mob.isdigit():
            if len(name)>=3 and len(name)<=20 and name.isalnum():
                if len(email)>=13 and len(email)<=31 and email.split('@')[-1].split('.')[0]=='gmail':
                    if len(otp)>=4 and len(otp)<=6 and otp.isdigit():
                        return True
    except: pass
    return False

def login():
    mob=input("Enter the mobile number: \n")
    name=input("Enter the name: \n")
    email=input("Enter the email address: \n")
    otp=input(f"Enter the otp:\n(would come in {mob} number)\n")
    status=isLoggedIn(mob,name,email,otp)
    if status:
        print("Login Successful.")
        return True
    print('Login Unsuccessful.')
    return False

def bookCab():
    print(f"\n{'Rent Car'.center(60)}\n")
    pickup=input('Enter pickup location: ')
    drop=input('Enter drop location: ')
    later=0
    date,time,m=[None]*3
    if input("Now/Schedule for later (0/1): ")=='1':
        later=1
        try:
            date=tuple(map(int,input('Enter date (dd/mm/yyyy): ').split('/')))
            time=tuple(map(int,input('Time (hh:mm): ').split(':')))
        except:
            return False
        m=int(input('A.M/P.M (0/1): '))
    if isRight(len(pickup),len(drop),later,*date,*time,m):
        print('We will be there...')
        return True
    print('Fed details are wrong!!!')
    return False

def main():
    clrscr()
    logFlag=False
    while True:
        print(f'{" OLA ".center(100,"*")}\n{" Car Rental System ".center(100," ")}')
        if logFlag==False:
            print(f'\n{"LOGIN".center(60)}')
            logFlag=login()
            continue
        if bookCab():
            break
        else:
            input('Enter details again.\nPress enter to continue...')
            clrscr()

if __name__ == '__main__':
    main()
