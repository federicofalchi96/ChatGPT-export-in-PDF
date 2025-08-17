# 📑 ChatGPT Exporter in PDF

Questo script Python permette di **esportare una chat di ChatGPT in PDF** partendo dall’URL di condivisione.  
Utilizza **Selenium** per caricare la pagina, estrarre il contenuto della chat e **pdfkit / wkhtmltopdf** per generare un file PDF ben formattato.

---

## 🚀 Requisiti

- Python 3.8+
- [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) installato sul sistema  
  ⚠️ Assicurati di aggiornare nel codice il percorso corretto:  
 
 
 path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

### Avvio del programma

python exportchatGPT.py 

### Librerie necessarie
Installa le dipendenze con:

pip install selenium pdfkit webdriver-manager

### Informazioni

Esegui lo script da terminale:

python chatgpt_export.py --url "https://chatgpt.com/share/IL-TUO-LINK" --output "mia_chat.pdf" --all yes --wait 40

Argomenti disponibili

--url → URL della chat da esportare

--output → nome del file PDF in uscita (default: chat_emotional.pdf)

--all → "yes" per esportare tutta la chat (domande + risposte), "no" per esportare solo le risposte di GPT

--wait → tempo di attesa in secondi per il caricamento completo della pagina (default: 30)