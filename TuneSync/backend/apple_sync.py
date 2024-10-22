# Código para integração com a API do Apple Music

import requests

class AppleMusicSync:
    def __init__(self, developer_token, user_token):
        """
        Inicializa a classe AppleMusicSync.

        :param developer_token: Token de desenvolvedor para autenticação na Apple Music.
        :param user_token: Token de usuário para autenticação na Apple Music.
        """
        self.developer_token = developer_token
        self.user_token = user_token
        self.base_url = "https://api.music.apple.com/v1/"

    def get_playlists(self):
        """
        Recupera as playlists do usuário.

        :return: Um dicionário contendo as playlists do usuário.
        """
        headers = {
            "Authorization": f"Bearer {self.developer_token}",
            "Music-User-Token": self.user_token,
        }
        response = requests.get(f"{self.base_url}me/playlists", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter playlists: {response.status_code}, {response.text}")
            return None

    def create_playlist(self, name):
        """
        Cria uma nova playlist com o nome especificado.

        :param name: O nome da nova playlist.
        :return: O ID da nova playlist ou None em caso de erro.
        """
        headers = {
            "Authorization": f"Bearer {self.developer_token}",
            "Music-User-Token": self.user_token,
            "Content-Type": "application/json",
        }
        data = {
            "attributes": {
                "name": name,
                "description": "Playlist criada automaticamente pela sincronização.",
                "curatorName": "Music Sync"
            }
        }
        response = requests.post(f"{self.base_url}me/playlists", headers=headers, json=data)

        if response.status_code == 201:
            return response.json().get("data")[0]["id"]
        else:
            print(f"Erro ao criar playlist: {response.status_code}, {response.text}")
            return None

    def add_tracks_to_playlist(self, playlist_id, track_ids):
        """
        Adiciona faixas a uma playlist existente.

        :param playlist_id: O ID da playlist onde as faixas serão adicionadas.
        :param track_ids: Uma lista de IDs das faixas a serem adicionadas.
        """
        headers = {
            "Authorization": f"Bearer {self.developer_token}",
            "Music-User-Token": self.user_token,
            "Content-Type": "application/json",
        }
        data = {
            "data": [{"id": track_id, "type": "songs"} for track_id in track_ids]
        }
        response = requests.post(f"{self.base_url}playlists/{playlist_id}/tracks", headers=headers, json=data)

        if response.status_code == 201:
            print(f"Faixas adicionadas à playlist {playlist_id}.")
        else:
            print(f"Erro ao adicionar faixas: {response.status_code}, {response.text}")

    def playlist_exists(self, playlist_name):
        """
        Verifica se uma playlist com o nome especificado já existe.

        :param playlist_name: O nome da playlist a ser verificada.
        :return: True se a playlist existir, False caso contrário.
        """
        playlists = self.get_playlists()
        if playlists:
            for playlist in playlists.get("data", []):
                if playlist["attributes"]["name"] == playlist_name:
                    return True
        return False
