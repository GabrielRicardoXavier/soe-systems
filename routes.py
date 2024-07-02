from flask import render_template, redirect, url_for, flash, request, session, send_from_directory, send_file, jsonify
from saie import app, database, bcrypt
from saie.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from saie.models import Usuario, Post, Alunos, Aditamento, MatrizCurricular, Turma, Turma_Pagina, Individual, \
    CodigoAfls, Protocolo_AFLs, Notas_Alunos, CP_Aluno, PEI, Perguntas, Cid, Peso_Nota_P1, Professor, CP_Turma, \
    Recuperacao_Simultanea, Resultado_dos_Alunos, CC, CD, Planejamento, Plano_PcD, Anamnese
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func, and_
from datetime import datetime
import secrets
import os
from werkzeug.utils import secure_filename
import csv
from PIL import Image
import requests


### Decorators / ou Links do site ###
def import_alunos_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith('.csv'):
            reader = csv.reader(file)
            alunos = [row for row in reader if len(row) == 150]
        else:
            lines = file.readlines()
            alunos = [line.strip().split(';') for line in lines if len(line.strip().split(';')) == 150]

        for aluno in alunos:
            aluno_ano_nascimento, aluno_autoriza_imagem, aluno_autoriza_imagem_voz, aluno_autoriza_saida, aluno_bairro, aluno_cep, aluno_certidao_nascimento, aluno_certidao_nascimento_cartorio, aluno_certidao_nascimento_cidade, aluno_certidao_nascimento_data_emissao, aluno_certidao_nascimento_folha, aluno_certidao_nascimento_livro, aluno_certidao_nascimento_termo, aluno_certidao_nascimento_uf, aluno_cidade, aluno_cod_barras, aluno_codigo, aluno_codigo_religiao, aluno_complemento, aluno_cpf, aluno_documentos_faltando, aluno_e_mail, aluno_endereco, aluno_fator_rh, aluno_filho_funcionario, aluno_filho_obreiro, aluno_idade, aluno_inep, aluno_irmao_matriculado, aluno_nacionalidade, aluno_nascimento, aluno_naturalidade, aluno_nome, aluno_observacao, aluno_pcd, aluno_percentual_bolsa, aluno_percentual_desconto, aluno_RA, aluno_raca, aluno_religiao, aluno_rg, aluno_rg_data, aluno_rg_orgao, aluno_rg_uf, aluno_RM, aluno_sexo, aluno_telefone_celular, aluno_telefone_comercial, aluno_telefone_residencial, aluno_tipo_sanguineo, aluno_uf, aluno_uf_naturalidade, escola_codigo, escola_instalacao, escola_nome, mae_bairro, mae_cep, mae_cidade, mae_complemento, mae_cpf, mae_e_mail, mae_endereco, mae_estado_civil, mae_grau_instrucao, mae_nascimento, mae_naturalidade, mae_naturalidade_uf, mae_nome, mae_profissao, mae_telefone, mae_uf, matricula_carteirinha_bloqueada, matricula_cod_serie, matricula_cod_tipo_aluno, matricula_data, matricula_data_matricula_turma, matricula_desligamento_data, matricula_desligamento_motivo, matricula_mes_parcela_final, matricula_mes_parcela_inicio, matricula_motivo, matricula_numero_chamada, matricula_numero_parcela, matricula_observacao, matricula_online, matricula_plano, matricula_pode_sair_com, matricula_restricao, matricula_serie, matricula_tipo_aluno, matricula_turma, pai_bairro, pai_cep, pai_cidade, pai_complemento, pai_cpf, pai_e_mail, pai_endereco, pai_estado_civil, pai_grau_instrucao, pai_nascimento, pai_naturalidade, pai_naturalidade_uf, pai_nome, pai_profissao, pai_telefone, pai_uf, resp_legal_bairro, resp_legal_cep, resp_legal_cidade, resp_legal_ciencia_portal, resp_legal_complemento, resp_legal_cpf, resp_legal_cx_postal, resp_legal_e_mail, resp_legal_endereco, resp_legal_estado_civil, resp_legal_nascimento, resp_legal_nome, resp_legal_outras_rendas, resp_legal_profissao, resp_legal_renda_mensal, resp_legal_rg, resp_legal_rg_data, resp_legal_rg_orgao, resp_legal_rg_uf, resp_legal_telefone, resp_legal_uf, responsavel_bairro, responsavel_cep, responsavel_cidade, responsavel_complemento, responsavel_cpf, responsavel_cx_postal, responsavel_e_mail, responsavel_endereco, responsavel_estado_civil, responsavel_grau_instrucao, responsavel_nascimento, responsavel_nome, responsavel_outras_rendas, responsavel_profissao, responsavel_renda_mensal, responsavel_rg, responsavel_rg_data, responsavel_rg_orgao, responsavel_rg_uf, responsavel_telefone, responsavel_uf, nada_vazio = aluno
            aluno_obj = Alunos(aluno_ano_nascimento=aluno_ano_nascimento,
                               aluno_autoriza_imagem=aluno_autoriza_imagem,
                               aluno_autoriza_imagem_voz=aluno_autoriza_imagem_voz,
                               aluno_autoriza_saida=aluno_autoriza_saida,
                               aluno_bairro=aluno_bairro,
                               aluno_cep=aluno_cep,
                               aluno_certidao_nascimento=aluno_certidao_nascimento,
                               aluno_certidao_nascimento_cartorio=aluno_certidao_nascimento_cartorio,
                               aluno_certidao_nascimento_cidade=aluno_certidao_nascimento_cidade,
                               aluno_certidao_nascimento_data_emissao=aluno_certidao_nascimento_data_emissao,
                               aluno_certidao_nascimento_folha=aluno_certidao_nascimento_folha,
                               aluno_certidao_nascimento_livro=aluno_certidao_nascimento_livro,
                               aluno_certidao_nascimento_termo=aluno_certidao_nascimento_termo,
                               aluno_certidao_nascimento_uf=aluno_certidao_nascimento_uf,
                               aluno_cidade=aluno_cidade,
                               aluno_cod_barras=aluno_cod_barras,
                               aluno_codigo=aluno_codigo,
                               aluno_codigo_religiao=aluno_codigo_religiao,
                               aluno_complemento=aluno_complemento,
                               aluno_cpf=aluno_cpf,
                               aluno_documentos_faltando=aluno_documentos_faltando,
                               aluno_e_mail=aluno_e_mail,
                               aluno_endereco=aluno_endereco,
                               aluno_fator_rh=aluno_fator_rh,
                               aluno_filho_funcionario=aluno_filho_funcionario,
                               aluno_filho_obreiro=aluno_filho_obreiro,
                               aluno_idade=aluno_idade,
                               aluno_inep=aluno_inep,
                               aluno_irmao_matriculado=aluno_irmao_matriculado,
                               aluno_nacionalidade=aluno_nacionalidade,
                               aluno_nascimento=aluno_nascimento,
                               aluno_naturalidade=aluno_naturalidade,
                               aluno_nome=aluno_nome,
                               aluno_observacao=aluno_observacao,
                               aluno_pcd=aluno_pcd,
                               aluno_percentual_bolsa=aluno_percentual_bolsa,
                               aluno_percentual_desconto=aluno_percentual_desconto,
                               aluno_RA=aluno_RA,
                               aluno_raca=aluno_raca,
                               aluno_religiao=aluno_religiao,
                               aluno_rg=aluno_rg,
                               aluno_rg_data=aluno_rg_data,
                               aluno_rg_orgao=aluno_rg_orgao,
                               aluno_rg_uf=aluno_rg_uf,
                               aluno_RM=aluno_RM,
                               aluno_sexo=aluno_sexo,
                               aluno_telefone_celular=aluno_telefone_celular,
                               aluno_telefone_comercial=aluno_telefone_comercial,
                               aluno_telefone_residencial=aluno_telefone_residencial,
                               aluno_tipo_sanguineo=aluno_tipo_sanguineo,
                               aluno_uf=aluno_uf,
                               aluno_uf_naturalidade=aluno_uf_naturalidade,
                               escola_codigo=escola_codigo,
                               escola_instalacao=escola_instalacao,
                               escola_nome=escola_nome,
                               mae_bairro=mae_bairro,
                               mae_cep=mae_cep,
                               mae_cidade=mae_cidade,
                               mae_complemento=mae_complemento,
                               mae_cpf=mae_cpf,
                               mae_e_mail=mae_e_mail,
                               mae_endereco=mae_endereco,
                               mae_estado_civil=mae_estado_civil,
                               mae_grau_instrucao=mae_grau_instrucao,
                               mae_nascimento=mae_nascimento,
                               mae_naturalidade=mae_naturalidade,
                               mae_naturalidade_uf=mae_naturalidade_uf,
                               mae_nome=mae_nome,
                               mae_profissao=mae_profissao,
                               mae_telefone=mae_telefone,
                               mae_uf=mae_uf,
                               matricula_carteirinha_bloqueada=matricula_carteirinha_bloqueada,
                               matricula_cod_serie=matricula_cod_serie,
                               matricula_cod_tipo_aluno=matricula_cod_tipo_aluno,
                               matricula_data=matricula_data,
                               matricula_data_matricula_turma=matricula_data_matricula_turma,
                               matricula_desligamento_data=matricula_desligamento_data,
                               matricula_desligamento_motivo=matricula_desligamento_motivo,
                               matricula_mes_parcela_final=matricula_mes_parcela_final,
                               matricula_mes_parcela_inicio=matricula_mes_parcela_inicio,
                               matricula_motivo=matricula_motivo,
                               matricula_numero_chamada=matricula_numero_chamada,
                               matricula_numero_parcela=matricula_numero_parcela,
                               matricula_observacao=matricula_observacao,
                               matricula_online=matricula_online,
                               matricula_plano=matricula_plano,
                               matricula_pode_sair_com=matricula_pode_sair_com,
                               matricula_restricao=matricula_restricao,
                               matricula_serie=matricula_serie,
                               matricula_tipo_aluno=matricula_tipo_aluno,
                               matricula_turma=matricula_turma,
                               pai_bairro=pai_bairro,
                               pai_cep=pai_cep,
                               pai_cidade=pai_cidade,
                               pai_complemento=pai_complemento,
                               pai_cpf=pai_cpf,
                               pai_e_mail=pai_e_mail,
                               pai_endereco=pai_endereco,
                               pai_estado_civil=pai_estado_civil,
                               pai_grau_instrucao=pai_grau_instrucao,
                               pai_nascimento=pai_nascimento,
                               pai_naturalidade=pai_naturalidade,
                               pai_naturalidade_uf=pai_naturalidade_uf,
                               pai_nome=pai_nome,
                               pai_profissao=pai_profissao,
                               pai_telefone=pai_telefone,
                               pai_uf=pai_uf,
                               resp_legal_bairro=resp_legal_bairro,
                               resp_legal_cep=resp_legal_cep,
                               resp_legal_cidade=resp_legal_cidade,
                               resp_legal_ciencia_portal=resp_legal_ciencia_portal,
                               resp_legal_complemento=resp_legal_complemento,
                               resp_legal_cpf=resp_legal_cpf,
                               resp_legal_cx_postal=resp_legal_cx_postal,
                               resp_legal_e_mail=resp_legal_e_mail,
                               resp_legal_endereco=resp_legal_endereco,
                               resp_legal_estado_civil=resp_legal_estado_civil,
                               resp_legal_nascimento=resp_legal_nascimento,
                               resp_legal_nome=resp_legal_nome,
                               resp_legal_outras_rendas=resp_legal_outras_rendas,
                               resp_legal_profissao=resp_legal_profissao,
                               resp_legal_renda_mensal=resp_legal_renda_mensal,
                               resp_legal_rg=resp_legal_rg,
                               resp_legal_rg_data=resp_legal_rg_data,
                               resp_legal_rg_orgao=resp_legal_rg_orgao,
                               resp_legal_rg_uf=resp_legal_rg_uf,
                               resp_legal_telefone=resp_legal_telefone,
                               resp_legal_uf=resp_legal_uf,
                               responsavel_bairro=responsavel_bairro,
                               responsavel_cep=responsavel_cep,
                               responsavel_cidade=responsavel_cidade,
                               responsavel_complemento=responsavel_complemento,
                               responsavel_cpf=responsavel_cpf,
                               responsavel_cx_postal=responsavel_cx_postal,
                               responsavel_e_mail=responsavel_e_mail,
                               responsavel_endereco=responsavel_endereco,
                               responsavel_estado_civil=responsavel_estado_civil,
                               responsavel_grau_instrucao=responsavel_grau_instrucao,
                               responsavel_nascimento=responsavel_nascimento,
                               responsavel_nome=responsavel_nome,
                               responsavel_outras_rendas=responsavel_outras_rendas,
                               responsavel_profissao=responsavel_profissao,
                               responsavel_renda_mensal=responsavel_renda_mensal,
                               responsavel_rg=responsavel_rg,
                               responsavel_rg_data=responsavel_rg_data,
                               responsavel_rg_orgao=responsavel_rg_orgao,
                               responsavel_rg_uf=responsavel_rg_uf,
                               responsavel_telefone=responsavel_telefone,
                               responsavel_uf=responsavel_uf
                               )
            database.session.add(aluno_obj)

        database.session.commit()


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.chmod(UPLOAD_FOLDER, 0o777)


@app.route('/suporte')
@login_required
def contato():
    return render_template('contato.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        alunos_file = request.files.get('file')
        if alunos_file:
            filename, file_extension = os.path.splitext(alunos_file.filename)
            if file_extension.lower() == '.txt' or file_extension.lower() == '.csv':
                file_path = os.path.join(UPLOAD_FOLDER, alunos_file.filename)
                alunos_file.save(file_path)
                import_alunos_from_file(file_path)
                return render_template('home.html')
            else:
                flash('Apenas (.txt e .csv) são permitidos!', 'alert-danger')
    return render_template('home.html')

@app.route('/suporte/FAQ', methods=['GET', 'POST'])
@login_required
def contatoFAQ():
    perguntas_query = Perguntas.query.all()
    if request.method == 'POST':
        titulo_pergunta = request.form.get('titulo_pergunta')
        corpo_pergunta = request.form.get('corpo_pergunta')
        existing_pergunta = Perguntas.query.filter_by(titulo_pergunta=titulo_pergunta).first()
        if existing_pergunta:
            flash('Essa pergunta já foi feita!', 'alert-info')
        else:
            pergunta = Perguntas(
                titulo_pergunta=titulo_pergunta,
                corpo_pergunta=corpo_pergunta
            )
            database.session.add(pergunta)
            database.session.commit()
            flash('Pergunta Feita com Sucesso, Espere por até 24h para sua resposta', 'alert-success')

        return redirect('/suporte/FAQ')

    return render_template('contatoFAQ.html', perguntas_query=perguntas_query)


@app.route("/suporte/ajuda%contatos")
@login_required
def contato_ajudatele():
    return render_template('contato_ajudatele.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login Feito com Sucesso no E-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou Senha Incorretos', 'alert_denger')
    if form_criarconta.validate_on_submit and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta Criada para o E-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    posts = Post.query.order_by(Post.id.desc())
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
    return render_template('criarpost.html', form=form, posts=posts)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_funcao(form):
    lista_funcao = []
    for campo in form:
        if 'funcao_' in campo.name:
            if campo.data:
                lista_funcao.append(campo.label.text)
    return ';'.join(lista_funcao)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.funcao = atualizar_funcao(form)
        database.session.commit()
        flash(f'Perfil Atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('criar_post'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('criar_post'))
    else:
        abort(403, 'Unauthorized action.')


def import_turma_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith('.csv'):
            reader = csv.reader(file)
            turmas = [row for row in reader if len(row) == 3]
        else:
            lines = file.readlines()
            turmas = [line.strip().split(';') for line in lines if len(line.strip().split(';')) == 3]

        for turmasfor in turmas:
            turma, serie, turno = turmasfor
            turma_obj = Turma(
                turma=turma,
                serie=serie,
                turno=turno
            )
            database.session.add(turma_obj)  # Assuming `database.session` is properly configured
        database.session.commit()


@app.route('/series', methods=['GET', 'POST'])
@login_required
def series_config():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    turma_file = request.files.get('file')
    if turma_file:
        filename, file_extension = os.path.splitext(turma_file.filename)
        if file_extension.lower() == '.txt' or file_extension.lower() == '.csv':
            file_path = os.path.join(UPLOAD_FOLDER, turma_file.filename)
            turma_file.save(file_path)
            import_turma_from_file(file_path)
            return redirect('/')
        else:
            flash('Apenas (.txt e .csv) são permitidos!', 'alert-danger')
    if request.method == 'POST':
        turma = request.form.get('turma')
        if MatrizCurricular.query.filter_by(turma=turma).first():
            flash('Turma já Registrada, Registre Outra Turma ou Edite!', 'alert-danger')
        else:
            config_series = MatrizCurricular(
                turma=turma,
                serie=request.form.get('serie'),
                turno=request.form.get('turno'),
                nivel=request.form.get('nivel'),
                Frente_Gramatica='Frente_Gramatica' in request.form,
                Frente_Literatura='Frente_Literatura' in request.form,
                Aprofundamento_Biologia='Aprofundamento_Biologia' in request.form,
                Aprofundamento_Fisica='Aprofundamento_Fisica' in request.form,
                Aprofundamento_Geografia='Aprofundamento_Geografia' in request.form,
                Aprofundamento_Historia='Aprofundamento_Historia' in request.form,
                Aprofundamento_Lingua_Inglesa='Aprofundamento_Lingua_Inglesa' in request.form,
                Aprofundamento_Quimica='Aprofundamento_Quimica' in request.form,
                Argumentacao='Argumentacao' in request.form,
                Arte='Arte' in request.form,
                Arte_Cultura_Desporto='Arte_Cultura_Desporto' in request.form,
                Biologia='Biologia' in request.form,
                Educacao_Fisica='Educacao_Fisica' in request.form,
                Cultura_Geral='Cultura_Geral' in request.form,
                Debates_Filosoficos='Debates_Filosoficos' in request.form,
                Ensino_Religioso='Ensino_Religioso' in request.form,
                Filosofia='Filosofia' in request.form,
                Fisica='Fisica' in request.form,
                Geografia='Geografia' in request.form,
                Historia='Historia' in request.form,
                Investigacao_Matematica='Investigacao_Matematica' in request.form,
                Itinerario_Aprofundamento='Itinerario_Aprofundamento' in request.form,
                Lingua_Portuguesa='Lingua_Portuguesa' in request.form,
                Matematica='Matematica' in request.form,
                Projeto_Vida='Projeto_Vida' in request.form,
                Quimica='Quimica' in request.form,
                Redacao='Redacao' in request.form,
                Sociologia='Sociologia' in request.form,
                Ling_Espanhol='Ling_Espanhol' in request.form,
                Ling_Ingles='Ling_Ingles' in request.form,
                Ciencias='Ciencias' in request.form,
                Educacao_Religiosa='Educacao_Religiosa' in request.form,
                Agencia_Voluntariado='Agencia_Voluntariado' in request.form,
                Analise_Obras_Artes='Analise_Obras_Artes' in request.form,
                Estudo_Direito_Constitucional='Estudo_Direito_Constitucional' in request.form,
                Marketing_Influencia_Digital='Marketing_Influencia_Digital' in request.form,
                Corpo_Gestos_Movimentos='Corpo_Gestos_Movimentos' in request.form,
                Educacao_Fisica_inf='Educacao_Fisica_inf' in request.form,
                Ensino_Religioso_Principios_Valores='Ensino_Religioso_Principios_Valores' in request.form,
                Escuta_Fala_Pensamento_Imaginacao='Escuta_Fala_Pensamento_Imaginacao' in request.form,
                Espacos_Tempos_Quantidades_Relacoes_Transformacoes='Espacos_Tempos_Quantidades_Relacoes_Transformacoes' in request.form,
                Ingles_Bilingue='Ingles_Bilingue' in request.form,
                Lingua_Estrangeira_Moderna_Ingles='Lingua_Estrangeira_Moderna_Ingles' in request.form,
                Musicalizacao='Musicalizacao' in request.form,
                Eu_Outro_Nos='Eu_Outro_Nos' in request.form,
                Tracos_Sons_Cores_Formas='Tracos_Sons_Cores_Formas' in request.form
            )

            database.session.add(config_series)
            database.session.commit()
            flash('Matriz Curricular e Turma Cadastrada com Sucesso!', 'alert-success')
        return redirect(url_for('series_config'))
    return render_template('series_config.html', foto_perfil=foto_perfil)


@app.route('/series/pesquisar', methods=['GET', 'POST'])
@login_required
def series_config_pesquisar():
    turma_query_matriz = MatrizCurricular.query.all()

    if request.method == 'POST':
        selected_turma = request.form.get('turma')
        checkboxes = MatrizCurricular.query.filter(MatrizCurricular.turma.like(selected_turma)).all()
        if turma_query_matriz:
            flash('Dados carregados com sucesso!', 'alert-success')
        else:
            flash('Turma não encontrada na tabela MatrizCurricular!', 'alert-danger')

        flash('Edição feita com sucesso!', 'alert-success')

        return render_template('series_config_pesquisar.html', turma_query_matriz=turma_query_matriz,
                               selected_turma=selected_turma, checkboxes=checkboxes)
    return render_template('series_config_pesquisar.html', turma_query_matriz=turma_query_matriz)


@app.route('/importar/imagem/saieDB', methods=['GET', 'POST'])
def import_foto_alunos():
    if request.method == 'POST':
        arquivo = request.files['arquivo']
        if arquivo and arquivo.filename.endswith('.jpg'):
            nome_arquivo = secure_filename(arquivo.filename)  # Segurança para o nome do arquivo
            codigo_aluno = nome_arquivo.split('.')[0]  # Extrair o código do nome do arquivo
            aluno = Alunos.query.filter_by(aluno_codigo=codigo_aluno).first()

            if aluno:
                caminho_arquivo = os.path.join('foto_alunos', nome_arquivo)  # Atualize o caminho
                arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo))
                aluno.foto_aluno_nome_arquivo = nome_arquivo
                aluno.foto_aluno_caminho_arquivo = caminho_arquivo
                database.session.commit()
                flash('Foto Importada.', 'alert-success')
            else:
                flash('Importação não funcionou. Aluno não encontrado.', 'alert-danger')
        else:
            flash('Apenas arquivos JPG são permitidos.', 'alert-warning')

    alunos = Alunos.query.all()
    return render_template('import_foto_alunos.html', alunos=alunos)


