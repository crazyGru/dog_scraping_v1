import time
import json
import argparse
import csv


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from restricted_input import r_input
from functions import *
import mysql.connector
import base64, requests, json

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
    driver.get("https://www.nawt.org.uk/rehoming/dogs/")

    # Click accept all button
    "onetrust-accept-btn-handler"
    ts = time.time()
    ACCPET_ALL_BUTTON = '[class *= "ch2-btn ch2-allow-all-btn ch2-btn-primary"]'
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

    
    # Click Next Button
    time.sleep(1)    
    NEXT_BUTTON = '[title="Next page"]'
    count_failed=0
    all_dog_info = []
    all_dog_live_info=[]
    all_dog_id=[]
    all_dog_urls=[]
    all_individual_url=[]
    while count_failed < 2:
        time.sleep(1)
        GET_IMAGE_URL_SCRIPT = '''
            image_urls=[];
            elements=document.querySelectorAll('[class *= "page-cards__image"]');
            elements.forEach(element => {
                const url = element.style.backgroundImage.slice(4, -1).replace(/"/g, "");
                image_urls.push(url);
            });
            return image_urls;
        '''
        all_dog_urls.extend(driver.execute_script(GET_IMAGE_URL_SCRIPT))


        GET_DOG_INDIVIDUAL_PAGE_SCRPIT='''
            dg_individual_urls=[]
            elements=document.querySelectorAll('[class *= "page-cards__image"]');
            elements.forEach(element=>{
                dg_individual_urls.push(element.getAttribute("href"));
            });
            return dg_individual_urls;
        '''
        all_individual_url.extend(driver.execute_script(GET_DOG_INDIVIDUAL_PAGE_SCRPIT))
        

        GET_DOG_ID_SCRIPT = '''
            dog_id=[];
            elements=document.querySelectorAll('[class *= "page-cards__image"]');
            elements.forEach(element => {
                dog_id.push(element.href.match(/\d+/)[0]);
            });
            return dog_id;
        '''
        all_dog_id.extend(driver.execute_script(GET_DOG_ID_SCRIPT))

        get_total_info_script = '''
            eles = document.querySelectorAll('[title="Find out more"]');
            var i = 0;
            dog_info = [];
            for (i = 0; i < eles.length; i++) {
                sentence = eles[i].outerText;
                sentenceArray = sentence.split('\\n').filter(tag => tag.trim().length > 0);
                dog_info.push(sentenceArray);
            }
            return dog_info;
        '''
        temp_dog_info=driver.execute_script(get_total_info_script)
        all_dog_info.extend(temp_dog_info)


        get_dog_live_info_script='''
            const elements = document.querySelectorAll('[class*="page-cards__icons"]');
            dogs_live_detail=[];
            elements.forEach(element => {
                const images = element.querySelectorAll('img');
                dog_live_detail=[];
                images.forEach(image => {
                    const title = image.getAttribute('title');
                    dog_live_detail.push(title);
                });
                dogs_live_detail.push(dog_live_detail);
            });
            return dogs_live_detail;
        '''
        temp_dog_live_info=driver.execute_script(get_dog_live_info_script)
        all_dog_live_info.extend(temp_dog_live_info)
        

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, NEXT_BUTTON))
            )
            driver.find_element(By.CSS_SELECTOR, NEXT_BUTTON).click()
            count_failed=0
        except:
            count_failed +=1
            print('Can\'t Click choose show more button!')
            break
        
    dog_introductions=[]
    for individual_url in all_individual_url:
        driver.get("https://www.nawt.org.uk"+individual_url)
        GET_INTRO_SCRIPT='''
            return document.querySelector('[class *= "intro"]').textContent;
        '''
        dog_introductions.append(driver.execute_script(GET_INTRO_SCRIPT))


    for temp_url in all_dog_urls:
        driver.get(temp_url)

    connection = mysql.connector.connect(
       host="35.214.46.153",
       user="upbhfcibi1c6j",
       password="@7h35@1i5@@3",
       database="dbuabl3ljbq6px"
    )

    cursor=connection.cursor()

    file_name='dog_info.csv'

    hed = header("DEVGURU","ptJl zgJu T2a5 DaZ8 fcnC QOKg")   

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'Name', 'Status', 'Location', 'Age', 'Sex', 'Breed', 'Dog', 'Cat', 'Children', 'Can live with older children', 'Microchipped', 'Neutered', 'Alone', 'Src'])
        for dog, dog_live_info, dog_id, src_url, dog_intro in zip(all_dog_info, all_dog_live_info, all_dog_id, all_dog_urls, dog_introductions):
            dog_info_sentence = ', '.join(dog_live_info).lower()
            print(dog, dog_live_info)
            dog_info = []
            dog_info.append(dog_id) # id
            dog_info.append(dog[0]) # Name
            dog_info.append(dog[1]) # Status
            dog_info.append(dog[2]) # Location
            age_gender = dog[3].split(', ')
            dog_info.append(age_gender[0]) # Age
            dog_info.append(age_gender[1]) # Sex 
            dog_info.append(dog[4]) # Breed
            details = dog[5].split(', ')
            #dog_info.append('1' if 'dog' in dog_info_sentence and 'not dog friendly' not in dog_info_sentence else '0') # Can live with dogs
            

            if 'not dog' in dog_info_sentence.lower(): dog_info.append('0')
            elif 'dog' in dog_info_sentence.lower(): dog_info.append('1')
            else: dog_info.append('2')
                
            #dog_info.append('1' if 'cat' in dog_info_sentence and 'not cat friendly' not in dog_info_sentence else '0') # Can live with cats
            
            if 'not cat' in dog_info_sentence.lower(): dog_info.append('0')
            elif 'cat' in dog_info_sentence.lower(): dog_info.append('1')
            else: dog_info.append('2')

            #dog_info.append('1' if 'child' in dog_info_sentence else '0') # Can live with small children
            
            if 'not child' in dog_info_sentence.lower(): dog_info.append('0')
            elif 'child' in dog_info_sentence.lower(): dog_info.append('1')
            else: dog_info.append('2')

            #dog_info.append('1' if 'Older Children' in dog_info_sentence else '0') # Can live with older children
            
            if 'not older' in dog_info_sentence.lower(): dog_info.append('0')
            elif 'older' in dog_info_sentence.lower(): dog_info.append('1')
            else: dog_info.append('2')

            dog_info.append('1' if 'Microchipped' in dog_info_sentence else '1') # Microchipped
            dog_info.append('1' if 'Neutered' in dog_info_sentence else '1') # Neutered

            #dog_info.append('0' if 'cannot be left alone' in dog_info_sentence else '1') # Can be left alone
            if 'alone' in dog_info_sentence.lower(): dog_info.append('1')
            elif 'cannot' in dog_info_sentence.lower(): dog_info.append('0')
            else: dog_info.append('2')

            dog_info.append(dog_intro)

            if "=" in src_url:
                id = src_url.split('=')[1]
            else:
                id = src_url.split('/')[-1].split('.')[0]
            if "&" in src_url:
                dimensions = src_url.split('&')[1].split('=')[1]
            else:
                dimensions = "unknown"
            # Create the new filename
            dimensions="450x400"
            filename = f"{id[:-2]}_{dimensions}.jpg"

            dog_info.append(filename)

            sql = "INSERT INTO `wp_dogs`(`dog_id`, `dog_name`, `dog_status`, `dog_location`, `dog_age`, `dog_sex`, `dog_breed`, `dog_dog`, `dog_cat`, `dog_children`, `dog_olderchildren`, `dog_microchipped`, `dog_neutered`, `dog_alone`, `dog_intro`, `dog_image`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `dog_status` = VALUES(`dog_status`), `dog_location` = VALUES(`dog_location`), `dog_age` = VALUES(`dog_age`), `dog_sex` = VALUES(`dog_sex`), `dog_breed` = VALUES(`dog_breed`), `dog_dog` = VALUES(`dog_dog`), `dog_cat` = VALUES(`dog_cat`), `dog_children` = VALUES(`dog_children`), `dog_olderchildren` = VALUES(`dog_olderchildren`), `dog_microchipped` = VALUES(`dog_microchipped`), `dog_neutered` = VALUES(`dog_neutered`), `dog_alone` = VALUES(`dog_alone`)"
            values = (dog_info[0], dog_info[1], dog_info[2], dog_info[3], dog_info[4], dog_info[5], dog_info[6], dog_info[7], dog_info[8], dog_info[9], dog_info[10], dog_info[11], dog_info[12], dog_info[13], dog_info[14], dog_info[15])
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
            
            file_path = r"C://Users//Administrator//Downloads//{}_{}.png".format(id[:-2], dimensions)
            upload_image_to_wordpress(file_path, 'https://www.dogowner.co.uk/',hed)
            writer.writerow(dog_info)
            
            
    cursor.close()
    connection.close() 
