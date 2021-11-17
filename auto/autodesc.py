import sys
sys.path.insert(0, 'D:/Users/mdabe/Documentos/GitHub/JuliaBot/src/')

import modules.database as db
import modules.entity as entity
from commands import *
from scripts import *


prefix = 'j!'
content = ''

content += '# JuliaBot\n'
content += 'Um bot de discord feito em python utilizando a API [discord.py](https://github.com/Rapptz/discord.py) e totalmente personalizável.\n\n'
content += 'Clique [aqui](https://discord.com/oauth2/authorize?client_id=483054181176049685&scope=bot) para adicionar a `JuliaBot` ao seu servidor.\n'


content += '# O que tem no bot?\n'
content += """
- Sistema de economia.
- Rank do servidor baseado em quem possui mais `coins`.
- Eventos aleatórios para distribuir `coins`.
- Possibilidade de criar comandos personalizádos para o servidor.
- Notificar episódios novos de animes.
- Bot totalmente personalizável.
""" + '\n'


content += '# Comandos \n'
content += '## Guia de parâmetros\n'
content += '| Simbolo | Descrição | Exemplo na tabela | Exemplo no comando |\n'
content += '|---------|-----------|---------|-----------------|' + '\n'
content += f'| * | Parâmetro obrigatório. | `<preço>`* | {prefix}roulette 50 |' + '\n'
content += f'| º | Possivel mais de um. | `<pessoa>`º | {prefix}coins @pessoa1 @pessoa2 @pessoa3 |\n'

for category in entity.Command.getcategories():
    content += f'## {category[0]} \n'
    content += '| Comando | Descrição | Parâmetros | Permissão |' + '\n'
    content += '|---------|-----------|------------|-----------|' + '\n'
    for command in entity.Command.commands:
        if command.category == category[0]:
            args = ''
            for arg in command.args:
                args += f'`<{arg[0].replace(" ", "_")}>`{arg[1]} '

            perm = ''
            if command.perm == 0:
                perm = 'Livre.'
            elif command.perm == 1:
                perm = 'Admin.'
            elif command.perm == 2:
                perm = 'Depuração.' 

            content += f'|{prefix}{command.name}|{command.desc}|{args}|{perm}|'+ '\n'
    

f = open('D:/Users/mdabe/Documentos/GitHub/JuliaBot/README.md', 'w', encoding='utf8')
f.write(content)
print(content)
f.close()