from flask import Flask, render_template,request
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re  # re as regular expresion  (REGEX)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input1 = request.form['input1']
        input2 = request.form['input2']
        print(input1, input2)
        action(input1, input2)
        return render_template('index2.html', input1=input1, input2=input2)

    return render_template('index2.html')


def action(user, password):

        #todo if we want to use chrome
        chrome_driver_path = "chromedriver/chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_driver_path)
        yahoo_url = driver.get("https://login.yahoo.com/?.src=ym&lang=en-US&done=https%3A%2F%2Fmail.yahoo.com%2F")


        #todo user input
        login_input = driver.find_element_by_css_selector("#login-username")
        login_input.send_keys(user)
        time.sleep(3)
        id_next_button = driver.find_element_by_css_selector("#login-signin")
        id_next_button.click()
        time.sleep(10)
        print("warmatebit moxda iuzeris chawera")

        #todo pass input   login-signin
        pass_input = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/form/div[2]/input')
        pass_input.send_keys(password)
        time.sleep(3)
        pass_next_button = driver.find_element_by_css_selector("#login-signin")
        pass_next_button.click()

        print("warmatebit moxda parolis sheyvana")
        print(f"shen ukve shesulixar rogorc {user}" )
        time.sleep(10)


        page_num = range(1,100)
        good_tittle = [""]
        email_counter = 0

        sleep_counter = 0
        sleep_time = 300
        break_time = 20


        for number in page_num:
            url = requests.get(f'https://jobs.ge/?page={number}&q=&cid=&lid=1&jid=1')
            soup = bs(url.content, "html.parser")
            links_toJob = soup.find_all("a", class_ = "vip")
            for jobs in links_toJob:
                for tittle in good_tittle:
                    if tittle in jobs.text:
                        info_url = requests.get(f"https://jobs.ge/{jobs['href']}")
                        text_info = bs(info_url.content , "html.parser")
                        email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_info.text)  #[\w.+-]+@[\w-]+\.[\w.-]+
                        job_info = (jobs.text , email , info_url.url)

                        # if TURN_ON_MAIL_SENDING == "ki" or TURN_ON_MAIL_SENDING == "KI":

                        try:
                            #todo compose letter https://mail.yahoo.com/d/compose
                            compose_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[1]/nav/div/div[1]/a")
                            compose_button.click()


                            #todo find "to whom to send"
                            to_whom = driver.find_element_by_xpath('//*[@id="message-to-field"]')
                            to_whom.send_keys(email)
                            time.sleep(2)


                            #todo find subject
                            msg_subject = driver.find_element_by_xpath('//*[@id="mail-app-component"]/div/div/div/div[1]/div[3]/div/div/input')
                            msg_subject.send_keys(jobs.text)
                            time.sleep(2)


                            #Todo  attach the file buttom
                            attach_button = driver.find_element_by_xpath('//*[@id="mail-app-component"]/div/div/div/div[2]/div[2]/div/span[1]/div/div/div/button/span')
                            attach_button.click()
                            time.sleep(3)

                            #todo  attach files from dropbox
                            attach_file_from_dropbox = driver.find_element_by_xpath('//*[@id="app"]/div[7]/div/div[1]/div/ul/li[2]/button/span/span')
                            attach_file_from_dropbox.click()
                            time.sleep(2)


                            #todo  choose resume file from recetn files
                            choose_file = driver.find_element_by_xpath('//*[@id="app"]/div[7]/div[2]/div[1]/div/div[3]/div/div/ul/li/div/div/div[1]')
                            choose_file.click()
                            time.sleep(3)

                            # #todo exit choose resume file from recetn files window
                            # exit_button = driver.find_element_by_xpath('//*[@id="app"]/div[7]/div[2]/div[1]/div/div[1]/div/button/span/svg/path')
                            # exit_button.click()
                            # time.sleep(2)


                            #hit send button
                            send_button = driver.find_element_by_xpath('//*[@id="mail-app-component"]/div/div/div/div[2]/div[2]/div/button/span')
                            send_button.click()
                            time.sleep(10)

                            print(f" {email} - {jobs.text}")


                        except Exception as er2:
                            print (f' >>>  Something went wrong... To {jobs.text}  on {email} counter {sleep_counter}')
                            print(f"  >>>  the reason is {er2}")
                            time.sleep(5)
                            sleep_counter += 1

                        if sleep_counter == break_time:
                            print("now sleeping time !!!")
                            time.sleep(sleep_time)
                            sleep_counter = 0
                            print(sleep_counter)
                    # else:
                    #     print(f"you have turned off mail sending {email_counter}")

if __name__ == '__main__':
    app.run(debug=True)