######################################################################
@app.route('/aditamento', methods=['GET', 'POST'])
@login_required
def aditamento():
    nome_alunoquery = Alunos.query.order_by(func.lower(Alunos.aluno_nome)).all()

    if request.method == 'POST':
        aluno_nome = request.form.get('aluno_nome')
        diagnostico = request.form.get('diagnostico')
        dia_laudo = request.form.get('dia_laudo')
        mes_laudo = request.form.get('mes_laudo')
        ano_laudo = request.form.get('ano_laudo')
        nome_medico = request.form.get('nome_medico')
        crm = request.form.get('crm')
        protocolo = request.form.get('protocolo')
        fm1 = request.form.get('fm1')
        fm2 = request.form.get('fm2')
        fm3 = request.form.get('fm3')
        fm4 = request.form.get('fm4')
        fm5 = request.form.get('fm5')
        fm6 = request.form.get('fm6')
        ec1 = request.form.get('ec1')
        ec2 = request.form.get('ec2')
        ec3 = request.form.get('ec3')
        ec4 = request.form.get('ec4')
        ec5 = request.form.get('ec5')
        ec6 = request.form.get('ec6')

        if Aditamento.query.filter_by(nome_aluno=aluno_nome).first():
            flash('Este aluno já foi registrado! Clique em Pesquisar e Edite ou Registre outro aluno.', 'alert-danger')
        else:
            aluno_selecionado = Alunos.query.filter_by(aluno_nome=aluno_nome).first()

            if aluno_selecionado:
                aditamento = Aditamento(
                    nome_aluno=aluno_selecionado.aluno_nome,
                    codigo_aluno=aluno_selecionado.aluno_codigo,
                    serie_matricula=aluno_selecionado.matricula_serie,
                    turma_matricula=aluno_selecionado.matricula_turma,
                    nome_mae=aluno_selecionado.mae_nome,
                    endereco=aluno_selecionado.aluno_endereco,
                    unidade_escolar=aluno_selecionado.escola_nome,
                    diagnostico=diagnostico,
                    nascimento=aluno_selecionado.aluno_nascimento,
                    dia_laudo=dia_laudo,
                    mes_laudo=mes_laudo,
                    ano_laudo=ano_laudo,
                    nome_medico=nome_medico,
                    crm=crm,
                    protocolo=protocolo,
                    nome_responsavel=aluno_selecionado.resp_legal_nome,
                    numero_registro=aluno_selecionado.resp_legal_rg,
                    orgao=aluno_selecionado.resp_legal_rg_orgao,
                    uf=aluno_selecionado.resp_legal_rg_uf,
                    cpf=aluno_selecionado.resp_legal_cpf,
                    fm1=fm1,
                    fm2=fm2,
                    fm3=fm3,
                    fm4=fm4,
                    fm5=fm5,
                    fm6=fm6,
                    ec1=ec1,
                    ec2=ec2,
                    ec3=ec3,
                    ec4=ec4,
                    ec5=ec5,
                    ec6=ec6
                )

                database.session.add(aditamento)
                database.session.commit()
                flash('Aditamento feito com sucesso!', 'alert-success')
            else:
                flash('Ocorreu algum erro. Verifique se há algo errado nas informações do Aluno.', 'alert-danger')

    return render_template('aditamento.html', nome_alunoquery=nome_alunoquery)


@app.route('/foto_alunos/<path:filename>')
def get_photo(filename):
    return send_from_directory('foto_alunos', filename)


@app.route('/aditamento/pesquisa', methods=['GET', 'POST'])
@login_required
def aditamento_pesquisa():
    nomes_aditamentoquery = Aditamento.query.order_by(func.lower(Aditamento.nome_aluno)).all()
    if request.method == 'POST':
        nome_aluno = request.form.get('nome_aluno')
        aditamento = Aditamento.query.filter_by(nome_aluno=nome_aluno).first()
        if aditamento:
            aditamento.serie_matricula = request.form.get('serie')
            aditamento.turma_matricula = request.form.get('turma')
            aditamento.nome_mae = request.form.get('nome_mae')
            aditamento.endereco = request.form.get('endereco')
            aditamento.unidade_escolar = request.form.get('unidade_escolar')
            aditamento.diagnostico = request.form.get('diagnostico')
            aditamento.nascimento = request.form.get('nascimento')
            aditamento.dia_laudo = request.form.get('dia_laudo')
            aditamento.mes_laudo = request.form.get('mes_laudo')
            aditamento.ano_laudo = request.form.get('ano_laudo')
            aditamento.nome_medico = request.form.get('nome_medico')
            aditamento.crm = request.form.get('crm')
            aditamento.protocolo = request.form.get('protocolo')
            aditamento.nome_responsavel = request.form.get('nome_responsavel')
            aditamento.numero_registro = request.form.get('numero_registro')
            aditamento.orgao = request.form.get('orgao')
            aditamento.uf = request.form.get('uf')
            aditamento.cpf = request.form.get('cpf')
            aditamento.fm1 = request.form.get('fm1')
            aditamento.fm2 = request.form.get('fm2')
            aditamento.fm3 = request.form.get('fm3')
            aditamento.fm4 = request.form.get('fm4')
            aditamento.fm5 = request.form.get('fm5')
            aditamento.fm6 = request.form.get('fm6')
            aditamento.ec1 = request.form.get('ec1')
            aditamento.ec2 = request.form.get('ec2')
            aditamento.ec3 = request.form.get('ec3')
            aditamento.ec4 = request.form.get('ec4')
            aditamento.ec5 = request.form.get('ec5')
            aditamento.ec6 = request.form.get('ec6')

            database.session.commit()
            flash('Aditamento atualizado com sucesso!', 'alert-success')
        else:
            flash('Aluno não encontrado.', 'alert-danger')

    return render_template('aditamento_pesquisa.html', nomes_aditamentoquery=nomes_aditamentoquery)


######################################################################
@app.route('/turma/pesquisa', methods=['GET', 'POST'])
@login_required
def turma_pesquisa():
    turma_pagina_query = Turma_Pagina.query.order_by(func.lower(Turma_Pagina.turma)).all()
    current_date = datetime.now()
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
              "novembro", "dezembro"]
    formatted_date = f"{current_date.day} de {months[current_date.month - 1]} de {current_date.year}"
    if request.method == 'POST':
        return redirect('/turma')
    return render_template('turma_pesquisa.html', turma_pagina_query=turma_pagina_query, formatted_date=formatted_date)


@app.route('/turma', methods=['GET', 'POST'])
@login_required
def turma():
    turmaquery = Turma.query.all()
    current_date = datetime.now()
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
              "novembro", "dezembro"]
    formatted_date = f"{current_date.day} de {months[current_date.month - 1]} de {current_date.year}"
    if request.method == 'POST':
        # Get the form data
        turma = request.form.get('turma')
        professor = request.form.get('professor')
        opcao101 = request.form.get('opcao101')
        opcao102 = request.form.get('opcao102')
        opcao103 = request.form.get('opcao103')
        opcao104 = request.form.get('opcao104')
        opcao105 = request.form.get('opcao105')
        opcao106 = request.form.get('opcao106')
        opcao107 = request.form.get('opcao107')
        opcao108 = request.form.get('opcao108')
        opcao109 = request.form.get('opcao109')
        opcao110 = request.form.get('opcao110')
        opcao111 = request.form.get('opcao111')
        opcao112 = request.form.get('opcao112')
        opcao113 = request.form.get('opcao113')
        opcao114 = request.form.get('opcao114')
        opcao115 = request.form.get('opcao115')
        opcao116 = request.form.get('opcao116')
        opcao117 = request.form.get('opcao117')
        opcao118 = request.form.get('opcao118')
        opcao119 = request.form.get('opcao119')
        opcao120 = request.form.get('opcao120')
        opcao121 = request.form.get('opcao121')
        opcao122 = request.form.get('opcao122')
        opcao123 = request.form.get('opcao123')
        opcao124 = request.form.get('opcao124')
        opcao125 = request.form.get('opcao125')
        opcao126 = request.form.get('opcao126')
        opcao127 = request.form.get('opcao127')
        opcao128 = request.form.get('opcao128')
        opcao129 = request.form.get('opcao129')
        opcao130 = request.form.get('opcao130')
        opcao131 = request.form.get('opcao131')
        # Continue getting the values for the rest of the checkboxes (opcao103, opcao104, ..., opcao131)

        turma_selecionado = Turma.query.filter_by(turma=turma).first()
        if turma_selecionado:
            session['turma_id'] = turma_selecionado.id
            session['professor'] = professor

            turma_pagina = Turma_Pagina(
                turma=turma_selecionado.turma,
                serie=turma_selecionado.serie,
                turno=turma_selecionado.turno,
                professores=professor,
                opcao101=opcao101,
                opcao102=opcao102,
                opcao103=opcao103,
                opcao104=opcao104,
                opcao105=opcao105,
                opcao106=opcao106,
                opcao107=opcao107,
                opcao108=opcao108,
                opcao109=opcao109,
                opcao110=opcao110,
                opcao111=opcao111,
                opcao112=opcao112,
                opcao113=opcao113,
                opcao114=opcao114,
                opcao115=opcao115,
                opcao116=opcao116,
                opcao117=opcao117,
                opcao118=opcao118,
                opcao119=opcao119,
                opcao120=opcao120,
                opcao121=opcao121,
                opcao122=opcao122,
                opcao123=opcao123,
                opcao124=opcao124,
                opcao125=opcao125,
                opcao126=opcao126,
                opcao127=opcao127,
                opcao128=opcao128,
                opcao129=opcao129,
                opcao130=opcao130,
                opcao131=opcao131
            )

            # Save the new entry to the database
            database.session.add(turma_pagina)
            database.session.commit()

        # Redirect to a page to display a success message or go to another route
        return redirect(url_for('turma_alunoscitadosdezoito'))

    return render_template('turma.html', turmaquery=turmaquery, formatted_date=formatted_date)


@app.route('/turma/alunos%citados', methods=['GET', 'POST'])
@login_required
def turma_alunoscitadosdezoito():
    turma_id = session.get('turma_id')
    professor = session.get('professor')
    turma_selecionada = Turma.query.get(turma_id)
    if turma_selecionada:
        if request.method == 'POST':
            alunos_citados_118 = request.form.get('alunos_citados_118')
            turmapagina = Turma_Pagina.query.filter_by(turma=turma_selecionada.turma).first()

            if turmapagina:
                turmapagina.alunos_citados_118 = alunos_citados_118
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/turma/alunos%citados%vinte')
            else:
                flash('Algo deu Errado Revise se o Campo está Preenchido Corretamente', 'alert-danger')

    return render_template('turma_alunoscitadosdezoito.html', professor=professor, turma_selecionada=turma_selecionada)


@app.route('/turma/alunos%citados%vinte', methods=['GET', 'POST'])
@login_required
def turma_alunoscitadosvinte():
    turma_id = session.get('turma_id')
    professor = session.get('professor')
    turma_selecionada = Turma.query.get(turma_id)
    if turma_selecionada:
        if request.method == 'POST':
            alunos_citados_120 = request.form.get('alunos_citados_120')
            turmapagina = Turma_Pagina.query.filter_by(turma=turma_selecionada.turma).first()

            if turmapagina:
                turmapagina.alunos_citados_120 = alunos_citados_120
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/turma/alunos%citados%trinta')
            else:
                flash('Algo deu Errado Revise se o Campo está Preenchido Corretamente', 'alert-danger')
    return render_template('turma_alunoscitadosvinte.html', professor=professor, turma_selecionada=turma_selecionada)


@app.route('/turma/alunos%citados%trinta', methods=['GET', 'POST'])
@login_required
def turma_alunoscitadostrinta():
    turma_id = session.get('turma_id')
    professor = session.get('professor')
    turma_selecionada = Turma.query.get(turma_id)
    if turma_selecionada:
        if request.method == 'POST':
            alunos_citados_130 = request.form.get('alunos_citados_130')
            turmapagina = Turma_Pagina.query.filter_by(turma=turma_selecionada.turma).first()

            if turmapagina:
                turmapagina.alunos_citados_130 = alunos_citados_130
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/turma/observacoes')
            else:
                flash('Algo deu Errado Revise se o Campo está Preenchido Corretamente', 'alert-danger')
    return render_template('turma_alunoscitadostrinta.html', professor=professor, turma_selecionada=turma_selecionada)


@app.route('/turma/observacoes', methods=['GET', 'POST'])
@login_required
def turma_observacoesadicionais():
    turma_id = session.get('turma_id')
    professor = session.get('professor')
    turma_selecionada = Turma.query.get(turma_id)
    if turma_selecionada:
        if request.method == 'POST':
            alunos_obs_adicionais = request.form.get('alunos_obs_adicionais')
            turmapagina = Turma_Pagina.query.filter_by(turma=turma_selecionada.turma).first()

            if turmapagina:
                turmapagina.alunos_obs_adicionais = alunos_obs_adicionais
                database.session.commit()
                flash('Formulário de Turma Concluído', 'alert-success')
                return redirect('/turma')
            else:
                flash('Algo deu Errado Revise se o Campo está Preenchido Corretamente', 'alert-danger')
    return render_template('turma_observacoesadicionais.html', professor=professor, turma_selecionada=turma_selecionada)


######################################################################
@app.route('/individual/pesquisa', methods=['GET', 'POST'])
@login_required
def individual_pesquisa():
    individual_query = Individual.query.order_by(func.lower(Individual.aluno_nome)).all()
    if request.method == 'POST':
        return redirect('/individual')
    return render_template('individual_pesquisa.html', individual_query=individual_query)


@app.route('/individual', methods=['GET', 'POST'])
@login_required
def individual():
    nome_alunoquery = Alunos.query.order_by(func.lower(Alunos.aluno_nome)).all()
    if request.method == 'POST':
        aluno_nome = request.form.get('aluno_nome')
        professores = request.form.get('professor')
        opcao101 = request.form.get('opcao101')
        opcao102 = request.form.get('opcao102')
        opcao103 = request.form.get('opcao103')
        opcao104 = request.form.get('opcao104')
        opcao105 = request.form.get('opcao105')
        opcao106 = request.form.get('opcao106')
        opcao107 = request.form.get('opcao107')
        opcao108 = request.form.get('opcao108')
        opcao109 = request.form.get('opcao109')
        opcao110 = request.form.get('opcao110')
        opcao111 = request.form.get('opcao111')
        opcao112 = request.form.get('opcao112')
        opcao113 = request.form.get('opcao113')
        opcao114 = request.form.get('opcao114')
        opcao115 = request.form.get('opcao115')
        opcao116 = request.form.get('opcao116')
        opcao117 = request.form.get('opcao117')
        opcao118 = request.form.get('opcao118')
        opcao119 = request.form.get('opcao119')
        opcao120 = request.form.get('opcao120')
        opcao121 = request.form.get('opcao121')
        opcao122 = request.form.get('opcao122')

        aluno_selecionado = Alunos.query.filter_by(aluno_nome=aluno_nome).first()

        if aluno_selecionado:
            # Salve os dados na sessão para acessá-los posteriormente na próxima página
            session['aluno_id'] = aluno_selecionado.id
            session['professor'] = professores

            individual = Individual(
                aluno_nome=aluno_selecionado.aluno_nome,
                serie_aluno=aluno_selecionado.matricula_serie,
                turma_aluno=aluno_selecionado.matricula_turma,
                professores=professores,
                opcao101=opcao101,
                opcao102=opcao102,
                opcao103=opcao103,
                opcao104=opcao104,
                opcao105=opcao105,
                opcao106=opcao106,
                opcao107=opcao107,
                opcao108=opcao108,
                opcao109=opcao109,
                opcao110=opcao110,
                opcao111=opcao111,
                opcao112=opcao112,
                opcao113=opcao113,
                opcao114=opcao114,
                opcao115=opcao115,
                opcao116=opcao116,
                opcao117=opcao117,
                opcao118=opcao118,
                opcao119=opcao119,
                opcao120=opcao120,
                opcao121=opcao121,
                opcao122=opcao122
            )

            database.session.add(individual)
            database.session.commit()

            session['aluno_selecionado'] = aluno_selecionado.aluno_nome
            flash('Continue o Formulário.', 'alert-success')
            return redirect('/individual/queixa')
        else:
            flash('Ocorreu algum erro. Verifique se há algum campo faltando.', 'alert-danger')
    return render_template('individual.html', nome_alunoquery=nome_alunoquery)


@app.route('/individual/queixa', methods=['GET', 'POST'])
@login_required
def individual_queixa():
    aluno_id = session.get('aluno_id')
    professor = session.get('professor')
    aluno_selecionado = Alunos.query.get(aluno_id)

    if aluno_selecionado:
        if request.method == 'POST':
            alunos_dificuldades = request.form.get('alunos_dificuldades')
            individual = Individual.query.filter_by(aluno_nome=aluno_selecionado.aluno_nome).first()

            if individual:
                individual.alunos_dificuldades = alunos_dificuldades
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/individual/estrategia')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    else:
        flash('Aluno não encontrado', 'alert-danger')
        return redirect('/individual')
    return render_template('individual_queixa.html', aluno_selecionado=aluno_selecionado, professor=professor)


@app.route('/individual/estrategia', methods=['GET', 'POST'])
@login_required
def individual_estrategia():
    aluno_id = session.get('aluno_id')
    professor = session.get('professor')
    aluno_selecionado = Alunos.query.get(aluno_id)

    if aluno_selecionado:
        if request.method == 'POST':
            alunos_estrategias = request.form.get('alunos_estrategias')
            individual = Individual.query.filter_by(aluno_nome=aluno_selecionado.aluno_nome).first()

            if individual:
                individual.alunos_estrategias = alunos_estrategias
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/individual/encaminhamentos')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    else:
        flash('Aluno não encontrado', 'alert-danger')
        return redirect('/individual')
    return render_template('individual_estrategia.html', aluno_selecionado=aluno_selecionado, professor=professor)


@app.route('/individual/encaminhamentos', methods=['GET', 'POST'])
@login_required
def individual_encaminhamentos():
    aluno_id = session.get('aluno_id')
    professor = session.get('professor')
    aluno_selecionado = Alunos.query.get(aluno_id)

    if aluno_selecionado:
        if request.method == 'POST':
            encaminhamentos_escolares = request.form.get('encaminhamentos_escolares')
            individual = Individual.query.filter_by(aluno_nome=aluno_selecionado.aluno_nome).first()

            if individual:
                individual.encaminhamentos_escolares = encaminhamentos_escolares
                database.session.commit()
                flash('Formulário Completo!', 'alert-success')
                return redirect('/individual')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    else:
        flash('Aluno não encontrado', 'alert-danger')
        return redirect('/individual')
    return render_template('individual_encaminhamentos.html', aluno_selecionado=aluno_selecionado, professor=professor)


######################################################################
@app.route('/anamnese_pesquisa', methods=['GET', 'POST'])
@login_required
def anamnese_pesquisa():
    nome_aditamentouery = Anamnese.query.order_by(func.lower(Anamnese.aluno_nome)).all()
    return render_template('anamnese_pesquisa.html', nome_aditamentouery=nome_aditamentouery)

@app.route('/anamnese', methods=['GET', 'POST'])
@login_required
def anamnese():
    nome_alunoquery = Alunos.query.order_by(func.lower(Alunos.aluno_nome)).all()
    if request.method == 'POST':
        aluno_nome = request.form.get('aluno_nome')
        data_laudo = request.form.get('data_laudo')
        medico = request.form.get('medico')
        crm = request.form.get('crm')
        data_protocolo = request.form.get('data_protocolo')
        hipotese = request.form.get('hipotese')
        cor = request.form.get('cor')
        mae_idade = request.form.get('mae_idade')
        pai_idade = request.form.get('pai_idade')
        familia_religiao = request.form.get('familia_religiao')
        aluno_selecionado_anam = Alunos.query.filter_by(aluno_nome=aluno_nome).first()

        if aluno_selecionado_anam:

            anamnese = Anamnese(
                data_laudo=data_laudo,
                medico=medico,
                crm=crm,
                data_protocolo=data_protocolo,
                hipotese=hipotese,
                aluno_nome=aluno_selecionado_anam.aluno_nome,
                matricula=aluno_selecionado_anam.aluno_codigo,
                idade=aluno_selecionado_anam.aluno_idade,
                nascimento=aluno_selecionado_anam.aluno_nascimento,
                sexo=aluno_selecionado_anam.aluno_sexo,
                cor=cor,
                naturalidade=aluno_selecionado_anam.aluno_naturalidade,
                nacionalidade=aluno_selecionado_anam.aluno_nacionalidade,
                endereco=aluno_selecionado_anam.aluno_endereco,
                unidade_escolar=aluno_selecionado_anam.escola_nome,
                serie=aluno_selecionado_anam.matricula_serie,
                turma=aluno_selecionado_anam.matricula_turma,
                mae_nome=aluno_selecionado_anam.mae_nome,
                mae_cpf=aluno_selecionado_anam.mae_cpf,
                mae_profissao=aluno_selecionado_anam.mae_profissao,
                mae_idade=mae_idade,
                mae_grau_instrucao=aluno_selecionado_anam.mae_grau_instrucao,
                pai_nome=aluno_selecionado_anam.pai_nome,
                pai_cpf=aluno_selecionado_anam.pai_cpf,
                pai_profissao=aluno_selecionado_anam.pai_profissao,
                pai_idade=pai_idade,
                pai_grau_instrucao=aluno_selecionado_anam.pai_grau_instrucao,
                familia_religiao=familia_religiao
            )
            database.session.add(anamnese)
            database.session.commit()

            session['aluno_id_anam'] = aluno_selecionado_anam.id
            session['aluno_selecionado_anam'] = aluno_selecionado_anam.aluno_nome
            flash('Continue o Formulário.', 'alert-success')
            return redirect('/anamnese/questionario')
        else:
            flash('Ocorreu algum erro. Verifique se há algum campo faltando.', 'alert-danger')
    return render_template('anamnese.html', nome_alunoquery=nome_alunoquery)


@app.route('/anamnese/questionario', methods=['GET', 'POST'])
@login_required
def anamnese_questionario():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)

    if aluno_selecionado_anam:
        if request.method == 'POST':
            opcao401 = request.form.get('opcao401')
            opcao40101 = request.form.getlist(
                'opcao40101')  # Recebe a lista de professores selecionados
            opcao40101_str = ",".join(opcao40101)  # Converte a lista em uma string com vírgulas
            opcao402 = request.form.get('opcao402')
            opcao40201 = request.form.getlist(
                'opcao40201')  # Recebe a lista de professores selecionados
            opcao40201_str = ",".join(opcao40201)  # Converte a lista em uma string com vírgulas
            qual402 = request.form.get('qual402')
            opcao403 = request.form.get('opcao403')
            qual403 = request.form.get('qual403')
            opcao404 = request.form.get('opcao404')
            opcao40401 = request.form.getlist(
                'opcao40401')  # Recebe a lista de professores selecionados
            opcao40401_str = ",".join(opcao40401)  # Converte a lista em uma string com vírgulas
            qual404 = request.form.get('qual404')
            opcao405 = request.form.get('opcao405')
            opcao40501 = request.form.getlist(
                'opcao40501')  # Recebe a lista de professores selecionados
            opcao40501_str = ",".join(opcao40501)  # Converte a lista em uma string com vírgulas
            qual405 = request.form.get('qual405')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.opcao401 = opcao401
                anamnese.opcao40101 = opcao40101_str
                anamnese.opcao402 = opcao402
                anamnese.opcao40201 = opcao40201_str
                anamnese.qual402 = qual402
                anamnese.opcao403 = opcao403
                anamnese.qual403 = qual403
                anamnese.opcao404 = opcao404
                anamnese.opcao40401 = opcao40401_str
                anamnese.qual404 = qual404
                anamnese.opcao405 = opcao405
                anamnese.opcao40501 = opcao40501_str
                anamnese.qual405 = qual405
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/queixas')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')

    return render_template('anamnese_questionario.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/queixas', methods=['GET', 'POST'])
@login_required
def anamnese_queixas():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            queixas_principais = request.form.get('queixas_principais')
            ha_quanto_tempo = request.form.get('ha_quanto_tempo')
            causa_atribuida = request.form.get('causa_atribuida')
            atitude_crianca = request.form.get('atitude_crianca')
            atitude_mae = request.form.get('atitude_mae')
            atitude_pai = request.form.get('atitude_pai')
            atitude_parente = request.form.get('atitude_parente')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.queixas_principais = queixas_principais
                anamnese.ha_quanto_tempo = ha_quanto_tempo
                anamnese.causa_atribuida = causa_atribuida
                anamnese.atitude_crianca = atitude_crianca
                anamnese.atitude_mae = atitude_mae
                anamnese.atitude_pai = atitude_pai
                anamnese.atitude_parente = atitude_parente
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/antecedentes')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')

    return render_template('anamnese_queixas.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/antecedentes', methods=['GET', 'POST'])
