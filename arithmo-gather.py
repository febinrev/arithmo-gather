#!/usr/bin/env python3
import readline
import requests
from bs4 import BeautifulSoup
import binlist
import json
import phonenumbers
from phonenumbers import carrier
from phonenumbers import timezone
from phonenumbers import geocoder

key1="e4b4ac1c7eb77ef45f4a867728cfa2f7"
pkey="38d492d349e67433b3a2a229fd784821"


def CC(cc):
	if cc.isdigit() and len(cc)==16:
		print("\n........................\n")
		checkbin=binlist.BIN(str(cc)[0:6])
		credit_card=checkbin.lookup().verbose_name
		print(f"CREDIT CARD : {credit_card} ")
		if checkbin.lookup().active==True:
			print("Current Status : ACTIVE! ")
		else:
			print("Current Status : Not ACTIVE!")
		print("Fetching Informations.....\n")
		try:
			
			result=requests.get(f"https://api.bincodes.com/cc/?format=json&api_key={key1}&cc={cc}")
			online_check=json.loads(result.text)
			print(f"""
			BIN           : {cc[0:6]}
			BANK          : {online_check['bank']}
			CARD          : {online_check['card']}
			TYPE          : {online_check['type']}
			LEVEL         : {online_check['level']}
			COUNTRY       : {online_check['country']}
			COUNTRY_CODE  : {online_check['countrycode']}
			BANK_WESBSITE : {online_check['website']}
			PHONE         : {online_check['phone']}
			VALID         : {online_check['valid']}
			 """)
		except:
			print("Cannot fetch informations!! Check Your Internet And Try Again later!!")
	else:
		print("failed! Invalid CC!!")
def Bin(Bin):
	if Bin.isdigit() and len(Bin)==6:
		print("\nLuhn Algorithm check Success\n")
		checkbin=binlist.BIN(Bin)
		credit_card=checkbin.lookup().verbose_name
		print(f"CREDIT CARD : {credit_card} ")
		if checkbin.lookup().active==True:
			print("Current Status : ACTIVE! ")
		else:
			print("Current Status : Not ACTIVE!")
		print("Fetching Informations.....\n")
		try:
			online_check=requests.get(f"https://api.bincodes.com/bin/?format=json&api_key={key1}&bin={Bin}")
			result=json.loads(online_check.text)
			print(f"""
			BIN           : {result['bin']}
			BANK          : {result['bank']}
			CARD          : {result['card']}
			TYPE          : {result['type']}
			LEVEL         : {result['level']}
			COUNTRY       : {result['country']}
			COUNTRY_CODE  : {result['countrycode']}
			BANK_WESBSITE : {result['website']}
			PHONE         : {result['phone']}
			VALID         : {result['valid']}
			 """)
		except:
			print("Cannot fetch informations!! Check Your Internet And Try Again later!!")
	else:
		print("Length/value exception! Invalid BIN!!")
def ifsc(ifsc):
	if len(ifsc)==11 and ifsc.isalnum():
		if ifsc.isupper():
			ifsc=ifsc
		elif ifsc.islower():
			ifsc=ifsc.upper()
		try:
			print("\nGathering info....\n")
			data1=BeautifulSoup(requests.post("https://bank.codes/india-ifsc-code-checker/",data={'ifsc':ifsc}).text , "html.parser")
			data=data1.find('table')
			for script in data(["script","style"]):
				script.extract()
			display=data.get_text()
			print(display.strip().replace("Bank","Bank  ").replace("Branch","Branch  ").replace("Address","Address  ").replace("City","City  ").replace("State","State  ").replace("Contact","Contact  ").replace("District","District  ").replace("MICR Number","MICR Number  ").replace("IFSC Code","IFSC Code  "))
		except:
			print("Cannot fetch info!! Something Error! check internet and try again!")
	else:
		print("Length/Alpha numeric exception!! Invalid IFSC!")
