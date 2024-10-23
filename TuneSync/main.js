/* Arquivo principal do Electron */

const { app, BrowserWindow, ipcMain } = require('electron');
const { exec } = require('child_process');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'renderer.js'),
            nodeIntegration: true,
            contextIsolation: false,
        }
    });

    win.loadFile('index.html');
    win.webContents.openDevTools();
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

// Manipulador IPC para sincronizar playlists
ipcMain.handle('syncPlaylists', async () => {
    return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, '../backend/sync_manager.py');
        exec(`python3 ${scriptPath}`, (error, stdout, stderr) => {
            if (error) {
                reject(`Erro ao sincronizar playlists: ${error.message}`);
                return;
            }
            resolve(stdout || stderr);
        });
    });
});

// Manipulador IPC para obter o perfil do usuário do Spotify
ipcMain.handle('getSpotifyUserProfile', async () => {
    return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, '../backend/spotify_sync.py');
        exec(`python3 ${scriptPath} --get_user_profile`, (error, stdout, stderr) => {
            if (error) {
                reject(`Erro ao obter perfil do Spotify: ${error.message}`);
                return;
            }
            try {
                const userProfile = JSON.parse(stdout);
                resolve(userProfile);
            } catch (parseError) {
                reject(`Erro ao parsear resposta do perfil: ${parseError.message}`);
            }
        });
    });
});
