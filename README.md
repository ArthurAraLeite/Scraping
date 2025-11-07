Aqui está o conteúdo de um arquivo `README.md` completo explicando o código `webscrapping.py`, suas funções e como utilizá-lo:

---

```
# 🕸️ MangaDex WebScraper

Este projeto é um **script Python** para **baixar capítulos de mangás** diretamente da [API do MangaDex](https://api.mangadex.org).  
Ele automatiza o processo de listar e baixar capítulos, salvando cada imagem em pastas organizadas por capítulo.

---

## 🧠 Visão Geral

O script realiza três etapas principais:

1. **Listar capítulos** de um mangá específico, com suporte a idiomas e paginação.
2. **Baixar páginas** (imagens) de cada capítulo usando o endpoint `at-home/server`.
3. **Salvar capítulos** em uma estrutura de pastas organizada, evitando duplicações.

---

## ⚙️ Requisitos

Antes de executar, instale as dependências necessárias:

```bash
pip install requests
````

## 📂 Estrutura do Projeto

```
webscrapping.py   # Script principal
README.md         # (este arquivo)
meu_manga/        # Pasta onde os capítulos serão salvos (gerada automaticamente)
```

Cada capítulo será salvo dentro de uma subpasta numerada, por exemplo:

```
meu_manga/
 ├── 001_cap_1/
 │    ├── 001.jpg
 │    ├── 002.jpg
 │    └── ...
 ├── 002_cap_2/
 │    ├── 001.jpg
 │    ├── 002.jpg
 │    └── ...
```

---

## 🧩 Estrutura do Código

### `listar_capitulos(manga_id, langs=None, limit=100)`

Lista todos os capítulos disponíveis de um mangá usando a API `/manga/{id}/feed`.

* **Parâmetros:**

  * `manga_id` *(str)* — ID do mangá no MangaDex.
  * `langs` *(List[str] | None)* — Lista de idiomas (ex: `["pt-br", "en"]`).
  * `limit` *(int)* — Quantidade de capítulos por página da API.

* **Retorna:** lista de dicionários com informações dos capítulos:

  ```python
  [
    {"id": "uuid", "chapter": "1", "title": "Título", "lang": "pt-br", ...},
    ...
  ]
  ```

---

### `_chapter_sort_key(ch)`

Função auxiliar que organiza os capítulos numericamente.
Usada internamente por `baixar_manga()` para garantir a ordem correta.

---

### `baixar_capitulo(chapter_id, pasta_destino, prefer_saver=True)`

Baixa todas as páginas de um capítulo.

* **Parâmetros:**

  * `chapter_id` *(str)* — ID do capítulo.
  * `pasta_destino` *(str)* — Caminho onde as imagens serão salvas.
  * `prefer_saver` *(bool)* — Se `True`, usa o modo *data-saver* (imagens menores).

* **Comportamento:**

  * Cria a pasta de destino se não existir.
  * Ignora imagens que já existem.
  * Faz pequenas pausas entre downloads (respeitando o servidor).

---

### `baixar_manga(manga_id, lang="pt-br", pasta_base="manga", prefer_saver=True)`

Baixa todos os capítulos de um mangá.

* **Parâmetros:**

  * `manga_id` *(str)* — ID do mangá (encontrado na URL do MangaDex).
  * `lang` *(str | None)* — Código de idioma (`"pt-br"`, `"en"`, etc.).
  * `pasta_base` *(str)* — Pasta raiz para salvar os capítulos.
  * `prefer_saver` *(bool)* — Define se baixa imagens compactadas.

---

### `if __name__ == "__main__":`

Bloco de execução principal.
Exemplo já incluso no código:

```python
if __name__ == "__main__":
    manga_id = "678b0682-b887-4de4-b774-addf10d16c8b"  # Code Geass: A Rebelião de Lelouch
    idioma = "pt-br"
    baixar_manga(manga_id, lang=idioma, pasta_base="meu_manga", prefer_saver=True)
```

---

## 🚀 Como Usar

1. **Obtenha o ID do mangá** no site do MangaDex:
   Exemplo de URL:

   ```
   https://mangadex.org/title/678b0682-b887-4de4-b774-addf10d16c8b/code-geass
   ```

   O ID é o trecho após `/title/`.

2. **Execute o script:**

   ```bash
   python webscrapping.py
   ```

3. **Espere o download terminar.**
   O progresso será mostrado no terminal.

---

## 🔍 Opções e Dicas

* Para listar **todos os idiomas disponíveis**, use:

  ```python
  baixar_manga(manga_id, lang=None)
  ```
* Para baixar **somente inglês**:

  ```python
  baixar_manga(manga_id, lang="en")
  ```
* Para evitar redownload de capítulos já salvos, o script verifica se a pasta já contém arquivos.

---

## 🧱 Exemplo Completo

```python
from webscrapping import baixar_manga

manga_id = "678b0682-b887-4de4-b774-addf10d16c8b"  # ID do mangá
baixar_manga(manga_id, lang="pt-br", pasta_base="code_geass", prefer_saver=True)
```

---

## ⚠️ Aviso Legal

Este script é apenas para **uso pessoal e educacional**.
O MangaDex hospeda conteúdo de diversos autores e tradutores — **respeite os direitos autorais** e as diretrizes da plataforma.

```

---

Deseja que eu gere esse arquivo `.md` pronto para download (`readme.md`) com esse conteúdo?
```
