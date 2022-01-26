import os
import threading 
from selenium.webdriver import Chrome, ChromeOptions 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager 
import time 
import pandas as pd
import traceback
import math
# chromedriver.pyを設置すること
import chromedriver as chr

# 検索件数を調べページ数を計算する
def calc_total_pages(driver, keyword, ITEMS_PER_PAGE):
  elem_input = driver.find_element(By.CSS_SELECTOR, value='.topSearch__text')
  elem_input.send_keys(keyword)
  time.sleep(5)
  #検索ボタンを押す
  driver.find_element(By.CLASS_NAME, value='iconFont--search').click()
  #情報件数を取得
  total_search = driver.find_element(By.CSS_SELECTOR, value='.result__num').find_element(By.TAG_NAME, value="em").text
  print(f'{total_search}件です。')
  time.sleep(5)
  
  #ページ数を求める
  page = math.ceil(int(total_search)/ITEMS_PER_PAGE)
  
  return page


#URLに付加する検索キーワードを生成する関数
def make_paramaters(words):
    word_list = words.split()
    num = len(word_list)
    count = 1
    words_search = ''
    for word in word_list:
      if num == count:
        words_search = words_search + f'kw{word}'
      else:
        words_search = words_search + f'kw{word}_'
      count += 1
    return words_search



def find_table_col_by_header_name(th_elms, td_elms, target:str):
  for th_elm, td_elm in zip(th_elms, td_elms):
    if th_elm.text == target:
      return td_elm.text

    '''table要素の中から、targetで指定したheaderを探し、対応するカラムのdataを取得する
    '''

def scraping_one_page(TARGET_SITE, driver, paramaters_search, page_number):
  df = pd.DataFrame()
  
  try:
    URL = TARGET_SITE + 'list/' + paramaters_search + '/pg' + str(page_number) + '/'
    print(URL)
    driver.get(URL)
        
    #検索された情報の大枠を取得
    results = driver.find_elements(By.CSS_SELECTOR, value='.cassetteRecruit')
    for result in results:
      name = result.find_element(By.CSS_SELECTOR, value=".cassetteRecruit__name").text
      copy = result.find_element(By.CLASS_NAME, value="cassetteRecruit__copy").text
      work = result.find_element(By.CLASS_NAME, value="tableCondition__body").text 
      table_elm = result.find_element(By.TAG_NAME, value='table')
      #初年度年収をtableから探す
      first_year_fee = find_table_col_by_header_name(table_elm.find_elements(by=By.TAG_NAME, value="th"), table_elm.find_elements(by=By.TAG_NAME, value="td"), "初年度年収")
      if first_year_fee == None:
        first_year_fee = '情報なし'

      df = df.append({
        "企業名": name,
        "キャッチコピー": copy,
        "仕事内容": work,
        "初年度年収": first_year_fee }, ignore_index=True)
  except:
    print(traceback.format_exc())
  
  print(df)        
  #return temp_list


def main():
  TARGET_SITE = "https://tenshoku.mynavi.jp/"
  ITEMS_PER_PAGE = 50
  driver = chr.set_driver(False)
  # Webサイトを開く
  driver.get(TARGET_SITE)
  time.sleep(5)
  
  # ポップアップを閉じる
  driver.execute_script('document.querySelector(".karte-close").click()')
  time.sleep(2)
  # ポップアップを閉じる
  driver.execute_script('document.querySelector(".karte-close").click()')

  #検索キーワードを入力
  #keyword = input('検索したいキーワードを入力して下さい。>>>')
  keyword = '新宿区 Python'
  
 # 検索件数を調べページ数を計算する
  total_pages = calc_total_pages(driver, keyword, ITEMS_PER_PAGE)
    
  #パラメーターを生成する
  paramaters_search = make_paramaters(keyword)
  for i in range(1, total_pages + 1):
    t= threading.Thread(target=scraping_one_page(TARGET_SITE,driver, paramaters_search, i))
    t.start()
  

  driver.quit()
  # df.to_csv('res20229121_3.csv', encoding='utf-8_sig')     
     
if __name__ == "__main__":

  main()