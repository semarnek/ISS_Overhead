import requests
from datetime import datetime
import smtplib

MY_LAT = 38.933365
MY_LONG = 32.859741
my_email = YOUR_EMAIL
passw = YOUR_PASS

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


time_now = datetime.now()
time_now = time_now.hour

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.


if (MY_LAT-5 <= iss_latitude <= MY_LAT+5) and (MY_LONG-5 <= iss_longitude <= MY_LONG+5):
    if time_now >= sunset or time_now <= sunrise:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=passw)
            connection.sendmail(from_addr=my_email, to_addrs=TO_EMAIL,
                                msg="Subject: Look Up!\n\nISS is above you.")
