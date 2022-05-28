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
                usuario_atual += usuario
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


# sg.theme_previewer()
# Creating the layout

def janelaLogin():
    sg.theme('LightTeal')
    janela_login = [
        #[sg.Column([[my_img]], justification='center')],
        [sg.Column([[sg.Image('Imagens/Logo.png')]], justification='center')],
        [sg.Text('Usuário')],
        [sg.Input(key='usuario')],
        [sg.Text('Senha')],
        [sg.Input(key='senha')],
        [sg.Button('login')],
        [sg.Text('', key='mensagem')],
    ]
    return sg.Window('Cardio Notes', resizable=True, size=(260, 450), layout=janela_login, finalize=True)


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


# Passing the layout to the janela_login
#janela_login = janelaLogin()
janela_login, janela_inicial = janelaLogin(), None

# Logic applied to the janela_login
while True:
    janela, event, values = sg.read_all_windows()
    if janela == janela_login and event == sg.WIN_CLOSED:
        usuario_atual = ''  # lógica para o logout
        break
    if janela == janela_login and event == 'login':
        usuario = str(values['usuario'])
        #senha = int(values['senha'])
        senha = values['senha']
        checarLogin(usuario, senha)
    if janela == janela_inicial and event == 'logout':
        usuario_atual = ''
        janela_inicial.hide()
        janela_login.un_hide()
    # if janela == janela_inicial and event == 'registro':
        # janelaRegistro()
    if janela == janela_inicial and event == sg.WIN_CLOSED:
        break
