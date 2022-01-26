from selenium.webdriver import Chrome, ChromeOptions 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Selenium4対応済 
# def set_driver(hidden_chrome: bool=False): 
def set_driver(headless_flg): 
    ''' 
    Chromeを自動操作するためのChromeDriverを起動してobjectを取得する 
    ''' 
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36" 
    options = ChromeOptions() 
    # ヘッドレスモード（画面非表示モード）をの設定 
    if headless_flg == True: #Falseで表示される 
        options.add_argument('--headless') 
    # 起動オプションの設定 
    options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列 
    options.add_argument('log-level=3') # 不要なログを非表示にする 
    options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする 
    options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする 
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする 
    options.add_argument('--incognito') # シークレットモードの設定を付与 
     
    # ChromeのWebDriverオブジェクトを作成する。 
    service=Service(ChromeDriverManager().install()) #必要な  Driverを自動でインストールしてくれる 
     
    return Chrome(service=service, options=options)