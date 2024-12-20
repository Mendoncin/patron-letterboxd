import requests
from bs4 import BeautifulSoup
import math
from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def janela_resultados(ord_media, ord_filmes, qnt_filmes, media_nota, nome_bonito, data):
    counting = 0
    nova_janela = Toplevel()
    nova_janela.title("Resultados")
    nova_janela.geometry("1000x800")
    nova_janela.config(bg='#1e1e1f')
    nova_janela.iconphoto(False, PhotoImage(file='images.png'))
    nova_janela.columnconfigure(0, weight=1)    

    brado = Label(nova_janela, text=nome_bonito, font=('Arial 40 bold'), fg='#fafbfc', bg='#1e1e1f')
    brado.grid(row=0, column= 0, pady=20)

    average = Label(nova_janela, text=f'Filmes assistidos:  {qnt_filmes}', font=('Arial 27'), fg='#fafbfc', bg='#1e1e1f')
    average.place(x=65, y=150)

    average1 = Label(nova_janela, text=f'Média das notas:  {media_nota:.2f}', font=('Arial 27'), fg='#fafbfc', bg='#1e1e1f')
    average1.place(x=65, y=190)

    texto_lista = Label(nova_janela, text='Diretores', font=('Arial 25 bold'), fg='#fafbfc', bg='#1e1e1f')
    texto_lista.place(x=100, y=300)

    labels_diretor = []
    labels_number = []
    labels_number1 = []


    for autor in ord_media:
        name = autor.split(' : ')
        counting +=1
        diretor = Label(nova_janela, text=name[0], font=('Arial 20'), fg='#fafbfc', bg='#1e1e1f')
        ipsilon = 300 + (counting * 40)
        diretor.place(x=100, y=ipsilon)
        number = Label(nova_janela, text=name[4], font=('Arial 20'), fg='#fafbfc', bg='#1e1e1f')
        number.place(x=650, y=ipsilon )
        number1 = Label(nova_janela, text=f"{float(name[3]):.2f}", font=('Arial 20'), fg='#fafbfc', bg='#1e1e1f')
        number1.place(x=450, y=ipsilon )

        labels_diretor.append(diretor)
        labels_number.append(number)
        labels_number1.append(number1)

        if counting == 10:
            break
    
    def alterar_labels():
        counting = 0
        for label in labels_diretor:
            name = ord_filmes[counting].split(' : ')
            label.config(text=name[0])
            counting +=1
        counting = 0
        for label in labels_number:
            number = ord_filmes[counting].split(' : ')
            label.config(text=number[4])
            counting+=1
        counting = 0
        for label in labels_number1:
            number = ord_filmes[counting].split(' : ')
            label.config(text=f"{float(number[3]):.2f}")
            counting+=1

    def retornar_labels():
        counting = 0
        for label in labels_diretor:
            name = ord_media[counting].split(' : ')
            label.config(text=name[0])  
            counting +=1
        counting = 0
        for label in labels_number:
            number = ord_media[counting].split(' : ')
            label.config(text=number[4])
            counting+=1
        counting = 0
        for label in labels_number1:
            number = ord_media[counting].split(' : ')
            label.config(text=f"{float(number[3]):.2f}")
            counting+=1
    
    def graf_notas():
        janela_grafico = Toplevel()
        janela_grafico.title('Gráfico de Décadas')
        janela_grafico.geometry('500x500')
        janela_grafico.config(bg='#1e1e1f')
        janela_grafico.iconphoto(False, PhotoImage(file='images.png'))

        dataframe = pd.DataFrame(data)
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        figure_plot = figure.add_subplot(1, 1, 1)
        figure_plot.set_ylabel('Média Notas')
        line_graph = FigureCanvasTkAgg(figure, janela_grafico)
        line_graph.get_tk_widget().pack(side=LEFT, fill=BOTH)
        dataframe = dataframe[['Décadas', 'Média_Notas']].groupby('Décadas').sum()
        dataframe.plot(kind='line', legend=True, ax = figure_plot, color='r', marker='o', fontsize =10)
        figure_plot.set_title('Rating Médio Por Década')
        figure_plot.set_facecolor('gray')



    botao_alterar = Button(nova_janela, text="Filmes", command=alterar_labels, font=('Arial 15'))
    botao_alterar.place(x=650, y=300)

    botao_retornar = Button(nova_janela, text="Notas", command=retornar_labels, font=('Arial 15'))
    botao_retornar.place(x=450, y=300)

    botao_grafico = Button(nova_janela, text="Gráfico de Décadas", command=graf_notas, font=('Arial 19'))
    botao_grafico.place(x=570, y=175)


