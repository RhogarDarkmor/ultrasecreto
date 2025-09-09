# Drakkar

Drakkar é uma ferramenta em Python para testar, validar e simular visualizações de transmissões ao vivo (especialmente Twitch) utilizando proxies. Seu objetivo é facilitar o gerenciamento, teste e automação de proxies para aumentar visualizações em lives, seja para fins de teste, demonstração ou pesquisa.

## Principais Funcionalidades

- **Validação de Proxies:** Testa proxies em paralelo, verifica quais estão ativos e prontos para uso.
- **Simulação de Visualizações:** Utiliza threads para simular múltiplas visualizações, com opções para comportamentos humanos realistas.
- **Integração com Selenium:** Permite abrir transmissões usando Selenium e proxies, simulando um usuário real.
- **Interface Gráfica (Tkinter e Qt):** Disponibiliza uma interface amigável para configuração, execução e acompanhamento dos resultados.
- **Extração automática de proxies:** Função para extrair proxies de sites como free-proxy-list.net.

## Uso

### Requisitos

- Python 3.8+
- Instalar as dependências do projeto:
  ```bash
  pip install requests beautifulsoup4 fake-useragent selenium webdriver-manager
  ```

### Exemplo Básico

```python
from projeto import ProxyViewerImproved

proxies = [
    "http://ip1:porta",
    "http://ip2:porta",
    # ...adicione proxies válidos...
]
stream_url = "https://www.twitch.tv/seu_canal"
viewer = ProxyViewerImproved(proxies)
validos = viewer.validate_all_proxies()
for proxy in validos:
    viewer.simulate_selenium_view(proxy, stream_url)
```

### Interface Gráfica

Execute a interface (Tkinter ou Qt) para facilitar o uso:
```bash
python interface.py
# ou
python stream_viewer_qt.py
```

## Como funciona

- **Validação:** Proxies são testados via requisição HTTP, usando User-Agent realista.
- **Simulação:** Visualizações são simuladas com delays e desconexões aleatórias para imitar comportamento humano.
- **Selenium:** Abre o navegador usando proxy para gerar visualização real.

## Licença

Este projeto ainda não possui uma licença definida.

## Autor

Desenvolvido por [RhogarDarkmor](https://github.com/RhogarDarkmor).

---

> **Nota:** Este projeto foi feito para fins educacionais e de pesquisa. O uso indevido pode violar termos de serviço de plataformas de streaming.
