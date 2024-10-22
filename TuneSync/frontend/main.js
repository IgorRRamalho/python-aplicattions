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
            contextIsolation: false, // Tenha cuidado ao usar isso; considere habilitar contextIsolation
        }
    });

    win.loadFile('index.html');

    // Opcional: Abra o DevTools para depuração
    win.webContents.openDevTools();
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// Manipulador IPC para sincronizar playlists
ipcMain.handle('syncPlaylists', async () => {
    return new Promise((resolve, reject) => {
        exec('python3 backend/sync_manager.py', (error, stdout, stderr) => {
            if (error) {
                reject(`Erro ao sincronizar playlists: ${error.message}`);
                return;
            }
            resolve(stdout || stderr);
        });
    });
});
