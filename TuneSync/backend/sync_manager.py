# Lógica para comparar e sincronizar playlists

class SyncManager:
    def __init__(self, spotify_sync, apple_music_sync):
        """
        Inicializa a classe SyncManager.

        :param spotify_sync: Instância da classe SpotifySync.
        :param apple_music_sync: Instância da classe AppleMusicSync.
        """
        self.spotify_sync = spotify_sync
        self.apple_music_sync = apple_music_sync

    def sync_playlists(self):
        """
        Sincroniza playlists entre Spotify e Apple Music.
        """
        spotify_playlists = self.spotify_sync.get_playlists()
        apple_playlists = self.apple_music_sync.get_playlists()

        # Lógica de comparação e sincronização
        for sp_playlist in spotify_playlists['items']:
            sp_playlist_name = sp_playlist['name']
            if not self.playlist_exists(sp_playlist_name, apple_playlists):
                # Cria a playlist na Apple Music
                apple_playlist_id = self.apple_music_sync.create_playlist(sp_playlist_name)
                # Adicionar músicas na Apple Music
                self.add_tracks_to_apple_playlist(apple_playlist_id, sp_playlist['tracks'])
            else:
                # Sincroniza as faixas entre as playlists
                apple_playlist_id = self.get_apple_playlist_id(sp_playlist_name, apple_playlists)
                self.sync_tracks(sp_playlist, apple_playlist_id)

    def playlist_exists(self, playlist_name, apple_playlists):
        """
        Verifica se uma playlist já existe no Apple Music.

        :param playlist_name: Nome da playlist a ser verificada.
        :param apple_playlists: Dicionário com as playlists da Apple Music.
        :return: True se a playlist existir, False caso contrário.
        """
        for apple_playlist in apple_playlists.get('data', []):
            if apple_playlist['attributes']['name'] == playlist_name:
                return True
        return False

    def get_apple_playlist_id(self, playlist_name, apple_playlists):
        """
        Obtém o ID da playlist da Apple Music pelo nome.

        :param playlist_name: Nome da playlist.
        :param apple_playlists: Dicionário com as playlists da Apple Music.
        :return: O ID da playlist ou None se não encontrado.
        """
        for apple_playlist in apple_playlists.get('data', []):
            if apple_playlist['attributes']['name'] == playlist_name:
                return apple_playlist['id']
        return None

    def sync_tracks(self, spotify_playlist, apple_playlist_id):
        """
        Sincroniza as faixas entre a playlist do Spotify e a playlist da Apple Music.

        :param spotify_playlist: Playlist do Spotify contendo as faixas.
        :param apple_playlist_id: ID da playlist na Apple Music.
        """
        spotify_track_uris = [track['uri'] for track in spotify_playlist['tracks']['items']]
        # Obtém as faixas existentes na playlist da Apple Music
        apple_playlist_tracks = self.apple_music_sync.get_tracks_in_playlist(apple_playlist_id)
        
        # Verifica quais faixas do Spotify não estão na Apple Music
        apple_track_ids = [track['id'] for track in apple_playlist_tracks['data']] if apple_playlist_tracks else []
        tracks_to_add = [uri for uri in spotify_track_uris if uri not in apple_track_ids]

        if tracks_to_add:
            self.apple_music_sync.add_tracks_to_playlist(apple_playlist_id, tracks_to_add)

    def add_tracks_to_apple_playlist(self, apple_playlist_id, spotify_tracks):
        """
        Adiciona faixas à playlist da Apple Music.

        :param apple_playlist_id: O ID da playlist na Apple Music.
        :param spotify_tracks: Faixas da playlist do Spotify.
        """
        track_ids = [track['uri'].split(':')[2] for track in spotify_tracks['items']]
        self.apple_music_sync.add_tracks_to_playlist(apple_playlist_id, track_ids)
