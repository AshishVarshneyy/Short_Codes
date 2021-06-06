import time
import json
import requests
from datetime import datetime, timedelta


def fetch_details():
    HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0;secssobrowser) Gecko/20100101 Firefox/86.0"
        }

    available_result = []
    pincode = 560049
    age = 18
    vaccine_name = 'COVISHIELD'
    current_date = datetime.today()
    date_list = [(current_date + timedelta(days=x)).strftime("%d-%m-%y") for x in range(7)]
    while True:
        for date in date_list:
            url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}"
            response = requests.get(url,headers=HEADER)
            data = response.json()
            for center in data['centers']:
                if center['sessions'][0]['available_capacity'] != 0 and center['sessions'][0]['min_age_limit'] == age and center['sessions'][0]['vaccine'] == vaccine_name:
                    aval_cent = {}
                    aval_cent['DATA'] = date
                    aval_cent['FEES'] = center['fee_type']
                    aval_cent['VAC_NAME'] = center['sessions'][0]['vaccine']
                    aval_cent['CAP'] = center['sessions'][0]['available_capacity']
                    aval_cent['CEN_NAME'] = center['name']
                    aval_cent['ADDRESS'] = f"{center['address']}, {center['district_name']}, {center['state_name']}, {center['pincode']}"
                    available_result.append(aval_cent)
        if len(available_result) != 0:
            send_notification(available_result)
            exit(0)
        else:
            time.sleep(300)


def send_notification(vac_aval_cent_list):
    for center in vac_aval_cent_list:
        print(f"DATE: {center['DATA']}")
        print("Fee Type: {}".format(center['FEES']))
        print("Vaccine Name: {}".format(center['VAC_NAME']))
        print("Available_capacity: {}".format(center['CAP']))
        print("Center Name: {}".format(center['CEN_NAME']))
        print("Address: {}".format(center['ADDRESS']))
        print("====================================================================================")

def main():
    fetch_details()
    

if __name__ == "__main__":
    main()
