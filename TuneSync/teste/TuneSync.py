import sys
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

class SpotifySync:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-read-private playlist-modify-private playlist-modify-public user-read-private"
        ))

    def get_playlists(self):
        """Recupera as playlists do usuário."""
        try:
            return self.sp.current_user_playlists()
        except Exception as e:
            print(f"Erro ao obter playlists: {e}")
            return None

    def add_tracks_to_playlist(self, playlist_id, track_uris):
        """Adiciona faixas a uma playlist existente."""
        try:
            self.sp.playlist_add_items(playlist_id, track_uris)
            print(f"Faixas adicionadas à playlist {playlist_id}.")
        except Exception as e:
            print(f"Erro ao adicionar faixas à playlist: {e}")

    def get_user_profile(self):
        """Obtém o perfil do usuário."""
        try:
            return self.sp.current_user()
        except Exception as e:
            print(f"Erro ao obter perfil do usuário: {e}")
            return None


class AppleMusicSync:
    def __init__(self, apple_api_key, apple_team_id, apple_key_id):
        self.apple_api_key = apple_api_key
        self.apple_team_id = apple_team_id
        self.apple_key_id = apple_key_id
        self.base_url = "https://api.music.apple.com/v1/"

    def get_playlists(self):
        """Recupera as playlists do usuário no Apple Music."""
        try:
            headers = self.get_auth_headers()
            response = requests.get(self.base_url + "me/playlists", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao obter playlists do Apple Music: {e}")
            return None

    def create_playlist(self, name):
        """Cria uma nova playlist no Apple Music."""
        try:
            headers = self.get_auth_headers()
            data = {"attributes": {"name": name, "description": "Sincronizada do Spotify"}}
            response = requests.post(self.base_url + "me/playlists", headers=headers, json=data)
            response.raise_for_status()
            return response.json()["data"][0]["id"]
        except Exception as e:
            print(f"Erro ao criar playlist no Apple Music: {e}")
            return None

    def get_auth_headers(self):
        """Gere os headers de autenticação para Apple Music."""
        return {
            "Authorization": f"Bearer {self.apple_api_key}",
            "Music-User-Token": self.apple_team_id  # Ajustar conforme a autenticação
        }

    def add_tracks_to_playlist(self, playlist_id, track_ids):
        """Adiciona faixas à playlist da Apple Music."""
        try:
            headers = self.get_auth_headers()
            data = {"data": [{"id": track_id, "type": "songs"} for track_id in track_ids]}
            response = requests.post(self.base_url + f"playlists/{playlist_id}/tracks", headers=headers, json=data)
            response.raise_for_status()
            print(f"Faixas adicionadas à playlist {playlist_id} no Apple Music.")
        except Exception as e:
            print(f"Erro ao adicionar faixas à playlist da Apple Music: {e}")


class SyncManager:
    def __init__(self, spotify_sync, apple_music_sync):
        self.spotify_sync = spotify_sync
        self.apple_music_sync = apple_music_sync

    def sync_playlists(self):
        """Sincroniza playlists entre Spotify e Apple Music."""
        spotify_playlists = self.spotify_sync.get_playlists()
        apple_playlists = self.apple_music_sync.get_playlists()

        # Lógica de comparação e sincronização
        for sp_playlist in spotify_playlists['items']:
            sp_playlist_name = sp_playlist['name']
            if not self.playlist_exists(sp_playlist_name, apple_playlists):
                # Cria a playlist na Apple Music
                apple_playlist_id = self.apple_music_sync.create_playlist(sp_playlist_name)
                # Adiciona músicas na Apple Music
                self.add_tracks_to_apple_playlist(apple_playlist_id, sp_playlist['tracks'])
            else:
                # Sincroniza as faixas entre as playlists
                apple_playlist_id = self.get_apple_playlist_id(sp_playlist_name, apple_playlists)
                self.sync_tracks(sp_playlist, apple_playlist_id)

    def playlist_exists(self, playlist_name, apple_playlists):
        """Verifica se uma playlist já existe no Apple Music."""
        for apple_playlist in apple_playlists.get('data', []):
            if apple_playlist['attributes']['name'] == playlist_name:
                return True
        return False

    def get_apple_playlist_id(self, playlist_name, apple_playlists):
        """Obtém o ID da playlist da Apple Music pelo nome."""
        for apple_playlist in apple_playlists.get('data', []):
            if apple_playlist['attributes']['name'] == playlist_name:
                return apple_playlist['id']
        return None

    def sync_tracks(self, spotify_playlist, apple_playlist_id):
        """Sincroniza as faixas entre a playlist do Spotify e a playlist da Apple Music."""
        spotify_track_uris = [track['uri'] for track in spotify_playlist['tracks']['items']]
        # Obtém as faixas existentes na playlist da Apple Music
        apple_playlist_tracks = self.apple_music_sync.get_tracks_in_playlist(apple_playlist_id)

        # Verifica quais faixas do Spotify não estão na Apple Music
        apple_track_ids = [track['id'] for track in apple_playlist_tracks['data']] if apple_playlist_tracks else []
        tracks_to_add = [uri for uri in spotify_track_uris if uri not in apple_track_ids]

        if tracks_to_add:
            self.apple_music_sync.add_tracks_to_playlist(apple_playlist_id, tracks_to_add)

    def add_tracks_to_apple_playlist(self, apple_playlist_id, spotify_tracks):
        """Adiciona faixas à playlist da Apple Music."""
        track_ids = [track['uri'].split(':')[2] for track in spotify_tracks['items']]
        self.apple_music_sync.add_tracks_to_playlist(apple_playlist_id, track_ids)


def main():
    # Configurações de autenticação
    SPOTIFY_CLIENT_ID = "seu_client_id"
    SPOTIFY_CLIENT_SECRET = "seu_client_secret"
    SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
    
    APPLE_API_KEY = "sua_chave_privada"
    APPLE_TEAM_ID = "seu_team_id"
    APPLE_KEY_ID = "seu_key_id"

    # Instanciando os gerenciadores
    spotify_sync = SpotifySync(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI)
    apple_music_sync = AppleMusicSync(APPLE_API_KEY, APPLE_TEAM_ID, APPLE_KEY_ID)

    # Gerenciador de sincronização
    sync_manager = SyncManager(spotify_sync, apple_music_sync)

    if '--sync_playlists' in sys.argv:
        print("Sincronizando playlists...")
        sync_manager.sync_playlists()
    elif '--get_user_profile' in sys.argv:
        user_profile = spotify_sync.get_user_profile()
        if user_profile:
            print(json.dumps(user_profile, indent=4))
    elif '--get_playlists' in sys.argv:
        playlists = spotify_sync.get_playlists()
        if playlists:
            print(json.dumps(playlists, indent=4))
    else:
        print("Uso: python tune_sync.py --sync_playlists | --get_user_profile | --get_playlists")


if __name__ == "__main__":
    main()
