# Imports principais
import requests
import random
import time
import logging
import re
import concurrent.futures
from threading import Thread, Semaphore
try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None
from bs4 import BeautifulSoup

def generate_test_proxies(count=50):
    """Gera endereços de proxy fictícios para testes de desenvolvimento"""
    import random
    test_proxies = []
    for i in range(count):
        ip = f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
        port = random.randint(8000, 9000)
        test_proxies.append(f"http://{ip}:{port}")
    return test_proxies

class ProxyViewerImproved:

    def simulate_selenium_view(self, proxy, stream_url, min_time=60, max_time=180):
        """
        Usa Selenium para abrir a live da Twitch com o proxy informado e simula uma visualização real.
        :param proxy: Proxy no formato http://ip:porta
        :param stream_url: URL da live da Twitch
        :param min_time: Tempo mínimo de permanência (segundos)
        :param max_time: Tempo máximo de permanência (segundos)
        """
        import time
        import random
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.common.exceptions import WebDriverException
        from webdriver_manager.chrome import ChromeDriverManager

        chrome_options = Options()
        chrome_options.add_argument(f'--proxy-server={proxy}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=800,600')
        # Não usar headless para evitar detecção

        driver = None
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(stream_url)
            # Espera o player carregar
            time.sleep(random.uniform(8, 15))
            # Permanece na live por tempo aleatório
            view_time = random.randint(min_time, max_time)
            time.sleep(view_time)
        except WebDriverException as e:
            print(f"[Selenium] Erro com proxy {proxy}: {e}")
        finally:
            if driver:
                driver.quit()
    """
    Classe melhorada para validação paralela de proxies com User-Agent realista.
    """
    def __init__(self, proxy_list, max_workers=10, validate_timeout=3):
        self.proxy_list = proxy_list
        self.valid_proxies = []
        self.max_workers = max_workers
        self.validate_timeout = validate_timeout
        if UserAgent:
            try:
                self.ua = UserAgent()
            except Exception:
                self.ua = None
        else:
            self.ua = None


    def validate_proxy(self, proxy):
        return self.validate_proxy_with_timeout(proxy, timeout=self.validate_timeout)

    def validate_proxy_with_timeout(self, proxy, timeout=8):
        """Testa proxy com timeout customizado e headers realistas"""
        try:
            headers = {'User-Agent': self.ua.random if self.ua else 'Mozilla/5.0'}
            import requests
            response = requests.get(
                'http://httpbin.org/ip',
                proxies={'http': proxy, 'https': proxy},
                timeout=timeout,
                headers=headers
            )
            return proxy if response.status_code == 200 else None
        except requests.exceptions.RequestException:
            return None

    def validate_all_proxies(self):
        """Valida proxies em paralelo para melhor performance"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.validate_proxy, self.proxy_list)
            self.valid_proxies = [proxy for proxy in results if proxy]
        return self.valid_proxies

class ProxyViewer:

    def simulate_human_view(self, proxy, stream_url, min_connect=3, max_connect=8, min_view=60, max_view=300, early_exit_chance=0.3, min_early=10, max_early=45):
        """
        Simula comportamento humano mais realista ao assistir um stream.
        :param proxy: Proxy a ser usado
        :param stream_url: URL do stream (não acessa de fato, apenas simula)
        :param min_connect: Tempo mínimo de conexão (s)
        :param max_connect: Tempo máximo de conexão (s)
        :param min_view: Tempo mínimo de visualização (s)
        :param max_view: Tempo máximo de visualização (s)
        :param early_exit_chance: Chance de desconexão precoce (0-1)
        :param min_early: Tempo mínimo de saída precoce (s)
        :param max_early: Tempo máximo de saída precoce (s)
        """
        import logging
        try:
            connect_delay = random.uniform(min_connect, max_connect)
            time.sleep(connect_delay)

            view_duration = random.randint(min_view, max_view)
            time.sleep(view_duration)

            if random.random() < early_exit_chance:
                early_exit = random.randint(min_early, max_early)
                time.sleep(early_exit)
                logging.info(f"Desconexão precoce via {proxy} após {early_exit}s")

            logging.info(f"Visualização simulada via {proxy} por {view_duration}s (stream: {stream_url})")
        except Exception as e:
            logging.error(f"Erro com proxy {proxy}: {str(e)}")
    """
    Classe para testar proxies e simular visualizações usando múltiplas threads.
    """
    def __init__(self, proxy_list, timeout=10, max_threads=10):
        """
        :param proxy_list: Lista de proxies (str)
        :param timeout: Timeout para teste de proxy (segundos)
        :param max_threads: Número máximo de threads simultâneas
        """
        self.proxy_list = proxy_list
        self.timeout = timeout
        self.max_threads = max_threads
        self.active = False
        self.results = []
        self.semaphore = Semaphore(max_threads)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

    def is_valid_proxy(self, proxy):
        """Valida o formato do proxy (http[s]://ip:porta)"""
        pattern = r'^https?://[\w\.-]+:\d{2,5}$'
        return re.match(pattern, proxy) is not None

    def test_proxy(self, proxy):
        """Testa se o proxy está funcionando"""
        try:
            response = requests.get(
                'http://httpbin.org/ip',
                proxies={'http': proxy, 'https': proxy},
                timeout=self.timeout
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logging.warning(f"Proxy {proxy} falhou: {e}")
            return False

    def simulate_view(self, proxy):
        """Simula uma visualização (apenas espera aleatória)"""
        with self.semaphore:
            try:
                logging.info(f"Tentando conectar via {proxy}")
                time.sleep(random.randint(5, 15))
                self.results.append((proxy, 'sucesso'))
            except Exception as e:
                logging.error(f"Erro com proxy {proxy}: {e}")
                self.results.append((proxy, f'erro: {e}'))

    def start(self):
        """Inicia o teste e simulação de visualizações usando os proxies válidos e funcionais."""
        self.active = True
        threads = []
        self.results = []

        for proxy in self.proxy_list:
            if not self.active:
                break
            if not self.is_valid_proxy(proxy):
                logging.warning(f"Proxy inválido: {proxy}")
                self.results.append((proxy, 'inválido'))
                continue
            if self.test_proxy(proxy):
                thread = Thread(target=self.simulate_view, args=(proxy,))
                thread.start()
                threads.append(thread)
                time.sleep(0.5)  # Delay entre conexões
            else:
                self.results.append((proxy, 'falhou'))

        for thread in threads:
            thread.join()
        logging.info(f"Resultados: {self.results}")
        return self.results

def fetch_proxies_from_free_proxy_list_net():
    """Extrai proxies do site free-proxy-list.net usando BeautifulSoup"""
    url = 'https://free-proxy-list.net/'
    proxies = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', id='proxylisttable')
        if not table:
            print('Tabela de proxies não encontrada! O HTML retornado foi:')
            print(response.text[:1000])  # Mostra só o início para debug
            return []
        for row in table.tbody.find_all('tr'):
            cols = row.find_all('td')
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            https = cols[6].text.strip()
            if https == 'yes':
                proxies.append(f'http://{ip}:{port}')
        return proxies
    except Exception as e:
        print(f'Erro ao buscar proxies de free-proxy-list.net: {e}')
        return []

if __name__ == "__main__":
    # Exemplo de uso: simular visualizações reais na Twitch com Selenium
    proxies = [
        'http://proxy1:porta',
        'http://proxy2:porta',
        # ...adicione proxies válidos aqui...
    ]
    stream_url = 'https://www.twitch.tv/seu_canal'  # Substitua pelo link da live desejada
    viewer = ProxyViewerImproved(proxies)
    valid_proxies = viewer.validate_all_proxies()
    print(f"Proxies válidos: {valid_proxies}")
    for proxy in valid_proxies:
        print(f"Abrindo Selenium com proxy {proxy}")
        viewer.simulate_selenium_view(proxy, stream_url)

    proxies = fetch_proxies_from_free_proxy_list_net()
    print("Proxies extraídos:")
    for proxy in proxies:
        print(proxy)