@login_required
def anamnese_antecedentes():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            concepcao_composicao_familia_antes = request.form.get('concepcao_composicao_familia_antes')
            concepcao_composicao_familia_hoje = request.form.get('concepcao_composicao_familia_hoje')
            crianca_desejada = request.form.get('crianca_desejada')
            posicao_crianca_nascimento = request.form.get('posicao_crianca_nascimento')
            idade_irmaos = request.form.get('idade_irmaos')
            pais_separados = request.form.get('pais_separados')
            vida_social_familia = request.form.get('vida_social_familia')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.concepcao_composicao_familia_antes = concepcao_composicao_familia_antes
                anamnese.concepcao_composicao_familia_hoje = concepcao_composicao_familia_hoje
                anamnese.crianca_desejada = crianca_desejada
                anamnese.posicao_crianca_nascimento = posicao_crianca_nascimento
                anamnese.idade_irmaos = idade_irmaos
                anamnese.pais_separados = pais_separados
                anamnese.vida_social_familia = vida_social_familia
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/gestacao')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')

    return render_template('anamnese_antecedentes.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/gestacao', methods=['GET', 'POST'])
@login_required
def anamnese_gestacao():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            gravidez_planejada = request.form.get('gravidez_planejada')
            duracao_gestacao = request.form.get('duracao_gestacao')
            quando_sentiu_crianca_mexer = request.form.get('quando_sentiu_crianca_mexer')
            tratamento_prenatal = request.form.get('tratamento_prenatal')
            necessario_tratamento = request.form.get('necessario_tratamento')
            gestacao_agradavel = request.form.get('gestacao_agradavel')
            descreva706 = request.form.get('descreva706')
            saude_mae = request.form.get('saude_mae')
            estado_emocional = request.form.get('estado_emocional')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.gravidez_planejada = gravidez_planejada
                anamnese.duracao_gestacao = duracao_gestacao
                anamnese.quando_sentiu_crianca_mexer = quando_sentiu_crianca_mexer
                anamnese.tratamento_prenatal = tratamento_prenatal
                anamnese.necessario_tratamento = necessario_tratamento
                anamnese.gestacao_agradavel = gestacao_agradavel
                anamnese.descreva706 = descreva706
                anamnese.saude_mae = saude_mae
                anamnese.estado_emocional = estado_emocional
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/condicoes')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')

    return render_template('anamnese_gestacao.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/condicoes', methods=['GET', 'POST'])
@login_required
def anamnese_condicoesnascimento():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            local_nascimento = request.form.get('local_nascimento')
            local_nascimento_qual = request.form.get('local_nascimento_qual')
            tipo_nascimento = request.form.get('tipo_nascimento')
            tipo_nascimento_qual = request.form.get('tipo_nascimento_qual')
            nasceu_tempo_normal = request.form.get('nasceu_tempo_normal')
            bebe_nasceu = request.form.get('bebe_nasceu')
            bebe_nasceu_obs = request.form.get('bebe_nasceu_obs')
            anestesia = request.form.get('anestesia')
            trauma_craniano = request.form.get('trauma_craniano')
            gestacao_duracao = request.form.get('gestacao_duracao')
            peso_nascer = request.form.get('peso_nascer')
            duracao_parto = request.form.get('duracao_parto')
            chorou_logo = request.form.get('chorou_logo')
            quanto_tempo_choro = request.form.get('quanto_tempo_choro')
            reacao_primeiro_dia_vida = request.form.get('reacao_primeiro_dia_vida')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.local_nascimento = local_nascimento
                anamnese.local_nascimento_qual = local_nascimento_qual
                anamnese.tipo_nascimento = tipo_nascimento
                anamnese.tipo_nascimento_qual = tipo_nascimento_qual
                anamnese.nasceu_tempo_normal = nasceu_tempo_normal
                anamnese.bebe_nasceu = bebe_nasceu
                anamnese.bebe_nasceu_obs = bebe_nasceu_obs
                anamnese.anestesia = anestesia
                anamnese.trauma_craniano = trauma_craniano
                anamnese.gestacao_duracao = gestacao_duracao
                anamnese.peso_nascer = peso_nascer
                anamnese.duracao_parto = duracao_parto
                anamnese.chorou_logo = chorou_logo
                anamnese.quanto_tempo_choro = quanto_tempo_choro
                anamnese.reacao_primeiro_dia_vida = reacao_primeiro_dia_vida
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/psicomotor')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_condicoesnascimento.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/psicomotor', methods=['GET', 'POST'])
@login_required
def anamnese_psicomotor():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            sustentou_cabeca_quando = request.form.get('sustentou_cabeca_quando')
            quando_rolou = request.form.get('quando_rolou')
            quando_sorriu = request.form.get('quando_sorriu')
            quando_sentou_com_ajuda = request.form.get('quando_sentou_com_ajuda')
            quando_engatinhou = request.form.get('quando_engatinhou')
            quando_ficou_em_pe = request.form.get('quando_ficou_em_pe')
            quando_andou = request.form.get('quando_andou')
            balbuciou_com_idade = request.form.get('balbuciou_com_idade')
            quando_falou_primeira_palavra = request.form.get('quando_falou_primeira_palavra')
            quando_falou_corretamente = request.form.get('quando_falou_corretamente')
            trocou_letras = request.form.get('trocou_letras')
            trocou_fonemas_falando_escrevendo = request.form.get('trocou_fonemas_falando_escrevendo')
            falou_muito_errado = request.form.get('falou_muito_errado')
            ate_quando_falou_errado = request.form.get('ate_quando_falou_errado')
            gaguejou = request.form.get('gaguejou')
            houve_dificuldade_aprender_ler = request.form.get('houve_dificuldade_aprender_ler')
            houve_dificuldade_aprender_escrever = request.form.get('houve_dificuldade_aprender_escrever')
            houve_dificuldade_aprender_contar = request.form.get('houve_dificuldade_aprender_contar')
            costuma_esquecer_aprender = request.form.get('costuma_esquecer_aprender')
            como_foi_denticao = request.form.get('como_foi_denticao')
            quando_adiquiriu_controle_esfincteres_anal_diurno = request.form.get('quando_adiquiriu_controle_esfincteres_anal_diurno')
            adiquiriu_controle_esfincteres_vesical_diurno = request.form.get('adiquiriu_controle_esfincteres_vesical_diurno')
            adiquiriu_controle_esfincteres_vesical_noturno = request.form.get('adiquiriu_controle_esfincteres_vesical_noturno')
            como_ensinou_controle_esfincteres = request.form.get('como_ensinou_controle_esfincteres')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.sustentou_cabeca_quando = sustentou_cabeca_quando
                anamnese.quando_rolou = quando_rolou
                anamnese.quando_sorriu = quando_sorriu
                anamnese.quando_sentou_com_ajuda = quando_sentou_com_ajuda
                anamnese.quando_engatinhou = quando_engatinhou
                anamnese.quando_ficou_em_pe = quando_ficou_em_pe
                anamnese.quando_andou = quando_andou
                anamnese.balbuciou_com_idade = balbuciou_com_idade
                anamnese.quando_falou_primeira_palavra = quando_falou_primeira_palavra
                anamnese.quando_falou_corretamente = quando_falou_corretamente
                anamnese.trocou_letras = trocou_letras
                anamnese.trocou_fonemas_falando_escrevendo = trocou_fonemas_falando_escrevendo
                anamnese.falou_muito_errado = falou_muito_errado
                anamnese.ate_quando_falou_errado = ate_quando_falou_errado
                anamnese.gaguejou = gaguejou
                anamnese.houve_dificuldade_aprender_ler = houve_dificuldade_aprender_ler
                anamnese.houve_dificuldade_aprender_escrever = houve_dificuldade_aprender_escrever
                anamnese.houve_dificuldade_aprender_contar = houve_dificuldade_aprender_contar
                anamnese.costuma_esquecer_aprender = costuma_esquecer_aprender
                anamnese.como_foi_denticao = como_foi_denticao
                anamnese.quando_adiquiriu_controle_esfincteres_anal_diurno = quando_adiquiriu_controle_esfincteres_anal_diurno
                anamnese.adiquiriu_controle_esfincteres_vesical_diurno = adiquiriu_controle_esfincteres_vesical_diurno
                anamnese.adiquiriu_controle_esfincteres_vesical_noturno = adiquiriu_controle_esfincteres_vesical_noturno
                anamnese.como_ensinou_controle_esfincteres = como_ensinou_controle_esfincteres
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/higienedosono')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_psicomotor.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/higienedosono', methods=['GET', 'POST'])
@login_required
def anamnese_higiene():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            qualidade_sono = request.form.get('qualidade_sono')
            dorme_bem = request.form.get('dorme_bem')
            tem_surdorese_durante_noite = request.form.get('tem_surdorese_durante_noite')
            range_dentes_enquanto_dorme = request.form.get('range_dentes_enquanto_dorme')
            acorda_varias_vezes = request.form.get('acorda_varias_vezes')
            dorme_facilmente = request.form.get('dorme_facilmente')
            fala_dormindo = request.form.get('fala_dormindo')
            sonambulo = request.form.get('sonambulo')
            tem_pesadelos = request.form.get('tem_pesadelos')
            apresenta_terror_noturno = request.form.get('apresenta_terror_noturno')
            dorme_sozinho = request.form.get('dorme_sozinho')
            tem_cama_individual = request.form.get('tem_cama_individual')
            acorda_vai_para_cama_dos_pais = request.form.get('acorda_vai_para_cama_dos_pais')
            dificuldade_fala = request.form.get('dificuldade_fala')
            apresenta_descontrole_nos_esfincteres = request.form.get('apresenta_descontrole_nos_esfincteres')
            independente_nas_atividades = request.form.get('independente_nas_atividades')
            idade_em_que_andou = request.form.get('idade_em_que_andou')
            idade_que_falou_bem = request.form.get('idade_que_falou_bem')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.qualidade_sono = qualidade_sono
                anamnese.dorme_bem = dorme_bem
                anamnese.tem_surdorese_durante_noite = tem_surdorese_durante_noite
                anamnese.range_dentes_enquanto_dorme = range_dentes_enquanto_dorme
                anamnese.acorda_varias_vezes = acorda_varias_vezes
                anamnese.dorme_facilmente = dorme_facilmente
                anamnese.fala_dormindo = fala_dormindo
                anamnese.sonambulo = sonambulo
                anamnese.tem_pesadelos = tem_pesadelos
                anamnese.apresenta_terror_noturno = apresenta_terror_noturno
                anamnese.dorme_sozinho = dorme_sozinho
                anamnese.tem_cama_individual = tem_cama_individual
                anamnese.acorda_vai_para_cama_dos_pais = acorda_vai_para_cama_dos_pais
                anamnese.dificuldade_fala = dificuldade_fala
                anamnese.apresenta_descontrole_nos_esfincteres = apresenta_descontrole_nos_esfincteres
                anamnese.independente_nas_atividades = independente_nas_atividades
                anamnese.idade_em_que_andou = idade_em_que_andou
                anamnese.idade_que_falou_bem = idade_que_falou_bem
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/lactacao')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_higiene.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/lactacao', methods=['GET', 'POST'])
@login_required
def anamnese_lactacao():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            foi_amamentado = request.form.get('foi_amamentado')
            teve_problemas_na_amamentacao = request.form.get('teve_problemas_na_amamentacao')
            apresentou_dificuldade_na_amamentacao = request.form.get('apresentou_dificuldade_na_amamentacao')
            quanto_tempo_se_alimentou_pelo_seio = request.form.get('quanto_tempo_se_alimentou_pelo_seio')
            usou_mamadeira = request.form.get('usou_mamadeira')
            ate_quando_usou_mamadeira = request.form.get('ate_quando_usou_mamadeira')
            descreva_alimentacao_atual = request.form.get('descreva_alimentacao_atual')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.foi_amamentado = foi_amamentado
                anamnese.teve_problemas_na_amamentacao = teve_problemas_na_amamentacao
                anamnese.apresentou_dificuldade_na_amamentacao = apresentou_dificuldade_na_amamentacao
                anamnese.quanto_tempo_se_alimentou_pelo_seio = quanto_tempo_se_alimentou_pelo_seio
                anamnese.usou_mamadeira = usou_mamadeira
                anamnese.ate_quando_usou_mamadeira = ate_quando_usou_mamadeira
                anamnese.descreva_alimentacao_atual = descreva_alimentacao_atual
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/familiares')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_lactacao.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/familiares', methods=['GET', 'POST'])
@login_required
def anamnese_familiares():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            nervoso_na_familia = request.form.get('nervoso_na_familia')
            deficiente_mental_na_familia = request.form.get('deficiente_mental_na_familia')
            internado = request.form.get('internado')
            descreva_causas_internacao = request.form.get('descreva_causas_internacao')
            alguem_bebe_muito = request.form.get('alguem_bebe_muito')
            alguem_viciado_drogas = request.form.get('alguem_viciado_drogas')
            alguem_com_asma = request.form.get('alguem_com_asma')
            alguem_com_ataques = request.form.get('alguem_com_ataques')
            descreva_tipos_de_ataques = request.form.get('descreva_tipos_de_ataques')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.nervoso_na_familia = nervoso_na_familia
                anamnese.deficiente_mental_na_familia = deficiente_mental_na_familia
                anamnese.internado = internado
                anamnese.descreva_causas_internacao = descreva_causas_internacao
                anamnese.alguem_bebe_muito = alguem_bebe_muito
                anamnese.alguem_viciado_drogas = alguem_viciado_drogas
                anamnese.alguem_com_asma = alguem_com_asma
                anamnese.alguem_com_ataques = alguem_com_ataques
                anamnese.descreva_tipos_de_ataques = descreva_tipos_de_ataques
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/sexualidade')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_familiares.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/sexualidade', methods=['GET', 'POST'])
@login_required
def anamnese_sexualidade():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            recebe_orientacao_sexual = request.form.get('recebe_orientacao_sexual')
            apresenta_curiosidade_sexual = request.form.get('apresenta_curiosidade_sexual')
            quando_apresenta_curiosidade_sexual = request.form.get('quando_apresenta_curiosidade_sexual')
            atitude_dos_pais_curiosidade_sexual = request.form.get('atitude_dos_pais_curiosidade_sexual')
            se_masturba = request.form.get('se_masturba')
            com_que_frequencia_se_masturba = request.form.get('com_que_frequencia_se_masturba')
            quando_comecou_se_masturba = request.form.get('quando_comecou_se_masturba')
            atitude_dos_pais_se_masturba = request.form.get('atitude_dos_pais_se_masturba')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.recebe_orientacao_sexual = recebe_orientacao_sexual
                anamnese.apresenta_curiosidade_sexual = apresenta_curiosidade_sexual
                anamnese.quando_apresenta_curiosidade_sexual = quando_apresenta_curiosidade_sexual
                anamnese.atitude_dos_pais_curiosidade_sexual = atitude_dos_pais_curiosidade_sexual
                anamnese.se_masturba = se_masturba
                anamnese.com_que_frequencia_se_masturba = com_que_frequencia_se_masturba
                anamnese.quando_comecou_se_masturba = quando_comecou_se_masturba
                anamnese.atitude_dos_pais_se_masturba = atitude_dos_pais_se_masturba
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/saude%e%doenca')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_sexualidade.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/saude%e%doenca', methods=['GET', 'POST'])
@login_required
def anamnese_saudeedoenca():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            esta_vacinado = request.form.get('esta_vacinado')
            doencas_infancia = request.form.getlist(
                'doencas_infancia')  # Recebe a lista de professores selecionados
            doencas_infancia_str = ",".join(doencas_infancia)  # Converte a lista em uma string com vírgulas
            especifique_cirurgia = request.form.get('especifique_cirurgia')
            especifique_alergias = request.form.get('especifique_alergias')
            especifique_tipo_tratamento = request.form.get('especifique_tipo_tratamento')
            especifique_uso_medicamentos = request.form.get('especifique_uso_medicamentos')
            especifique_outros = request.form.get('especifique_outros')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.esta_vacinado = esta_vacinado
                anamnese.doencas_infancia = doencas_infancia_str
                anamnese.especifique_cirurgia = especifique_cirurgia
                anamnese.especifique_alergias = especifique_alergias
                anamnese.especifique_tipo_tratamento = especifique_tipo_tratamento
                anamnese.especifique_uso_medicamentos = especifique_uso_medicamentos
                anamnese.especifique_outros = especifique_outros
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/tiques')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_saudeedoenca.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/tiques', methods=['GET', 'POST'])
@login_required
def anamnese_tiques():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            usou_chupeta_ate_quando = request.form.get('usou_chupeta_ate_quando')
            chupou_dedo_ate_quando = request.form.get('chupou_dedo_ate_quando')
            roi_unhas = request.form.get('roi_unhas')
            puxa_orelhas = request.form.get('puxa_orelhas')
            morde_labios = request.form.get('morde_labios')
            atitude_dos_pais_ml_ru_po = request.form.get('atitude_dos_pais_ml_ru_po')
            apresenta_tiques = request.form.get('apresenta_tiques')
            descreva_tiques = request.form.get('descreva_tiques')
            atitude_dos_pais_tiques = request.form.get('atitude_dos_pais_tiques')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.usou_chupeta_ate_quando = usou_chupeta_ate_quando
                anamnese.chupou_dedo_ate_quando = chupou_dedo_ate_quando
                anamnese.roi_unhas = roi_unhas
                anamnese.puxa_orelhas = puxa_orelhas
                anamnese.morde_labios = morde_labios
                anamnese.atitude_dos_pais_ml_ru_po = atitude_dos_pais_ml_ru_po
                anamnese.apresenta_tiques = apresenta_tiques
                anamnese.descreva_tiques = descreva_tiques
                anamnese.atitude_dos_pais_tiques = atitude_dos_pais_tiques
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/sociabilidade')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_tiques.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/sociabilidade', methods=['GET', 'POST'])
@login_required
def anamnese_sociabilidade():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            faz_amigos_facilmente = request.form.get('usou_chupeta_ate_quando')
            gosta_fazer_visitas = request.form.get('chupou_dedo_ate_quando')
            adapta_ao_meio = request.form.get('roi_unhas')
            tem_apelido = request.form.get('puxa_orelhas')
            lider = request.form.get('morde_labios')
            autoritario = request.form.get('atitude_dos_pais_ml_ru_po')
            gosta_de_esportes = request.form.get('apresenta_tiques')
            tem_amigos_visinhos = request.form.get('descreva_tiques')
            preferencia_divercao = request.form.get('atitude_dos_pais_tiques')
            gosta_de_festas = request.form.get('gosta_de_festas')
            caracteristicas_crianca = request.form.getlist(
                'caracteristicas_crianca')  # Recebe a lista de professores selecionados
            caracteristicas_crianca_str = ",".join(caracteristicas_crianca)  # Converte a lista em uma string com vírgulas
            tem_mania_habito = request.form.get('atitude_dos_pais_tiques')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.faz_amigos_facilmente = faz_amigos_facilmente
                anamnese.gosta_fazer_visitas = gosta_fazer_visitas
                anamnese.adapta_ao_meio = adapta_ao_meio
                anamnese.tem_apelido = tem_apelido
                anamnese.lider = lider
                anamnese.autoritario = autoritario
                anamnese.gosta_de_esportes = gosta_de_esportes
                anamnese.tem_amigos_visinhos = tem_amigos_visinhos
                anamnese.preferencia_divercao = preferencia_divercao
                anamnese.gosta_de_festas = gosta_de_festas
                anamnese.caracteristicas_crianca = caracteristicas_crianca_str
                anamnese.tem_mania_habito = tem_mania_habito
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/autonomia')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_sociabilidade.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/autonomia', methods=['GET', 'POST'])
@login_required
def anamnese_autonomia():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            idade_comecou_comer = request.form.get('idade_comecou_comer')
            idade_comecou_vestir_sozinha = request.form.get('idade_comecou_vestir_sozinha')
            idade_comecou_tomarbanho_sozinha = request.form.get('idade_comecou_tomarbanho_sozinha')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.idade_comecou_comer = idade_comecou_comer
                anamnese.idade_comecou_vestir_sozinha = idade_comecou_vestir_sozinha
                anamnese.idade_comecou_tomarbanho_sozinha = idade_comecou_tomarbanho_sozinha
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/escolaridade')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_autonomia.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/escolaridade', methods=['GET', 'POST'])
@login_required
def anamnese_escolaridade():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            vai_bem_escola = request.form.get('vai_bem_escola')
            gosta_estudar = request.form.get('gosta_estudar')
            costuma_falar_aulas = request.form.get('costuma_falar_aulas')
            descreva_causas_costuma_falar_aulas = request.form.get('descreva_causas_costuma_falar_aulas')
            pais_estudam_com_crianca = request.form.get('pais_estudam_com_crianca')
            gosta_da_professora = request.form.get('gosta_da_professora')
            castigado_quando_tira_nota_ruim = request.form.get('castigado_quando_tira_nota_ruim')
            materias_mais_faceis = request.form.get('materias_mais_faceis')
            materias_mais_dificeis = request.form.get('materias_mais_dificeis')
            irrequieta_na_classe = request.form.get('irrequieta_na_classe')
            reprovado_alguma_vez = request.form.get('reprovado_alguma_vez')
            motios_reprovado_alguma_vez = request.form.get('motios_reprovado_alguma_vez')
            frequentou_creche = request.form.get('frequentou_creche')
            frequentou_jardim_de_infancia = request.form.get('frequentou_jardim_de_infancia')
            mudou_muito_de_escola = request.form.get('mudou_muito_de_escola')
            maior_habilidade_motora = request.form.get('maior_habilidade_motora')
            relacionamento_com_colegas = request.form.get('relacionamento_com_colegas')
            relacionamento_com_funcionarios = request.form.get('relacionamento_com_funcionarios')
            como_crianca_educada = request.form.getlist(
                'como_crianca_educada')  # Recebe a lista de professores selecionados
            como_crianca_educada_str = ",".join(como_crianca_educada)  # Converte a lista em uma string com vírgulas
            reacao_da_crianca_quando_castigada = request.form.get('reacao_da_crianca_quando_castigada')
            autoridade_melhor_acatada_pela_crianca = request.form.get('autoridade_melhor_acatada_pela_crianca')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.vai_bem_escola = vai_bem_escola
                anamnese.gosta_estudar = gosta_estudar
                anamnese.costuma_falar_aulas = costuma_falar_aulas
                anamnese.descreva_causas_costuma_falar_aulas = descreva_causas_costuma_falar_aulas
                anamnese.pais_estudam_com_crianca = pais_estudam_com_crianca
                anamnese.gosta_da_professora = gosta_da_professora
                anamnese.castigado_quando_tira_nota_ruim = castigado_quando_tira_nota_ruim
                anamnese.materias_mais_faceis = materias_mais_faceis
                anamnese.materias_mais_dificeis = materias_mais_dificeis
                anamnese.irrequieta_na_classe = irrequieta_na_classe
                anamnese.reprovado_alguma_vez = reprovado_alguma_vez
                anamnese.motios_reprovado_alguma_vez = motios_reprovado_alguma_vez
                anamnese.frequentou_creche = frequentou_creche
                anamnese.frequentou_jardim_de_infancia = frequentou_jardim_de_infancia
                anamnese.mudou_muito_de_escola = mudou_muito_de_escola
                anamnese.maior_habilidade_motora = maior_habilidade_motora
                anamnese.relacionamento_com_colegas = relacionamento_com_colegas
                anamnese.relacionamento_com_funcionarios = relacionamento_com_funcionarios
                anamnese.como_crianca_educada = como_crianca_educada_str
                anamnese.reacao_da_crianca_quando_castigada = reacao_da_crianca_quando_castigada
                anamnese.autoridade_melhor_acatada_pela_crianca = autoridade_melhor_acatada_pela_crianca
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/interrelacoes')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_escolaridade.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/interrelacoes', methods=['GET', 'POST'])
@login_required
def anamnese_interrelacoes():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            tipo_de_moradia_familia = request.form.get('tipo_de_moradia_familia')
            relacao_com_mae = request.form.get('relacao_com_mae')
            relacao_com_pai = request.form.get('relacao_com_pai')
            relacao_com_familia = request.form.get('relacao_com_familia')
            mae_como_se_julga = request.form.get('mae_como_se_julga')
            mae_como_trata_filhos = request.form.get('mae_como_trata_filhos')
            pai_como_se_julga = request.form.get('pai_como_se_julga')
            pai_como_trata_filhos = request.form.get('pai_como_trata_filhos')
            relacao_do_casal = request.form.get('relacao_do_casal')
            quem_cuida_da_crianca = request.form.get('quem_cuida_da_crianca')
            quem_leva_ao_medico = request.form.get('quem_leva_ao_medico')
            quem_leva_a_escola = request.form.get('quem_leva_a_escola')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.tipo_de_moradia_familia = tipo_de_moradia_familia
                anamnese.relacao_com_mae = relacao_com_mae
                anamnese.relacao_com_pai = relacao_com_pai
                anamnese.relacao_com_familia = relacao_com_familia
                anamnese.mae_como_se_julga = mae_como_se_julga
                anamnese.mae_como_trata_filhos = mae_como_trata_filhos
                anamnese.pai_como_se_julga = pai_como_se_julga
                anamnese.pai_como_trata_filhos = pai_como_trata_filhos
                anamnese.relacao_do_casal = relacao_do_casal
                anamnese.quem_cuida_da_crianca = quem_cuida_da_crianca
                anamnese.quem_leva_ao_medico = quem_leva_ao_medico
                anamnese.quem_leva_a_escola = quem_leva_a_escola
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/vida%escolar')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_interrelacoes.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/vida%escolar', methods=['GET', 'POST'])
@login_required
def anamnese_vidaescolar():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            idade_que_entrou_escola = request.form.get('idade_que_entrou_escola')
            como_se_adaptou = request.form.get('como_se_adaptou')
            quem_levava_a_escola = request.form.get('quem_levava_a_escola')
            repetencias = request.form.get('repetencias')
            ressente_ao_trocar_professor = request.form.get('ressente_ao_trocar_professor')
            comente_frequencia_escolar = request.form.get('comente_frequencia_escolar')
            como_familia_participa_vida_escolar_filho = request.form.get('como_familia_participa_vida_escolar_filho')
            oque_acha_atendimento_escolar = request.form.get('oque_acha_atendimento_escolar')
            desenvolvimento_compativel_com_idade = request.form.get('desenvolvimento_compativel_com_idade')
            comentario_complementar = request.form.get('comentario_complementar')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.idade_que_entrou_escola = idade_que_entrou_escola
                anamnese.como_se_adaptou = como_se_adaptou
                anamnese.quem_levava_a_escola = quem_levava_a_escola
                anamnese.repetencias = repetencias
                anamnese.ressente_ao_trocar_professor = ressente_ao_trocar_professor
                anamnese.comente_frequencia_escolar = comente_frequencia_escolar
                anamnese.como_familia_participa_vida_escolar_filho = como_familia_participa_vida_escolar_filho
                anamnese.oque_acha_atendimento_escolar = oque_acha_atendimento_escolar
                anamnese.desenvolvimento_compativel_com_idade = desenvolvimento_compativel_com_idade
                anamnese.comentario_complementar = comentario_complementar
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/anamnese/fim')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_vidaescolar.html', aluno_selecionado_anam=aluno_selecionado_anam)


