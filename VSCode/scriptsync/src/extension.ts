// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as net from 'net';
import * as path from 'path';

let server: net.Server | null = null;
let connections: net.Socket[] = [];
let isLogging = false;

const outputChannel = vscode.window.createOutputChannel('scriptsync');
let lastReceivedMessage: { guid: any; } | null = null;

function startServer() {
    isLogging = true;
    server = net.createServer((socket) => {
        socket.setTimeout(0);
        connections.push(socket);
        socket.on('end', () => {
            connections = connections.filter(conn => conn !== socket);
        });
        socket.on('data', (data) => {
            try {
                const message = JSON.parse(data.toString());

                const activeEditor = vscode.window.activeTextEditor;
                if (activeEditor) {
                    let vscodeActiveScriptName = path.basename(activeEditor.document.uri.fsPath);
                    let ghScriptName = path.basename(message.script_path);

                    if (vscodeActiveScriptName === ghScriptName) {
                        if (lastReceivedMessage !== message.msg) {
                            if (isLogging) {
                                outputChannel.clear();
                                outputChannel.appendLine(message.msg);
                                lastReceivedMessage = message.msg;
                            }
                        }
                    }
                }

            } catch (error) {
                vscode.window.showErrorMessage(`scriptsync::Message parsing Error: ${(error as Error).message}`);
            }
        });
        socket.on('error', (error) => {
            if (error.message.includes('ECONNRESET')) {
                vscode.window.showWarningMessage('scriptsync::GHListener in standby.');
            } else {
                vscode.window.showErrorMessage(`scriptsync::Socket Error: ${error.message}`);
            }
        });
    });

    // start the server by reusing the same port with SO_REUSEADDR
    server.listen(58260, '127.0.0.1', () => {
        vscode.window.showInformationMessage('scriptsync::GHListener started.');
        outputChannel.clear();
        outputChannel.appendLine('scriptsync::Ready to listen to GHcomponent.');
    });
}

function silenceServer() {
    if (server) {
        // Close all connections
        connections.forEach((conn) => conn.end());
        connections = [];

        // Close server
        server.close(() => {
            vscode.window.showInformationMessage('scriptsync::GHListener stopped.');
            outputChannel.clear();
            outputChannel.appendLine('scriptsync::GHListener stopped.');
        });
        server = null;

        isLogging = false;
    }
}

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
    //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    //%% Rhino
    //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    let rhinoSenderCmd = vscode.commands.registerCommand('scriptsync.sendPath', () => {
        // port and ip address of the server
        const port = 58259;
        const host = '127.0.0.1';

        // check the file extension: accept only .py and .cs files
        const activeTextEditor = vscode.window.activeTextEditor;
        let fileExtension = '';
        
        if (activeTextEditor) {
            const activeDocument = activeTextEditor.document;
            fileExtension = activeDocument.uri.path.split('.').pop() || '';
        }
        if (fileExtension !== 'py' && fileExtension !== 'cs') {
            vscode.window.showWarningMessage('scriptsync::File extension not supported');
            return;
        }

        const client = new net.Socket();

        client.on('error', (error) => {
            vscode.window.showErrorMessage('scriptsync::Run ScriptSyncStart on Rhino first.');
            console.error('Error: ', error);
        });
        client.connect(58259, '127.0.0.1', () => {
            const activeTextEditor = vscode.window.activeTextEditor;
            if (activeTextEditor) {
                const activeDocument = activeTextEditor.document;
                const activeDocumentPath = activeDocument.uri.path;
                client.write(activeDocumentPath);
            }
            else {
                vscode.window.showWarningMessage('scriptsync::No active text editor');
            }
        });
    });
    context.subscriptions.push(rhinoSenderCmd);

    //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    //%% Grasshopper
    //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    let ghListenerCmd = vscode.commands.registerCommand('scriptsync.toggleGH', () => {
        // const outputChannel = vscode.window.createOutputChannel('scriptsync');
        outputChannel.show(true);

        if (server) {
            silenceServer();
            return;
        }
        startServer();

        context.subscriptions.push({
            dispose: () => server?.close()
        });
    });
    context.subscriptions.push(ghListenerCmd);
}

// This method is called when your extension is deactivated
export function deactivate() {
    if (server) {
        server.close(() => {
        });
    }
}

