# Tune Sync

Este é um projeto que sincroniza playlists entre as contas do **Spotify** e **Apple Music**. O objetivo é garantir que as playlists existentes em uma plataforma sejam replicadas na outra, adicionando músicas faltantes e criando playlists que ainda não existam. O projeto utiliza **Electron** para criar uma interface gráfica, enquanto o backend é desenvolvido em **Python**.

## Funcionalidades

- Sincroniza automaticamente playlists entre **Spotify** e **Apple Music**.
- Cria playlists que estão em uma plataforma e não na outra.
- Verifica playlists já existentes e adiciona músicas faltantes.
- Interface gráfica desenvolvida em **Electron** para facilitar a autenticação e o controle da sincronização.

## Requisitos

### Backend (Python)

- **Python 3.8+**
- **Spotify API** para autenticação e manipulação de playlists.
- **Apple Music API** com autenticação JWT.
- Bibliotecas Python necessárias (listadas abaixo).

### Frontend (Electron)

- **Node.js** e **npm** para gerenciar dependências e executar o projeto Electron.

## Estrutura do Projeto

```
music-sync/
│
├── backend/                # Backend em Python para lidar com APIs e lógica de sincronização
│   ├── __init__.py         # Inicializador do pacote backend
│   ├── spotify_sync.py     # Código para integração com a API do Spotify
│   ├── apple_sync.py       # Código para integração com a API do Apple Music
│   ├── sync_manager.py     # Lógica para comparar e sincronizar playlists
│   ├── auth.py             # Funções de autenticação (Spotify e Apple Music)
│   └── utils.py            # Funções auxiliares, como logs e tratamento de erros
│
├── frontend/               # Código do Electron para interface gráfica
│   ├── main.js             # Arquivo principal do Electron
│   ├── index.html          # Interface HTML inicial
│   ├── renderer.js         # Lógica para lidar com eventos de UI
│   ├── styles.css          # Arquivo de estilos da interface
│   └── package.json        # Configuração do projeto Electron
│
├── .env                    # Arquivo para variáveis de ambiente
├── requirements.txt        # Dependências do Python
└── README.md               # Documentação do projeto
```

## Instalação e Configuração

### Passo 1: Clonar o repositório

```bash
git clone https://github.com/seuusuario/music-sync.git
cd music-sync
```

### Passo 2: Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```txt
SPOTIFY_CLIENT_ID=seu_spotify_client_id
SPOTIFY_CLIENT_SECRET=seu_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

APPLE_DEVELOPER_TOKEN=seu_token_de_desenvolvedor
APPLE_MUSIC_USER_TOKEN=seu_token_de_usuario
```

### Passo 3: Instalar as dependências

#### Backend (Python)

Instale as dependências do Python usando o `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### Frontend (Electron)

Instale as dependências do **Electron**:

```bash
npm install
```

### Passo 4: Rodar o projeto

#### Rodar o Electron (Frontend)

Execute o seguinte comando para iniciar a interface gráfica:

```bash
npm start
```

Isso abrirá a interface de sincronização de playlists.

## Utilização

1. Abra o programa com `npm start`.
2. Faça a autenticação nas contas de **Spotify** e **Apple Music**.
3. Pressione o botão **"Sincronizar Playlists"** para sincronizar as playlists entre as duas plataformas.
4. O resultado da sincronização será mostrado na interface.

## Dependências

### Backend (Python)

- **spotipy**: Biblioteca para interagir com a API do Spotify.
- **requests**: Para fazer requisições HTTP à API da Apple Music.
- **PyJWT**: Utilizado para gerar tokens JWT para a autenticação da Apple Music.

### Frontend (Electron)

- **Electron**: Para criar a interface de usuário.

## Contribuição

1. Faça um **fork** do projeto.
2. Crie uma nova branch com a sua feature (`git checkout -b minha-feature`).
3. Faça o **commit** das suas alterações (`git commit -m 'Minha nova feature'`).
4. Faça o **push** para a branch (`git push origin minha-feature`).
5. Abra um **Pull Request**.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

