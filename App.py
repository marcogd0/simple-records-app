import PySimpleGUI as sg
import json
import botoes

usuario_atual = ''

def checarLogin(usuario, senha):
    with open(r'Accounts/accounts.txt', 'r') as arquivo:
        usuarios = arquivo.readlines()
        for i in usuarios:
            converted_i = json.loads(i)
            if usuario == '' or str(senha) == '':
                janela_login['mensagem'].update('Você deve fazer o acesso com um usuário e senha')
            elif usuario in converted_i and converted_i[usuario] == senha:
                janela_login.hide()
                global janela_inicial
                janela_inicial = janelaInicial()
                print('Login bem sucedido')
                global usuario_atual
                usuario_atual = usuario
                print(usuario_atual)
                janela_login['mensagem'].update('Successful login')
            elif usuario in converted_i and converted_i[usuario] != senha:
                janela_login['mensagem'].update('Senha invalida')
                print('Senha invalida')
            elif usuario not in converted_i and senha in converted_i.values():
                janela_login['mensagem'].update('Usuário invalido')
                print('Usuário invalido')
            elif usuario not in converted_i and senha not in converted_i.values():
                janela_login['mensagem'].update('Usuário ou senha invalidos')
                print('Usuário ou senha invalidos')

def checharCadastro(nome, novousuario, novasenha):
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
    else:
        arquivo = open(r'Accounts/accounts.txt', 'r')
        usuario = arquivo.readline()
        linha = arquivo.readline()
        print(usuario)
        for i in usuario: # trocar por while
            converted_i = json.loads(i)
            print(converted_i)
            if novousuario in converted_i:
                janela_cadastro['mensagem'].update('Usuário já existente')
            else:
                arquivo.close()
                nova_conta = {novousuario: novasenha}
                #nova_conta[novousuario] = novasenha
                with open(r'Accounts/accounts.txt', 'a') as arquivo:
                    arquivo.write(f'{nova_conta}' + '\n')

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

janela_login, janela_cadastro, janela_inicial = janelaLogin(), None, None

# Logica aplicada nas janelas
while True:
    janela, event, values = sg.read_all_windows()
    if janela == janela_login and event == sg.WIN_CLOSED or janela == janela_cadastro and event == sg.WIN_CLOSED or janela == janela_inicial and event == sg.WIN_CLOSED:
        usuario_atual = ''  # lógica para o logout
        break
    if janela == janela_login and event == 'login':
        usuario = str(values['usuario'])
        #senha = int(values['senha'])
        senha = values['senha']
        checarLogin(usuario, senha)
    if janela == janela_login and event == 'cadastro':
        janela_cadastro = janelaCadastro()
    if janela == janela_cadastro and event == 'Confirmar':
        nome = str(values['nome'])
        novo_usuario = str(values['novo_usuario'])
        nova_senha = str(values['nova_senha'])
        checharCadastro(nome, novo_usuario, nova_senha)
    if janela == janela_inicial and event == 'logout':
        janela_inicial.hide()
        janela_login.un_hide()
    # if janela == janela_inicial and event == 'registro':
        # janelaRegistro()
