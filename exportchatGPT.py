import argparse
import io
import sys
import time
import pdfkit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Forza stdout a UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

# === ARGOMENTI DA CLI ===
parser = argparse.ArgumentParser(
    description="Esporta una chat di ChatGPT in PDF"
)
parser.add_argument("--url", type=str,
    default="https://chatgpt.com/share/686e87f7-64d8-800b-96d1-0a7f5f0f20bd",
    help="URL della chat da esportare (default: chat di esempio)"
)
parser.add_argument("--output", type=str,
    default="chat_emotional.pdf",
    help="Nome del file PDF in output (default: chat_emotional.pdf)"
)
parser.add_argument("--all", type=str, choices=["yes", "no"],
    default="no",
    help="Esporta tutta la chat (domande + risposte) se 'yes'. Default: solo risposte"
)
parser.add_argument("--wait", type=int, default=30,
    help="Tempo di attesa (in secondi) per il caricamento della pagina. Default: 30"
)
args = parser.parse_args()

chat_url = args.url
output_pdf = args.output
export_all = args.all.lower() == "yes"
wait_time = args.wait

# === CONFIG ===
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # <-- verifica il percorso

# === HEADLESS CHROME ===
options = Options()
options.add_argument("--headless=new")  # modalità headless nuova
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# === VISITA LA PAGINA ===
print(f"🌐 Carico chat da: {chat_url}")
driver.get(chat_url)
time.sleep(wait_time)

# === ESTRAI CHAT ===
responses = []
if export_all:
    print("📑 Modalità: tutta la chat (domande + risposte)")
    # tutta la chat
    blocks = driver.find_elements(By.CSS_SELECTOR, "div.text-base")
else:
    print("💬 Modalità: solo risposte di GPT")
    # Solo blocchi GPT
    blocks = driver.find_elements(By.CLASS_NAME, "prose")

for block in blocks:
    html = block.get_attribute("innerHTML")
    if html and len(html.split()) > 10:
        responses.append(html)

driver.quit()

if not responses:
    print("⚠️ Nessun contenuto trovato, prova ad aumentare --wait")
    sys.exit(1)

# === TEMPLATE HTML ===
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; padding: 40px; line-height: 1.6; }}
        h1 {{ color: #2c3e50; margin-bottom: 40px; }}
        hr {{ margin: 40px 0; }}
        pre, code {{ background: #f4f4f4; padding: 10px; border-radius: 5px; font-size: 14px; overflow-x: auto; display: block; }}
        table {{ border-collapse: collapse; margin-top: 10px; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 6px 10px; text-align: left; }}
        .latex {{ font-style: italic; }}
    </style>
    <script>
      MathJax = {{
        tex: {{
          inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]
        }},
        svg: {{
          fontCache: 'global'
        }}
      }};
    </script>
    <script type="text/javascript" id="MathJax-script" async
      src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
    </script>
</head>
<body>
    <h1>Esportazione ChatGPT</h1>
    {content}
</body>
</html>
"""

# === GENERA HTML ===
html_content = "<hr>".join(responses)
final_html = html_template.format(content=html_content)

with open("chatgpt_export.html", "w", encoding="utf-8") as f:
    f.write(final_html)

# === GENERA PDF ===
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
pdfkit.from_file("chatgpt_export.html", output_pdf, configuration=config)

print(f"✅ PDF creato con successo: {output_pdf}")
