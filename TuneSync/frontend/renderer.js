/* Lógica para lidar com eventos de UI */


const { ipcRenderer } = require('electron');

document.getElementById('syncButton').addEventListener('click', async () => {
    const outputElement = document.getElementById('output');
    outputElement.textContent = 'Sincronizando playlists...'; 

    try {
        const result = await ipcRenderer.invoke('syncPlaylists');
        outputElement.textContent = `Resultado da sincronização:\n${result}`;
    } catch (error) {
        outputElement.textContent = `Erro: ${error}`;
    }
});
