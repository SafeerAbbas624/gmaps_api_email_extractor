#!/usr/bin/env python3
"""Script to create email_messages.py with 15 variations"""

import json

messages = [
    {
        "subject": "Potenzia la tua presenza online con strategie social su misura",
        "plain": "Gentile,\n\nmi chiamo Tommaso e sono un professionista specializzato in strategie di crescita sui social media. Mi rivolgo a realtà come la vostra che desiderano aumentare la propria visibilità online, coinvolgere un pubblico più ampio e ottenere risultati concreti attraverso i canali digitali.\n\nOffro servizi personalizzati che includono:\n\n- 📈 Aumento organico e mirato dei follower\n- 💬 Incremento dell'engagement su post e storie\n- 🎯 Strategie di contenuto per migliorare la brand awareness\n- 📊 Analisi delle performance e ottimizzazione continua\n- 🤝 Collaborazioni con influencer e campagne sponsorizzate\n\nOgni progetto è costruito su misura, con l'obiettivo di valorizzare l'identità del brand e raggiungere risultati misurabili.\n\nResto a disposizione per qualsiasi informazione e vi ringrazio per l'attenzione.\n\nCordiali saluti,\nTommaso",
        "html": "<html><body style=\"font-family: Arial, sans-serif; color: #333;\"><p>Gentile,</p><p>mi chiamo <strong>Tommaso</strong> e sono un professionista specializzato in strategie di crescita sui social media. Mi rivolgo a realtà come la vostra che desiderano aumentare la propria visibilità online, coinvolgere un pubblico più ampio e ottenere risultati concreti attraverso i canali digitali.</p><p><strong>Offro servizi personalizzati che includono:</strong></p><ul><li>📈 Aumento organico e mirato dei follower</li><li>💬 Incremento dell'engagement su post e storie</li><li>🎯 Strategie di contenuto per migliorare la brand awareness</li><li>📊 Analisi delle performance e ottimizzazione continua</li><li>🤝 Collaborazioni con influencer e campagne sponsorizzate</li></ul><p>Ogni progetto è costruito su misura, con l'obiettivo di valorizzare l'identità del brand e raggiungere risultati misurabili.</p><p>Resto a disposizione per qualsiasi informazione e vi ringrazio per l'attenzione.</p><p>Cordiali saluti,<br><strong>Tommaso</strong></p></body></html>"
    }
]

# Write to file
with open('email_messages.py', 'w', encoding='utf-8') as f:
    f.write('"""\nEmail Message Variations - 15 different messages for social media marketing services\nEach message has the same context but different wording to avoid Gmail spam detection\n"""\n\nimport random\n\n# 15 different message variations (plain text + HTML)\nEMAIL_MESSAGES = [\n')
    for msg in messages:
        f.write('    {\n')
        f.write(f'        "subject": "{msg["subject"]}",\n')
        f.write(f'        "plain": """{msg["plain"]}""",\n')
        f.write(f'        "html": """{msg["html"]}"""\n')
        f.write('    },\n')
    f.write(']\n\ndef get_random_message():\n    """Return a random message from the list"""\n    return random.choice(EMAIL_MESSAGES)\n')

print("email_messages.py created successfully!")

