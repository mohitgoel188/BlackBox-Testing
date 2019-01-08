import pandas as pd
from itertools import product
from numpy import prod
from interface import isRight
from datetime import datetime
import os

def isLoggedIn(name,email,otp,mob):
    try:
        if mob==10:
            if name>=3 and name<=20:
                if email>=13 and email<=31:
                    if otp>=4 and otp<=6:
                        return True
    except: pass
    return False

def rangeVal(low,high,out_boundary=False,in_boundary=True,boundary=True,nominal=True):
    rangeList=[]
    if low!=high:
        if nominal:
            rangeList.append(int((low+high)/2))
        if boundary:
            rangeList.append(low)
            rangeList.append(high)
        if in_boundary:
            if low+1<=high:
                rangeList.append(low+1)
            if high-1>=low:
                rangeList.append(high-1)
        if out_boundary:
            rangeList.append(low-1)
            rangeList.append(high+1)
    else:
        rangeList.append(int((low+high)/2))
    return set(rangeList)

def bva_robust(varDesc,cfun,robust=False,res='result',filename='TestSuite',verbose=False):
    ''' varDesc: The mapping of variable name and thier range {'varName':(low,high)}
        (type=dict)
        cfun: Function which gives boolean value by checking variable authencity
        (type=<class 'function'>)
        robust: For robustness testing
        (type: bool)
        res: The name of the result variable
        (type=str)
        filename: The name by which final csv file will be created
        (type=str)
        verbose: To display testcases
        (type=bool)
    '''
    if robust:
        print(f'\nDoing robustness testing with {len(varDesc)} variables')
        print(f'Expected test cases 6n+1 i.e {6*len(varDesc)+1}\n')
    else:
        print(f'\nDoing boundary value analysis(BVA) with {len(varDesc)} variables')
        print(f'Expected test cases 4n+1 i.e {4*len(varDesc)+1}\n')

    with open(f"{filename}.csv",'w') as fh:
        genTestCase=[None]*(len(varDesc)+1)
        colNames=[]
        i=0
        count=0
        for key,val in varDesc.items():
            genTestCase[i]=int((val[0]+val[1])/2)
            colNames.append(key)
            i+=1
        colNames.append(res)
        fh.write(f"{','.join(map(str,colNames))}\n")
        i=0
        for key,item in varDesc.items():
            testCase=genTestCase.copy()
            for val in rangeVal(item[0],item[1],robust):
                testCase[i]=val
                testCase[-1]=cfun(*testCase[0:-1])
                # if not robust:
                #     if not testCase[-1]:
                #         continue
                fh.write(f"{','.join(map(str,testCase))}\n")
                count+=1
                if verbose:
                    print(f"TestCase {count}: {testCase}")
            i+=1
        print(f"\nGot test cases: {count}")
    
    df=pd.read_csv(f'{filename}.csv')
    s=df.shape[0]
    # So that same values come together
    df.sort_values([*df.columns[::-1]],inplace=True)
    if s!=df.drop_duplicates().shape[0]:
        df.drop_duplicates(inplace=True)
        print(f'{s-df.shape[0]} duplicate entries removed')
    df.to_csv(f'{filename}.csv',index=False)

