# Cloudflare DDNS PI

This is a small piece of python code to pull current ip and set the A record DNS entry in Cloudlfare to it. 

## Code Setup

There are a number of of details that need to be personalised. Most of them are retrieved from your cloudflare account except for the Record ID which can be retrieved by doing an api call to list dns records for the domain.
These are contained in a file called apiData.json which has dummy data in it that needs to be repalced.

## Crontab
I wrote this to be run on a pi using crontab to run every 30 minutes.
>*/30 * * * * cd /home/pi/ddns/ && /usr/bin/python3 /home/pi/ddns/ddns.py

As the file references a another file in the foler the crontab has to change directory to the file directory. I preferd doing this over setting an absolute path in the code.
