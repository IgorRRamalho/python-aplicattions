# Código para integração com a API do Spotifyimport spotipy

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifySync:
    def __init__(self, client_id, client_secret, redirect_uri):
        """
        Inicializa a classe SpotifySync.

        :param client_id: O ID do cliente para autenticação na API do Spotify.
        :param client_secret: O segredo do cliente para autenticação na API do Spotify.
        :param redirect_uri: A URI de redirecionamento para autenticação.
        """
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-read-private playlist-modify-private playlist-modify-public user-read-private"
        ))

    def get_playlists(self):
        """
        Recupera as playlists do usuário.

        :return: Um dicionário contendo as playlists do usuário.
        """
        try:
            return self.sp.current_user_playlists()
        except Exception as e:
            print(f"Erro ao obter playlists: {e}")
            return None

    def add_tracks_to_playlist(self, playlist_id, track_uris):
        """
        Adiciona faixas a uma playlist existente.

        :param playlist_id: O ID da playlist onde as faixas serão adicionadas.
        :param track_uris: Uma lista de URIs das faixas a serem adicionadas.
        """
        try:
            self.sp.playlist_add_items(playlist_id, track_uris)
            print(f"Faixas adicionadas à playlist {playlist_id}.")
        except Exception as e:
            print(f"Erro ao adicionar faixas à playlist: {e}")

    def get_user_profile(self):
        """
        Obtém o perfil do usuário atual.

        :return: Um dicionário contendo o perfil do usuário, incluindo o nome.
        """
        try:
            return self.sp.current_user()
        except Exception as e:
            print(f"Erro ao obter perfil do usuário: {e}")
            return None
       
            
            