def micr(micr):
	if micr.isdigit() and len(micr)==9:
		try:
			print("\nGathering info....\n")
			data=BeautifulSoup(requests.get(f"https://micr.bankifsccode.com/{micr}").text, "html.parser")
			for script in data(["script","style"]):
				script.extract()
			display=data.get_text()
			start=display.strip().find("MICR Code:-")
			repl="""2010 - 20, BankIFSCcode.comDisclaimer: - We have tried our best to keep the latest information updated as available from RBI, users are requested to confirm information with the respective bank before using the information provided. The author reserves the right not to be responsible for the topicality, correctness, completeness or quality of the information provided. Liability claims regarding damage caused by the use of any information provided, including any kind of information which is incomplete or incorrect, will therefore be rejected."""
			result=display.strip()[start:].replace("HOME","").replace(repl,"").replace("|","").replace("LOCATE ANY BRANCH IN INDIA (Select Bank Name - State - District - branch to see Details)","").replace("Find Branch Details/Address/MICR Code By IFSC Code","").replace("Find IFSC/Branch Details By MICR Code","").replace("ALL INDIA BANK LIST","").replace("HELP/CONTACT US","").strip()
			print(result.replace("Bank","  Bank").replace("Branch","  Branch").replace("Address","  Address").replace("City","  City").replace("State","  State").replace("Contact","  Contact").replace("District","  District").replace("MICR Code","  MICR Code").replace("IFSC Code","  IFSC Code").replace("  ","\n").replace("(Click here for all the branches of","").replace(" District)","").replace("\n IFSC Code represent"," IFSC Code represent").replace("\n Branch code."," Branch code."))
		except:
			print("Cannot fetch info!! Something Error! check Internet And try again!")
	else:
		print("Invalid MICR number!!")


		
def num(num):
	if num.startswith("+"):
		number=phonenumbers.parse(num,None)
	else:
		num="+"+num
		number=phonenumbers.parse(num,None)
	try:
		print(f"""\nBasic Informations...
		
		NUMBER            :  {num}
		VALID             :  {phonenumbers.is_valid_number(number)}
		POSSIBLE NUMBER   :  {phonenumbers.is_possible_number(number)}
		CARRIER/ISP       :  {carrier.name_for_number(number,'en')}
		COUNTRY/LOCATION  :  {geocoder.description_for_number(number,'en')}
		TIMEZONES         :  {timezone.time_zones_for_number(number)}
		
		""")
	except:
		print("Something Error!!")
		
	try:
		print("Additional Informations....")
		online_check=requests.get(f"http://apilayer.net/api/validate?access_key={pkey}&number={num}&format=1")
		result=json.loads(online_check.text)
		print(f"""
		NUMBER               :  {result['number']}
		LOCAL_FORMAT         :  {result['local_format']}
		INTERNATIONAL_FROMAT :  {result['international_format']}
		COUNTRY_PREFIX       :  {result['country_prefix']}
		COUNTRY_CODE         :  {result['country_code']}
		COUNTRY NAME         :  {result['country_name']}
		LOCATION             :  {result['location']}
		CARRIER              :  {result['carrier']}
		LINE_TYPE            :  {result['line_type']}
		""")
	except:
		print("Something Error!!")
		


print("""
╔═╗╦═╗╦┌┬┐╦ ╦╔╦╗┌─┐   ╔═╗┌─┐╔╦╗┬ ┬╔═╗┬─┐
╠═╣╠╦╝║ │ ╠═╣║║║│ │───║ ╦├─┤ ║ ├─┤║╣ ├┬┘
╩ ╩╩╚═╩ ┴ ╩ ╩╩ ╩└─┘   ╚═╝┴ ┴ ╩ ┴ ┴╚═╝┴└─
                                        .-----< Coded by FEBIN >------.
                                        |   Gather Info from numbers  | 
                                        |Every numbers could reveal   |
                                        | the personal Informations   |
                                        '-----------------------------'
 """)	
print("""
Available Options:>

[1] Credit Card number info
[2] BIN info (first 6 digits of CC)
[3] IFSC Code info (India only)
[4] MICR number info
[5] Phone Number Info

 """)
try:
	choice=input("Enter the option :> ").strip()
	if choice=="1":
		cc=input("ENTER THE CREDIT CARD NUMBER : ").strip()
		CC(cc)
	elif choice=="2":
		binnum=input("ENTER THE BIN CODE [first 6 digits of the CC] : ").strip()
		Bin(binnum)
	elif choice=="3":
		ifsccode=input("ENTER THE IFSC CODE : ").strip()
		ifsc(ifsccode)
	elif choice=="4":
		micrnum=input("ENTER THE MICR NUMBER : ").strip()
		micr(micrnum)
	elif choice=="5":
		number=input("ENTER THE PHONE NUMBER [with country prefix eg: +91 ] : ").strip()
		num(number)
	else:
		print("Invalid Choice!!")
except KeyboardInterrupt:
	print("\n User Interrupted!! Bye!")
except:

	print("Something Went Wrong")
 			
 			
 			
 			
 			
