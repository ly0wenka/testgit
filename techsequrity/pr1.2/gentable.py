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
from docx import Document

# Створення документа
doc = Document()
doc.add_heading('Звіт про кіберінцидент (SC Media)', level=1)

incident = {
    "Дата інциденту": "З середини 2024 р.; оприлюднено у 2026 р.",
    "Постраждала організація": "Різні організації, що використовують Dell RecoverPoint for VMs",
    "Кількість постраждалих": "Не розкрито (цільові атаки на корпоративні середовища)",
    "Що було зроблено?": (
        "Кіберугруповання UNC6201, пов’язане з Китаєм, експлуатувало "
        "уразливість у Dell RecoverPoint for VMs версії 10.0 для отримання "
        "стійкого доступу, збору даних та подальшого переміщення в мережі."
    ),
    "Які експлойти використовувалися?": (
        "Експлуатація невідомої (ймовірно 0-day) уразливості в Dell RecoverPoint "
        "for VMs 10.0 для віддаленого доступу та закріплення в системі."
    ),
    "Яким чином налагоджено захист?": (
        "Оновлення та патчинг Dell RecoverPoint, ізоляція керуючих інтерфейсів, "
        "використання MFA, моніторинг логів, контроль доступу та сегментація мережі."
    ),
    "Посилання": "https://www.scworld.com/news/china-linked-unc6201-exploits-10-0-bug-in-dell-recoverpoint-for-vms-since-mid-2024"
}

# Додавання таблиці
table = doc.add_table(rows=len(incident), cols=2)
table.style = 'Table Grid'

for i, (key, value) in enumerate(incident.items()):
    table.rows[i].cells[0].text = key
    table.rows[i].cells[1].text = value

# Збереження файлу
doc.save("Звіт_UNC6201_Dell_RecoverPoint.docx")

print("DOCX файл успішно створено!")
from docx import Document

# Створення документа
doc = Document()
doc.add_heading('Звіт про кіберінцидент (SC Media)', level=1)

incident = {
    "Дата інциденту": "Лютий 2026 р. (опубліковано дослідження)",
    "Постраждала організація": "Користувачі Visual Studio Code та сумісних IDE (Cursor, Windsurf тощо)",
    "Кількість постраждалих": (
        "Потенційно мільйони розробників; вразливі розширення мають понад 125–128 млн завантажень"
    ),
    "Що було зроблено?": (
        "Дослідники виявили критичні вразливості в популярних розширеннях VS Code, "
        "які дозволяють виконання довільного коду та викрадення локальних файлів. "
        "Атаки можливі через відкриття шкідливих конфігурацій, HTML-файлів або робочих просторів."
    ),
    "Які експлойти використовувалися?": (
        "CVE-2025-65717 (Live Server), CVE-2025-65715 (Code Runner), "
        "CVE-2025-65716 (Markdown Preview Enhanced); XSS та небезпечні налаштування workspace."
    ),
    "Яким чином налагоджено захист?": (
        "Оновлення та видалення вразливих розширень, використання лише перевірених плагінів, "
        "обмеження відкриття недовірених файлів/конфігурацій, моніторинг змін налаштувань IDE, "
        "застосування принципу мінімальних привілеїв і контроль доступу до локальних ресурсів."
    ),
    "Посилання": "https://www.scworld.com/brief/critical-vscode-extension-vulnerabilities-could-lead-to-code-execution-and-data-theft"
}

# Додавання таблиці
table = doc.add_table(rows=len(incident), cols=2)
table.style = 'Table Grid'

for i, (key, value) in enumerate(incident.items()):
    table.rows[i].cells[0].text = key
    table.rows[i].cells[1].text = value

# Збереження
doc.save("Звіт_VSCode_Extension_Vulnerabilities.docx")

print("DOCX файл успішно створено!")
from docx import Document

# Створення документа
doc = Document()
doc.add_heading('Звіт про кіберінцидент (SC Media)', level=1)

incident = {
    "Дата інциденту": "Лютий 2026 р.",
    "Постраждала організація": "Користувачі Google Chrome (Windows, macOS, Linux)",
    "Кількість постраждалих": (
        "Потенційно мільярди користувачів Chrome; активна експлуатація zero-day у дикій природі"
    ),
    "Що було зроблено?": (
        "Google випустила екстрене оновлення Chrome для усунення активно "
        "експлуатованої zero-day уразливості, що дозволяє виконання довільного коду "
        "через спеціально сформовані вебсторінки."
    ),
    "Які експлойти використовувалися?": (
        "CVE-2026-2441 — use-after-free у CSS компоненті Chrome; "
        "можливе виконання довільного коду в sandbox через шкідливу HTML-сторінку."
    ),
    "Яким чином налагоджено захист?": (
        "Негайне оновлення браузера до Chrome 145.0.7632.75/76 (Win/Mac) "
        "або 144.0.7559.75 (Linux), застосування автоматичних оновлень, "
        "моніторинг підозрілих вебресурсів, використання sandbox-захисту та EDR."
    ),
    "Посилання": "https://www.scworld.com/brief/google-releases-emergency-chrome-update-for-zero-day-exploit"
}

# Додавання таблиці
table = doc.add_table(rows=len(incident), cols=2)
table.style = 'Table Grid'

for i, (key, value) in enumerate(incident.items()):
    table.rows[i].cells[0].text = key
    table.rows[i].cells[1].text = value

# Збереження
doc.save("Звіт_Chrome_ZeroDay_Exploit.docx")

print("DOCX файл успішно створено!")
from docx import Document

# Створення документа
doc = Document()
doc.add_heading('Звіт про кіберінцидент (SC Media)', level=1)

incident = {
    "Дата інциденту": "Лютий 2026 р.",
    "Постраждала організація": (
        "WordPress-сайти, що використовують плагін WPvivid Backup & Migration"
    ),
    "Кількість постраждалих": (
        "Понад 900 000 сайтів WordPress, що використовують вразливі версії плагіна"
    ),
    "Що було зроблено?": (
        "Виявлено критичну вразливість, яка дозволяє неавторизованим зловмисникам "
        "завантажувати довільні файли та виконувати віддалений код на сервері, "
        "що може призвести до повного захоплення сайту."
    ),
    "Які експлойти використовувалися?": (
        "CVE-2026-1357 — Unauthenticated Arbitrary File Upload, що призводить до RCE "
        "через помилки обробки RSA-дешифрування та відсутність санітизації шляхів."
    ),
    "Яким чином налагоджено захист?": (
        "Оновлення плагіна до версії 0.9.124 або новішої, вимкнення функції "
        "'receive backup from another site', застосування WAF, контроль завантажень, "
        "моніторинг логів та перевірка сайту на наявність вебшелів."
    ),
    "Посилання": "https://www.scworld.com/brief/critical-vulnerability-in-wpvivid-backup-plugin-allows-remote-code-execution"
}

# Додавання таблиці
table = doc.add_table(rows=len(incident), cols=2)
table.style = 'Table Grid'

for i, (key, value) in enumerate(incident.items()):
    table.rows[i].cells[0].text = key
    table.rows[i].cells[1].text = value

# Збереження файлу
doc.save("Звіт_WPvivid_RCE_Vulnerability.docx")

print("DOCX файл успішно створено!")
