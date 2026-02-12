from docx import Document

# Create document
doc = Document()
doc.add_heading('Звіт про кіберінциденти (SC Media)', level=1)

incidents = [
    {
        "title": "1. European Commission – Ivanti EPMM Vulnerabilities (2026)",
        "fields": {
            "Дата інциденту": "30 січня 2026 р.",
            "Постраждала організація": "Європейська Комісія (European Commission)",
            "Кількість постраждалих": "Не вказано; потенційний доступ до контактних даних співробітників",
            "Що було зроблено?": "CERT-EU локалізував інцидент (~9 годин), очищено системи, випущені патчі Ivanti.",
            "Які експлойти використовувалися?": "CVE-2026-1281 та CVE-2026-1340 (RCE, code injection, Ivanti EPMM).",
            "Яким чином налагоджено захист?": "Негайний патчинг, сегментація доступу, MFA, моніторинг логів, аудит облікових записів.",
            "Посилання": "https://www.scworld.com/brief/european-commission-hit-by-cyberattack-linked-to-ivanti-software-flaws"
        }
    },
    {
        "title": "2. France Travail – Data Breach (2024, fine in 2026)",
        "fields": {
            "Дата інциденту": "Початок 2024 р.; штраф 22 січня 2026 р.",
            "Постраждала організація": "France Travail (Національне агентство зайнятості Франції)",
            "Кількість постраждалих": "43 мільйони осіб",
            "Що було зроблено?": "CNIL наклав штраф €5 млн; зобов'язання посилити захист (щоденний штраф за невиконання).",
            "Які експлойти використовувалися?": "Соціальна інженерія, компрометація облікових записів партнерської організації.",
            "Яким чином налагоджено захист?": "MFA, принцип мінімальних привілеїв, моніторинг логів, навчання персоналу.",
            "Посилання": "https://www.scworld.com/brief/france-fines-employment-agency-e5-million-for-data-breach-affecting-43-million"
        }
    },
    {
        "title": "3. Scattered Spider – Rapid Ransomware Deployment (2025)",
        "fields": {
            "Дата інциденту": "2025 р. (звіт CrowdStrike)",
            "Постраждала організація": "Не конкретизовано (загальний тренд атак)",
            "Кількість постраждалих": "Не вказано",
            "Що було зроблено?": "Атаки скорочені до 24 годин від доступу до шифрування; використання SaaS і Entra ID.",
            "Які експлойти використовувалися?": "Vishing, компрометація MFA, living-off-the-land техніки.",
            "Яким чином налагоджено захист?": "Посилення IAM, MFA, поведінковий моніторинг, сегментація доступу.",
            "Посилання": "https://www.scworld.com/news/scattered-spider-now-moves-from-initial-access-to-encryption-in-24-hours"
        }
    }
]

for incident in incidents:
    doc.add_heading(incident["title"], level=2)
    table = doc.add_table(rows=len(incident["fields"]), cols=2)
    table.style = 'Table Grid'
    
    for i, (key, value) in enumerate(incident["fields"].items()):
        table.rows[i].cells[0].text = key
        table.rows[i].cells[1].text = value

    doc.add_paragraph("")

doc.save("Звіт_про_кіберінциденти_SC_Media.docx")

print("Файл створено успішно!")
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Створення документа
doc = Document()
doc.add_heading('Звіт про шкідливе ПЗ проти українських цілей (CoreWin)', level=1)

# Дані інциденту
incident = {
    "Дата інциденту": "Січень–квітень 2022 року",
    "Постраждала організація": "Державні органи України, банки, енергетика, телеком",
    "Кількість постраждалих": "Десятки державних сайтів, сотні систем, тисячі пристроїв (KA-SAT)",
    "Що було зроблено?": (
        "Здійснено масові кібератаки із застосуванням destructive malware "
        "(вайпери) для знищення даних, дефейсу сайтів та атак на критичну інфраструктуру."
    ),
    "Які експлойти / шкідливе ПЗ використовувалися?": (
        "WhisperGate, HermeticWiper, IsaacWiper, AcidRain, CaddyWiper, "
        "DoubleZero, Industroyer2."
    ),
    "Яким чином налагоджено захист?": (
        "Сегментація мереж (IT/OT), резервне копіювання, EDR/AV рішення, "
        "MFA, моніторинг логів, навчання персоналу, аудит доступів."
    ),
    "Посилання на джерело": "https://corewin.ua/blog/malware-being-used-on-ukrainian-targets/"
}

# Додавання таблиці
table = doc.add_table(rows=len(incident), cols=2)
table.style = 'Table Grid'

for i, (key, value) in enumerate(incident.items()):
    table.rows[i].cells[0].text = key
    table.rows[i].cells[1].text = value

# Збереження файлу
doc.save("Звіт_CoreWin_Malware_UA.docx")

print("DOCX файл успішно створено!")
