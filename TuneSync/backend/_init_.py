"""
Pacote Tune Sync

Este pacote contém a lógica para sincronizar playlists entre Spotify e Apple Music.

Versão: 1.0.0
"""

# Importação das classes principais do pacote
from .spotify_sync import SpotifySync
from .apple_sync import AppleMusicSync
from .sync_manager import SyncManager
from .auth import AuthManager

# Exemplo de uso
def example_usage():
    """
    Exemplo de uso do pacote Tune Sync.
    
    Este exemplo mostra como criar instâncias das classes e chamar o método de sincronização.
    """
    # Configurações (substitua com suas credenciais)
    SPOTIFY_CLIENT_ID = "seu_client_id"
    SPOTIFY_CLIENT_SECRET = "seu_client_secret"
    REDIRECT_URI = "http://localhost:8888/callback"
    
    APPLE_PRIVATE_KEY = "sua_chave_privada"
    APPLE_TEAM_ID = "seu_team_id"
    APPLE_KEY_ID = "seu_key_id"

    # Instanciando os gerenciadores de autenticação
    auth_manager = AuthManager(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI)
    spotify_sync = SpotifySync(auth_manager.spotify_auth())
    apple_music_sync = AppleMusicSync(auth_manager.apple_music_auth(APPLE_PRIVATE_KEY, APPLE_TEAM_ID, APPLE_KEY_ID))

    # Gerenciador de sincronização
    sync_manager = SyncManager(spotify_sync, apple_music_sync)
    
    # Sincronizar playlists
    sync_manager.sync_playlists()

# Caso o módulo seja executado diretamente, execute o exemplo
if __name__ == "__main__":
    example_usage()
