from flask import Flask, request, render_template, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# Verifica se o arquivo 'agenda.txt' existe, se não, cria-o
if not os.path.exists('agenda.txt'):
    with open('agenda.txt', 'w') as f:
        pass  # Arquivo criado vazio

@app.route('/')
def menu():
    return render_template('menu.html', mensagem=None)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_contato():
    if request.method == 'POST':
        idcontato = request.form['idcontato']
        nome = request.form['nome']
        telefone = request.form['telefone']
        data_agendamento = request.form['data_agendamento']
        hora_agendamento = request.form['hora_agendamento']
        
        try:
            hora_formatada = datetime.strptime(hora_agendamento, '%H:%M').strftime('%H:%M:%S')
            with open("agenda.txt", "a") as agenda:
                dados = f'ID: {idcontato} / Nome: {nome} / Telefone: {telefone} / Data: {data_agendamento} / Hora: {hora_formatada}\n'
                agenda.write(dados)
            return render_template('menu.html', mensagem='Contato agendado com sucesso')
        except Exception as e:
            return render_template('menu.html', mensagem=f'Erro ao agendar contato: {e}')

    return render_template('cadastrar.html')

@app.route('/listar', methods=['GET'])
def listar_contato():
    with open("agenda.txt", "r") as agenda:
        contatos = agenda.readlines()
    return render_template('listar.html', contatos=contatos)

@app.route('/listar', methods=['POST'])
def deletar_contato():
    nome_deletado = request.form['nome_deletado']
    with open("agenda.txt", "r") as agenda:
        aux = agenda.readlines()
    aux2 = [contato for contato in aux if nome_deletado.lower() not in contato.lower()]
    with open("agenda.txt", "w") as agenda:
        for i in aux2:
            agenda.write(i)
    return redirect(url_for('listar_contato'))

@app.route('/buscar', methods=['POST'])
def buscar_contato_pelo_nome():
    nome = request.form['nome']
    return redirect(url_for('resultado_busca', nome=nome))

@app.route('/resultado_busca/<nome>', methods=['GET'])
def resultado_busca(nome):
    with open("agenda.txt", "r") as agenda:
        contatos = [contato for contato in agenda.readlines() if nome.lower() in contato.lower()]
    return render_template('resultado_busca.html', contatos=contatos, nome_buscado=nome)

# Rotas para o Cliente
@app.route('/cliente')
def cliente_menu():
    return render_template('cliente_menu.html')

@app.route('/cliente/agendar', methods=['GET', 'POST'])
def cliente_agendar():
    mensagem = None  # Inicializa a mensagem como None

    if request.method == 'POST':
        idcontato = request.form['idcontato']
        nome = request.form['nome']
        telefone = request.form['telefone']
        data_agendamento = request.form['data_agendamento']
        hora_agendamento = request.form['hora_agendamento']
        
        try:
            hora_formatada = datetime.strptime(hora_agendamento, '%H:%M').strftime('%H:%M:%S')
            with open("agenda.txt", "a") as agenda:
                dados = f'ID: {idcontato} / Nome: {nome} / Telefone: {telefone} / Data: {data_agendamento} / Hora: {hora_formatada}\n'
                agenda.write(dados)
            mensagem = 'Agendamento realizado com sucesso'  # Define a mensagem de sucesso
        except Exception as e:
            mensagem = f'Erro ao agendar: {e}'  # Define a mensagem de erro

    return render_template('cliente_agendar.html', mensagem=mensagem)

@app.route('/cliente/agendamentos')
def cliente_agendamentos():
    with open("agenda.txt", "r") as agenda:
        contatos = agenda.readlines()
    return render_template('cliente_agendamentos.html', contatos=contatos)

@app.route('/cliente/listar', methods=['GET'])
def cliente_listar_contato():
    with open("agenda.txt", "r") as agenda:
        contatos = agenda.readlines()
    return render_template('cliente_listar.html', contatos=contatos)

if __name__ == '__main__':
    app.run(debug=True)
