# Funções de autenticação (Spotify e Apple Music)

import time
import jwt
from spotipy.oauth2 import SpotifyOAuth

class AuthManager:
    def __init__(self, spotify_client_id, spotify_client_secret, redirect_uri):
        """
        Inicializa a classe AuthManager.

        :param spotify_client_id: O ID do cliente para autenticação na API do Spotify.
        :param spotify_client_secret: O segredo do cliente para autenticação na API do Spotify.
        :param redirect_uri: A URI de redirecionamento para autenticação do Spotify.
        """
        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret
        self.redirect_uri = redirect_uri

    def spotify_auth(self):
        """
        Autentica o usuário no Spotify e retorna o objeto SpotifyOAuth.

        :return: Instância do SpotifyOAuth.
        """
        try:
            return SpotifyOAuth(
                client_id=self.spotify_client_id,
                client_secret=self.spotify_client_secret,
                redirect_uri=self.redirect_uri,
                scope="playlist-read-private playlist-modify-private playlist-modify-public"
            )
        except Exception as e:
            print(f"Erro durante a autenticação no Spotify: {e}")
            return None

    def apple_music_auth(self, private_key, team_id, key_id):
        """
        Autentica o usuário na Apple Music e retorna um token JWT.

        :param private_key: A chave privada usada para gerar o token JWT.
        :param team_id: O ID da equipe para autenticação na Apple Music.
        :param key_id: O ID da chave usada para autenticação.
        :return: Token JWT para autenticação na Apple Music.
        """
        try:
            token = jwt.encode(
                {"iss": team_id, "iat": time.time(), "exp": time.time() + 86400, "aud": "music"},
                private_key,
                algorithm="ES256",
                headers={"kid": key_id}
            )
            return token
        except Exception as e:
            print(f"Erro durante a autenticação na Apple Music: {e}")
            return None

