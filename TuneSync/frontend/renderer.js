/* Lógica para lidar com eventos de UI */
const { ipcRenderer } = require('electron');

document.getElementById('syncButton').addEventListener('click', async () => {
    const result = await ipcRenderer.invoke('syncPlaylists');
    document.getElementById('output').textContent = result;
});

document.getElementById('spotifyLogin').addEventListener('click', async () => {
    authenticateSpotify();
});

async function authenticateSpotify() {
    const authWindow = new BrowserWindow({ width: 800, height: 600 });
    const spotifyAuthURL = "https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost:8888/callback&scope=playlist-read-private playlist-modify-private user-read-private";
    authWindow.loadURL(spotifyAuthURL);

    // Após autenticação, chame o método para obter o nome do usuário
    authWindow.on('closed', async () => {
        const userProfile = await ipcRenderer.invoke('getSpotifyUserProfile');
        document.getElementById('output').textContent = `Bem-vindo, ${userProfile.display_name}`;
    });
}

document.getElementById('appleMusicLogin').addEventListener('click', () => {
    authenticateAppleMusic();
});


function authenticateAppleMusic() {
    MusicKit.getInstance().authorize().then(token => {
        console.log('Apple Music token:', token);
    });
}