def worst_bva_robust(varDesc,cfun,robust=False,res='result',filename='TestSuite',verbose=False):
    ''' varDesc: The mapping of variable name and thier range {'varName':(low,high)}
        (type=dict)
        cfun: Function which gives boolean value by checking variable authencity
        (type=<class 'function'>)
        robust: For robustness testing
        (type: bool)
        res: The name of the result variable
        (type=str)
        filename: The name by which final csv file will be created
        (type=str)
        verbose: To display test cases
        (type=bool)
    '''
    if robust:
        print(f'\nDoing worst case robustness testing with {len(varDesc)} variables')
        print(f'Expected test cases 7^n i.e {7**len(varDesc)}\n')
    else:
        print(f'\nDoing worst case boundary value analysis(BVA) with {len(varDesc)} variables')
        print(f'Expected test cases 5^n i.e {5**len(varDesc)}\n')

    with open(f"{filename}.csv",'w') as fh:
        rangeList=[]
        colNames=[]
        i=0
        count=0
        for key,item in varDesc.items():
            colNames.append(key)
            rangeList.append(rangeVal(item[0],item[1],robust))
            i+=1
        colNames.append(res)
        fh.write(f"{','.join(map(str,colNames))}\n")
        print(f"Test cases based on input: {prod(list(map(len,rangeList)))}")
        rangeList=set(list(product(*rangeList)))
        i=0
        for testCase in rangeList:
            result=cfun(*testCase)
            if not robust:
                if not result:
                    continue
            fh.write(f"{','.join(map(str,testCase))},{result}\n")
            count+=1
            if verbose:
                print(f"TestCase {count}: {testCase},{result}")
            i+=1
        print(f"\nGot test cases: {count}")
    
    df=pd.read_csv(f'{filename}.csv')
    s=df.shape[0]
    # So that same values come together
    df.sort_values([*df.columns[::-1]],inplace=True)
    if s!=df.drop_duplicates().shape[0]:
        df.drop_duplicates(inplace=True)
        print(f'{s-df.shape[0]} duplicate entries removed')
    df.to_csv(f'{filename}.csv',index=False)


def equival_normal(varDesc,cfun,robust=False,res='result',filename='TestSuite',verbose=False):
    ''' varDesc: The mapping of variable name and thier range {'varName':(low,high)}
        (type=dict)
        cfun: Function which gives boolean value by checking variable authencity
        (type=<class 'function'>)
        robust: For weak robust equivalence class testing
        (type: bool)
        res: The name of the result variable
        (type=str)
        filename: The name by which final csv file will be created
        (type=str)
        verbose: To display testcases
        (type=bool)
    '''
    if robust:
        print(f'\nDoing weak robust equivalence class testing with {len(varDesc)} variables')
        # print(f'Expected test cases 6n+1 i.e {6*len(varDesc)+1}\n')
    else:
        print(f'\nDoing weak normal equivalence class testing with {len(varDesc)} variables')
        # print(f'Expected test cases 4n+1 i.e {4*len(varDesc)+1}\n')

    with open(f"{filename}.csv",'w') as fh:
        genTestCase=[None]*(len(varDesc)+1)
        colNames=[]
        i=0
        count=0
        for key,val in varDesc.items():
            genTestCase[i]=int((val[0]+val[1])/2)
            colNames.append(key)
            i+=1
        colNames.append(res)
        fh.write(f"{','.join(map(str,colNames))}\n")
        i=0
        for key,item in varDesc.items():
            testCase=genTestCase.copy()
            if robust or item[0]!=item[1]:
                for val in rangeVal(item[0],item[1],robust,not robust,False,False):
                    testCase[i]=val
                    testCase[-1]=cfun(*testCase[0:-1])
                    fh.write(f"{','.join(map(str,testCase))}\n")
                    count+=1
                    if verbose:
                        print(f"TestCase {count}: {testCase}")
            i+=1
        print(f"\nGot test cases: {count}")
    
    df=pd.read_csv(f'{filename}.csv')
    s=df.shape[0]
    # So that same values come together
    df.sort_values([*df.columns[::-1]],inplace=True)
    if s!=df.drop_duplicates().shape[0]:
        df.drop_duplicates(inplace=True)
        print(f'{s-df.shape[0]} duplicate entries removed')
    df.to_csv(f'{filename}.csv',index=False)

