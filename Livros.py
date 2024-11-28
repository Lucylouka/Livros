import streamlit as st
import os
import json

# Caminho dos arquivos de dados
DATA_FILE = 'livros.json'
FRIENDS_FILE = 'amigos.json'

# Função para carregar os livros existentes
def load_books():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Função para salvar os livros no arquivo
def save_books(books):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

# Inicializa o arquivo de livros se ele não existir
if not os.path.exists(DATA_FILE):
    save_books([])

# Função para carregar amigos existentes
def load_friends():
    if os.path.exists(FRIENDS_FILE):
        with open(FRIENDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Função para salvar amigos no arquivo
def save_friends(friends):
    with open(FRIENDS_FILE, "w", encoding="utf-8") as f:
        json.dump(friends, f, ensure_ascii=False, indent=4)

# Inicializa o arquivo de amigos se ele não existir
if not os.path.exists(FRIENDS_FILE):
    save_friends([])

# Função para definir a cor da avaliação
def get_avaliacao_color(avaliacao):
    if avaliacao <= 6:
        return "red"
    elif avaliacao <= 8:
        return "yellow"
    else:
        return "green"

# Navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio("Escolha uma página:", ["Adicionar Livro", "Livros Lidos", "Quero Ler", "Livros Favoritos", "Encontrar um Livro", "Gráficos de Gêneros", "Amigos"])

# Inicializa session_state para o formulário
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'titulo': '',
        'autor': '',
        'resumo': '',
        'genero': '',
        'avaliacao': 0,
        'anotacoes': '',
        'citacoes': '',
        'status': 'Lido'
    }

# Página 1: Adicionar Livro
if page == "Adicionar Livro":
    st.title('Adicionar Livro')
    st.image("bibli.jpg", caption="Biblioteca Mosteiro Admont, Austria", use_column_width=True)

    # Formulário para adicionar um novo livro
    with st.form(key='book_form'):
        st.session_state.form_data['titulo'] = st.text_input('Título do Livro', st.session_state.form_data['titulo'])
        st.session_state.form_data['autor'] = st.text_input('Autor', st.session_state.form_data['autor'])
        st.session_state.form_data['resumo'] = st.text_area('Resumo', st.session_state.form_data['resumo'])
        st.session_state.form_data['genero'] = st.text_input('Gênero', st.session_state.form_data['genero'])
        st.session_state.form_data['avaliacao'] = st.slider("Avaliação (0-10)", 0, 10, st.session_state.form_data['avaliacao'])
        st.session_state.form_data['anotacoes'] = st.text_area('Anotações', st.session_state.form_data['anotacoes'])
        st.session_state.form_data['citacoes'] = st.text_area('Citações', st.session_state.form_data['citacoes'])
        st.session_state.form_data['status'] = st.radio("Status", ["Lido", "Lendo", "Quero Ler"], index=["Lido", "Lendo", "Quero Ler"].index(st.session_state.form_data['status']))

        # Campo de empréstimo com opções de escolha
        emprestado = st.checkbox("Emprestado")
        emprestei_para = ""
        peguei_de = ""
        if emprestado:
            emprestei_para = st.text_input("Emprestei para quem?", "")
            peguei_de = st.text_input("Peguei emprestado de quem?", "")
        
        submit_button = st.form_submit_button(label='Adicionar Livro')

    if submit_button:
        if st.session_state.form_data['titulo'] and st.session_state.form_data['autor']:
            novo_livro = {
                'titulo': st.session_state.form_data['titulo'],
                'autor': st.session_state.form_data['autor'],
                'resumo': st.session_state.form_data['resumo'],
                'genero': st.session_state.form_data['genero'],
                'avaliacao': st.session_state.form_data['avaliacao'],
                'anotacoes': st.session_state.form_data['anotacoes'],
                'citacoes': st.session_state.form_data['citacoes'],
                'status': st.session_state.form_data['status'],
                'emprestado': emprestado,
                'emprestei_para': emprestei_para,
                'peguei_de': peguei_de
            }
            books = load_books()
            books.append(novo_livro)
            save_books(books)
            st.success('Livro adicionado com sucesso!')

            # Resetando os campos do formulário
            st.session_state.form_data = {
                'titulo': '',
                'autor': '',
                'resumo': '',
                'genero': '',
                'avaliacao': 0,
                'anotacoes': '',
                'citacoes': '',
                'status': 'Lido'
            }