def pagina_filmes_individual (slug, lista_diretor, nota):
    liberado = False
    contador3 = 0
    url1= f'https://letterboxd.com/film/{slug}/'
    cabecalhos = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    resposta = requests.get(url1, headers=cabecalhos)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, 'html.parser')
        nome_filme = soup.find('h1', class_="headline-1 filmtitle").find('span', class_='name')
        nome_filme = nome_filme.text.strip()
        tag_ano = soup.find('div', class_='metablock').find('div', class_='releaseyear')
        ano_filme = tag_ano.text.strip()
        tag_diretor = soup.find('span', class_='directorlist')
        if tag_diretor:
            diretor = tag_diretor.text.strip()
        else:
            diretor = "Unknown"
        if diretor.endswith('\n…'):
            diretor = diretor.replace('\n…', '')
        while ',' in diretor:
            liberado = False
            contador3 = 0
            diretores = diretor.split(', ')
            for diretor1 in diretores:
                contador3 = 0
                for teste in lista_diretor:
                    lista_teste = teste.split(' : ')
                    if lista_teste[0] == diretor1:
                        qnt_filme_diretor1 = int(lista_teste[2])
                        if nota != 'filme sem nota':
                            qnt_filme_diretor1 +=1
                        else:
                            nota = 0
                        nota_diretor = int(lista_teste[1]) + nota 
                        qnt_filme_diretor = int(lista_teste[4]) + 1
                        index = contador3
                        if qnt_filme_diretor1 == 0:
                            media_diretor = 0
                        else:
                            media_diretor = nota_diretor / qnt_filme_diretor1
                            media_diretor = round(media_diretor, 2)

                    else:
                        contador3 +=1
                        if contador3 == len(lista_diretor):
                            liberado = True

            for teste in lista_diretor:
                lista_teste = teste.split(' : ')
                if lista_teste[0] == diretor:
                    qnt_filme_diretor1 = int(lista_teste[2])
                    if nota != 'filme sem nota':
                        qnt_filme_diretor1 +=1
                    else:
                        nota = 0
                    nota_diretor = int(lista_teste[1]) + nota
                    qnt_filme_diretor = int(lista_teste[4]) + 1
                    index = contador3
                    if qnt_filme_diretor1 == 0:
                        media_diretor = 0
                    else:
                        media_diretor = nota_diretor / qnt_filme_diretor1
                        media_diretor = round(media_diretor, 2)
                else:
                    contador3 +=1
                    if contador3 == len(lista_diretor):
                        liberado = True
            if liberado == True:
                if nota == 'filme sem nota':
                    lista_diretor.append(f'{diretor} : 0 : 0 : 0 : 1')
                else:
                    lista_diretor.append(f'{diretor1} : {nota} : 1 : {nota} : 1')
                diretores.pop()
                diretor = ', '.join(diretores)
            else:
                lista_diretor[index] = f'{diretor} : {nota_diretor} : {qnt_filme_diretor1} : {media_diretor} : {qnt_filme_diretor}'
                diretores.pop()
                diretor = ', '.join(diretores)
            
        liberado = False
        contador3 = 0

        for teste in lista_diretor:
                lista_teste = teste.split(' : ')
                if lista_teste[0] == diretor:
                    qnt_filme_diretor1 = int(lista_teste[2])
                    if nota != 'filme sem nota':
                        qnt_filme_diretor1 +=1
                    else:
                        nota = 0
                    nota_diretor = int(lista_teste[1]) + nota
                    qnt_filme_diretor = int(lista_teste[4]) + 1
                    index = contador3
                    if qnt_filme_diretor1 == 0:
                        media_diretor = 0
                    else:
                        media_diretor = nota_diretor / qnt_filme_diretor1
                        media_diretor = round(media_diretor, 2)
                else:
                    contador3 +=1
                    if contador3 == len(lista_diretor):
                        liberado = True
        if liberado == True:
                if nota == 'filme sem nota':
                    lista_diretor.append(f'{diretor} : 0 : 0 : 0 : 1')
                else:
                    lista_diretor.append(f'{diretor} : {nota} : 1 : {nota} : 1')
        else:
                lista_diretor[index] = f'{diretor} : {nota_diretor} : {qnt_filme_diretor1} : {media_diretor} : {qnt_filme_diretor}'
        return(lista_diretor, ano_filme, nome_filme)


