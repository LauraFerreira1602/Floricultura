from typing import Tuple

from flask import Flask, render_template, redirect, url_for, request, session, flash
from sqlalchemy import select, Select

from models import *
from models import Clientes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/lista_clientes')
def lista_clientes():
    sql_lista_clientes = select(Clientes)
    resultado_clientes = db_session.execute(sql_lista_clientes).scalars().all()
    lista_clientes = []
    for n in resultado_clientes:
        lista_clientes.append(n.serialize_cliente())
        print(lista_clientes[-1])
    return render_template("lista_clientes.html",
                           lista_clientes=lista_clientes)


@app.route('/novo_cliente', methods=['POST', 'GET'])
def novo_cliente():
    if request.method == 'POST':
        if not request.form['form_nome'] or not request.form['form_sobrenome'] or not request.form['form_CPF'] or not \
        request.form['form_telefone']:
            flash("Preencha todos os campos", "error")
        else:
            nome = request.form['form_nome']
            sobrenome = request.form['form_sobrenome']
            CPF = request.form['form_CPF']
            telefone = request.form['form_telefone']

            cliente_CPF: Select[Clientes] = select(Clientes).where(Clientes.CPF == CPF)
            cliente_CPF = db_session.execute(cliente_CPF).scalars().first()
            print(f"user_cpf: {cliente_CPF}")

            if not cliente_CPF:

                cliente = Clientes(Nome=nome, Sobrenome=sobrenome, CPF=int(CPF), telefone=int(telefone))
                print(cliente)

                cliente.save()
                db_session.close()
                flash("Novo cliente cadastrado com sucesso!", "success")
                return redirect(url_for('lista_clientes'))
            else:
                flash(" O CPF ja existe")
    return render_template('novo_cliente.html')


@app.route('/lista_produtos')
def lista_produtos():
    sql_lista_produtos = select(Produtos)
    resultado_produtos = db_session.execute(sql_lista_produtos).scalars().all()
    lista_produtos = []
    for n in resultado_produtos:
        lista_produtos.append(n.serialize_produto())
        print(lista_produtos[-1])
    return render_template("lista_produtos.html",
                           lista_produtos=lista_produtos)


@app.route('/novo_produto', methods=['POST', 'GET'])
def novo_produto():
    if request.method == 'POST':
        if (not request.form['form_nome_produto'] or not request.form['form_tipo'] or not request.form['form_cor'] or
                not request.form['form_preco']):
            flash("Preencha todos os campos", "error")
        else:
            nome_produto = request.form['form_nome_produto']
            tipo = request.form['form_tipo']
            cor = request.form['form_cor']
            preco = request.form['form_preco']

            produto = Produtos(Nome_produto=nome_produto, tipo=tipo, cor=cor, preco=float(preco))
            print(produto)

            produto.save()
            db_session.close()
            flash("Novo produto cadastrado com sucesso!", "success")
            return redirect(url_for('lista_produtos'))
    return render_template('novo_produto.html')


@app.route('/lista_vendas')
def lista_vendas():
    sql_lista_vendas = select(Vendas)
    resultado_vendas = db_session.execute(sql_lista_vendas).scalars().all()
    lista_vendas = []
    for n in resultado_vendas:
        lista_vendas.append(n.serialize_vendas())
        print(lista_vendas[-1])
    return render_template("lista_vendas.html",
                           lista_vendas=lista_vendas)


@app.route('/nova_venda', methods=['POST', 'GET'])
def nova_venda():
    if request.method == 'POST':
        if (not request.form['form_nome'] or not request.form['form_tipo'] or not request.form['form_cor']
                or not request.form['form_preco'] or not request.form['form_id_cliente'] or not request.form['form_id_produto']):
            flash("Preencha todos os campos", "error")
        else:
            nome = request.form['form_nome']
            tipo = request.form['form_tipo']
            cor = request.form['form_cor']
            preco = request.form['form_preco']
            id_cliente = request.form['form_id_cliente']
            id_produto = request.form['form_id_produto']

            vendas = Vendas(Nome=nome, tipo=tipo, cor=cor, preco=float(preco), id_cliente=int(id_cliente), id_produto=int(id_produto))
            print(vendas)

            vendas.save()
            db_session.close()
            flash("Nova venda cadastrada com sucesso!", "success")
            return redirect(url_for('lista_vendas'))
    return render_template('nova_venda.html')

app.run(debug=True)
