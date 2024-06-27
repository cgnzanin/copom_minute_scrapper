
# COPOM Minutes Scraper

Este projeto é uma aplicação de web scraping em Python para extrair e processar as atas das reuniões do COPOM (Comitê de Política Monetária do Banco Central do Brasil).

## Funcionalidades

- Extrai dados de atas de reuniões antigas e novas do COPOM.
- Processa tanto conteúdos HTML quanto PDFs.
- Salva os textos extraídos em um arquivo de saída.

## Estrutura do Projeto

- `fetch_json(url: str) -> dict`: Faz uma requisição GET para a URL fornecida e retorna o JSON.
- `extract_data(json_data: dict, link_key: str) -> pd.DataFrame`: Normaliza o conteúdo do JSON e extrai colunas específicas.
- `get_copom_data() -> pd.DataFrame`: Combina dados de APIs de atas antigas e novas em um único DataFrame.
- `fetch_html_content(link: str, base_url: str = "https://www.bcb.gov.br") -> str`: Extrai e processa o conteúdo HTML das atas antigas.
- `fetch_pdf_content(link: str, base_url: str = "https://www.bcb.gov.br") -> str`: Faz uma requisição GET para a URL do "PDF" e processa o conteúdo.
- `fetch_content(row)`: Determina o tipo de conteúdo (PDF ou HTML) e chama a função apropriada para extrair o texto.
- `process_atas() -> pd.DataFrame`: Processa as atas e extrai o conteúdo completo para cada uma.
- `parcial(text: str) -> str`: Extrai partes do texto para visualização.
- `main()`: Executa o processo completo e salva o resultado em um arquivo de saída.

## Requisitos

- Python 3.8+
- Bibliotecas Python listadas no arquivo `requirements.txt`

## Como Usar

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/copom-minutes-scraper.git
    cd copom-minutes-scraper
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scriptsctivate  # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute o script:
    ```bash
    python main.py
    ```

## Saída

O script gera um arquivo `df_atas.fst` na pasta `assets`, contendo as atas das reuniões do COPOM processadas.

## Licença

Este projeto está licenciado sob a MIT License.
