import os
import time
import requests
from typing import List, Optional, Dict

BASE_API = "https://api.mangadex.org"
HEADERS = {
    "User-Agent": "python-mangadex-downloader/1.0 (by Hiroshi)",
    "Accept": "application/json"
}

def listar_capitulos(manga_id: str, langs: Optional[List[str]] = None, limit:int = 100) -> List[Dict]:
    """
    Lista capítulos do mangá usando paginação offset.
    Se langs for None, traz todos os idiomas.
    Retorna lista de dicionários com keys: id, chapter, title, lang.
    """
    url = f"{BASE_API}/manga/{manga_id}/feed"
    offset = 0
    capitulos = []

    print(f"-> Consultando feed do mangá {manga_id} (limit={limit}) ...")
    while True:
        params = {
            "limit": limit,
            "offset": offset,
            "order[chapter]": "asc"
        }
        if langs:
            for lang in langs:
                params.setdefault("translatedLanguage[]", []).append(lang)

        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"  Erro {r.status_code} ao consultar feed: {r.text[:200]}")
            break

        j = r.json()
        data = j.get("data", [])
        print(f"  Paginação offset={offset} -> capítulos retornados: {len(data)}")
        if not data:
            break

        for ch in data:
            attrs = ch.get("attributes", {})
            capitulos.append({
                "id": ch.get("id"),
                "chapter": attrs.get("chapter"),
                "title": attrs.get("title"),
                "lang": attrs.get("translatedLanguage"),
                "hash": attrs.get("hash"),
                "attributes": attrs
            })

        if len(data) < limit:
            break
        offset += len(data)
        time.sleep(0.25)

    print(f"-> Total de capítulos listados: {len(capitulos)}")
    return capitulos

def _chapter_sort_key(ch):
    chap = ch.get("chapter")
    try:
        return (0, float(chap))
    except Exception:
        if chap is None:
            return (1, ch["id"])
        return (1, str(chap))

def baixar_capitulo(chapter_id: str, pasta_destino: str, prefer_saver: bool = True):
    """
    Baixa o capítulo usando endpoint at-home/server.
    Se arquivos já existirem na pasta, eles são pulados.
    """
    api_url = f"{BASE_API}/at-home/server/{chapter_id}"
    r = requests.get(api_url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        print(f"    Erro ao obter servidor at-home para capítulo {chapter_id}: {r.status_code}")
        return

    j = r.json()
    base_url = j.get("baseUrl")
    chapter_info = j.get("chapter", {})
    if not base_url or not chapter_info:
        print("    Resposta at-home inesperada, pulando.")
        return

    chap_hash = chapter_info.get("hash")
    pages_saver = chapter_info.get("dataSaver") or chapter_info.get("data-saver")
    pages_full  = chapter_info.get("data") or chapter_info.get("data_full")

    if prefer_saver and pages_saver:
        mode = "data-saver"
        page_list = pages_saver
    elif pages_full:
        mode = "data"
        page_list = pages_full
    else:
        page_list = chapter_info.get("data") or chapter_info.get("dataSaver") or []
        mode = "data-saver" if "dataSaver" in chapter_info else "data"

    if not page_list:
        print("    Nenhuma página encontrada no capítulo (resposta at-home).")
        return

    os.makedirs(pasta_destino, exist_ok=True)
    print(f"    Baixando {len(page_list)} páginas para {pasta_destino} ...")

    for i, filename in enumerate(page_list, start=1):
        ext = os.path.splitext(filename)[1] or ".jpg"
        out_path = os.path.join(pasta_destino, f"{i:03d}{ext}")
        if os.path.exists(out_path):

            print(f"      Página {i} já existe, pulando.")
            continue

        img_url = f"{base_url}/{mode}/{chap_hash}/{filename}"
        try:
            img_r = requests.get(img_url, headers=HEADERS, stream=True, timeout=20)
            if img_r.status_code == 200:
                with open(out_path, "wb") as f:
                    for chunk in img_r.iter_content(1024*32):
                        if chunk:
                            f.write(chunk)
                print(f"      Página {i} salva.")
            else:
                print(f"      Erro {img_r.status_code} ao baixar página {i}: {img_url}")
        except Exception as e:
            print(f"      Exceção ao baixar página {i}: {e}")

        time.sleep(0.15)

def baixar_manga(manga_id: str, lang: Optional[str] = "pt-br", pasta_base: str = "manga", prefer_saver: bool = True):
    """
    Baixa todos os capítulos de um mangá.
    lang: código do idioma (ex: 'pt-br'). Se passar None, busca TODOS os idiomas.
    """
    langs = None if lang is None else [lang]
    caps = listar_capitulos(manga_id, langs=langs)
    if not caps:
        print("\nNenhum capítulo encontrado com os parâmetros informados.")
        print("- Verifique se o 'manga_id' está correto.")
        print("- Verifique se há capítulos no idioma solicitado (ex: 'pt-br').")
        print("- Tente executar com lang=None para listar todos os idiomas.")
        return


    caps_sorted = sorted(caps, key=_chapter_sort_key)

    os.makedirs(pasta_base, exist_ok=True)
    for idx, ch in enumerate(caps_sorted, start=1):
        chap_num = ch.get("chapter") or "no-chapter"

        nome_seguro = str(chap_num).replace("/", "_").replace(" ", "_")
        pasta_cap = os.path.join(pasta_base, f"{idx:03d}_cap_{nome_seguro}")
        print(f"\nCapítulo {idx}: chapter={chap_num} id={ch['id']} lang={ch.get('lang')}")

        if os.path.isdir(pasta_cap) and os.listdir(pasta_cap):
            print("  Pasta já existe e contém arquivos — pulando capítulo.")
            continue

        baixar_capitulo(ch["id"], pasta_cap, prefer_saver=prefer_saver)

if __name__ == "__main__":
    # 
    manga_id = "678b0682-b887-4de4-b774-addf10d16c8b"  # ex: "678b0682-b887-4de4-b774-addf10d16c8b" - Code Geass: A Rebelião de Lelouch 
    # Coloque 'pt-br' ou 'en'
    idioma = "pt-br"


    baixar_manga(manga_id, lang=idioma, pasta_base="meu_manga", prefer_saver=True)
    # baixar_manga(manga_id, lang=idioma, pasta_base="manga", prefer_saver=True)
    pass
