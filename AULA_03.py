from selenium import webdriver
import pandas as pd
import datetime

# Passo a passo

# Passo 1: Abrir o navegdor

navegador = webdriver.Edge()
navegador.get('https://google.com')

# Passo 2: Importar a base de dados

tabela = pd.read_excel('commodities.xlsx')

for linha in tabela.index:
    # Passo 3: Para cada produto da base de dados
    produto = tabela.loc[linha, 'Produto']
    produto = produto.replace('ó', 'o').replace('ã', 'a').replace('ç', 'c').replace('ú', 'u').replace('é', 'e').replace('á', 'a')
    link = (f'https://www.melhorcambio.com/{produto}-hoje')
    navegador.get(link)

    # Passo 4: Pesquisar o preço de produtos
    # .click() -> clicar
    # .send_keys('texto') -> escrever
    # .get_attribute() -> pegar um valor
    preco = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute('value')
    preco = preco.replace('.', '').replace(',', '.')

    # Passo 5: Atualizar o preço na base de dados
    tabela.loc[linha, 'Preço Atual'] = float(preco)

# Passo 6: Decidir quais produtos comprar
'''
    for linha in tabela.index:
        if tabela.loc[linha, 'Preço Atual'] < tabela.loc[linha, 'Preço Ideal']:
            tabela.loc[linha, 'Comprar'] = 'True'
        else:
            tabela.loc[linha, 'Comprar'] = 'False' 
'''

#Preencher coluna Comprar
tabela['Comprar'] = tabela['Preço Atual'] <= tabela['Preço Ideal']

data = f'{datetime.date.today().day}-{datetime.date.today().month}'
tabela.to_excel(f'commodities_atualizada {data}.xlsx', index = False)

# import os
# os.startfile(f'commodities_atualizada {data}.xlsx')
print(pd.read_excel(f'commodities_atualizada {data}.xlsx'))