# Inicializa o estado de edição
if 'selected_book_index' not in st.session_state:
    st.session_state.selected_book_index = None

# Página 2: Livros Lidos
elif page == "Livros Lidos":
    st.title('Livros Lidos e Lendo')
    books = load_books()
    st.image("bibli6.webp", caption="Real Gabinete Português de Leitura, Rio de Janeiro", use_column_width=True)

    # Exibe os livros no formato de lista
    for i, livro in enumerate(books):
        if livro['status'] in ['Lido', 'Lendo']:  # Verifica o status do livro
            st.write(f"Título: {livro['titulo']}")
            st.write(f"Autor: {livro['autor']}")
            st.write(f"Resumo: {livro['resumo']}")
            st.write(f"Gênero: {livro['genero']}")
            cor_avaliacao = get_avaliacao_color(livro.get('avaliacao', 0))
            st.markdown(f"Avaliação: <span style='color:{cor_avaliacao}; font-weight:bold;'>{livro.get('avaliacao', 0)}/10</span>", unsafe_allow_html=True)
            st.write(f"Anotações: {livro.get('anotacoes', '')}")
            st.write(f"Citações: {livro.get('citacoes', '')}")
        
            # Botão para editar o livro com uma chave única usando o índice i
            if st.button(f"Editar", key=f"edit_btn_{i}"):
                st.session_state.selected_book_index = i  # Define o índice do livro para edição
            st.write("---")

    # Exibe o formulário de edição se um livro tiver sido selecionado
    if st.session_state.selected_book_index is not None:
        livro_editar = books[st.session_state.selected_book_index]
        
        st.write("### Editando Livro")
        with st.form(key='edit_book_form'):
            titulo = st.text_input('Título do Livro', value=livro_editar['titulo'])
            autor = st.text_input('Autor', value=livro_editar['autor'])
            resumo = st.text_area('Resumo', value=livro_editar['resumo'])
            genero = st.text_input('Gênero', value=livro_editar['genero'])
            avaliacao = st.slider("Avaliação (0-10)", 0, 10, value=livro_editar['avaliacao'])
            anotacoes = st.text_area('Anotações', value=livro_editar['anotacoes'])
            citacoes = st.text_area('Citações', value=livro_editar['citacoes'])
            status = st.radio("Status", ["Lido", "Lendo", "Quero Ler"], index=["Lido", "Lendo", "Quero Ler"].index(livro_editar['status']))
            
            emprestado = st.checkbox("Emprestado", value=livro_editar.get('emprestado', False))
            emprestei_para = st.text_input("Emprestei para quem?", value=livro_editar.get('emprestei_para', ''))
            peguei_de = st.text_input("Peguei emprestado de quem?", value=livro_editar.get('peguei_de', ''))
            
            save_button = st.form_submit_button(label='Salvar Alterações')
            cancel_button = st.form_submit_button(label='Cancelar')
        
        if save_button:
            # Atualiza o livro com as informações editadas
            livro_editar.update({
                'titulo': titulo,
                'autor': autor,
                'resumo': resumo,
                'genero': genero,
                'avaliacao': avaliacao,
                'anotacoes': anotacoes,
                'citacoes': citacoes,
                'status': status,
                'emprestado': emprestado,
                'emprestei_para': emprestei_para,
                'peguei_de': peguei_de
            })
            save_books(books)  # Salva as alterações no arquivo
            st.success('Alterações salvas com sucesso!')
            st.session_state.selected_book_index = None  # Limpa o estado de edição

        elif cancel_button:
            st.session_state.selected_book_index = None  # Cancela a edição

# Página 3: Quero Ler
elif page == "Quero Ler":
    st.title('Quero Ler')
    st.image("bibli9.webp", caption="Biblioteca Nacional da França, Paris", use_column_width=True)
    books = load_books()
    livros_quero_ler = [livro for livro in books if livro.get('status') == 'Quero Ler']
    if livros_quero_ler:
        for livro in livros_quero_ler:
            st.write(f"Título: {livro['titulo']}")
            st.write(f"Autor: {livro['autor']}")
            st.write("---")
    else:
        st.write("Nenhum livro na lista de 'Quero Ler'.")