def main(nome_usuario):

    lista_anota = []
    lista_diretor = ['a : b : c : d : e']
    contador1 = 0
    contador2 = 0
    informações = []
    informações_ord_media = []
    informações_ord_filmes = []
    url = f'https://letterboxd.com/{nome_usuario}/'
    cabecalhos = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    resposta = requests.get(url, headers=cabecalhos)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, 'html.parser') 
        tag_nome_exibicao = soup.find('h1', class_='person-display-name').find('span', class_='displayname')
        nome_bonito = tag_nome_exibicao.text.strip() 
        tag_filmes = soup.find('a', href=f'/{nome_usuario}/films/').find('span', class_='value')
        if len(tag_filmes.text) > 3:
            tag_filmes = tag_filmes.text.replace(",", "")
            qnt_filmes = int(tag_filmes)
        else:
            qnt_filmes = int(tag_filmes.text)

    qnt_pag = math.ceil(qnt_filmes/72)
    for pagina in range(1, qnt_pag+1):
        url = f'https://letterboxd.com/{nome_usuario}/films/'
        if pagina > 1:
            url = f'{url}page/{pagina}/'
        cabecalhos = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resposta = requests.get(url, headers=cabecalhos)
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            filmes = soup.find_all('li', class_='poster-container')
            for filme in filmes:
                notas = False
                dados = str(filme).split()
                for dado in dados:
                    if dado.startswith('rated-'):
                        lixo=dado.split('"')
                        nota = int(lixo[0][-1])
                        notas = True
                        if nota == 0:
                            nota = 10
                        contador2 += nota
                        informações, ano, nome = pagina_filmes_individual(slug, lista_diretor, nota)
                        lista_anota.append(f'{ano[:3]}0, {nota}')
                        print(nome)
                    elif dado.startswith('</p') and notas == False:
                        nota = 'filme sem nota'
                        informações, ano, nome = pagina_filmes_individual(slug, lista_diretor, nota)
                        contador1 += 1
                        print(nome)
                    elif dado.startswith('data-film-slug='):
                        lixo = dado.split('=')
                        slug = lixo[1]
                        slug = slug[1:-1]


    filmes_cm_nota = qnt_filmes - contador1
    if filmes_cm_nota == 0:
        print(f'{nome_bonito} é paia por não dar nota')
    else:

        media_nota = contador2 /filmes_cm_nota
        print(f'média de notas de {nome_bonito}: {media_nota}')

    informações.pop(0)
    informações_ord_filmes = informações.copy()
    informações_ord_media = informações.copy()
    tamanho_informações = len(informações)
    for i in range(tamanho_informações):
        for j in range(0, tamanho_informações - i - 1):
            media1 = float(informações_ord_media[j].split(' : ')[3])
            media2 = float(informações_ord_media[j+1].split(' : ')[3])
            if media1 < media2:
                informações_ord_media[j], informações_ord_media[j+1] = informações_ord_media[j+1], informações_ord_media[j]
    
    def pegar_indice(item):
        valores = item.split(' : ')
        index3 = float(valores[3])
        index4 = float(valores[4])
        return index3, index4

    for i in range(len(informações_ord_media)):
        for j in range(i + 1, len(informações_ord_media)):
            index3_i, index4_i = pegar_indice(informações_ord_media[i])
            index3_j, index4_j = pegar_indice(informações_ord_media[j])
            if index3_i == index3_j and index4_i < index4_j:
                informações_ord_media[i], informações_ord_media[j] = informações_ord_media[j], informações_ord_media[i]

    for i in range(tamanho_informações):
        for j in range(0, tamanho_informações - i - 1):
            filmes1 = float(informações_ord_filmes[j].split(' : ')[4])
            filmes2 = float(informações_ord_filmes[j+1].split(' : ')[4])
            if filmes1 < filmes2:
                informações_ord_filmes[j], informações_ord_filmes[j+1] = informações_ord_filmes[j+1], informações_ord_filmes[j]

    for i in range(len(informações_ord_filmes)):
        for j in range(i + 1, len(informações_ord_filmes)):
            index3_i, index4_i = pegar_indice(informações_ord_filmes[i])
            index3_j, index4_j = pegar_indice(informações_ord_filmes[j])
            if index4_i == index4_j and index3_i < index3_j:
                informações_ord_filmes[i], informações_ord_filmes[j] = informações_ord_filmes[j], informações_ord_filmes[i]

    somas_decadas = []

    for i in lista_anota:
        decada, parcela = i.split(', ')
        parcela = int(parcela)
        liberado = False
        for j in somas_decadas:
            if j[0] == decada:
                j[1] += parcela
                j[2] +=1
                liberado = True
                break
        if liberado == False:
            somas_decadas.append([decada, parcela, 1])
    
    anos = ['1890', '1900', '1910', '1920', '1930', '1940', '1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020']

    lista_decada = []
    lista_media = []

    for decada, soma, contador in somas_decadas:
        media = soma / contador
        lista_decada.append(decada)
        lista_media.append(round(media, 2))

    for ano in anos:
        if ano not in lista_decada:
            lista_media.insert(anos.index(ano), 0)

    data = {'Décadas': anos, 
           'Média_Notas': lista_media}
    
    janela_resultados(informações_ord_media, informações_ord_filmes, qnt_filmes, media_nota, nome_bonito, data)


def processar_input(event=None):
    nome_usuario = barra.get()
    main(nome_usuario)

janela = Tk()
janela.geometry('900x300')
janela.title('Patron Moral')
janela.config(bg='#1e1e1f')
janela.iconphoto(False, PhotoImage(file='images.png'))
titulo = Label(janela, text='Patreon', font=('Arial 45 bold'), fg='#fafbfc', bg='#1e1e1f')
titulo.place(x=10, y=10)
instrucao = Label(janela, text='Nome de Usuário :', font=('Arial 25'), fg='#fafbfc', bg='#1e1e1f')
instrucao.place(relx=0.5, rely=0.5, anchor='center', x=-200, y=20)
barra = Entry(janela, width=20, font=('Arial 15'))
barra.place(relx=0.5, rely=0.5, anchor='center', x=80, y=20)
barra.bind('<Return>', processar_input)
credito = Label(janela, text='Made by BielNoAppCringe', font=('Arial 9'), fg='#fafbfc', bg='#1e1e1f')
credito.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)
janela.mainloop()