@app.route('/anamnese/fim', methods=['GET', 'POST'])
@login_required
def anamnese_fim():
    aluno_id_anam = session.get('aluno_id_anam')
    aluno_selecionado_anam = Alunos.query.get(aluno_id_anam)
    if aluno_selecionado_anam:
        if request.method == 'POST':
            informante = request.form.get('informante')
            grau_parentesco = request.form.get('grau_parentesco')
            entrevistador = request.form.get('entrevistador')
            funcao = request.form.get('funcao')

            anamnese = Anamnese.query.filter_by(aluno_nome=aluno_selecionado_anam.aluno_nome).first()

            if anamnese:
                anamnese.informante = informante
                anamnese.grau_parentesco = grau_parentesco
                anamnese.entrevistador = entrevistador
                anamnese.funcao = funcao
                database.session.commit()
                flash('Formulário Anamnese Concluído', 'alert-success')
                return redirect('/anamnese')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('anamnese_fim.html', aluno_selecionado_anam=aluno_selecionado_anam)


######################################################################

@app.route('/protocolo-de-avaliacao', methods=['GET', 'POST'])
@login_required
def protocolo():
    current_date = datetime.now()
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
              "novembro", "dezembro"]
    formatted_date = f"{current_date.day} de {months[current_date.month - 1]} de {current_date.year}"

    # Recupera os dados para preencher dropdowns ou campos de seleção
    nome_aditamentoquery = Aditamento.query.order_by(func.lower(Aditamento.nome_aluno)).all()
    codigoquery = CodigoAfls.query.all()

    # Recupera os dados do formulário existente da sessão ou cria um dicionário vazio
    form_data = session.get('form_data', {})

    if request.method == 'POST':
        # Recupera os dados do formulário da requisição POST
        nome_aluno = request.form.get('aluno_nome')
        ordem_aplicacao = request.form.get('ordem_aplicacao')
        data_aplicacao = request.form.get('data_aplicacao')
        aplicador = request.form.get('aplicador')
        supervisor = request.form.get('supervisor')
        select_codigo = request.form['selectCodigo']
        pontos = request.form['pontos']

        # Recupera o objeto de aluno com base no nome do aluno selecionado
        aluno_selecionado = Aditamento.query.filter_by(nome_aluno=nome_aluno).first()
        session['selected_data'] = {
            'aluno_nome': nome_aluno,
            'serie_aluno': aluno_selecionado.serie_matricula,
            'turma_aluno': aluno_selecionado.turma_matricula,
            'ordem_aplicacao': request.form['ordem_aplicacao'],
            'data_aplicacao': request.form['data_aplicacao'],
            'aplicador': request.form['aplicador'],
            'supervisor': request.form['supervisor'],
            'selectCodigo': request.form['selectCodigo'],
        }
        if request.method == 'POST' and request.form.get('limpar'):
            # Botão "Limpar" foi clicado, então removemos os dados de selected_data da sessão
            session.pop('selected_data', None)
            return redirect(url_for('protocolo'))
        if aluno_selecionado:
            # Check if the Protocolo_AFLs object already exists for the selected student
            protocolo_afls_existing = Protocolo_AFLs.query.filter_by(aluno_nome=aluno_selecionado.nome_aluno).first()

            if protocolo_afls_existing:
                # Update the specific column in the existing Protocolo_AFLs object
                column_name = f'{select_codigo.replace(" ", "_")}_{ordem_aplicacao}'
                setattr(protocolo_afls_existing, column_name, pontos)
                database.session.commit()
                flash('Formulário Protocolo Atualizado com Sucesso!', 'alert-success')
            else:
                # Create and save the new object Protocolo_AFLs
                column_name = f'{select_codigo.replace(" ", "_")}_{ordem_aplicacao}'
                protocoloafls = Protocolo_AFLs(
                    aluno_nome=aluno_selecionado.nome_aluno,
                    serie_aluno=aluno_selecionado.serie_matricula,
                    turma_aluno=aluno_selecionado.turma_matricula,
                    ordem_aplicacao=ordem_aplicacao,
                    data_aplicacao=data_aplicacao,
                    aplicador=aplicador,
                    supervisor=supervisor,
                    **{column_name: pontos}
                )
                # Add the new object Protocolo_AFLs to the database
                database.session.add(protocoloafls)
                database.session.commit()
                flash('Formulário Protocolo Salvo com Sucesso!', 'alert-success')

            # Redireciona para a mesma rota usando o método GET to avoid re-sending the form
            return redirect(url_for('protocolo'))

        else:
            flash('Ocorreu algum erro. Verifique se há algum campo faltando.', 'alert-danger')
    selected_data = session.get('selected_data', {})
    # Retorna o template com os dados do formulário atualizados
    return render_template('protocolo.html', nome_aditamentoquery=nome_aditamentoquery,
                           codigoquery=codigoquery, formatted_date=formatted_date,
                           form_data=form_data, selected_data=selected_data)


@app.route('/protocolo%de%avaliacao/pesquisa')
@login_required
def protocolo_pesquisa():
    nome_alunoquery = Protocolo_AFLs.query.order_by(func.lower(Protocolo_AFLs.aluno_nome)).all()
    codigoquery = CodigoAfls.query.all()
    return render_template('protocolo_pesquisa.html', nome_alunoquery=nome_alunoquery, codigoquery=codigoquery)


@app.route('/clear_session', methods=['POST'])
@login_required
def clear_session():
    # Clear the session data
    session.pop('form_data', None)
    session.pop('selected_data', None)
    return redirect('/protocolo-de-avaliacao')


def import_protocolo_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith('.csv'):
            reader = csv.reader(file)
            protocolo_import = [row for row in reader if len(row) == 8]
        else:
            lines = file.readlines()
            protocolo_import = [line.strip().split(';') for line in lines if
                                len(line.strip().split(';')) == 8]  # Change to 8

        for protocolofor in protocolo_import:
            tarefa, escala_pontos, nome_tarefa, objetivo, pergunta, exemplo, criterio, comentario = protocolofor  # Add 'criterio' to the unpacking
            protocolo_obj = CodigoAfls(
                tarefa=tarefa,
                escala_pontos=escala_pontos,
                nome_tarefa=nome_tarefa,
                objetivo=objetivo,
                pergunta=pergunta,
                exemplo=exemplo,
                criterio=criterio,
                comentario=comentario
            )
            database.session.add(protocolo_obj)  # Assuming `database.session` is properly configured
        database.session.commit()


@app.route('/protocolo/importação', methods=['GET', 'POST'])
@login_required
def protocolo_importacao():
    protocolo_file = request.files.get('file')
    if protocolo_file:
        filename, file_extension = os.path.splitext(protocolo_file.filename)
        if file_extension.lower() == '.txt' or file_extension.lower() == '.csv':
            file_path = os.path.join(UPLOAD_FOLDER, protocolo_file.filename)
            protocolo_file.save(file_path)
            import_protocolo_from_file(file_path)
            return redirect('/')
        else:
            flash('Apenas (.txt e .csv) são permitidos!', 'alert-danger')
    return render_template('protocoloimportacao.html')


######################################################################

@app.route('/PEI', methods=['GET', 'POST'])
@login_required
def pei():
    nome_alunoquery = Alunos.query.order_by(func.lower(Alunos.aluno_nome)).all()
    page = request.args.get('page', 1, type=int)
    per_page = 55000  # Number of items per page

    search_query = request.args.get('search_query', '')

    if search_query:
        cids = Cid.query.filter(Cid.numero_cid.contains(search_query)).paginate(page=page, per_page=per_page,
                                                                                error_out=False)
    else:
        cids = Cid.query.paginate(page=page, per_page=per_page, error_out=False)

    if request.method == 'POST':
        aluno_nome_selecionado = request.form.get('aluno_nome')
        data_laudo = request.form.get('data_laudo')
        medico = request.form.get('medico')
        crm = request.form.get('crm')
        data_protocolo = request.form.get('data_protocolo')
        codigo_cid = request.form.get('cid_selecionados')

        alunos_selecionados = Alunos.query.filter_by(aluno_nome=aluno_nome_selecionado).first()

        if alunos_selecionados:

            session['aluno_ids'] = alunos_selecionados.id

            pei = PEI(
                aluno_nome=alunos_selecionados.aluno_nome,
                aluno_matricula=alunos_selecionados.aluno_codigo,
                serie_aluno=alunos_selecionados.matricula_serie,
                turma_aluno=alunos_selecionados.matricula_turma,
                nome_mae=alunos_selecionados.mae_nome,
                endereco=alunos_selecionados.aluno_endereco,
                unidade_escolar=alunos_selecionados.escola_nome,
                data_laudo=data_laudo,
                medico=medico,
                crm=crm,
                data_protocolo=data_protocolo,
                codigo_cid=codigo_cid
            )
            database.session.add(pei)
            database.session.commit()
            session['alunos_selecionados'] = alunos_selecionados.aluno_nome
            flash('Continue o Formulário.', 'alert-success')
            return redirect('/PEI/resumo')
        else:
            flash('Ocorreu algum erro. Verifique se há algum campo faltando.', 'alert-danger')

    foto_aluno = url_for('static', filename='foto_alunos/{}'.format(Alunos.foto_aluno))
    return render_template('pei.html', nome_alunoquery=nome_alunoquery, foto_aluno=foto_aluno,
                           search_query=search_query, cids=cids)


@app.route('/PEI/resumo', methods=['GET', 'POST'])
@login_required
def pei_resumo():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            resumo_escolaridade = request.form.get('resumo_escolaridade')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.resumo_escolaridade = resumo_escolaridade
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/funcionalidades')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_resumo.html')


@app.route('/PEI/funcionalidades', methods=['GET', 'POST'])
@login_required
def pei_funcionalidades():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            funcionalidades = request.form.get('funcionalidades')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.funcionalidades = funcionalidades
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/habilidades')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_Funcionalidades.html')


@app.route('/PEI/habilidades', methods=['GET', 'POST'])
@login_required
def pei_habilidades():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item500 = request.form.get('item500')
            item501 = request.form.get('item501')
            item502 = request.form.get('item502')
            item503 = request.form.get('item503')
            item504 = request.form.get('item504')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item500 = item500
                pei.item501 = item501
                pei.item502 = item502
                pei.item503 = item503
                pei.item504 = item504
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/habilidades/leitura%e%escrita')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_habilidades.html')


@app.route('/PEI/habilidades/leitura%e%escrita', methods=['GET', 'POST'])
@login_required
def pei_habilidades_leituraeescrita():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item510 = request.form.get('item510')
            item511 = request.form.get('item511')
            item512 = request.form.get('item512')
            item513 = request.form.get('item513')
            item514 = request.form.get('item514')
            item515 = request.form.get('item515')
            item516 = request.form.get('item516')
            item517 = request.form.get('item517')
            item518 = request.form.get('item518')
            item519 = request.form.get('item519')
            item5110 = request.form.get('item5110')
            item5111 = request.form.get('item5111')
            item5112 = request.form.get('item5112')
            item5113 = request.form.get('item5113')
            item5114 = request.form.get('item5114')
            item5115 = request.form.get('item5115')
            item5116 = request.form.get('item5116')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item510 = item510
                pei.item511 = item511
                pei.item512 = item512
                pei.item513 = item513
                pei.item514 = item514
                pei.item515 = item515
                pei.item516 = item516
                pei.item517 = item517
                pei.item518 = item518
                pei.item519 = item519
                pei.item5110 = item5110
                pei.item5111 = item5111
                pei.item5112 = item5112
                pei.item5113 = item5113
                pei.item5114 = item5114
                pei.item5115 = item5115
                pei.item5116 = item5116

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/habilidades/raciocinio%logico')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_habilidades_leituraeescrita.html')


@app.route('/PEI/habilidades/raciocinio%logico', methods=['GET', 'POST'])
@login_required
def pei_habilidades_raciociniologico():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item520 = request.form.get('item520')
            item521 = request.form.get('item521')
            item522 = request.form.get('item522')
            item523 = request.form.get('item523')
            item524 = request.form.get('item524')
            item525 = request.form.get('item525')
            item526 = request.form.get('item526')
            item527 = request.form.get('item527')
            item528 = request.form.get('item528')
            item529 = request.form.get('item529')
            item5210 = request.form.get('item5210')
            item5211 = request.form.get('item5211')
            item5212 = request.form.get('item5212')
            item5213 = request.form.get('item5213')
            item5214 = request.form.get('item5214')
            item5215 = request.form.get('item5215')
            item5216 = request.form.get('item5216')
            item5217 = request.form.get('item5217')
            item5218 = request.form.get('item5218')
            item5219 = request.form.get('item5219')
            item5220 = request.form.get('item5220')
            item5221 = request.form.get('item5221')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item520 = item520
                pei.item521 = item521
                pei.item522 = item522
                pei.item523 = item523
                pei.item524 = item524
                pei.item525 = item525
                pei.item526 = item526
                pei.item527 = item527
                pei.item528 = item528
                pei.item529 = item529
                pei.item5210 = item5210
                pei.item5211 = item5211
                pei.item5212 = item5212
                pei.item5213 = item5213
                pei.item5214 = item5214
                pei.item5215 = item5215
                pei.item5216 = item5216
                pei.item5217 = item5217
                pei.item5218 = item5218
                pei.item5219 = item5219
                pei.item5220 = item5220
                pei.item5221 = item5221

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/habilidades/informatica')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_habilidades_raciociniologico.html')


@app.route('/PEI/habilidades/informatica', methods=['GET', 'POST'])
@login_required
def pei_habilidades_informatica():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item530 = request.form.get('item530')
            item531 = request.form.get('item531')
            item532 = request.form.get('item532')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item530 = item530
                pei.item531 = item531
                pei.item532 = item532

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/habilidade%social')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_habilidades_informatica.html')


@app.route('/PEI/habilidade%social', methods=['GET', 'POST'])
@login_required
def pei_habilidades_social():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item600 = request.form.get('item600')
            item601 = request.form.get('item601')
            item602 = request.form.get('item602')
            item603 = request.form.get('item603')
            item604 = request.form.get('item604')
            item605 = request.form.get('item605')
            item606 = request.form.get('item606')
            item607 = request.form.get('item607')
            item608 = request.form.get('item608')
            item609 = request.form.get('item609')
            item6010 = request.form.get('item6010')
            item6011 = request.form.get('item6011')
            item6012 = request.form.get('item6012')
            item6013 = request.form.get('item6013')
            item6014 = request.form.get('item6014')
            item6015 = request.form.get('item6015')
            item6016 = request.form.get('item6016')
            item6017 = request.form.get('item6017')
            item6018 = request.form.get('item6018')
            item6019 = request.form.get('item6019')
            item6020 = request.form.get('item6020')
            item6021 = request.form.get('item6021')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item600 = item600
                pei.item601 = item601
                pei.item602 = item602
                pei.item603 = item603
                pei.item604 = item604
                pei.item605 = item605
                pei.item606 = item606
                pei.item607 = item607
                pei.item608 = item608
                pei.item609 = item609
                pei.item6010 = item6010
                pei.item6011 = item6011
                pei.item6012 = item6012
                pei.item6013 = item6013
                pei.item6014 = item6014
                pei.item6015 = item6015
                pei.item6016 = item6016
                pei.item6017 = item6017
                pei.item6018 = item6018
                pei.item6019 = item6019
                pei.item6020 = item6020
                pei.item6021 = item6021

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/CEI')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_habilidades_social.html')


@app.route('/PEI/CEI', methods=['GET', 'POST'])
@login_required
def pei_cei():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item700 = request.form.get('item700')
            item701 = request.form.get('item701')
            item702 = request.form.get('item702')
            item703 = request.form.get('item703')
            item704 = request.form.get('item704')
            item705 = request.form.get('item705')
            item706 = request.form.get('item706')
            item707 = request.form.get('item707')
            item708 = request.form.get('item708')
            item709 = request.form.get('item709')
            item7010 = request.form.get('item7010')
            item7011 = request.form.get('item7011')
            item7012 = request.form.get('item7012')
            item7013 = request.form.get('item7013')
            item7014 = request.form.get('item7014')
            item7015 = request.form.get('item7015')
            item7016 = request.form.get('item7016')
            item7017 = request.form.get('item7017')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item700 = item700
                pei.item701 = item701
                pei.item702 = item702
                pei.item703 = item703
                pei.item704 = item704
                pei.item705 = item705
                pei.item706 = item706
                pei.item707 = item707
                pei.item708 = item708
                pei.item709 = item709
                pei.item7010 = item7010
                pei.item7011 = item7011
                pei.item7012 = item7012
                pei.item7013 = item7013
                pei.item7014 = item7014
                pei.item7015 = item7015
                pei.item7016 = item7016
                pei.item7017 = item7017

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/CEI/tecnologias')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_CEI.html')


@app.route('/PEI/CEI/tecnologias', methods=['GET', 'POST'])
@login_required
def pei_CEI_tecnologiadeapoio():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item710 = request.form.get('item710')
            item711 = request.form.get('item711')
            item712 = request.form.get('item712')
            item713 = request.form.get('item713')
            item714 = request.form.get('item714')
            item715 = request.form.get('item715')
            item716 = request.form.get('item716')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item710 = item710
                pei.item711 = item711
                pei.item712 = item712
                pei.item713 = item713
                pei.item714 = item714
                pei.item715 = item715
                pei.item716 = item716

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/intervencao')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_CEI_tecnologiadeapoio.html')


@app.route('/PEI/intervencao', methods=['GET', 'POST'])
@login_required
def pei_intervencao():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item800 = request.form.get('item800')
            item801 = request.form.get('item801')
            item802 = request.form.get('item802')
            item803 = request.form.get('item803')
            item804 = request.form.get('item804')
            item805 = request.form.get('item805')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item800 = item800
                pei.item801 = item801
                pei.item802 = item802
                pei.item803 = item803
                pei.item804 = item804
                pei.item805 = item805

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/intervencao/treino_da_percepcao')  # Redirecionar para outra página após salvar
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_intervencao.html')


@app.route('/PEI/intervencao/treino_da_percepcao', methods=['GET', 'POST'])
@login_required
def pei_intervencao_treinodapercepcao():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item810 = request.form.get('item810')
            item811 = request.form.get('item811')
            item812 = request.form.get('item812')
            item813 = request.form.get('item813')
            item814 = request.form.get('item814')
            item815 = request.form.get('item815')
            item816 = request.form.get('item816')
            item817 = request.form.get('item817')
            item818 = request.form.get('item818')
            item819 = request.form.get('item819')
            item8110 = request.form.get('item8110')
            item8111 = request.form.get('item8111')
            item8112 = request.form.get('item8112')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item810 = item810
                pei.item811 = item811
                pei.item812 = item812
                pei.item813 = item813
                pei.item814 = item814
                pei.item815 = item815
                pei.item816 = item816
                pei.item817 = item817
                pei.item818 = item818
                pei.item819 = item819
                pei.item8110 = item8110
                pei.item8111 = item8111
                pei.item8112 = item8112

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect(
                    '/PEI/intervencao/desenvolvimento_da_linguagem')  # Redirecionar para outra página após salvar
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_intervencao_treinodapercepcao.html')


@app.route('/PEI/intervencao/desenvolvimento_da_linguagem', methods=['GET', 'POST'])
@login_required
def pei_intervencao_desenvolvimentodalinguagem():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item820 = request.form.get('item820')
            item821 = request.form.get('item821')
            item822 = request.form.get('item822')
            item823 = request.form.get('item823')
            item824 = request.form.get('item824')
            item825 = request.form.get('item825')
            item826 = request.form.get('item826')
            item827 = request.form.get('item827')
            item828 = request.form.get('item828')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item820 = item820
                pei.item821 = item821
                pei.item822 = item822
                pei.item823 = item823
                pei.item824 = item824
                pei.item825 = item825
                pei.item826 = item826
                pei.item827 = item827
                pei.item828 = item828

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect(
                    '/PEI/intervencao/desenvolvimento_da_consciencia_fonologica')  # Redirecionar para outra página após salvar
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_intervencao_desenvolvimentodalinguagem.html')


@app.route('/PEI/intervencao/desenvolvimento_da_consciencia_fonologica', methods=['GET', 'POST'])
@login_required
def pei_intervencao_desenvolvimentofonologico():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item830 = request.form.get('item830')
            item831 = request.form.get('item831')
            item832 = request.form.get('item832')
            item833 = request.form.get('item833')
            item834 = request.form.get('item834')
            item835 = request.form.get('item835')
            item836 = request.form.get('item836')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item830 = item830
                pei.item831 = item831
                pei.item832 = item832
                pei.item833 = item833
                pei.item834 = item834
                pei.item835 = item835
                pei.item836 = item836

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect(
                    '/PEI/intervencao/treino_de_memoria_auditiva')  # Redirecionar para outra página após salvar
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_intervencao_desenvolvimentofonologico.html')