# Página 4: Livros Favoritos    
elif page == "Livros Favoritos":
    st.title("Livros Favoritos")
    st.image("bibli10.jpg", caption="Biblioteca Nacional da China, Pequim", use_column_width=True)
    books = load_books()
    livros_favoritos = [livro for livro in books if livro.get('avaliacao', 0) >= 9]
    if livros_favoritos:
        for livro in livros_favoritos:
            st.write(f"Título: {livro['titulo']}")
            st.write(f"Autor: {livro['autor']}")
            st.write(f"Avaliação: {livro['avaliacao']}/10")
            st.write("---")
    else:
        st.write("Nenhum livro com avaliação entre 9 e 10.")

# Página 5: Encontrar um Livro
elif page == "Encontrar um Livro":
    st.title("Encontrar um Livro")
    st.image("bibli11.jpg", caption="Biblioteca Joanina, Coimbra", use_column_width=True)
    # Campo de entrada para a palavra-chave
    palavra_chave = st.text_input("Digite uma palavra-chave para buscar um livro:", key="busca_palavra_chave")
    
    # Botão de busca
    if st.button("Buscar"):
        if palavra_chave:  # Verifica se a palavra-chave foi fornecida
            livros_encontrados = []
            books = load_books()

            # Busca livros que contenham a palavra-chave em qualquer uma das partes
            for livro in books:
                if (palavra_chave.lower() in livro.get('titulo', '').lower() or
                    palavra_chave.lower() in livro.get('resumo', '').lower() or
                    palavra_chave.lower() in livro.get('anotacoes', '').lower() or
                    palavra_chave.lower() in livro.get('citacoes', '').lower()):
                    livros_encontrados.append(livro)
            
            # Exibe os livros encontrados
            if livros_encontrados:
                for livro in livros_encontrados:
                    st.write(f"Título: {livro['titulo']}")
                    st.write(f"Autor: {livro['autor']}")
                    st.write(f"Resumo: {livro['resumo']}")
                    st.write(f"Gênero: {livro['genero']}")
                    cor_avaliacao = get_avaliacao_color(livro.get('avaliacao', 0))
                    st.markdown(f"Avaliação: <span style='color:{cor_avaliacao}; font-weight:bold;'>{livro.get('avaliacao', 0)}/10</span>", unsafe_allow_html=True)
                    st.write(f"Anotações: {livro.get('anotacoes', '')}")
                    st.write(f"Citações: {livro.get('citacoes', '')}")
                    st.write("---")
            else:
                st.write("Nenhum livro encontrado com essa palavra-chave.")
        else:
            st.write("Digite uma palavra-chave para buscar um livro.")
# Página 6: Gráficos de Gêneros
elif page == "Gráficos de Gêneros":
    st.title("Gráficos de Gêneros")
    st.write("Em breve: Gráficos interativos de gêneros.")

# Página 7: Amigos
elif page == "Amigos":
    st.title("Amigos")
    st.image("best.jpg", caption="", use_column_width=True)
    
    # Formulário para cadastrar um novo amigo
    with st.form(key="friend_form"):
        nome = st.text_input("Nome do Amigo")
        telefone = st.text_input("Telefone")
        adicionar_amigo = st.form_submit_button("Adicionar Amigo")

        # Adicionar o novo amigo à lista
    if adicionar_amigo:
        if nome:
            amigos = load_friends()
            novo_amigo = {"nome": nome, "telefone": telefone}
            amigos.append(novo_amigo)
            save_friends(amigos)
            st.success("Amigo adicionado com sucesso!")

    # Exibir a lista de amigos cadastrados
    amigos = load_friends()
    if amigos:
        st.subheader("Lista de Amigos")
        for amigo in amigos:
            st.write(f"Nome: {amigo['nome']}")
            if amigo["telefone"]:
                st.write(f"Telefone: {amigo['telefone']}")
            st.write("---")
    else:
        st.write("Nenhum amigo cadastrado ainda.")
