import requests
import pandas as pd
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from typing import Dict
from tqdm import tqdm


def fetch_json(url: str) -> Dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def extract_data(json_data: Dict, link_key: str) -> pd.DataFrame:
    content = json_data["conteudo"]
    df = pd.json_normalize(content)
    df = df[["DataReferencia", "Titulo", link_key]]
    df["Tipo"] = "pdf" if link_key == "Url" else "html"
    df.rename(columns={link_key: "LinkPagina"}, inplace=True)
    return df


def get_copom_data() -> pd.DataFrame:
    base_url = "https://www.bcb.gov.br"
    api_antigas = "/api/servico/sitebcb/atascopom-conteudo/ultimas?quantidade=1000&filtro="
    api_novas = "/api/servico/sitebcb/atascopom/ultimas?quantidade=1000&filtro="

    json_antigas = fetch_json(f"{base_url}{api_antigas}")
    json_novas = fetch_json(f"{base_url}{api_novas}")

    df_antigas = extract_data(json_antigas, "LinkPagina")
    df_novas = extract_data(json_novas, "Url")

    df_atas = pd.concat([df_antigas, df_novas], ignore_index=True)
    return df_atas


def fetch_html_content(link: str, base_url: str = "https://www.bcb.gov.br") -> str:
    api = "/api/servico/sitebcb/atascopom-conteudo/principal?filtro=IdentificadorUrl"
    code = link.split("/")[-1]
    encoded_code = f" eq '{code}'"
    json_url = f"{base_url}{api}{encoded_code}"
    json_response = fetch_json(json_url)

    if "conteudo" in json_response:
        if isinstance(json_response["conteudo"], list) and len(json_response["conteudo"]) > 0:
            first_item = json_response["conteudo"][0]
            if "OutrasInformacoes" in first_item:
                html_content = first_item["OutrasInformacoes"]
                soup = BeautifulSoup(html_content, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                return text
            else:
                raise KeyError("Key 'OutrasInformacoes' not found in the first item of 'conteudo'.")
        else:
            raise TypeError("'conteudo' is not a list or is empty.")
    else:
        raise KeyError("Key 'conteudo' not found in the JSON response.")


def fetch_pdf_content(link: str, base_url: str = "https://www.bcb.gov.br") -> str:
    if not link:
        return "Link vazio ou inválido"

    pdf_url = f"{base_url}{link}"
    response = requests.get(pdf_url)
    response.raise_for_status()

    pdf_document = fitz.open(stream=response.content, filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text


def fetch_content(row) -> str:
    if row["Tipo"] == "pdf":
        return fetch_pdf_content(row["LinkPagina"])
    return fetch_html_content(row["LinkPagina"])


def process_atas() -> pd.DataFrame:
    df_atas = get_copom_data()
    df_atas["integra"] = [fetch_content(row) for _, row in tqdm(df_atas.iterrows(), total=df_atas.shape[0])]
    return df_atas


def parcial(text: str) -> str:
    return f"{text[:500]} (.......) {text[-500:]}"


def main():
    df_atas = process_atas()

    df_pdfs = df_atas[df_atas["Tipo"] == "pdf"]
    df_htmls = df_atas[df_atas["Tipo"] == "html"]

    df_pdfs["parcial"] = df_pdfs["integra"].apply(parcial)
    df_htmls["parcial"] = df_htmls["integra"].apply(parcial)

    df_pdfs.to_parquet("assets/df_pdfs.parquet", compression='brotli')
    df_htmls.to_parquet("assets/df_htmls.parquet", compression='brotli')


if __name__ == "__main__":
    main()