@app.route('/PEI/intervencao/treino_de_memoria_auditiva', methods=['GET', 'POST'])
@login_required
def pei_intervencao_treinodememoriaauditiva():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item840 = request.form.get('item840')
            item841 = request.form.get('item841')
            item842 = request.form.get('item842')
            item843 = request.form.get('item843')
            item844 = request.form.get('item844')
            item845 = request.form.get('item845')
            item846 = request.form.get('item846')
            item847 = request.form.get('item847')
            item848 = request.form.get('item848')
            item849 = request.form.get('item849')
            item8410 = request.form.get('item8410')
            item8411 = request.form.get('item8411')
            item8412 = request.form.get('item8412')
            item8413 = request.form.get('item8413')
            item8414 = request.form.get('item8414')
            item8415 = request.form.get('item8415')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item840 = item840
                pei.item841 = item841
                pei.item842 = item842
                pei.item843 = item843
                pei.item844 = item844
                pei.item845 = item845
                pei.item846 = item846
                pei.item847 = item847
                pei.item848 = item848
                pei.item849 = item849
                pei.item8410 = item8410
                pei.item8411 = item8411
                pei.item8412 = item8412
                pei.item8413 = item8413
                pei.item8414 = item8414
                pei.item8415 = item8415

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/FAC')  # Redirecionar para outra página após salvar
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_intervencao_treinodememoriaauditiva.html')


@app.route('/PEI/FAC', methods=['GET', 'POST'])
@login_required
def pei_fac():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item900 = request.form.get('item900')
            item901 = request.form.get('item901')
            item902 = request.form.get('item902')
            item903 = request.form.get('item903')
            item904 = request.form.get('item904')
            item905 = request.form.get('item905')
            item906 = request.form.get('item906')
            item907 = request.form.get('item907')
            item908 = request.form.get('item908')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item900 = item900
                pei.item901 = item901
                pei.item902 = item902
                pei.item903 = item903
                pei.item904 = item904
                pei.item905 = item905
                pei.item906 = item906
                pei.item907 = item907
                pei.item908 = item908

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/FAC/metodologias')  # Redirecionar para outra página após salvar
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_FAC.html')


@app.route('/PEI/FAC/metodologias', methods=['GET', 'POST'])
@login_required
def pei_FAC_metodologia():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item910 = request.form.get('item910')
            item911 = request.form.get('item911')
            item912 = request.form.get('item912')
            item913 = request.form.get('item913')
            item914 = request.form.get('item914')
            item915 = request.form.get('item915')
            item916 = request.form.get('item916')
            item917 = request.form.get('item917')
            item918 = request.form.get('item918')
            item919 = request.form.get('item919')
            item9110 = request.form.get('item9110')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item910 = item910
                pei.item911 = item911
                pei.item912 = item912
                pei.item913 = item913
                pei.item914 = item914
                pei.item915 = item915
                pei.item916 = item916
                pei.item917 = item917
                pei.item918 = item918
                pei.item919 = item919
                pei.item9110 = item9110

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/FAC/temporalidade')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_FAC_metodologia.html')


@app.route('/PEI/FAC/temporalidade', methods=['GET', 'POST'])
@login_required
def pei_FAC_temporalidade():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item920 = request.form.get('item920')
            item921 = request.form.get('item921')
            item922 = request.form.get('item922')
            item923 = request.form.get('item923')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item920 = item920
                pei.item921 = item921
                pei.item922 = item922
                pei.item923 = item923

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/FAC/praticas%para%o%aluno')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_FAC_temporalidade.html')


@app.route('/PEI/FAC/praticas%para%o%aluno', methods=['GET', 'POST'])
@login_required
def pei_FAC_praticasaluno():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item930 = request.form.get('item930')
            item931 = request.form.get('item931')
            item932 = request.form.get('item932')
            item933 = request.form.get('item933')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item930 = item930
                pei.item931 = item931
                pei.item932 = item932
                pei.item933 = item933

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/FAC/contexto%escolar')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_FAC_praticasaluno.html')


@app.route('/PEI/FAC/contexto%escolar', methods=['GET', 'POST'])
@login_required
def pei_FAC_contexto():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item940 = request.form.get('item940')
            item941 = request.form.get('item941')
            item942 = request.form.get('item942')
            item943 = request.form.get('item943')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item940 = item940
                pei.item941 = item941
                pei.item942 = item942
                pei.item943 = item943

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/FAC/conceituais')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_FAC_contexto.html')


@app.route('/PEI/FAC/conceituais', methods=['GET', 'POST'])
@login_required
def pei_FAC_conceituais():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item950 = request.form.get('item950')
            item951 = request.form.get('item951')
            item952 = request.form.get('item952')
            item953 = request.form.get('item953')
            item954 = request.form.get('item954')
            item955 = request.form.get('item955')
            item956 = request.form.get('item956')
            item957 = request.form.get('item957')
            item958 = request.form.get('item958')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item950 = item950
                pei.item951 = item951
                pei.item952 = item952
                pei.item953 = item953
                pei.item954 = item954
                pei.item955 = item955
                pei.item956 = item956
                pei.item957 = item957
                pei.item958 = item958

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/FAC/sociais')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_FAC_conceituais.html')


@app.route('/PEI/FAC/sociais', methods=['GET', 'POST'])
@login_required
def pei_FAC_social():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item960 = request.form.get('item960')
            item961 = request.form.get('item961')
            item962 = request.form.get('item962')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item960 = item960
                pei.item961 = item961
                pei.item962 = item962

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/FAC/familia')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_FAC_social.html')


@app.route('/PEI/FAC/familia', methods=['GET', 'POST'])
@login_required
def pei_FAC_familia():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            item970 = request.form.get('item970')
            item971 = request.form.get('item971')
            item972 = request.form.get('item972')
            item973 = request.form.get('item973')
            item974 = request.form.get('item974')
            fm1_98 = request.form.get('fm1_98')
            fm2_98 = request.form.get('fm2_98')
            fm3_98 = request.form.get('fm3_98')
            fm4_98 = request.form.get('fm4_98')
            fm5_98 = request.form.get('fm5_98')
            fm6_98 = request.form.get('fm6_98')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.item970 = item970
                pei.item971 = item971
                pei.item972 = item972
                pei.item973 = item973
                pei.item974 = item974
                pei.fm1_98 = fm1_98
                pei.fm2_98 = fm2_98
                pei.fm3_98 = fm3_98
                pei.fm4_98 = fm4_98
                pei.fm5_98 = fm5_98
                pei.fm6_98 = fm6_98

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/Total_de_horas_por_aula')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_FAC_familia.html')


@app.route('/PEI/Total_de_horas_por_aula', methods=['GET', 'POST'])
@login_required
def pei_horadeaula():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            basenacional101 = request.form.get('basenacional101')
            acompanhamento102 = request.form.get('acompanhamento102')
            formacao103 = request.form.get('formacao103')
            basenacional104 = request.form.get('basenacional104')
            atividadesartisticas105 = request.form.get('atividadesartisticas105')
            totaldeaulas106 = request.form.get('totaldeaulas106')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.basenacional101 = basenacional101
                pei.acompanhamento102 = acompanhamento102
                pei.formacao103 = formacao103
                pei.basenacional104 = basenacional104
                pei.atividadesartisticas105 = atividadesartisticas105
                pei.totaldeaulas106 = totaldeaulas106

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/metas_alunos')  # Redirecionar para outra página após salvar
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_HoraAula.html')


@app.route('/PEI/metas_alunos', methods=['GET', 'POST'])
@login_required
def pei_metas_alunos():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            metaspriorizadasdisciplinas11 = request.form.get('metaspriorizadasdisciplinas11')
            metaspriorizadasdescricao11 = request.form.get('metaspriorizadasdescricao11')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.metaspriorizadasdisciplinas11 = metaspriorizadasdisciplinas11
                pei.metaspriorizadasdescricao11 = metaspriorizadasdescricao11

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/implantacao')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_metas_alunos.html')


@app.route('/PEI/implantacao', methods=['GET', 'POST'])
@login_required
def pei_implantacao():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            criterios131 = request.form.get('criterios131')
            instrumentos132 = request.form.get('instrumentos132')
            intervenientes133 = request.form.get('intervenientes133')
            momentos_avaliacao134 = request.form.get('momentos_avaliacao134')
            proxima_revisao135 = request.form.get('proxima_revisao135')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.criterios131 = criterios131
                pei.instrumentos132 = instrumentos132
                pei.intervenientes133 = intervenientes133
                pei.momentos_avaliacao134 = momentos_avaliacao134
                pei.proxima_revisao135 = proxima_revisao135

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/participacao')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_implantacao.html')


@app.route('/PEI/participacao', methods=['GET', 'POST'])
@login_required
def pei_participacao():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            descricao_participacao_do_aluno12 = request.form.get('descricao_participacao_do_aluno12')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.descricao_participacao_do_aluno12 = descricao_participacao_do_aluno12

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/avaliacao')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_participacao.html')


@app.route('/PEI/avaliacao', methods=['GET', 'POST'])
@login_required
def pei_avaliacao():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            descricao_avaliacao_pei14 = request.form.get('descricao_avaliacao_pei14')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.descricao_avaliacao_pei14 = descricao_avaliacao_pei14

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/PEI/homologacao')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_avaliacao.html')


@app.route('/PEI/homologacao', methods=['GET', 'POST'])
@login_required
def pei_homologacao():
    aluno_ids = session.get('aluno_ids')
    alunos_selecionados = Alunos.query.get(aluno_ids)
    if alunos_selecionados:
        if request.method == 'POST':
            professor1_151 = request.form.get('professor1_151')
            professor2_151 = request.form.get('professor2_151')
            professor3_151 = request.form.get('professor3_151')
            professor4_151 = request.form.get('professor4_151')
            professor5_151 = request.form.get('professor5_151')
            professor6_151 = request.form.get('professor6_151')
            professor7_151 = request.form.get('professor7_151')
            professor8_151 = request.form.get('professor8_151')
            professor9_151 = request.form.get('professor9_151')
            professor10_151 = request.form.get('professor10_151')
            professor11_151 = request.form.get('professor11_151')
            componente1_151 = request.form.get('componente1_151')
            componente2_151 = request.form.get('componente2_151')
            componente3_151 = request.form.get('componente3_151')
            componente4_151 = request.form.get('componente4_151')
            componente5_151 = request.form.get('componente5_151')
            componente6_151 = request.form.get('componente6_151')
            componente7_151 = request.form.get('componente7_151')
            componente8_151 = request.form.get('componente8_151')
            componente9_151 = request.form.get('componente9_151')
            componente10_151 = request.form.get('componente10_151')
            componente11_151 = request.form.get('componente11_151')
            coordenacao_152 = request.form.get('coordenacao_152')
            aprovado_153 = request.form.get('aprovado_153')
            homologacao_154 = request.form.get('homologacao_154')
            concordo_medidas_155 = request.form.get('concordo_medidas_155')
            ciencia_familia_156 = request.form.get('ciencia_familia_156')
            profissional_157 = request.form.get('profissional_157')
            pei = PEI.query.filter_by(aluno_nome=alunos_selecionados.aluno_nome).first()

            if pei:
                pei.professor1_151 = professor1_151
                pei.professor2_151 = professor2_151
                pei.professor3_151 = professor3_151
                pei.professor4_151 = professor4_151
                pei.professor5_151 = professor5_151
                pei.professor6_151 = professor6_151
                pei.professor7_151 = professor7_151
                pei.professor8_151 = professor8_151
                pei.professor9_151 = professor9_151
                pei.professor10_151 = professor10_151
                pei.professor11_151 = professor11_151
                pei.componente1_151 = componente1_151
                pei.componente2_151 = componente2_151
                pei.componente3_151 = componente3_151
                pei.componente4_151 = componente4_151
                pei.componente5_151 = componente5_151
                pei.componente6_151 = componente6_151
                pei.componente7_151 = componente7_151
                pei.componente8_151 = componente8_151
                pei.componente9_151 = componente9_151
                pei.componente10_151 = componente10_151
                pei.componente11_151 = componente11_151
                pei.coordenacao_152 = coordenacao_152
                pei.aprovado_153 = aprovado_153
                pei.homologacao_154 = homologacao_154
                pei.concordo_medidas_155 = concordo_medidas_155
                pei.ciencia_familia_156 = ciencia_familia_156
                pei.profissional_157 = profissional_157

                database.session.commit()
                flash('Formulário salvo com sucesso', 'alert-success')
                return redirect('/PEI')  # Redirecionar para outra página após salvar
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
                return redirect('/PEI')
    return render_template('pei_homologacao.html')


@app.route('/open_pdf')
def open_pdf():
    pdf_path = 'pdfs/Modelo_PEI.pdf'
    return send_file(pdf_path, as_attachment=False)


def import_cid_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith('.csv'):
            reader = csv.reader(file)
            cid_import = [row for row in reader if len(row) == 2]
        else:
            lines = file.readlines()
            cid_import = [line.strip().split(';') for line in lines if
                          len(line.strip().split(';')) == 2]  # Change to 8

        for cidfor in cid_import:
            numero_cid, doenca_cid = cidfor  # Add 'criterio' to the unpacking
            cid_ = Cid(
                numero_cid=numero_cid,
                doenca_cid=doenca_cid
            )
            database.session.add(cid_)  # Assuming `database.session` is properly configured
        database.session.commit()


@app.route('/PEI/cid/import', methods=['GET', 'POST'])
@login_required
def cid_pag():
    cid_file = request.files.get('file')
    if cid_file:
        filename, file_extension = os.path.splitext(cid_file.filename)
        if file_extension.lower() == '.txt' or file_extension.lower() == '.csv':
            file_path = os.path.join(UPLOAD_FOLDER, cid_file.filename)
            cid_file.save(file_path)
            import_cid_file(file_path)
            return redirect('/PEI')
        else:
            flash('Apenas (.txt e .csv) são permitidos!', 'alert-danger')
    return render_template('cid.html')


######################################################################
def obter_estados():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    response = requests.get(url)
    estados = {}
    if response.status_code == 200:
        data = response.json()
        for estado in data:
            estados[estado["sigla"]] = estado["nome"]
    return estados


def obter_cidades(estado_id):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado_id}/municipios"
    response = requests.get(url)
    cidades = []
    if response.status_code == 200:
        data = response.json()
        for cidade in data:
            cidades.append(cidade["nome"])
    return cidades


@app.route('/conselho_de_classe_pesquisa', methods=['GET', 'POST'])
@login_required
def conselho_classe_pesquisa():
    turma_cc_query = CC.query.order_by(func.lower(CC.turma)).all()
    return render_template('conselho_classe_pesquisa.html', turma_cc_query=turma_cc_query)


@app.route('/conselho_de_classe', methods=['GET', 'POST'])
@login_required
def conselho_classe():
    estados = obter_estados()
    professoresquery = Professor.query.order_by(func.lower(Professor.professor)).all()
    turma_pagina_query = Turma.query.order_by(func.lower(Turma.turma)).all()
    current_date = datetime.now()
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
              "novembro", "dezembro"]
    formatted_date = f"{current_date.day} de {months[current_date.month - 1]} de {current_date.year}"

    if request.method == 'POST':
        professores_presentes = request.form.getlist(
            'professores_presentes')  # Recebe a lista de professores selecionados
        professores_presentes_str = ",".join(professores_presentes)  # Converte a lista em uma string com vírgulas

        turma = request.form.get('turma')
        ordem = request.form.get('ordem')
        unidade = request.form.get('unidade')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        data_cc = request.form.get('data_cc')
        diretoria = request.form.get('diretoria')
        secretaria = request.form.get('secretaria')
        coordenacao = request.form.get('coordenacao')
        orientacao = request.form.get('orientacao')
        capelania = request.form.get('capelania')
        outro = request.form.get('outro')
        orador = request.form.get('orador')
        tema_explanado_cc = request.form.get('tema_explanado_cc')
        dia = request.form.get('dia')
        mes = request.form.get('mes')
        ano = request.form.get('ano')
        periodo_inicial = request.form.get('periodo_inicial')
        periodo_final = request.form.get('periodo_final')
        bimestre = request.form.get('bimestre')

        # Criar uma instância da tabela "CC" e preencher os campos
        turma_selecionada_cc = Turma.query.filter_by(turma=turma).first()
        if turma_selecionada_cc:
            session['turma_id_cc'] = turma_selecionada_cc.id

            conselho_classe_data = CC(
                turma=turma_selecionada_cc.turma,
                serie=turma_selecionada_cc.serie,
                ordem=ordem,
                unidade=unidade,
                cidade=cidade,
                estado=estado,
                data_cc=data_cc,
                diretoria=diretoria,
                secretaria=secretaria,
                coordenacao=coordenacao,
                orientacao=orientacao,
                capelania=capelania,
                ourto=outro,
                professores_presentes=professores_presentes_str,  # Salva a string com vírgulas no banco de dados
                orador=orador,
                tema_explanado_cc=tema_explanado_cc,
                dia=dia,
                mes=mes,
                ano=ano,
                periodo_inicial=periodo_inicial,
                periodo_final=periodo_final,
                bimestre=bimestre
            )

            # Adicionar e commit no banco de dados
            database.session.add(conselho_classe_data)
            database.session.commit()

            session['turma_selecionada_cc'] = turma_selecionada_cc.turma
            flash('Continue o Formulário', 'alert-success')
            return redirect('/conselho_de_classe_estatisticas')
        else:
            flash('Correu algum Erro', 'alert-danger')

    return render_template('conselho_classe.html', professoresquery=professoresquery, estados=estados,
                           turma_pagina_query=turma_pagina_query, formatted_date=formatted_date, months=months)


@app.route('/cidades/<estado_id>')
def cidades(estado_id):
    cidades = obter_cidades(estado_id)
    return jsonify(cidades)


@app.route('/conselho_de_classe_estatisticas', methods=['GET', 'POST'])
@login_required
def conselho_classe_estatisticas():
    turma_id_cc = session.get('turma_id_cc')
    turma_selecionada_cc = Turma.query.get(turma_id_cc)
    if request.method == 'POST':
        flash('Continue o Formulário', 'alert-success')
        return redirect("/conselho_de_classe_avaliacao_turma")
    return render_template('conselho_classe_estatisticas.html', turma_selecionada_cc=turma_selecionada_cc)


@app.route('/conselho_de_classe_avaliacao_turma', methods=['GET', 'POST'])
@login_required
def conselho_classe_avaliacaoturma():
    turma_id_cc = session.get('turma_id_cc')
    turma_selecionada_cc = Turma.query.get(turma_id_cc)
    if turma_selecionada_cc:
        if request.method == 'POST':
            quanto_ao_aproveitamento = request.form.get('quanto_ao_aproveitamento')
            quanto_a_disciplina = request.form.get('quanto_a_disciplina')
            quanto_a_participacao = request.form.get('quanto_a_participacao')
            quanto_a_frequencia = request.form.get('quanto_a_frequencia')
            quanto_a_comunicacao_com_professor = request.form.get('quanto_a_comunicacao_com_professor')
            quanto_a_relacao_interpessoal = request.form.get('quanto_a_relacao_interpessoal')
            conselho_classe_table = CC.query.filter_by(turma=turma_selecionada_cc.turma).first()

            if conselho_classe_table:
                conselho_classe_table.quanto_ao_aproveitamento = quanto_ao_aproveitamento
                conselho_classe_table.quanto_a_disciplina = quanto_a_disciplina
                conselho_classe_table.quanto_a_participacao = quanto_a_participacao
                conselho_classe_table.quanto_a_frequencia = quanto_a_frequencia
                conselho_classe_table.quanto_a_comunicacao_com_professor = quanto_a_comunicacao_com_professor
                conselho_classe_table.quanto_a_relacao_interpessoal = quanto_a_relacao_interpessoal
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/conselho_de_classe_apontamentos')
            else:
                flash('Erro', 'alert-danger')
    return render_template('conselho_classe_avaliacaoturma.html', turma_selecionada_cc=turma_selecionada_cc)


@app.route('/conselho_de_classe_apontamentos', methods=['GET', 'POST'])
@login_required
def conselho_classe_apontamentos():
    nome_alunoquery = Alunos.query.order_by(func.lower(Alunos.aluno_nome)).all()
    turma_id_cc = session.get('turma_id_cc')
    turma_selecionada_cc = Turma.query.get(turma_id_cc)

    if turma_selecionada_cc:
        if request.method == 'POST':
            alunos_destaque_positivo = request.form.getlist(
                'alunos_destaque_positivo')  # Recebe a lista de professores selecionados
            alunos_destaque_positivo_str = ",".join(
                alunos_destaque_positivo)  # Converte a lista em uma string com vírgulas

            alunos_com_dificuldade = request.form.getlist(
                'alunos_com_dificuldade')  # Recebe a lista de professores selecionados
            alunos_com_dificuldade_str = ",".join(
                alunos_com_dificuldade)  # Converte a lista em uma string com vírgulas
            conselho_classe_table = CC.query.filter_by(turma=turma_selecionada_cc.turma).first()

            if conselho_classe_table:
                conselho_classe_table.alunos_destaque_positivo = alunos_destaque_positivo_str
                conselho_classe_table.alunos_com_dificuldade = alunos_com_dificuldade_str
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/conselho_de_classe_proposicao')
            else:
                flash('Erro', 'alert-danger')

    return render_template('conselho_classe_apontamentos.html', nome_alunoquery=nome_alunoquery,
                           turma_selecionada_cc=turma_selecionada_cc)


@app.route('/conselho_de_classe_proposicao', methods=['GET', 'POST'])
@login_required
def conselho_classe_proposicao():
    turma_id_cc = session.get('turma_id_cc')
    turma_selecionada_cc = Turma.query.get(turma_id_cc)
    if turma_selecionada_cc:
        if request.method == 'POST':
            opcoes_proposicao = request.form.getlist('opcoes_proposicao')  # Recebe a lista de professores selecionados
            opcoes_proposicao_str = " ; ".join(opcoes_proposicao)  # Converte a lista em uma string com vírgulas
            conselho_classe_table = CC.query.filter_by(turma=turma_selecionada_cc.turma).first()

            if conselho_classe_table:
                conselho_classe_table.opcoes_proposicao = opcoes_proposicao_str
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/conselho_de_classe_proposicao_descricao')
            else:
                flash('Erro', 'alert-danger')
    return render_template('conselho_classe_proposicao.html', turma_selecionada_cc=turma_selecionada_cc)


@app.route('/conselho_de_classe_proposicao_descricao', methods=['GET', 'POST'])
@login_required
def conselho_classe_proposicao_desc():
    turma_id_cc = session.get('turma_id_cc')
    turma_selecionada_cc = Turma.query.get(turma_id_cc)

    # Obtenha as opções de proposição da turma selecionada
    conselho_classe_table = CC.query.filter_by(turma=turma_selecionada_cc.turma).first()
    opcoes_proposicao = []

    if conselho_classe_table:
        opcoes_proposicao = conselho_classe_table.opcoes_proposicao.split(' ; ')

    if turma_selecionada_cc:
        if request.method == 'POST':
            consideracoes_finais = request.form.get('consideracoes_finais')
            conselho_classe_table = CC.query.filter_by(turma=turma_selecionada_cc.turma).first()

            if conselho_classe_table:
                conselho_classe_table.consideracoes_finais = consideracoes_finais
                database.session.commit()
                flash('Formulário de Conselho de Classe Concluído com Sucesso!', 'alert-success')
                return redirect('/conselho_de_classe')
            else:
                flash('Erro', 'alert-danger')

    return render_template('conselho_classe_proposicao_desc.html', turma_selecionada_cc=turma_selecionada_cc,
                           opcoes_proposicao=opcoes_proposicao)


######################################################################

@app.route('/conselho_disciplinar_pesquisa', methods=['GET', 'POST'])
@login_required
def conselho_disciplinar_pesquisa():
    nome_alunoquery = CD.query.order_by(func.lower(CD.aluno_nome)).all()
    return render_template('conselho_disciplinar_pesquisa.html', nome_alunoquery=nome_alunoquery)