def equival_strong(varDesc,cfun,robust=False,res='result',filename='TestSuite',verbose=False):
    ''' varDesc: The mapping of variable name and thier range {'varName':(low,high)}
        (type=dict)
        cfun: Function which gives boolean value by checking variable authencity
        (type=<class 'function'>)
        robust: For strong robust ECT
        (type: bool)
        res: The name of the result variable
        (type=str)
        filename: The name by which final csv file will be created
        (type=str)
        verbose: To display test cases
        (type=bool)
    '''
    if robust:
        print(f'\nDoing strong robust equivalence class testing with {len(varDesc)} variables')
        # print(f'Expected test cases 7^n i.e {7**len(varDesc)}\n')
    else:
        print(f'\nDoing strong normal equivalence class testing with {len(varDesc)} variables')
        # print(f'Expected test cases 5^n i.e {5**len(varDesc)}\n')

    with open(f"{filename}.csv",'w') as fh:
        rangeList=[]
        colNames=[]
        i=0
        count=0
        for key,item in varDesc.items():
            colNames.append(key)
            rangeList.append(rangeVal(item[0],item[1],robust,not robust,False,False))
            i+=1
        colNames.append(res)
        fh.write(f"{','.join(map(str,colNames))}\n")
        # print(f"Test cases based on input: {prod(list(map(len,rangeList)))}")
        rangeList=set(list(product(*rangeList)))
        i=0
        for testCase in rangeList:
            result=cfun(*testCase)
            fh.write(f"{','.join(map(str,testCase))},{result}\n")
            count+=1
            if verbose:
                print(f"TestCase {count}: {testCase},{result}")
            i+=1
        print(f"\nGot test cases: {count}")
    
    df=pd.read_csv(f'{filename}.csv')
    s=df.shape[0]
    # So that same values come together
    df.sort_values([*df.columns[::-1]],inplace=True)
    if s!=df.drop_duplicates().shape[0]:
        df.drop_duplicates(inplace=True)
        print(f'{s-df.shape[0]} duplicate entries removed')
    df.to_csv(f'{filename}.csv',index=False)

def main():
    if not os.path.exists('./login'):
        os.mkdir('./login')
    varDesc_login={'Name':(3,20),
              'Email Id':(13,31),
              'OTP':(4,6),
              'Mobile Number':(10,10)}
    bva_robust(varDesc_login,isLoggedIn,False,'Logged In','login/login_bva')
    bva_robust(varDesc_login,isLoggedIn,True,'Logged In','login/login_robust')
    worst_bva_robust(varDesc_login,isLoggedIn,False,'Logged In','login/login_worstcase_bva')
    worst_bva_robust(varDesc_login,isLoggedIn,True,'Logged In','login/login_worstcase_robust')
    equival_normal(varDesc_login,isLoggedIn,False,'Logged In','login/login_weak_normal_ECT')
    equival_normal(varDesc_login,isLoggedIn,True,'Logged In','login/login_weak_robust_ECT')
    equival_strong(varDesc_login,isLoggedIn,False,'Logged In','login/login_strong_normal_ECT')
    equival_strong(varDesc_login,isLoggedIn,True,'Logged In','login/login_strong_robust_ECT')

    if not os.path.exists('./booking'):
        os.mkdir('./booking')
    varDesc_book={'Pickup Location':(3,15),
              'Drop Location':(3,15),
              'Day':(1,31),
              'Month':(1,12),
              'Hour':(1,12),
              'Minutes':(1,59),
              'A.M/P.M':(0,1),
              'Year':(datetime.utcnow().year,datetime.utcnow().year+1),
              'When':(0,1),}
    bva_robust(varDesc_book,isRight,False,'Booked','booking/booking_bva')
    bva_robust(varDesc_book,isRight,True,'Booked','booking/booking_robust')
    worst_bva_robust(varDesc_book,isRight,False,'Booked','booking/booking_worstcase_bva')
    worst_bva_robust(varDesc_book,isRight,True,'Booked','booking/booking_worstcase_robust')
    equival_normal(varDesc_book,isRight,False,'Booked','booking/booking_weak_normal_ECT')
    equival_normal(varDesc_book,isRight,True,'Booked','booking/booking_weak_robust_ECT')
    equival_strong(varDesc_book,isRight,False,'Booked','booking/booking_strong_normal_ECT')
    equival_strong(varDesc_book,isRight,True,'Booked','booking/booking_strong_robust_ECT')


if __name__ == '__main__':
    main()