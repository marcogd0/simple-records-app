import PySimpleGUI as sg
import json
from datetime import datetime
import botoes

usuario_atual = ''

def checarLogin(usuario, senha):
    global janela_inicial
    with open(r'Accounts/accounts.txt', 'r') as arquivo:
        usuarios = arquivo.readline()
        print(usuarios)
        json_usuario = json.loads(usuarios)
        if usuario in json_usuario and json_usuario[usuario] == senha:
            janela_login.hide()
            #global janela_inicial
            janela_inicial = janelaInicial()
            print('Login bem sucedido')
            global usuario_atual
            usuario_atual = usuario
            janela_login['mensagem'].update('Successful login')
            return janela_inicial
        else:
            while usuarios != '':
                usuarios = arquivo.readline()
                if usuarios == '':
                    break
                json_usuario = json.loads(usuarios)
                if usuario == '' or str(senha) == '':
                    janela_login['mensagem'].update('Você deve fazer o acesso com um usuário e senha')
                elif usuario in json_usuario and json_usuario[usuario] == senha:
                    janela_login.hide()
                    #global janela_inicial
                    janela_inicial = janelaInicial()
                    print('Login bem sucedido')
                    #global usuario_atual
                    usuario_atual = usuario
                    print(usuario_atual)
                    janela_login['mensagem'].update('Successful login')
                    return janela_inicial
                elif usuario in json_usuario and json_usuario[usuario] != senha:
                    janela_login['mensagem'].update('Senha invalida')
                    print('Senha invalida')
                elif usuario not in json_usuario and senha in json_usuario.values():
                    janela_login['mensagem'].update('Usuário invalido')
                    print('Usuário invalido')
                elif usuario not in json_usuario and senha not in json_usuario.values():
                    janela_login['mensagem'].update('Usuário ou senha invalidos')
                    print('Usuário ou senha invalidos')

def realizarCadastro(nome, novousuario, novasenha):
    usuario = ''
    if nome == '' and novousuario == '' and novasenha == '':
        janela_cadastro['mensagem'].update('Preencha todos os campos')
    elif novousuario == '' and novasenha == '':
        janela_cadastro['mensagem'].update('"Usuário" e "Senha" vazios')
    elif nome == '' and novousuario == '':
        janela_cadastro['mensagem'].update('"Nome" e "Usuário" vazios')
    elif nome == '':
        janela_cadastro['mensagem'].update('Preencha o campo "Nome"')
    elif novousuario == '':
        janela_cadastro['mensagem'].update('Preencha o campo "Usuário"')
    elif novasenha == '':
        janela_cadastro['mensagem'].update('Preencha o campo "Senha"')
    else: # Verificando se o novousuario já está no arquivo
        arquivo = open(r'Accounts/accounts.txt', 'r')
        usuario = arquivo.readline()
        print(usuario)
        json_usuario = json.loads(usuario)
        print(json_usuario)
        if novousuario in json_usuario:
            janela_cadastro['mensagem'].update('Usuário já existente')
            arquivo.close()
            return
        else:
            while usuario != '':
                usuario = arquivo.readline()
                if usuario == '':
                    arquivo.close()
                    break
                # json.load() --> Converts json string into Python dictionary
                json_usuario = json.loads(usuario)
                if novousuario in json_usuario:
                    janela_cadastro['mensagem'].update('Usuário já existente')
                    arquivo.close()
                    return
        nova_conta = {novousuario: novasenha}
        #nova_conta[novousuario] = novasenha
        with open(r'Accounts/accounts.txt', 'a') as arquivo:
            # json.dumps() --> Converts Python dictionary into json string
            arquivo.write(f'{json.dumps(nova_conta)}' + '\n')
            janela_cadastro['mensagem'].update('Cadastro efetuado com sucesso!')

def janelaLogin():
    sg.theme('LightTeal')
    janela_login = [
        #[sg.Column([[my_img]], justification='center')],
        [sg.Column([[sg.Image('Imagens/Logo.png')]], justification='center')],
        [sg.Text('Usuário')],
        [sg.Input(key='usuario')],
        [sg.Text('Senha')],
        [sg.Input(key='senha', password_char='*')],
        [sg.Push(), sg.Button('login'), sg.Button('cadastro'), sg.Push()],
        [sg.Text('', key='mensagem')],
    ]
    return sg.Window('Cardio Notes', resizable=True, size=(260, 450), layout=janela_login, finalize=True)

def janelaCadastro():
    sg.theme('LightTeal')
    janela_cadastro = [
    [sg.Column([[sg.Image('Imagens/Logo.png')]], justification='center')],
    [sg.Push(), sg.Text('CADASTRO'), sg.Push()],
    [sg.Text('Nome completo*:')],
    [sg.In(key='nome')],
    [sg.Text('Usuário*:')],
    [sg.In(key='novo_usuario')],
    [sg.Text('Senha*:')],
    [sg.In(key='nova_senha', password_char='*')],
    [sg.Push(), sg.Button('Confirmar'), sg.Button('Cancelar'), sg.Push()],
    [sg.Text('', key='mensagem')],
    ]
    return sg.Window('Cadastro', resizable=True, size=(260, 450), layout=janela_cadastro, finalize=True)