@app.route('/conselho_disciplinar', methods=['GET', 'POST'])
@login_required
def conselho_disciplinar():
    nome_alunoquery = Alunos.query.order_by(func.lower(Alunos.aluno_nome)).all()
    professoresquery = Professor.query.order_by(func.lower(Professor.professor)).all()
    estados = obter_estados()
    if request.method == 'POST':
        professores_presentes = request.form.getlist(
            'professores_presentes')  # Recebe a lista de professores selecionados
        professores_presentes_str = ",".join(professores_presentes)  # Converte a lista em uma string com vírgulas

        aluno_nome = request.form.get('aluno_nome')
        unidade = request.form.get('unidade')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        ordem = request.form.get('ordem')
        data_cd = request.form.get('data_cd')
        diretoria = request.form.get('diretoria')
        coordenacao = request.form.get('coordenacao')
        capelania = request.form.get('capelania')
        secretaria = request.form.get('secretaria')
        orientacao = request.form.get('orientacao')
        ourto = request.form.get('ourto')
        responsavel_legal = request.form.get('responsavel_legal')
        apresentacao_cd = request.form.get('apresentacao_cd')

        # Criar uma instância da tabela "CC" e preencher os campos
        aluno_selecionado_cd = Alunos.query.filter_by(aluno_nome=aluno_nome).first()
        if aluno_selecionado_cd:
            session['aluno_nome_cd'] = aluno_selecionado_cd.id

            conselho_disciplinar_data = CD(
                aluno_nome=aluno_selecionado_cd.aluno_nome,
                turma_aluno=aluno_selecionado_cd.matricula_serie,
                serie_aluno=aluno_selecionado_cd.matricula_turma,
                ra=aluno_selecionado_cd.aluno_codigo,
                unidade=unidade,
                cidade=cidade,
                estado=estado,
                ordem=ordem,
                data_cd=data_cd,
                diretoria=diretoria,
                coordenacao=coordenacao,
                capelania=capelania,  # Salva a string com vírgulas no banco de dados
                secretaria=secretaria,
                orientacao=orientacao,
                ourto=ourto,
                professores_presentes=professores_presentes_str,
                responsavel_legal=responsavel_legal,
                apresentacao_cd=apresentacao_cd,
            )

            # Adicionar e commit no banco de dados
            database.session.add(conselho_disciplinar_data)
            database.session.commit()

            session['aluno_selecionado_cd'] = aluno_selecionado_cd.aluno_nome
            flash('Continue o Formulário', 'alert-success')
            return redirect('/conselho_disciplinar_estatisticas')
        else:
            flash('Correu algum Erro', 'alert-danger')
    return render_template('conselho_disciplinar.html', nome_alunoquery=nome_alunoquery,
                           professoresquery=professoresquery, estados=estados)


@app.route('/conselho_disciplinar_estatisticas', methods=['GET', 'POST'])
@login_required
def conselho_disciplinar_estatisticas():
    aluno_nome_cd = session.get('aluno_nome_cd')
    aluno_selecionado_cd = Alunos.query.get(aluno_nome_cd)
    if request.method == 'POST':
        flash('Continue o Formulário', 'alert-success')
        return redirect("/conselho_disciplinar_avaliacao")
    return render_template('conselho_disciplinar_estatisticas.html', aluno_selecionado_cd=aluno_selecionado_cd)


@app.route('/conselho_disciplinar_avaliacao', methods=['GET', 'POST'])
@login_required
def conselho_disciplinar_avaliacao():
    aluno_nome_cd = session.get('aluno_nome_cd')
    aluno_selecionado_cd = Alunos.query.get(aluno_nome_cd)
    if aluno_selecionado_cd:
        if request.method == 'POST':
            item1 = request.form.get('item1')
            item2 = request.form.get('item2')
            item3 = request.form.get('item3')
            item4 = request.form.get('item4')
            item5 = request.form.get('item5')
            item6 = request.form.get('item6')

            cd = CD.query.filter_by(aluno_nome=aluno_selecionado_cd.aluno_nome).first()

            if cd:
                cd.item1 = item1
                cd.item2 = item2
                cd.item3 = item3
                cd.item4 = item4
                cd.item5 = item5
                cd.item6 = item6
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/conselho_disciplinar_composicao')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')

    return render_template('conselho_disciplinar_avaliacao.html', aluno_selecionado_cd=aluno_selecionado_cd)


@app.route('/conselho_disciplinar_composicao', methods=['GET', 'POST'])
@login_required
def conselho_disciplinar_composicao():
    aluno_nome_cd = session.get('aluno_nome_cd')
    aluno_selecionado_cd = Alunos.query.get(aluno_nome_cd)
    if aluno_selecionado_cd:
        if request.method == 'POST':
            itens_cd = request.form.getlist(
                'itens_cd')  # Recebe a lista de professores selecionados
            itens_cd_str = ",".join(itens_cd)
            consideracoes_finais = request.form.get('consideracoes_finais')
            cd = CD.query.filter_by(aluno_nome=aluno_selecionado_cd.aluno_nome).first()

            if cd:
                cd.itens_cd = itens_cd_str
                cd.consideracoes_finais = consideracoes_finais
                database.session.commit()
                flash('Formulário Concluido', 'alert-success')
                return redirect('/conselho_disciplinar')
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    return render_template('conselho_disciplinar_composicao.html', aluno_selecionado_cd=aluno_selecionado_cd)


######################################################################
@app.route('/avaliacao/aluno', methods=['GET', 'POST'])
@login_required
def avaliacao_aluno():
    nome_alunoquery = Alunos.query.order_by(func.lower(Alunos.aluno_nome)).all()
    notas_alunosquery = Notas_Alunos.query.order_by(func.lower(Notas_Alunos.aluno_nome_notas)).all()
    peso_notas_alunosquery = Peso_Nota_P1.query.order_by(func.lower(Peso_Nota_P1.aluno_nome_notas)).all()
    current_date = datetime.now()
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
              "novembro", "dezembro"]
    formatted_date = f"{current_date.day} de {months[current_date.month - 1]} de {current_date.year}"
    if request.method == 'POST':
        aluno_nome_cp = request.form.get('aluno_nome')
        bimestres = request.form.get('bimestre')
        foto_aluno = request.form.get('foto_aluno')
        aluno_selecionado_cp = Alunos.query.filter_by(aluno_nome=aluno_nome_cp).first()

        if aluno_selecionado_cp:
            session['aluno_id_cp'] = aluno_selecionado_cp.id
            session['foto_aluno'] = foto_aluno
            session['aluno_selecionado_cp'] = aluno_selecionado_cp.aluno_nome  # Add this line

            cp_aluno = CP_Aluno(
                aluno_nome=aluno_selecionado_cp.aluno_nome,
                serie_aluno=aluno_selecionado_cp.matricula_serie,
                turma_aluno=aluno_selecionado_cp.matricula_turma,
                matricula_aluno=aluno_selecionado_cp.aluno_codigo,
                bimestre=bimestres
            )
            database.session.add(cp_aluno)
            database.session.commit()

            flash('Continue o Formulário.', 'alert-success')
            return redirect("/avaliacao%aluno%apontamento")
        else:
            flash('Ocorreu algum erro. Verifique se há algum campo faltando.', 'alert-danger')
    return render_template('avaliacao_aluno.html', nome_alunoquery=nome_alunoquery, notas_alunosquery=notas_alunosquery,
                           formatted_date=formatted_date, peso_notas_alunosquery=peso_notas_alunosquery)


@app.route('/avaliacao%aluno%apontamento', methods=['GET', 'POST'])
@login_required
def avaliacao_aluno_apontamento():
    # Data atual
    current_date = datetime.now()
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
              "outubro",
              "novembro", "dezembro"]
    formatted_date = f"{current_date.day} de {months[current_date.month - 1]} de {current_date.year}"
    # Salvar
    aluno_id_cp = session.get('aluno_id_cp')
    foto_aluno = session.get('foto_aluno')
    aluno_selecionado_cp = Alunos.query.get(aluno_id_cp)

    if aluno_selecionado_cp:
        if request.method == 'POST':
            opcao100_01 = request.form.get('opcao100_01')
            opcao100_02 = request.form.get('opcao100_02')
            opcao100_03 = request.form.get('opcao100_03')
            opcao100_04 = request.form.get('opcao100_04')
            opcao100_05 = request.form.get('opcao100_05')
            opcao100_06 = request.form.get('opcao100_06')
            opcao100_07 = request.form.get('opcao100_07')
            opcao100_08 = request.form.get('opcao100_08')
            opcao100_09 = request.form.get('opcao100_09')
            opcao100_10 = request.form.get('opcao100_10')
            opcao100_11 = request.form.get('opcao100_11')
            opcao100_12 = request.form.get('opcao100_12')
            opcao100_13 = request.form.get('opcao100_13')
            opcao100_14 = request.form.get('opcao100_14')
            opcao100_15 = request.form.get('opcao100_15')
            opcao100_16 = request.form.get('opcao100_16')
            opcao100_17 = request.form.get('opcao100_17')
            opcao100_18 = request.form.get('opcao100_18')
            opcao100_19 = request.form.get('opcao100_19')
            opcao100_20 = request.form.get('opcao100_20')
            opcao100 = request.form.get('opcao100')
            opcao101 = request.form.get('opcao101')
            opcao102 = request.form.get('opcao102')
            opcao103 = request.form.get('opcao103')
            opcao104 = request.form.get('opcao104')
            opcao105 = request.form.get('opcao105')
            opcao106 = request.form.get('opcao106')
            opcao107 = request.form.get('opcao107')
            opcao108 = request.form.get('opcao108')
            opcao109 = request.form.get('opcao109')
            opcao110 = request.form.get('opcao110')
            opcao111 = request.form.get('opcao111')
            opcao112 = request.form.get('opcao112')
            opcao113 = request.form.get('opcao113')
            opcao114 = request.form.get('opcao114')
            opcao115 = request.form.get('opcao115')
            opcao116 = request.form.get('opcao116')
            opcao117 = request.form.get('opcao117')
            opcao118 = request.form.get('opcao118')
            opcao119 = request.form.get('opcao119')
            opcao120 = request.form.get('opcao120')
            opcao121 = request.form.get('opcao121')
            opcao122 = request.form.get('opcao122')
            opcao123 = request.form.get('opcao123')
            opcao124 = request.form.get('opcao124')
            opcao125 = request.form.get('opcao125')
            opcao126 = request.form.get('opcao126')
            opcao127 = request.form.get('opcao127')
            opcao128 = request.form.get('opcao128')
            opcao129 = request.form.get('opcao129')
            opcao130 = request.form.get('opcao130')
            opcao131 = request.form.get('opcao131')
            opcao132 = request.form.get('opcao132')
            opcao133 = request.form.get('opcao133')
            opcao134 = request.form.get('opcao134')
            opcao135 = request.form.get('opcao135')
            opcao136 = request.form.get('opcao136')
            opcao137 = request.form.get('opcao137')
            opcao138 = request.form.get('opcao138')
            opcao139 = request.form.get('opcao139')
            opcao140 = request.form.get('opcao140')
            opcao141 = request.form.get('opcao141')
            opcao142 = request.form.get('opcao142')
            opcao143 = request.form.get('opcao143')
            opcao144 = request.form.get('opcao144')
            opcao145 = request.form.get('opcao145')
            opcao146 = request.form.get('opcao146')
            opcao147 = request.form.get('opcao147')
            opcao148 = request.form.get('opcao148')
            opcao149 = request.form.get('opcao149')
            opcao150 = request.form.get('opcao150')

            cp_aluno = CP_Aluno.query.filter_by(aluno_nome=aluno_selecionado_cp.aluno_nome).first()

            if cp_aluno:
                cp_aluno.opcao100_01 = opcao100_01
                cp_aluno.opcao100_02 = opcao100_02
                cp_aluno.opcao100_03 = opcao100_03
                cp_aluno.opcao100_04 = opcao100_04
                cp_aluno.opcao100_05 = opcao100_05
                cp_aluno.opcao100_06 = opcao100_06
                cp_aluno.opcao100_07 = opcao100_07
                cp_aluno.opcao100_08 = opcao100_08
                cp_aluno.opcao100_09 = opcao100_09
                cp_aluno.opcao100_10 = opcao100_10
                cp_aluno.opcao100_11 = opcao100_11
                cp_aluno.opcao100_12 = opcao100_12
                cp_aluno.opcao100_13 = opcao100_13
                cp_aluno.opcao100_14 = opcao100_14
                cp_aluno.opcao100_15 = opcao100_15
                cp_aluno.opcao100_16 = opcao100_16
                cp_aluno.opcao100_17 = opcao100_17
                cp_aluno.opcao100_18 = opcao100_18
                cp_aluno.opcao100_19 = opcao100_19
                cp_aluno.opcao100_20 = opcao100_20
                cp_aluno.opcao100 = opcao100
                cp_aluno.opcao101 = opcao101
                cp_aluno.opcao102 = opcao102
                cp_aluno.opcao103 = opcao103
                cp_aluno.opcao104 = opcao104
                cp_aluno.opcao105 = opcao105
                cp_aluno.opcao106 = opcao106
                cp_aluno.opcao107 = opcao107
                cp_aluno.opcao108 = opcao108
                cp_aluno.opcao109 = opcao109
                cp_aluno.opcao110 = opcao110
                cp_aluno.opcao111 = opcao111
                cp_aluno.opcao112 = opcao112
                cp_aluno.opcao113 = opcao113
                cp_aluno.opcao114 = opcao114
                cp_aluno.opcao115 = opcao115
                cp_aluno.opcao116 = opcao116
                cp_aluno.opcao117 = opcao117
                cp_aluno.opcao118 = opcao118
                cp_aluno.opcao119 = opcao119
                cp_aluno.opcao120 = opcao120
                cp_aluno.opcao121 = opcao121
                cp_aluno.opcao122 = opcao122
                cp_aluno.opcao123 = opcao123
                cp_aluno.opcao124 = opcao124
                cp_aluno.opcao125 = opcao125
                cp_aluno.opcao126 = opcao126
                cp_aluno.opcao127 = opcao127
                cp_aluno.opcao128 = opcao128
                cp_aluno.opcao129 = opcao129
                cp_aluno.opcao130 = opcao130
                cp_aluno.opcao131 = opcao131
                cp_aluno.opcao132 = opcao132
                cp_aluno.opcao133 = opcao133
                cp_aluno.opcao134 = opcao134
                cp_aluno.opcao135 = opcao135
                cp_aluno.opcao136 = opcao136
                cp_aluno.opcao137 = opcao137
                cp_aluno.opcao138 = opcao138
                cp_aluno.opcao139 = opcao139
                cp_aluno.opcao140 = opcao140
                cp_aluno.opcao141 = opcao141
                cp_aluno.opcao142 = opcao142
                cp_aluno.opcao143 = opcao143
                cp_aluno.opcao144 = opcao144
                cp_aluno.opcao145 = opcao145
                cp_aluno.opcao146 = opcao146
                cp_aluno.opcao147 = opcao147
                cp_aluno.opcao148 = opcao148
                cp_aluno.opcao149 = opcao149
                cp_aluno.opcao150 = opcao150

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/avaliacao%aluno%proposta')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    else:
        flash('Aluno não encontrado', 'alert-danger')
        return redirect('/avaliacao/aluno')
    return render_template('avaliacao_aluno_apontamento.html', formatted_date=formatted_date,
                           aluno_selecionado_cp=aluno_selecionado_cp, foto_aluno=foto_aluno)


@app.route('/avaliacao%aluno%proposta', methods=['GET', 'POST'])
@login_required
def avaliacao_aluno_proposta():
    # Data atual
    current_date = datetime.now()
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
              "outubro",
              "novembro", "dezembro"]
    formatted_date = f"{current_date.day} de {months[current_date.month - 1]} de {current_date.year}"
    # Salvar
    aluno_id_cp = session.get('aluno_id_cp')
    aluno_selecionado_cp = Alunos.query.get(aluno_id_cp)

    if aluno_selecionado_cp:
        if request.method == 'POST':
            opcao01 = request.form.get('opcao01')
            opcao02 = request.form.get('opcao02')
            opcao03 = request.form.get('opcao03')
            opcao04 = request.form.get('opcao04')
            opcao05 = request.form.get('opcao05')
            opcao06 = request.form.get('opcao06')
            opcao07 = request.form.get('opcao07')
            opcao08 = request.form.get('opcao08')
            opcao09 = request.form.get('opcao09')
            opcao10 = request.form.get('opcao10')
            opcao11 = request.form.get('opcao11')
            opcao12 = request.form.get('opcao12')
            opcao13 = request.form.get('opcao13')
            opcao14 = request.form.get('opcao14')
            opcao15 = request.form.get('opcao15')
            opcao16 = request.form.get('opcao16')
            opcao17 = request.form.get('opcao17')
            opcao18 = request.form.get('opcao18')
            opcao19 = request.form.get('opcao19')
            opcao20 = request.form.get('opcao20')
            opcao21 = request.form.get('opcao21')
            opcao22 = request.form.get('opcao22')
            opcao23 = request.form.get('opcao23')
            opcao24 = request.form.get('opcao24')
            opcao25 = request.form.get('opcao25')
            opcao26 = request.form.get('opcao26')
            opcao27 = request.form.get('opcao27')
            opcao28 = request.form.get('opcao28')
            opcao29 = request.form.get('opcao29')
            opcao30 = request.form.get('opcao30')
            opcao31 = request.form.get('opcao31')
            opcao32 = request.form.get('opcao32')
            opcao33 = request.form.get('opcao33')
            opcao34 = request.form.get('opcao34')
            opcao35 = request.form.get('opcao35')
            opcao36 = request.form.get('opcao36')
            opcao37 = request.form.get('opcao37')
            opcao38 = request.form.get('opcao38')
            opcao39 = request.form.get('opcao39')
            opcao40 = request.form.get('opcao40')
            opcao41 = request.form.get('opcao41')
            opcao42 = request.form.get('opcao42')
            opcao43 = request.form.get('opcao43')
            opcao44 = request.form.get('opcao44')
            opcao45 = request.form.get('opcao45')
            opcao46 = request.form.get('opcao46')
            opcao47 = request.form.get('opcao47')

            cp_aluno = CP_Aluno.query.filter_by(aluno_nome=aluno_selecionado_cp.aluno_nome).first()

            if cp_aluno:
                cp_aluno.opcao01 = opcao01
                cp_aluno.opcao02 = opcao02
                cp_aluno.opcao03 = opcao03
                cp_aluno.opcao04 = opcao04
                cp_aluno.opcao05 = opcao05
                cp_aluno.opcao06 = opcao06
                cp_aluno.opcao07 = opcao07
                cp_aluno.opcao08 = opcao08
                cp_aluno.opcao09 = opcao09
                cp_aluno.opcao10 = opcao10
                cp_aluno.opcao11 = opcao11
                cp_aluno.opcao12 = opcao12
                cp_aluno.opcao13 = opcao13
                cp_aluno.opcao14 = opcao14
                cp_aluno.opcao15 = opcao15
                cp_aluno.opcao16 = opcao16
                cp_aluno.opcao17 = opcao17
                cp_aluno.opcao18 = opcao18
                cp_aluno.opcao19 = opcao19
                cp_aluno.opcao20 = opcao20
                cp_aluno.opcao21 = opcao21
                cp_aluno.opcao22 = opcao22
                cp_aluno.opcao23 = opcao23
                cp_aluno.opcao24 = opcao24
                cp_aluno.opcao25 = opcao25
                cp_aluno.opcao26 = opcao26
                cp_aluno.opcao27 = opcao27
                cp_aluno.opcao28 = opcao28
                cp_aluno.opcao29 = opcao29
                cp_aluno.opcao30 = opcao30
                cp_aluno.opcao31 = opcao31
                cp_aluno.opcao32 = opcao32
                cp_aluno.opcao33 = opcao33
                cp_aluno.opcao34 = opcao34
                cp_aluno.opcao35 = opcao35
                cp_aluno.opcao36 = opcao36
                cp_aluno.opcao37 = opcao37
                cp_aluno.opcao38 = opcao38
                cp_aluno.opcao39 = opcao39
                cp_aluno.opcao40 = opcao40
                cp_aluno.opcao41 = opcao41
                cp_aluno.opcao42 = opcao42
                cp_aluno.opcao43 = opcao43
                cp_aluno.opcao44 = opcao44
                cp_aluno.opcao45 = opcao45
                cp_aluno.opcao46 = opcao46
                cp_aluno.opcao47 = opcao47

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/avaliacao%aluno/consideracoesfinais')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    else:
        flash('Aluno não encontrado', 'alert-danger')
        return redirect('/avaliacao/aluno')
    return render_template('avaliacao_aluno_proposta.html', formatted_date=formatted_date,
                           aluno_selecionado_cp=aluno_selecionado_cp)


@app.route('/avaliacao%aluno/consideracoesfinais', methods=['GET', 'POST'])
@login_required
def avaliacao_aluno_consideracoesfinais():
    # Data atual
    current_date = datetime.now()
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
              "outubro",
              "novembro", "dezembro"]
    formatted_date = f"{current_date.day} de {months[current_date.month - 1]} de {current_date.year}"
    # Salvar
    aluno_id_cp = session.get('aluno_id_cp')
    aluno_selecionado_cp = Alunos.query.get(aluno_id_cp)

    if aluno_selecionado_cp:
        if request.method == 'POST':
            consideracoes_finais = request.form.get('consideracoes_finais')

            cp_aluno = CP_Aluno.query.filter_by(aluno_nome=aluno_selecionado_cp.aluno_nome).first()

            if cp_aluno:
                cp_aluno.consideracoes_finais = consideracoes_finais

                database.session.commit()
                flash('Formulário Concluído', 'alert-success')
                return redirect('/avaliacao/aluno')  # Redirect to another page after saving
            else:
                flash('Erro ao encontrar os dados do aluno.', 'alert-danger')
    else:
        flash('Aluno não encontrado', 'alert-danger')
        return redirect('/avaliacao/aluno')
    return render_template('avaliacao_aluno_consideracoesfinais.html', formatted_date=formatted_date,
                           aluno_selecionado_cp=aluno_selecionado_cp)


@app.route('/import/notas', methods=['GET', 'POST'])
@login_required
def importar_notas():
    notas_file = request.files.get('file')
    if notas_file:
        filename, file_extension = os.path.splitext(notas_file.filename)
        if file_extension.lower() == '.txt':
            file_path = os.path.join(UPLOAD_FOLDER, notas_file.filename)
            notas_file.save(file_path)
            import_notas_from_file(file_path)
            return redirect('/avaliacao/aluno')
        else:
            flash('Apenas (.txt) são permitidos!', 'alert-danger')
    return render_template('notas_importacao.html')


