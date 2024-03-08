import requests
from bs4 import BeautifulSoup
import json

#Requisição do site por meio do get
resposta=requests.get("https://infosimples.com/vagas/desafio/commercia/product.html")
#Conteúdo retirado da requisição
conteudo=resposta.content
#Transformando o conteúdo em html-parser
site=BeautifulSoup(conteudo,"html.parser")
#Usando o print prettyfy método é possível ver toda a página html
#print(site.prettify())
#buscando as informações solicitada
titulo=site.find("h2",attrs={'id':"product_title"})
brand=site.find("div",attrs={"class":"brand"})
categoria=site.find("ul",attrs={"class":"breadcrumb"})
descricao=site.find("div",attrs={"class":"proddet"})
skus=site.find_all("div",attrs={"class":"card"})
#Busca da propriedades onde o resultado é armazenado em array propriedade_valores,
#um loop for é usado para salvar as informações de propiedade e valor da tabela solicitada
propriedades=site.find("table",attrs={"class":"pure-table pure-table-bordered"})
propriedades_valores = []
for row in propriedades.find_all('tr'):
    propriedade = row.find('td').text.strip()
    valor = row.find_all('td')[1].text.strip()
    propriedade_valor = {propriedade: valor}
    #print(propriedade)
    propriedades_valores.append(propriedade_valor)

media_review=site.find("div",attrs={"id":"comments"})
review=media_review.find("h4")
avaliacoes=site.find_all("div",attrs={"class":"analisebox"})

#Método para salvar todas as informações procuradas de uma área especifica como uma div
def produto(sku):
    nome = sku.find("div", attrs={"class": "prod-nome"})
    preco_atua = sku.find("div", attrs={"class": "prod-pnow"})
    preco_antigo = sku.find("div", attrs={"class": "prod-pold"})
    estoque = bool(sku.find("div", attrs={"class": "card not-avaliable"}))

    #Verifica se há valor e transforma em float caso não haja passa o valor como none
    if preco_atua:
        preco_atua = float(preco_atua.text.replace('R$', '').replace(',', '.'))
    else:
        preco_atua = None

    if preco_antigo:
        preco_antigo = float(preco_antigo.text.replace('R$', '').replace(',', '.'))
    else:
        preco_antigo = None

    return {'name': nome.text.strip() if nome else '', 'current': preco_atua, 'antigo': preco_antigo,
            'estoque': estoque}
#Outro método para salvar todas as informações procuradas de uma área especifica porém, para as avaliações
def avaliar(avaliacao):
    nome = avaliacao.find("span", attrs={"class": "analiseusername"})
    date = avaliacao.find("span", attrs={"class": "analisedate"})
    score = avaliacao.find("span", attrs={"class": "analisestars"})
    text = avaliacao.find("p", attrs={"class": "analisebox"})

    return {'nome': nome.text.strip() if nome else '', 'date': date.text.strip() if date else '',
            'score': score.text.strip() if score else '', 'text': text.text.strip() if text else ''}

#Variáveis auxiliares
tit=titulo.string
marca=brand.string
categ=[item.text.strip() for item in categoria.find_all('li')]
descri=descricao.text.strip()
produtos = [produto(sku) for sku in skus]
aval = [avaliar(avaliacao) for avaliacao in avaliacoes]
rew=review.string
url="https://infosimples.com/vagas/desafio/commercia/product.html"

#Dicionário usado para imprimir as informações
dados_produto = {
    "Title": tit,
    "Brand": marca,
    "Categoria": categ,
    "Description": descri,
    "skus": produtos,
    "Properties":propriedades_valores,
    "Reviews": aval,
    "Reviews_avarage_score":rew,
    "Url":url
}

# Convertendo o dicionário em uma string JSON
json_string = json.dumps(dados_produto, ensure_ascii=False, indent=4)

#Escrevendo a string JSON em um arquivo e imprimindo o resultado
with open("Produto.json", "w", encoding='utf-8') as arquivo_json:
    arquivo_json.write(json_string)
    print(json_string)