def janelaInicial():
    sg.theme('LightTeal')
    interface = [
        [sg.Column([[sg.Image('Imagens/Logo 32x32.png')]], justification='left'), sg.Push(),
         sg.Column([[sg.Button('', image_data=botoes.botao_usuario, key='interface_usuario', button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)]])],
        [sg.VPush()],
        [sg.Column([[sg.Button('Fazer Registro', key='registro')]],
                   justification='center')],
        [sg.Column([[sg.Button('Mostrar Registros', key='mostra_registro')]],
                   justification='center')],
        [sg.Column([[sg.Button('Logout', key='logout')]],
                   justification='center')],
        [sg.VPush()],
    ]
    return sg.Window('Cardio Notes', resizable=True, size=(260, 450), layout=interface, finalize=True)

def janelaRegistro():
    sg.theme('LightTeal')
    layout_registro = [
        [sg.Text('Data do registro:')],
        [sg.In(key='-DATA-', size=(20,1)), sg.CalendarButton('', image_data=botoes.botao_calendario, button_color=(sg.theme_background_color(), sg.theme_background_color()),close_when_date_chosen=True, target='-DATA-', no_titlebar=False, format='%d-%m-%Y')], # # format='%d-%m-%Y %H:%M:%S'
        [sg.Text('Registro da consulta:')],
        [sg.Multiline(size=(30,8), key='-TEXTO_REGISTRO-')],
        [sg.Push(), sg.Button('Confirmar', key='-CONFIRMAR_REGISTRO-'), sg.Button('Cancelar', key='-CANCELAR_REGISTRO-'), sg.Push()]
    ]
    janela_registro = sg.Window('a', size=(260, 450), resizable=True, layout=layout_registro)
    return janela_registro

def janelaVerRegistros():
    sg.theme('LightTeal')
    janela_ver_registros = [
        [sg.Output(size=(30, 10), key='-OUTPUT-')]
    ]
    return sg.Window('Registros', size=(260, 450), layout=janela_ver_registros, finalize=True)


janela_login, janela_cadastro, janela_inicial, janela_registro, janela_ver_registros = janelaLogin(), None, None, None, None

# Logica aplicada nas janelas
while True:
    janela, event, values = sg.read_all_windows()
    if janela == janela_login and event == sg.WIN_CLOSED or janela == janela_cadastro and event == sg.WIN_CLOSED or janela == janela_inicial and event == sg.WIN_CLOSED or janela == janela_registro and event == sg.WIN_CLOSED or janela == janela_ver_registros and event == sg.WIN_CLOSED:
        usuario_atual = ''  # lógica para o logout
        break
    if janela == janela_login and event == 'login':
        usuario = str(values['usuario'])
        #senha = int(values['senha'])
        senha = values['senha']
        checarLogin(usuario, senha)
    if janela == janela_login and event == 'cadastro':
        janela_login.hide()
        janela_cadastro = janelaCadastro()
    if janela == janela_cadastro and event == 'Confirmar':
        nome = str(values['nome'])
        novo_usuario = str(values['novo_usuario'])
        nova_senha = str(values['nova_senha'])
        realizarCadastro(nome, novo_usuario, nova_senha)
    if janela == janela_cadastro and event =='Cancelar':
        janela_cadastro.hide()
        janela_login.un_hide()
    if janela == janela_inicial and event == 'registro':
        janela_inicial.hide()
        janela_registro = janelaRegistro()
        while True:
            event, values = janela_registro.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == '-CANCELAR_REGISTRO-':
                janela_inicial.un_hide()
                janela_registro.hide()
                break
            elif event == '-CONFIRMAR_REGISTRO-':
                data = values['-DATA-']
                registro = values['-TEXTO_REGISTRO-']
                registro_dict = {data:registro}
                with open('Registros/registros.txt', 'a') as arquivo:
                    arquivo.write(f'{usuario_atual} = {json.dumps(registro_dict)}' + '\n')
                janela_registro.hide()
                janela_inicial.un_hide()
                break
    if janela == janela_inicial and event == 'mostra_registro':
        janela_inicial.hide()
        janela_ver_registros = janelaVerRegistros()
        with open('Registros/registros.txt', 'r') as arquivo:
            linha = arquivo.readline()
            print(linha)
            n_registro = 1
            # ****************** NEEDS TO BE FIXED ***********************
            #if usuario_atual.lower() == linha[:len(usuario_atual)].lower():
            #    posicao = linha.find('=')
            #    dict_registro = json.loads(linha[posicao+2])
            #    print(type(dict_registro))
            #    #print(dict_registro.items())
            #    print('Registro ', n_registro)
            #    #print(dict_registro.keys())
            #    #print(dict_registro.values())
            #    print('=' * 30)
            #    n_registro += 1
            #else:
            #else:
            # ***************************************************************
            while linha != '':
                linha = arquivo.readline()
                posicao = linha.find('=')
                if linha == '':
                    break
                elif usuario_atual != linha[:posicao-1]:
                    continue
                elif usuario_atual == linha[:posicao-1]:
                    posicao = linha.find('=')
                    dict_registro = json.loads(linha[posicao+2:])
                    print(linha[:posicao-1])
                    #print(dict_registro.items())
                    for i, (key, value) in enumerate(dict_registro.items()):
                        print('Registro ', n_registro)
                        print(key)
                        print(value)
                    #print(dict_registro)
                    n_registro += 1
    if janela == janela_inicial and event == 'logout':
        janela_inicial.hide()
        janela_login.un_hide()