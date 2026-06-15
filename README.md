# TikTok Comments Exporter

Ferramenta de linha de comando para exportar comentarios publicos de videos do TikTok em JSON.

## Destaques

- Codigo refeito em uma estrutura limpa e modular.
- Aceita ID, URL normal e URL curta do TikTok.
- Exporta comentarios com metadados uteis: usuario, nickname, texto, data, avatar, likes e replies.
- Coleta todos os comentarios por padrao; use `--limit` para limitar.
- Permite acelerar a coleta ignorando replies com `--no-replies`.
- Salva JSON bonito por padrao ou compacto com `--compact`.
- Exporta CSV, TXT e XLSX (Excel) alem do JSON.
- Mostra progresso da coleta no terminal (silenciavel com `--quiet`).
- Pega a legenda do video na propria coleta, sem requisicao extra.
- Usa mensagens de erro amigaveis no terminal.

## Requisitos

- Python 3.11 ou superior
- requests
- click
- openpyxl (para exportar XLSX)

## Instalacao

```sh
git clone https://github.com/Servico/tiktok-comments-exporter.git
cd tiktok-comments-exporter

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

No Linux/macOS:

```sh
source venv/bin/activate
```

## Uso

Com ID do video:

```sh
python main.py --video 7418294751977327878 --output data
```

Com URL:

```sh
python main.py --video "https://www.tiktok.com/@usuario/video/7418294751977327878"
```

Limitando a quantidade de comentarios:

```sh
python main.py --video 7418294751977327878 --limit 100
```

Sem coletar replies:

```sh
python main.py --video 7418294751977327878 --no-replies
```

JSON compacto:

```sh
python main.py --video 7418294751977327878 --compact
```

CSV:

```sh
python main.py --video 7418294751977327878 --format csv
```

TXT (legivel):

```sh
python main.py --video 7418294751977327878 --format txt
```

XLSX (Excel):

```sh
python main.py --video 7418294751977327878 --format xlsx
```

JSON e CSV ao mesmo tempo:

```sh
python main.py --video 7418294751977327878 --format both
```

Todos os formatos de uma vez:

```sh
python main.py --video 7418294751977327878 --format all
```

## Opcoes

| Opcao | Descricao | Padrao |
| --- | --- | --- |
| `--video`, `--aweme-id` | ID ou URL do video do TikTok | obrigatorio |
| `--limit`, `--size`, `-s` | Limita a quantidade de comentarios | coleta todos |
| `--output`, `-o` | Pasta onde o JSON sera salvo | `data` |
| `--replies / --no-replies` | Inclui ou ignora replies | `--replies` |
| `--pretty / --compact` | JSON formatado ou compacto | `--pretty` |
| `--format` | Saida: `json`, `csv`, `txt`, `xlsx`, `both` (json+csv) ou `all` | `json` |
| `--quiet / --verbose` | Silencia ou mostra o progresso da coleta | `--verbose` |

## Formato da saida

O arquivo e salvo como:

```txt
data/<video_id>.json
data/<video_id>.csv
data/<video_id>.txt
data/<video_id>.xlsx
```

Exemplo:

```json
{
  "video_id": "7418294751977327878",
  "caption": "Legenda do video",
  "video_url": "https://www.tiktok.com/...",
  "comment_count": 1,
  "comments": [
    {
      "id": "7418575915603985158",
      "username": "usuario",
      "nickname": "Nome",
      "text": "Comentario",
      "created_at": "2024-09-25T10:43:41",
      "avatar_url": "https://...",
      "like_count": 0,
      "reply_count": 0,
      "replies": []
    }
  ]
}
```

## Aviso

Esta ferramenta consulta endpoints publicos usados pelo TikTok Web. Esses endpoints podem mudar, limitar requisicoes ou parar de responder sem aviso. Use com responsabilidade e respeite os termos da plataforma.

## Licenca

MIT. Veja [LICENSE](LICENSE).