def import_notas_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith('.csv'):
            reader = csv.reader(file)
            notas = [row for row in reader if len(row) == 72]
        else:
            lines = file.readlines()
            notas = [line.strip().split(';') for line in lines if len(line.strip().split(';')) == 72]

        for notasfor in notas:
            aluno_codigo_notas, aluno_nome_notas, port_1Bimestre, mate_1Bimestre, geog_1Bimestre, espa_1Bimestre, hist_1Bimestre, ingl_1Bimestre, arte_1Bimestre, edfis_1Bimestre, reli_1Bimestre, redac_1Bimestre, port_2Bimestre, mate_2Bimestre, geog_2Bimestre, espa_2Bimestre, hist_2Bimestre, ingl_2Bimestre, arte_2Bimestre, edfis_2Bimestre, reli_2Bimestre, redac_2Bimestre, port_3Bimestre, mate_3Bimestre, geog_3Bimestre, espa_3Bimestre, hist_3Bimestre, ingl_3Bimestre, arte_3Bimestre, edfis_3Bimestre, reli_3Bimestre, redac_3Bimestre, falta_port_1Bimestre, falta_mate_1Bimestre, falta_geog_1Bimestre, falta_espa_1Bimestre, falta_hist_1Bimestre, falta_ingl_1Bimestre, falta_arte_1Bimestre, falta_edfis_1Bimestre, falta_reli_1Bimestre, falta_redac_1Bimestre, falta_port_2Bimestre, falta_mate_2Bimestre, falta_geog_2Bimestre, falta_espa_2Bimestre, falta_hist_2Bimestre, falta_ingl_2Bimestre, falta_arte_2Bimestre, falta_edfis_2Bimestre, falta_reli_2Bimestre, falta_redac_2Bimestre, falta_port_3Bimestre, falta_mate_3Bimestre, falta_geog_3Bimestre, falta_espa_3Bimestre, falta_hist_3Bimestre, falta_ingl_3Bimestre, falta_arte_3Bimestre, falta_edfis_3Bimestre, falta_reli_3Bimestre, falta_redac_3Bimestre, total_faltas_port, total_faltas_mate, total_faltas_geog, total_faltas_espa, total_faltas_hist, total_faltas_ingl, total_faltas_arte, total_faltas_edfis, total_faltas_reli, total_faltas_redac = notasfor
            notas_alunos = Notas_Alunos(
                aluno_codigo_notas=aluno_codigo_notas,
                aluno_nome_notas=aluno_nome_notas,
                port_1Bimestre=port_1Bimestre,
                mate_1Bimestre=mate_1Bimestre,
                geog_1Bimestre=geog_1Bimestre,
                espa_1Bimestre=espa_1Bimestre,
                hist_1Bimestre=hist_1Bimestre,
                ingl_1Bimestre=ingl_1Bimestre,
                arte_1Bimestre=arte_1Bimestre,
                edfis_1Bimestre=edfis_1Bimestre,
                reli_1Bimestre=reli_1Bimestre,
                redac_1Bimestre=redac_1Bimestre,
                port_2Bimestre=port_2Bimestre,
                mate_2Bimestre=mate_2Bimestre,
                geog_2Bimestre=geog_2Bimestre,
                espa_2Bimestre=espa_2Bimestre,
                hist_2Bimestre=hist_2Bimestre,
                ingl_2Bimestre=ingl_2Bimestre,
                arte_2Bimestre=arte_2Bimestre,
                edfis_2Bimestre=edfis_2Bimestre,
                reli_2Bimestre=reli_2Bimestre,
                redac_2Bimestre=redac_2Bimestre,
                port_3Bimestre=port_3Bimestre,
                mate_3Bimestre=mate_3Bimestre,
                geog_3Bimestre=geog_3Bimestre,
                espa_3Bimestre=espa_3Bimestre,
                hist_3Bimestre=hist_3Bimestre,
                ingl_3Bimestre=ingl_3Bimestre,
                arte_3Bimestre=arte_3Bimestre,
                edfis_3Bimestre=edfis_3Bimestre,
                reli_3Bimestre=reli_3Bimestre,
                redac_3Bimestre=redac_3Bimestre,
                falta_port_1Bimestre=falta_port_1Bimestre,
                falta_mate_1Bimestre=falta_mate_1Bimestre,
                falta_geog_1Bimestre=falta_geog_1Bimestre,
                falta_espa_1Bimestre=falta_espa_1Bimestre,
                falta_hist_1Bimestre=falta_hist_1Bimestre,
                falta_ingl_1Bimestre=falta_ingl_1Bimestre,
                falta_arte_1Bimestre=falta_arte_1Bimestre,
                falta_edfis_1Bimestre=falta_edfis_1Bimestre,
                falta_reli_1Bimestre=falta_reli_1Bimestre,
                falta_redac_1Bimestre=falta_redac_1Bimestre,
                falta_port_2Bimestre=falta_port_2Bimestre,
                falta_mate_2Bimestre=falta_mate_2Bimestre,
                falta_geog_2Bimestre=falta_geog_2Bimestre,
                falta_espa_2Bimestre=falta_espa_2Bimestre,
                falta_hist_2Bimestre=falta_hist_2Bimestre,
                falta_ingl_2Bimestre=falta_ingl_2Bimestre,
                falta_arte_2Bimestre=falta_arte_2Bimestre,
                falta_edfis_2Bimestre=falta_edfis_2Bimestre,
                falta_reli_2Bimestre=falta_reli_2Bimestre,
                falta_redac_2Bimestre=falta_redac_2Bimestre,
                falta_port_3Bimestre=falta_port_3Bimestre,
                falta_mate_3Bimestre=falta_mate_3Bimestre,
                falta_geog_3Bimestre=falta_geog_3Bimestre,
                falta_espa_3Bimestre=falta_espa_3Bimestre,
                falta_hist_3Bimestre=falta_hist_3Bimestre,
                falta_ingl_3Bimestre=falta_ingl_3Bimestre,
                falta_arte_3Bimestre=falta_arte_3Bimestre,
                falta_edfis_3Bimestre=falta_edfis_3Bimestre,
                falta_reli_3Bimestre=falta_reli_3Bimestre,
                falta_redac_3Bimestre=falta_redac_3Bimestre,
                total_faltas_port=total_faltas_port,
                total_faltas_mate=total_faltas_mate,
                total_faltas_geog=total_faltas_geog,
                total_faltas_espa=total_faltas_espa,
                total_faltas_hist=total_faltas_hist,
                total_faltas_ingl=total_faltas_ingl,
                total_faltas_arte=total_faltas_arte,
                total_faltas_edfis=total_faltas_edfis,
                total_faltas_reli=total_faltas_reli,
                total_faltas_redac=total_faltas_redac
            )
            database.session.add(notas_alunos)  # Assuming `database.session` is properly configured
        database.session.commit()


@app.route('/import/peso_notas', methods=['GET', 'POST'])
@login_required
def importar_peso_notas():
    peso_notas_file = request.files.get('file')
    if peso_notas_file:
        filename, file_extension = os.path.splitext(peso_notas_file.filename)
        if file_extension.lower() == '.txt':
            file_path = os.path.join(UPLOAD_FOLDER, peso_notas_file.filename)
            peso_notas_file.save(file_path)
            import_peso_notas_from_file(file_path)
            return redirect('/avaliacao/aluno')
        else:
            flash('Apenas (.txt) são permitidos!', 'alert-danger')
    return render_template('pesos_notas_importacao.html')


def import_peso_notas_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith('.csv'):
            reader = csv.reader(file)
            peso_notas = [row for row in reader if len(row) == 26]
        else:
            lines = file.readlines()
            peso_notas = [line.strip().split(';') for line in lines if len(line.strip().split(';')) == 26]

        for peso_notasfor in peso_notas:
            aluno_codigo_notas, aluno_nome_notas, port_P1_PesoNota, mate_P1_PesoNota, geog_P1_PesoNota, espa_P1_PesoNota, hist_P1_PesoNota, ingl_P1_PesoNota, arte_P1_PesoNota, edfis_P1_PesoNota, fisic_P1_PesoNota, quimi_P1_PesoNota, reli_P1_PesoNota, redac_P1_PesoNota, port_notas_P1, mate_notas_P1, geog_notas_P1, espa_notas_P1, hist_notas_P1, ingl_notas_P1, arte_notas_P1, edfis_notas_P1, fisic_notas_P1, quimi_notas_P1, reli_notas_P1, redac_notas_P1 = peso_notasfor
            peso_p1 = Peso_Nota_P1(
                aluno_codigo_notas=aluno_codigo_notas,
                aluno_nome_notas=aluno_nome_notas,
                port_P1_PesoNota=port_P1_PesoNota,
                mate_P1_PesoNota=mate_P1_PesoNota,
                geog_P1_PesoNota=geog_P1_PesoNota,
                espa_P1_PesoNota=espa_P1_PesoNota,
                hist_P1_PesoNota=hist_P1_PesoNota,
                ingl_P1_PesoNota=ingl_P1_PesoNota,
                arte_P1_PesoNota=arte_P1_PesoNota,
                edfis_P1_PesoNota=edfis_P1_PesoNota,
                fisic_P1_PesoNota=fisic_P1_PesoNota,
                quimi_P1_PesoNota=quimi_P1_PesoNota,
                reli_P1_PesoNota=reli_P1_PesoNota,
                redac_P1_PesoNota=redac_P1_PesoNota,
                port_notas_P1=port_notas_P1,
                mate_notas_P1=mate_notas_P1,
                geog_notas_P1=geog_notas_P1,
                espa_notas_P1=espa_notas_P1,
                hist_notas_P1=hist_notas_P1,
                ingl_notas_P1=ingl_notas_P1,
                arte_notas_P1=arte_notas_P1,
                edfis_notas_P1=edfis_notas_P1,
                fisic_notas_P1=fisic_notas_P1,
                quimi_notas_P1=quimi_notas_P1,
                reli_notas_P1=reli_notas_P1,
                redac_notas_P1=redac_notas_P1
            )
            database.session.add(peso_p1)  # Assuming `database.session` is properly configured
        database.session.commit()


######################################################################

@app.route('/avaliacao%turma', methods=['GET', 'POST'])
@login_required
def avaliacao_turma():
    turmaquery = Turma.query.order_by(func.lower(Turma.turma)).all()
    if request.method == 'POST':
        turma = request.form.get('turma')
        bimestre = request.form.get('bimestre')
        professor_conselheiro = request.form.get('professor_conselheiro')
        representante_turma = request.form.get('representante_turma')
        item101 = request.form.get('item101')
        item102 = request.form.get('item102')
        item103 = request.form.get('item103')
        item104 = request.form.get('item104')
        item105 = request.form.get('item105')
        item106 = request.form.get('item106')
        item107 = request.form.get('item107')

        turma_selecionado_cp_turma = Turma.query.filter_by(turma=turma).first()

        if turma_selecionado_cp_turma:
            session['turma_id_cp'] = turma_selecionado_cp_turma.id

            cp_turma = CP_Turma(
                turma=turma_selecionado_cp_turma.turma,
                serie=turma_selecionado_cp_turma.serie,
                bimestre=bimestre,
                professor_conselheiro=professor_conselheiro,
                representante_turma=representante_turma,
                item101=item101,
                item102=item102,
                item103=item103,
                item104=item104,
                item105=item105,
                item106=item106,
                item107=item107
            )
            database.session.add(cp_turma)
            database.session.commit()

            session['turma_selecionado_cp_turma'] = turma_selecionado_cp_turma.turma
            flash('Continue o Formulário.', 'alert-success')
            return redirect('/avaliacao%25turma%25avalieprofessor')
        else:
            flash('Ocorreu algum erro. Verifique se há algum campo faltando.', 'alert-danger')
    return render_template('avaliacao_turma.html', turmaquery=turmaquery)


@app.route('/avaliacao%turma%avalieprofessor', methods=['GET', 'POST'])
@login_required
def avaliacao_turma_avalieprofessor():
    professoresquery = Professor.query.order_by(func.lower(Professor.professor)).all()
    turma_id_cp = session.get('turma_id_cp')
    turma_selecionado_cp_turma = Turma.query.get(turma_id_cp)
    if turma_selecionado_cp_turma:
        if request.method == 'POST':
            opcao_201 = request.form.get('opcao_201')
            opcao_202 = request.form.get('opcao_202')
            opcao_203 = request.form.get('opcao_203')
            opcao_204 = request.form.get('opcao_204')
            opcao_205 = request.form.get('opcao_205')
            opcao_206 = request.form.get('opcao_206')
            opcao_207 = request.form.get('opcao_207')
            opcao_208 = request.form.get('opcao_208')
            opcao_209 = request.form.get('opcao_209')
            opcao_210 = request.form.get('opcao_210')
            opcao_211 = request.form.get('opcao_211')
            opcao_212 = request.form.get('opcao_212')
            opcao_213 = request.form.get('opcao_213')
            opcao_214 = request.form.get('opcao_214')
            opcao_215 = request.form.get('opcao_215')
            opcao_216 = request.form.get('opcao_216')
            opcao_217 = request.form.get('opcao_217')
            opcao_218 = request.form.get('opcao_218')
            opcao_219 = request.form.get('opcao_219')
            opcao_220 = request.form.get('opcao_220')
            opcao_221 = request.form.get('opcao_221')
            opcao_222 = request.form.get('opcao_222')
            opcao_223 = request.form.get('opcao_223')
            opcao_224 = request.form.get('opcao_224')
            opcao_225 = request.form.get('opcao_225')
            opcao_226 = request.form.get('opcao_226')
            opcao_227 = request.form.get('opcao_227')
            opcao_228 = request.form.get('opcao_228')
            opcao_229 = request.form.get('opcao_229')
            opcao_230 = request.form.get('opcao_230')
            opcao_231 = request.form.get('opcao_231')
            opcao_232 = request.form.get('opcao_232')
            opcao_233 = request.form.get('opcao_233')
            opcao_234 = request.form.get('opcao_234')
            opcao_235 = request.form.get('opcao_235')
            opcao_236 = request.form.get('opcao_236')
            opcao_237 = request.form.get('opcao_237')
            opcao_238 = request.form.get('opcao_238')
            opcao_239 = request.form.get('opcao_239')
            opcao_240 = request.form.get('opcao_240')
            opcao_241 = request.form.get('opcao_241')
            opcao_242 = request.form.get('opcao_242')
            opcao_243 = request.form.get('opcao_243')
            opcao_244 = request.form.get('opcao_244')

            cp_turma = CP_Turma.query.filter_by(turma=turma_selecionado_cp_turma.turma).first()

            if cp_turma:
                cp_turma.opcao_201 = opcao_201
                cp_turma.opcao_202 = opcao_202
                cp_turma.opcao_203 = opcao_203
                cp_turma.opcao_204 = opcao_204
                cp_turma.opcao_205 = opcao_205
                cp_turma.opcao_206 = opcao_206
                cp_turma.opcao_207 = opcao_207
                cp_turma.opcao_208 = opcao_208
                cp_turma.opcao_209 = opcao_209
                cp_turma.opcao_210 = opcao_210
                cp_turma.opcao_211 = opcao_211
                cp_turma.opcao_212 = opcao_212
                cp_turma.opcao_213 = opcao_213
                cp_turma.opcao_214 = opcao_214
                cp_turma.opcao_215 = opcao_215
                cp_turma.opcao_216 = opcao_216
                cp_turma.opcao_217 = opcao_217
                cp_turma.opcao_218 = opcao_218
                cp_turma.opcao_219 = opcao_219
                cp_turma.opcao_220 = opcao_220
                cp_turma.opcao_221 = opcao_221
                cp_turma.opcao_222 = opcao_222
                cp_turma.opcao_223 = opcao_223
                cp_turma.opcao_224 = opcao_224
                cp_turma.opcao_225 = opcao_225
                cp_turma.opcao_226 = opcao_226
                cp_turma.opcao_227 = opcao_227
                cp_turma.opcao_228 = opcao_228
                cp_turma.opcao_229 = opcao_229
                cp_turma.opcao_230 = opcao_230
                cp_turma.opcao_231 = opcao_231
                cp_turma.opcao_232 = opcao_232
                cp_turma.opcao_233 = opcao_233
                cp_turma.opcao_234 = opcao_234
                cp_turma.opcao_235 = opcao_235
                cp_turma.opcao_236 = opcao_236
                cp_turma.opcao_237 = opcao_237
                cp_turma.opcao_238 = opcao_238
                cp_turma.opcao_239 = opcao_239
                cp_turma.opcao_240 = opcao_240
                cp_turma.opcao_241 = opcao_241
                cp_turma.opcao_242 = opcao_242
                cp_turma.opcao_243 = opcao_243
                cp_turma.opcao_244 = opcao_244
                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/avaliacao%turma%perguntasabertas')
            else:
                flash('Erro!', 'alert-danger')
                return redirect('/avaliacao%turma')

    return render_template('avaliacao_turma_avalieprofessor.html', professoresquery=professoresquery)


@app.route('/avaliacao%turma%perguntasabertas', methods=['GET', 'POST'])
@login_required
def avaliacao_turma_perguntasabertas():
    turma_id_cp = session.get('turma_id_cp')
    turma_selecionado_cp_turma = Turma.query.get(turma_id_cp)
    if turma_selecionado_cp_turma:
        if request.method == 'POST':
            resposta301 = request.form.get('resposta301')
            resposta302 = request.form.get('resposta302')
            resposta303 = request.form.get('resposta303')
            resposta304 = request.form.get('resposta304')
            resposta305 = request.form.get('resposta305')
            resposta306 = request.form.get('resposta306')

            cp_turma = CP_Turma.query.filter_by(turma=turma_selecionado_cp_turma.turma).first()

            if cp_turma:
                cp_turma.resposta301 = resposta301
                cp_turma.resposta302 = resposta302
                cp_turma.resposta303 = resposta303
                cp_turma.resposta304 = resposta304
                cp_turma.resposta305 = resposta305
                cp_turma.resposta306 = resposta306

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/avaliacao%turma%recomendacoes')
            else:
                flash('Erro!', 'alert-danger')
                return redirect('/avaliacao%turma')
    return render_template('avaliacao_turma_perguntasabertas.html')


@app.route('/avaliacao%turma%recomendacoes', methods=['GET', 'POST'])
@login_required
def avaliacao_turma_recomendacoes():
    turma_id_cp = session.get('turma_id_cp')
    turma_selecionado_cp_turma = Turma.query.get(turma_id_cp)
    if turma_selecionado_cp_turma:
        if request.method == 'POST':
            item401 = request.form.get('item401')
            item402 = request.form.get('item402')
            item403 = request.form.get('item403')
            item404 = request.form.get('item404')
            item405 = request.form.get('item405')
            item406 = request.form.get('item406')
            item407 = request.form.get('item407')
            item408 = request.form.get('item408')
            item409 = request.form.get('item409')

            cp_turma = CP_Turma.query.filter_by(turma=turma_selecionado_cp_turma.turma).first()

            if cp_turma:
                cp_turma.item401 = item401
                cp_turma.item402 = item402
                cp_turma.item403 = item403
                cp_turma.item404 = item404
                cp_turma.item405 = item405
                cp_turma.item406 = item406
                cp_turma.item407 = item407
                cp_turma.item408 = item408
                cp_turma.item409 = item409

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/avaliacao%turma%autoavaliacao')
            else:
                flash('Erro!', 'alert-danger')
                return redirect('/avaliacao%turma')

    return render_template('avaliacao_turma_recomendacoes.html')


@app.route('/avaliacao%turma%autoavaliacao', methods=['GET', 'POST'])
@login_required
def avaliacao_turma_autoavaliacao():
    turma_id_cp = session.get('turma_id_cp')
    turma_selecionado_cp_turma = Turma.query.get(turma_id_cp)
    if turma_selecionado_cp_turma:
        if request.method == 'POST':
            opcao_501 = request.form.get('opcao_501')
            opcao_502 = request.form.get('opcao_502')
            opcao_503 = request.form.get('opcao_503')
            opcao_504 = request.form.get('opcao_504')
            opcao_505 = request.form.get('opcao_505')
            opcao_506 = request.form.get('opcao_506')
            opcao_507 = request.form.get('opcao_507')
            opcao_508 = request.form.get('opcao_508')
            opcao_509 = request.form.get('opcao_509')
            opcao_510 = request.form.get('opcao_510')
            opcao_511 = request.form.get('opcao_511')
            opcao_512 = request.form.get('opcao_512')
            opcao_513 = request.form.get('opcao_513')
            opcao_514 = request.form.get('opcao_514')
            opcao_515 = request.form.get('opcao_515')
            opcao_516 = request.form.get('opcao_516')
            opcao_517 = request.form.get('opcao_517')
            opcao_518 = request.form.get('opcao_518')
            opcao_519 = request.form.get('opcao_519')
            opcao_520 = request.form.get('opcao_520')
            opcao_521 = request.form.get('opcao_521')
            opcao_522 = request.form.get('opcao_522')
            opcao_523 = request.form.get('opcao_523')
            opcao_524 = request.form.get('opcao_524')
            opcao_525 = request.form.get('opcao_525')
            opcao_526 = request.form.get('opcao_526')
            opcao_527 = request.form.get('opcao_527')
            opcao_528 = request.form.get('opcao_528')
            opcao_529 = request.form.get('opcao_529')
            opcao_530 = request.form.get('opcao_530')
            opcao_531 = request.form.get('opcao_531')
            opcao_532 = request.form.get('opcao_532')
            opcao_533 = request.form.get('opcao_533')
            opcao_534 = request.form.get('opcao_534')
            opcao_535 = request.form.get('opcao_535')
            opcao_536 = request.form.get('opcao_536')
            opcao_537 = request.form.get('opcao_537')
            opcao_538 = request.form.get('opcao_538')
            opcao_539 = request.form.get('opcao_539')
            opcao_540 = request.form.get('opcao_540')
            opcao_541 = request.form.get('opcao_541')
            opcao_542 = request.form.get('opcao_542')
            opcao_543 = request.form.get('opcao_543')
            opcao_544 = request.form.get('opcao_544')

            cp_turma = CP_Turma.query.filter_by(turma=turma_selecionado_cp_turma.turma).first()

            if cp_turma:
                cp_turma.opcao_501 = opcao_501
                cp_turma.opcao_502 = opcao_502
                cp_turma.opcao_503 = opcao_503
                cp_turma.opcao_504 = opcao_504
                cp_turma.opcao_505 = opcao_505
                cp_turma.opcao_506 = opcao_506
                cp_turma.opcao_507 = opcao_507
                cp_turma.opcao_508 = opcao_508
                cp_turma.opcao_509 = opcao_509
                cp_turma.opcao_510 = opcao_510
                cp_turma.opcao_511 = opcao_511
                cp_turma.opcao_512 = opcao_512
                cp_turma.opcao_513 = opcao_513
                cp_turma.opcao_514 = opcao_514
                cp_turma.opcao_515 = opcao_515
                cp_turma.opcao_516 = opcao_516
                cp_turma.opcao_517 = opcao_517
                cp_turma.opcao_518 = opcao_518
                cp_turma.opcao_519 = opcao_519
                cp_turma.opcao_520 = opcao_520
                cp_turma.opcao_521 = opcao_521
                cp_turma.opcao_522 = opcao_522
                cp_turma.opcao_523 = opcao_523
                cp_turma.opcao_524 = opcao_524
                cp_turma.opcao_525 = opcao_525
                cp_turma.opcao_526 = opcao_526
                cp_turma.opcao_527 = opcao_527
                cp_turma.opcao_528 = opcao_528
                cp_turma.opcao_529 = opcao_529
                cp_turma.opcao_530 = opcao_530
                cp_turma.opcao_531 = opcao_531
                cp_turma.opcao_532 = opcao_532
                cp_turma.opcao_533 = opcao_533
                cp_turma.opcao_534 = opcao_534
                cp_turma.opcao_535 = opcao_535
                cp_turma.opcao_536 = opcao_536
                cp_turma.opcao_537 = opcao_537
                cp_turma.opcao_538 = opcao_538
                cp_turma.opcao_539 = opcao_539
                cp_turma.opcao_540 = opcao_540
                cp_turma.opcao_541 = opcao_541
                cp_turma.opcao_542 = opcao_542
                cp_turma.opcao_543 = opcao_543
                cp_turma.opcao_544 = opcao_544

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/avaliacao%turma%consideracoesfinais')
            else:
                flash('Erro!', 'alert-danger')
                return redirect('/avaliacao%turma')

    return render_template('avaliacao_turma_autoavaliacao.html')


@app.route('/avaliacao%turma%consideracoesfinais', methods=['GET', 'POST'])
@login_required
def avaliacao_turma_consideracoesfinais():
    turma_id_cp = session.get('turma_id_cp')
    turma_selecionado_cp_turma = Turma.query.get(turma_id_cp)
    if turma_selecionado_cp_turma:
        if request.method == 'POST':
            consideracoes_finais = request.form.get('consideracoes_finais')

            cp_turma = CP_Turma.query.filter_by(turma=turma_selecionado_cp_turma.turma).first()

            if cp_turma:
                cp_turma.consideracoes_finais = consideracoes_finais

                database.session.commit()
                flash('Continue o Formulário', 'alert-success')
                return redirect('/avaliacao%turma')
            else:
                flash('Erro!', 'alert-danger')
                return redirect('/avaliacao%turma')
    return render_template('avaliacao_turma_consideracoesfinais.html')


