import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
import bcrypt

# Caminho do arquivo de configuração
config_path = Path('config.yaml')

# Função para carregar o arquivo de configuração
def load_config(path):
    if path.exists():
        with open(path) as file:
            return yaml.load(file, Loader=SafeLoader)
    else:
        # Configuração padrão se o arquivo não existir
        return {
            'credentials': {'usernames': {}},
            'cookie': {'expiry_days': 30, 'key': 'some_signature_key', 'name': 'some_cookie_name'}
        }

# Função para salvar o arquivo de configuração
def save_config(path, config):
    with open(path, 'w') as file:
        yaml.dump(config, file)

# Função para criar hash da senha
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Carregar o arquivo de configuração
config = load_config(config_path)

# Criar uma instância do authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Verificar o status da autenticação
authentication_status = None

# Configurar a página inicial
if 'page' not in st.session_state:
    st.session_state.page = None

# Sidebar com opções de login e registro
st.sidebar.title('Autenticação')
choice = st.sidebar.selectbox('Escolha uma opção', ['Login', 'Registro'])

# Tela de Login
if choice == 'Login':
    name, authentication_status, username = authenticator.login('main', 'Login', fields=['Nome de usuário', 'Senha'])

    if authentication_status:
        st.sidebar.success(f'Bem-vindo, {name}')
        # Se o usuário estiver autenticado, definir a página como "dash"
        st.session_state.page = "dash"
        # Forçar a recarga da página para garantir que o estado da sessão seja limpo
        if authenticator.logout('Logout', 'sidebar'):
            st.session_state.page = None
            st.experimental_rerun()  # Recarregar a página para redefinir o estado da sessão
    elif authentication_status == False:
        st.error('Nome de usuário ou senha incorretos')
    elif authentication_status == None:
        st.warning('Por favor, insira seu nome de usuário e senha')

# Tela de Registro
elif choice == 'Registro':
    st.title('Registro de Novo Usuário')

    new_username = st.text_input('Nome de usuário')
    new_email = st.text_input('Email')
    new_name = st.text_input('Nome completo')
    new_password = st.text_input('Senha', type='password')
    confirm_password = st.text_input('Confirme a senha', type='password')

    if st.button('Registrar'):
        if new_password == confirm_password:
            hashed_password = hash_password(new_password)
            config['credentials']['usernames'][new_username] = {
                'email': new_email,
                'name': new_name,
                'password': hashed_password
            }
            save_config(config_path, config)
            st.success('Usuário registrado com sucesso!')
        else:
            st.error('As senhas não coincidem.')

# Mostrar o conteúdo da página com base no estado de sessão
if st.session_state.page == "dash":
    import dash  # Importar o módulo que contém a função show_dash
    dash.show_dash()  # Chamar a função show_dash para exibir o conteúdo
elif st.session_state.page is None:
    st.write('Por favor, faça login para acessar o conteúdo.')
else:
    st.write('Página não encontrada.')
