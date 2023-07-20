import time
import json
import argparse
import csv


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from restricted_input import r_input

from setting import *
from functions import *

import mysql.connector
import base64, requests, json
import os
from datetime import datetime

def header(user, password):
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())
    header_json = {'Authorization': 'Basic ' + token.decode('utf-8')}
    return header_json

def upload_image_to_wordpress(file_path, url, header_json):
    media = {'file': open(file_path,"rb"),'caption': 'My great demo picture'}
    responce = requests.post(url + "wp-json/wp/v2/media", headers = header_json, files = media)
    print(responce)

if __name__ == '__main__':

    driver = webdriver.Chrome()
    driver.get("https://www.dogstrust.org.uk/rehoming/dogs/")

    # Click accept all button
    "onetrust-accept-btn-handler"
    ts = time.time()
    ACCPET_ALL_BUTTON = '[id *= "onetrust-accept-btn-handler"]'
    while time.time()-ts < 20 :
        time.sleep(1)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ACCPET_ALL_BUTTON))
            )
            driver.find_element(By.CSS_SELECTOR, ACCPET_ALL_BUTTON).click()
            print ("Succeed")
            break
        except:
            print('Can\'t Click choose accept all button!')


    # Click Show More Button
    time.sleep(1)    
    SHOW_MORE_BOTTON = '[class *= "SectionDogList-module--showmorebutton"]'
    count_failed=0
    while count_failed < 1:
        time.sleep(1)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SHOW_MORE_BOTTON))
            )
            driver.find_element(By.CSS_SELECTOR, SHOW_MORE_BOTTON).click()
            count_failed=0
        except:
            count_failed +=1
            print('Can\'t Click choose show more button!')

    #Click Dog Cards
    time.sleep(1)
    dogURLs = []
    try:
        js_script = 'eles = document.querySelectorAll("[class *= \\"SectionDogList-module--component\\"] a[href]");\
            var i = 0;\
            urls = [];\
            for (i = 0; i < eles.length; i++) {\
                urls.push(eles[i].getAttribute("href"));\
            }\
            return urls;\
            '
        dogURLs = driver.execute_script(js_script)
        print(dogURLs)
    except:
        print("Can't click Card")
        pass

    connection = mysql.connector.connect(
       host="35.214.46.153",
       user="upbhfcibi1c6j",
       password="@7h35@1i5@@3",
       database="dbuabl3ljbq6px"
    )

    cursor=connection.cursor()
    hed = header("DEVGURU","ptJl zgJu T2a5 DaZ8 fcnC QOKg")

    for url in dogURLs:
        if '/rehoming/dogs/' not in url:
            continue
        
        driver.get(f'https://www.dogstrust.org.uk{url}')
        temp_dog_name=''
        try:
            get_name_js_script = 'return document.querySelector(".SectionDogBio-module--text--a4c24 h1").textContent;'
            temp_dog_name = driver.execute_script(get_name_js_script)
        except Exception as e:
            # Handle the exception here
            print("An error occurred:", str(e))
            continue

        get_INTRO_js_script='''
        var eles = document.querySelectorAll(".SectionTitleBody-module--textarea--4ca48 p");
        var i = 0;
        var info = '';
        for (i = 0; i < eles.length; i++) {
            info+=eles[i].textContent;
        }
        return info;
        '''
        temp_dog_intro=driver.execute_script(get_INTRO_js_script)

        get_info_js_script = '''
        var eles = document.querySelectorAll(".SectionDogBio-module--value--994d8 a");
        var i = 0;
        var info = [];
        for (i = 0; i < eles.length; i++) {
            info.push(eles[i].text);
        }
        return info;
        '''
        tmp_inf=driver.execute_script(get_info_js_script)        
        print(temp_dog_name, tmp_inf, temp_dog_intro)
        with open('dog_info.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the header row if the file is empty
            if file.tell() == 0:
                writer.writerow(['Name', 'Status', 'Location','Age','Sex','Breed','Dog','Cat','Children','Older_Children','Microchipped','Neutered','Alone','Src'])
            # Write the data row
            if tmp_inf[3] in ["Large", "Medium", "Small"]:
                tmp_inf[3] = tmp_inf[4]
            
            with_dog=2
            if "Dogs" in tmp_inf:
                with_dog=1

            with_cat=2
            if "Cats" in tmp_inf:
                with_cat=1

            with_child=2
            if "Secondary" in tmp_inf:
                with_child=1

            with_alone=2
            if "Alone" in tmp_inf:
                with_alone=1

            strkey=datetime.now().strftime("%Y%m%d%H%M%S")
            save_dog_name=temp_dog_name.replace(" ", "_")
            writer.writerow([temp_dog_name, 'available', tmp_inf[3],tmp_inf[1],tmp_inf[2],tmp_inf[0],0,0,0,0,0,0,0,save_dog_name+".jpeg"])
            sql = "INSERT INTO `wp_dogs`(`dog_name`, `dog_status`, `dog_location`, `dog_age`, `dog_sex`, `dog_breed`, `dog_dog`, `dog_cat`, `dog_children`, `dog_olderchildren`, `dog_microchipped`, `dog_neutered`, `dog_alone`,`dog_intro`, `dog_image`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `dog_status` = VALUES(`dog_status`), `dog_location` = VALUES(`dog_location`), `dog_age` = VALUES(`dog_age`), `dog_sex` = VALUES(`dog_sex`), `dog_breed` = VALUES(`dog_breed`), `dog_dog` = VALUES(`dog_dog`), `dog_cat` = VALUES(`dog_cat`), `dog_children` = VALUES(`dog_children`), `dog_olderchildren` = VALUES(`dog_olderchildren`), `dog_microchipped` = VALUES(`dog_microchipped`), `dog_neutered` = VALUES(`dog_neutered`), `dog_alone` = VALUES(`dog_alone`), `dog_image` = VALUES(`dog_image`)"
            values = (temp_dog_name, 'available', tmp_inf[3], tmp_inf[1], tmp_inf[2], tmp_inf[0], with_dog, with_cat, with_child, with_child, 1, 1, with_alone,temp_dog_intro, save_dog_name + strkey +".webp")

            try:
                cursor.execute(sql, values)
                connection.commit()
                print("Data inserted successfully!")
            except mysql.connector.IntegrityError as e:
                if e.errno == 1062:
                    print("Duplicate entry found. Handle the duplicate entry case.")
                    continue
                else:
                    print("An error occurred:", e)    

        file_path = "C:\\Users\\Administrator\\Downloads\\" + save_dog_name +strkey +".jpeg"
        if not os.path.exists(file_path):
            get_img_js_script = '''
            const imgUrlElement = document.querySelector('[class*="IntroDogBio-module--imagewrapper--094a3"] picture source');
            let imgUrl = "";

            if (imgUrlElement) {
                imgUrl = imgUrlElement.getAttribute("srcset").split(",")[0].trim().split(" ")[0];
            }

            if (imgUrl) {
                const xhr = new XMLHttpRequest();
                xhr.open("GET", imgUrl, true);
                xhr.responseType = "arraybuffer";
                xhr.onload = function () {
                    if (this.status === 200) {
                    const blob = new Blob([this.response], { type: "image/jpeg" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "%s.jpeg";
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                    }
                };
                xhr.send();
            }
            ''' % (save_dog_name + strkey)
       
            temp_dog_img=driver.execute_script(get_img_js_script) 
            time.sleep(0.1)
            
            print(file_path)
            print(os.path.exists(file_path))
            if os.path.exists(file_path):
                upload_image_to_wordpress(file_path, 'https://www.dogowner.co.uk/', hed)
            else:
                print("File does not exist.")