@app.route('/import/professores', methods=['GET', 'POST'])
@login_required
def importar_professores():
    professores_file = request.files.get('file')
    if professores_file:
        filename, file_extension = os.path.splitext(professores_file.filename)
        if file_extension.lower() == '.txt':
            file_path = os.path.join(UPLOAD_FOLDER, professores_file.filename)
            professores_file.save(file_path)
            importar_professores_from_file(file_path)
            return redirect('/avaliacao%turma')
        else:
            flash('Apenas (.txt) são permitidos!', 'alert-danger')
    return render_template('professores_importar.html')


def importar_professores_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith('.csv'):
            reader = csv.reader(file)
            professores = [row for row in reader if len(row) == 2]
        else:
            lines = file.readlines()
            professores = [line.strip().split(';') for line in lines if len(line.strip().split(';')) == 2]

        for professor, unidade in professores:
            # Verificar se o professor já existe no banco de dados antes de adicioná-lo
            existing_professor = Professor.query.filter_by(professor=professor).first()
            if existing_professor is None:
                prof = Professor(
                    professor=professor,
                    unidade=unidade
                )
                database.session.add(prof)  # Assuming `database.session` is properly configured
        database.session.commit()


######################################################################

@app.route('/planejamento', methods=['GET', 'POST'])
@login_required
def planejamento():
    turmaquery = Turma.query.order_by(func.lower(Turma.turma)).all()
    if request.method == 'POST':
        serie = request.form.get('serie')
        bimestre = request.form.get('bimestre')
        componentes = request.form.get('componentes')
        conteudo = request.form.get('conteudo')
        objetivo = request.form.get('objetivo')
        estrategias = request.form.get('estrategias')
        recursos = request.form.get('recursos')
        metas_gerais_para_turma = request.form.get('metas_gerais_para_turma')
        aula = request.form.get('aula')
        data = request.form.get('data')
        habilidade = request.form.get('habilidade')

        serie_selecionada_planejamento = Turma.query.filter_by(serie=serie).first()

        existing_plano_pcd = Plano_PcD.query.filter_by(
            bimestre=bimestre,
            data=data
        ).first()

        if existing_plano_pcd:
            flash('Aluno já Existente no banco de dados.', 'alert-danger')

        if serie_selecionada_planejamento:
            planejamento_salvar = Planejamento(
                serie=serie_selecionada_planejamento.serie,
                bimestre=bimestre,
                data=data
            )
            if componentes == "Português":
                planejamento_salvar.aula_port = aula
                planejamento_salvar.habilidade_port = habilidade
                planejamento_salvar.conteudo_port = conteudo
                planejamento_salvar.objetivo_port = objetivo
                planejamento_salvar.estrategias_port = estrategias
                planejamento_salvar.recursos_port = recursos
                planejamento_salvar.metas_gerais_para_turma_port = metas_gerais_para_turma

            if componentes == "Artes":
                planejamento_salvar.aula_arte = aula
                planejamento_salvar.habilidade_arte = habilidade
                planejamento_salvar.conteudo_arte = conteudo
                planejamento_salvar.objetivo_arte = objetivo
                planejamento_salvar.estrategias_arte = estrategias
                planejamento_salvar.recursos_arte = recursos
                planejamento_salvar.metas_gerais_para_turma_arte = metas_gerais_para_turma

            if componentes == "Matemática":
                planejamento_salvar.aula_mate = aula
                planejamento_salvar.habilidade_mate = habilidade
                planejamento_salvar.conteudo_mate = conteudo
                planejamento_salvar.objetivo_mate = objetivo
                planejamento_salvar.estrategias_mate = estrategias
                planejamento_salvar.recursos_mate = recursos
                planejamento_salvar.metas_gerais_para_turma_mate = metas_gerais_para_turma

            if componentes == "Geografia":
                planejamento_salvar.aula_geog = aula
                planejamento_salvar.habilidade_geog = habilidade
                planejamento_salvar.conteudo_geog = conteudo
                planejamento_salvar.objetivo_geog = objetivo
                planejamento_salvar.estrategias_geog = estrategias
                planejamento_salvar.recursos_geog = recursos
                planejamento_salvar.metas_gerais_para_turma_geog = metas_gerais_para_turma

            if componentes == "História":
                planejamento_salvar.aula_hist = aula
                planejamento_salvar.habilidade_hist = habilidade
                planejamento_salvar.conteudo_hist = conteudo
                planejamento_salvar.objetivo_hist = objetivo
                planejamento_salvar.estrategias_hist = estrategias
                planejamento_salvar.recursos_hist = recursos
                planejamento_salvar.metas_gerais_para_turma_hist = metas_gerais_para_turma

            if componentes == "Ed.Física":
                planejamento_salvar.aula_edfi = aula
                planejamento_salvar.habilidade_edfi = habilidade
                planejamento_salvar.conteudo_edfi = conteudo
                planejamento_salvar.objetivo_edfi = objetivo
                planejamento_salvar.estrategias_edfi = estrategias
                planejamento_salvar.recursos_edfi = recursos
                planejamento_salvar.metas_gerais_para_turma_edfi = metas_gerais_para_turma

            if componentes == "Física":
                planejamento_salvar.aula_fisc = aula
                planejamento_salvar.habilidade_fisc = habilidade
                planejamento_salvar.conteudo_fisc = conteudo
                planejamento_salvar.objetivo_fisc = objetivo
                planejamento_salvar.estrategias_fisc = estrategias
                planejamento_salvar.recursos_fisc = recursos
                planejamento_salvar.metas_gerais_para_turma_fisc = metas_gerais_para_turma

            if componentes == "Química":
                planejamento_salvar.aula_quim = aula
                planejamento_salvar.habilidade_quim = habilidade
                planejamento_salvar.conteudo_quim = conteudo
                planejamento_salvar.objetivo_quim = objetivo
                planejamento_salvar.estrategias_quim = estrategias
                planejamento_salvar.recursos_quim = recursos
                planejamento_salvar.metas_gerais_para_turma_quim = metas_gerais_para_turma

            if componentes == "Língua Inlgesa":
                planejamento_salvar.aula_ling = aula
                planejamento_salvar.habilidade_ling = habilidade
                planejamento_salvar.conteudo_ling = conteudo
                planejamento_salvar.objetivo_ling = objetivo
                planejamento_salvar.estrategias_ling = estrategias
                planejamento_salvar.recursos_ling = recursos
                planejamento_salvar.metas_gerais_para_turma_ling = metas_gerais_para_turma

            if componentes == "Religião":
                planejamento_salvar.aula_reli = aula
                planejamento_salvar.habilidade_reli = habilidade
                planejamento_salvar.conteudo_reli = conteudo
                planejamento_salvar.objetivo_reli = objetivo
                planejamento_salvar.estrategias_reli = estrategias
                planejamento_salvar.recursos_reli = recursos
                planejamento_salvar.metas_gerais_para_turma_reli = metas_gerais_para_turma

            if componentes == "Redação":
                planejamento_salvar.aula_reda = aula
                planejamento_salvar.habilidade_reda = habilidade
                planejamento_salvar.conteudo_reda = conteudo
                planejamento_salvar.objetivo_reda = objetivo
                planejamento_salvar.estrategias_reda = estrategias
                planejamento_salvar.recursos_reda = recursos
                planejamento_salvar.metas_gerais_para_turma_reda = metas_gerais_para_turma

            if componentes == "Espanhol":
                planejamento_salvar.aula_espa = aula
                planejamento_salvar.habilidade_espa = habilidade
                planejamento_salvar.conteudo_espa = conteudo
                planejamento_salvar.objetivo_espa = objetivo
                planejamento_salvar.estrategias_espa = estrategias
                planejamento_salvar.recursos_espa = recursos
                planejamento_salvar.metas_gerais_para_turma_espa = metas_gerais_para_turma

            if componentes == "Ciências":
                planejamento_salvar.aula_cien = aula
                planejamento_salvar.habilidade_cien = habilidade
                planejamento_salvar.conteudo_cien = conteudo
                planejamento_salvar.objetivo_cien = objetivo
                planejamento_salvar.estrategias_cien = estrategias
                planejamento_salvar.recursos_cien = recursos
                planejamento_salvar.metas_gerais_para_turma_cien = metas_gerais_para_turma

            database.session.add(planejamento_salvar)
            database.session.commit()
            flash('Formulário Salvo com Sucesso.', 'alert-success')
        else:
            flash('Error.', 'alert-danger')
    return render_template('planejamento.html', turmaquery=turmaquery)


@app.route('/planejamento/pesquisa')
@login_required
def planejamento_pesquisa():
    planejamentoquery = Planejamento.query.order_by(func.lower(Planejamento.serie)).all()
    return render_template('planejamento_pesquisa.html', planejamentoquery=planejamentoquery)


######################################################################

@app.route('/planoPCD', methods=['GET', 'POST'])
@login_required
def plano_pcd():
    nome_alunoquery = Alunos.query.order_by(func.lower(Alunos.aluno_nome)).all()

    if request.method == 'POST':
        aluno_nome = request.form.get('aluno_nome')
        bimestre = request.form.get('bimestre')
        componentes = request.form.get('componentes')
        aula = request.form.get('aula')
        data = request.form.get('data')
        habilidade = request.form.get('habilidade')
        conteudo = request.form.get('conteudo')
        objetivo = request.form.get('objetivo')
        estrategias = request.form.get('estrategias')
        recursos = request.form.get('recursos')
        metas_gerais_para_turma = request.form.get('metas_gerais_para_turma')
        aluno_selecionado_plano_pcd = Alunos.query.filter_by(aluno_nome=aluno_nome).first()

        existing_plano_pcd = Plano_PcD.query.filter_by(
            aluno_nome=aluno_nome,
            bimestre=bimestre,
            data=data
        ).first()

        if existing_plano_pcd:
            flash('Aluno já Existente no banco de dados.', 'alert-danger')

        if aluno_selecionado_plano_pcd:
            plano_pcd_salvar = Plano_PcD(
                aluno_nome=aluno_selecionado_plano_pcd.aluno_nome,
                aluno_codigo=aluno_selecionado_plano_pcd.aluno_codigo,
                bimestre=bimestre,
                data=data,
            )

            # Check the selected component and update the corresponding columns
            if componentes == "Portugues":
                plano_pcd_salvar.aula_port = aula
                plano_pcd_salvar.habilidade_port = habilidade
                plano_pcd_salvar.conteudo_port = conteudo
                plano_pcd_salvar.objetivo_port = objetivo
                plano_pcd_salvar.estrategias_port = estrategias
                plano_pcd_salvar.recursos_port = recursos
                plano_pcd_salvar.metas_gerais_para_turma_port = metas_gerais_para_turma

            if componentes == "Artes":
                plano_pcd_salvar.aula_arte = aula
                plano_pcd_salvar.habilidade_arte = habilidade
                plano_pcd_salvar.conteudo_arte = conteudo
                plano_pcd_salvar.objetivo_arte = objetivo
                plano_pcd_salvar.estrategias_arte = estrategias
                plano_pcd_salvar.recursos_arte = recursos
                plano_pcd_salvar.metas_gerais_para_turma_arte = metas_gerais_para_turma

            if componentes == "Matematica":
                plano_pcd_salvar.aula_mate = aula
                plano_pcd_salvar.habilidade_mate = habilidade
                plano_pcd_salvar.conteudo_mate = conteudo
                plano_pcd_salvar.objetivo_mate = objetivo
                plano_pcd_salvar.estrategias_mate = estrategias
                plano_pcd_salvar.recursos_mate = recursos
                plano_pcd_salvar.metas_gerais_para_turma_mate = metas_gerais_para_turma

            if componentes == "Geografia":
                plano_pcd_salvar.aula_geog = aula
                plano_pcd_salvar.habilidade_geog = habilidade
                plano_pcd_salvar.conteudo_geog = conteudo
                plano_pcd_salvar.objetivo_geog = objetivo
                plano_pcd_salvar.estrategias_geog = estrategias
                plano_pcd_salvar.recursos_geog = recursos
                plano_pcd_salvar.metas_gerais_para_turma_geog = metas_gerais_para_turma

            if componentes == "Historia":
                plano_pcd_salvar.aula_hist = aula
                plano_pcd_salvar.habilidade_hist = habilidade
                plano_pcd_salvar.conteudo_hist = conteudo
                plano_pcd_salvar.objetivo_hist = objetivo
                plano_pcd_salvar.estrategias_hist = estrategias
                plano_pcd_salvar.recursos_hist = recursos
                plano_pcd_salvar.metas_gerais_para_turma_hist = metas_gerais_para_turma

            if componentes == "EdFisica":
                plano_pcd_salvar.aula_edfi = aula
                plano_pcd_salvar.habilidade_edfi = habilidade
                plano_pcd_salvar.conteudo_edfi = conteudo
                plano_pcd_salvar.objetivo_edfi = objetivo
                plano_pcd_salvar.estrategias_edfi = estrategias
                plano_pcd_salvar.recursos_edfi = recursos
                plano_pcd_salvar.metas_gerais_para_turma_edfi = metas_gerais_para_turma

            if componentes == "Fisica":
                plano_pcd_salvar.aula_fisc = aula
                plano_pcd_salvar.habilidade_fisc = habilidade
                plano_pcd_salvar.conteudo_fisc = conteudo
                plano_pcd_salvar.objetivo_fisc = objetivo
                plano_pcd_salvar.estrategias_fisc = estrategias
                plano_pcd_salvar.recursos_fisc = recursos
                plano_pcd_salvar.metas_gerais_para_turma_fisc = metas_gerais_para_turma

            if componentes == "Quimica":
                plano_pcd_salvar.aula_quim = aula
                plano_pcd_salvar.habilidade_quim = habilidade
                plano_pcd_salvar.conteudo_quim = conteudo
                plano_pcd_salvar.objetivo_quim = objetivo
                plano_pcd_salvar.estrategias_quim = estrategias
                plano_pcd_salvar.recursos_quim = recursos
                plano_pcd_salvar.metas_gerais_para_turma_quim = metas_gerais_para_turma

            if componentes == "LinguaInglesa":
                plano_pcd_salvar.aula_ling = aula
                plano_pcd_salvar.habilidade_ling = habilidade
                plano_pcd_salvar.conteudo_ling = conteudo
                plano_pcd_salvar.objetivo_ling = objetivo
                plano_pcd_salvar.estrategias_ling = estrategias
                plano_pcd_salvar.recursos_ling = recursos
                plano_pcd_salvar.metas_gerais_para_turma_ling = metas_gerais_para_turma

            if componentes == "Religiao":
                plano_pcd_salvar.aula_reli = aula
                plano_pcd_salvar.habilidade_reli = habilidade
                plano_pcd_salvar.conteudo_reli = conteudo
                plano_pcd_salvar.objetivo_reli = objetivo
                plano_pcd_salvar.estrategias_reli = estrategias
                plano_pcd_salvar.recursos_reli = recursos
                plano_pcd_salvar.metas_gerais_para_turma_reli = metas_gerais_para_turma

            if componentes == "Redacao":
                plano_pcd_salvar.aula_reda = aula
                plano_pcd_salvar.habilidade_reda = habilidade
                plano_pcd_salvar.conteudo_reda = conteudo
                plano_pcd_salvar.objetivo_reda = objetivo
                plano_pcd_salvar.estrategias_reda = estrategias
                plano_pcd_salvar.recursos_reda = recursos
                plano_pcd_salvar.metas_gerais_para_turma_reda = metas_gerais_para_turma

            if componentes == "Espanhol":
                plano_pcd_salvar.aula_espa = aula
                plano_pcd_salvar.habilidade_espa = habilidade
                plano_pcd_salvar.conteudo_espa = conteudo
                plano_pcd_salvar.objetivo_espa = objetivo
                plano_pcd_salvar.estrategias_espa = estrategias
                plano_pcd_salvar.recursos_espa = recursos
                plano_pcd_salvar.metas_gerais_para_turma_espa = metas_gerais_para_turma

            if componentes == "Ciencias":
                plano_pcd_salvar.aula_cien = aula
                plano_pcd_salvar.habilidade_cien = habilidade
                plano_pcd_salvar.conteudo_cien = conteudo
                plano_pcd_salvar.objetivo_cien = objetivo
                plano_pcd_salvar.estrategias_cien = estrategias
                plano_pcd_salvar.recursos_cien = recursos
                plano_pcd_salvar.metas_gerais_para_turma_cien = metas_gerais_para_turma

            database.session.add(plano_pcd_salvar)
            database.session.commit()
            flash('Formulário Salvo com Sucesso.', 'alert-success')
        else:
            flash('Error.', 'alert-danger')
    return render_template('plano_pcd.html', nome_alunoquery=nome_alunoquery)


@app.route('/planoPCD/pesquisa')
@login_required
def plano_pcd_pesquisa():
    planopcdquery = Plano_PcD.query.order_by(func.lower(Plano_PcD.aluno_nome)).all()
    return render_template('plano_pcd_pesquisa.html', planopcdquery=planopcdquery)


######################################################################

@app.route('/sondagem')
@login_required
def sondagem():
    return render_template('sondagem.html')


######################################################################

@app.route('/recuperacao/simultanea', methods=['GET', 'POST'])
@login_required
def recuperacao_simultanea():
    recuperacaosimultanea = Recuperacao_Simultanea.query.all()
    # Recupere os valores armazenados nas sessões
    turma_selecionada_recuperacao = session.get('turma_selecionada_recuperacao')
    professor_selecionado_recuperacao = session.get('professor_selecionado_recuperacao')
    componente_selecionado_recuperacao = session.get('componente_selecionado_recuperacao')
    bimestre_selecionado_recuperacao = session.get('bimestre_selecionado_recuperacao')
    ano_letivo_selecionado_recuperacao = session.get('ano_letivo_selecionado_recuperacao')
    turno_selecionado_recuperacao = session.get('turno_selecionado_recuperacao')

    conteudo = ""

    if request.method == 'POST':
        # Verifique se o campo "conteudo" está preenchido
        conteudo = request.form.get('conteudo_edit')
        if not conteudo:
            flash('O campo "conteudo" deve ser preenchido.', 'alert-danger')
        else:
            # Verifique se já existe um registro com os mesmos valores
            existing_record = Recuperacao_Simultanea.query.filter(
                and_(
                    Recuperacao_Simultanea.turma == turma_selecionada_recuperacao,
                    Recuperacao_Simultanea.componente == componente_selecionado_recuperacao,
                    Recuperacao_Simultanea.bimestre == bimestre_selecionado_recuperacao,
                    Recuperacao_Simultanea.ano_letivo == ano_letivo_selecionado_recuperacao
                )
            ).first()

            if existing_record:
                flash('Já existe um registro com os mesmos valores na tabela.', 'alert-danger')
            else:
                # Crie uma instância do modelo Recuperacao_Simultanea com os valores do formulário
                recuperacao_simultanea = Recuperacao_Simultanea(
                    turma=turma_selecionada_recuperacao,
                    professor=professor_selecionado_recuperacao,
                    componente=componente_selecionado_recuperacao,
                    bimestre=bimestre_selecionado_recuperacao,
                    ano_letivo=ano_letivo_selecionado_recuperacao,
                    turno=turno_selecionado_recuperacao,
                    conteudo=conteudo
                )

                session['recuperacao_simultanea_id'] = recuperacao_simultanea.id
                session['conteudo_antigo'] = conteudo

                # Adicione a instância ao banco de dados
                database.session.add(recuperacao_simultanea)

                # Commit as mudanças no banco de dados para salvar o conteúdo atualizado ou o novo registro
                database.session.commit()

                flash('Dados salvos com sucesso.', 'alert-success')
                return redirect('/recuperacao/simultanea')

    return render_template('recuperacao_simultanea.html',
                           turma_selecionada_recuperacao=turma_selecionada_recuperacao,
                           professor_selecionado_recuperacao=professor_selecionado_recuperacao,
                           componente_selecionado_recuperacao=componente_selecionado_recuperacao,
                           bimestre_selecionado_recuperacao=bimestre_selecionado_recuperacao,
                           ano_letivo_selecionado_recuperacao=ano_letivo_selecionado_recuperacao,
                           turno_selecionado_recuperacao=turno_selecionado_recuperacao,
                           recuperacaosimultanea=recuperacaosimultanea,
                           conteudo=conteudo)


@app.route('/recuperacao/simultanea/editar', methods=['GET', 'POST'])
@login_required
def recuperacao_simultanea_editar():
    recuperacao_simultanea_id = session.get('recuperacao_simultanea_id')
    conteudo_antigo = session.get('conteudo_antigo')

    turma_selecionada_recuperacao_simu = Recuperacao_Simultanea.query.get(recuperacao_simultanea_id)
    if turma_selecionada_recuperacao_simu:
        if request.method == 'POST':
            conteudo_editado = request.form.get('conteudo_editado')
            recuperacaosimultanea = Recuperacao_Simultanea.query.filter_by(
                turma=turma_selecionada_recuperacao_simu.turma).first()
            if recuperacaosimultanea:
                recuperacaosimultanea.conteudo = conteudo_editado
                database.session.commit()
                flash('Editado com Sucesso', 'alert-success')
                return redirect("/recuperacao/simultanea")
            else:
                flash('Erro ao Editar.', 'alert-danger')
        else:
            flash('Erro ao tentar selecionar uma turma para editar seu conteúdo', 'alert-danger')
            return redirect('/recuperacao/simultanea')

    return render_template('recuperacao_simultanea_editar.html', conteudo_antigo=conteudo_antigo,
                           turma_selecionada_recuperacao_simu=turma_selecionada_recuperacao_simu)


@app.route('/recuperacao/simultanea/proposicao')
@login_required
def recuperacao_simultanea_proposicao():
    recuperacaosimultanea = Recuperacao_Simultanea.query.all()
    return render_template('recuperacao_simultanea_proposicao.html', recuperacaosimultanea=recuperacaosimultanea)


@app.route('/recuperacao/simultanea/filtro', methods=['GET', 'POST'])
@login_required
def recuperacao_simultanea_filtro():
    turmaquery = Turma.query.order_by(func.lower(Turma.turma)).all()
    profquery = Professor.query.order_by(func.lower(Professor.professor)).all()
    if request.method == 'POST':
        turma = request.form.get('Turma')
        professor = request.form.get('Professor')
        componentes = request.form.get('Componentes')
        bimestre = request.form.get('Bimestre')
        ano_letivo = request.form.get('Ano_Letivo')
        turno = request.form.get('Turno')

        turma_selecionada_recuperacao = Turma.query.filter_by(turma=turma).first()
        if turma_selecionada_recuperacao:
            # Armazene os valores selecionados nas sessões
            session['turma_selecionada_recuperacao'] = turma_selecionada_recuperacao.turma
            session['professor_selecionado_recuperacao'] = professor
            session['componente_selecionado_recuperacao'] = componentes
            session['bimestre_selecionado_recuperacao'] = bimestre
            session['ano_letivo_selecionado_recuperacao'] = ano_letivo
            session['turno_selecionado_recuperacao'] = turno

            flash('Continue o Registro.', 'alert-success')
            return redirect('/recuperacao/simultanea')
    return render_template('recuperacao_simultanea_filtro.html', turmaquery=turmaquery, profquery=profquery)


######################################################################

@app.route('/controle%da%p3')
@login_required
def controle_da_p3():
    alunoquery = Alunos.query.order_by(func.lower(Alunos.matricula_turma)).all()
    resultadoquery = Resultado_dos_Alunos.query.all()
    return render_template('controle_da_p3.html', alunoquery=alunoquery, resultadoquery=resultadoquery)


######################################################################

def pagina_nao_encontrada(error):
    render_template('errors/404.html'), 404
