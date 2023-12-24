// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as net from 'net';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('extension.sendPath', () => {
        const outputChannel = vscode.window.createOutputChannel('scriptsync');
        outputChannel.show(true);
        outputChannel.appendLine('scriptsync::executing file in Rhino scriptsync...');

        // check the file extension: accept only .py and .cs files
        const activeTextEditor = vscode.window.activeTextEditor;
        let fileExtension = '';
        const activeDocument = null
        if (activeTextEditor) {
            const activeDocument = activeTextEditor.document;
            fileExtension = activeDocument.uri.path.split('.').pop() || '';
        }
        if (fileExtension !== 'py' && fileExtension !== 'cs') {
            vscode.window.showWarningMessage('scriptsync::File extension not supported');
            return;
        }

        // check if the server is on
        let serverIsOn = false;
        const clientCheck = new net.Socket();
        clientCheck.connect(58259, '127.0.0.1', () => {
            console.log('scriptsync::Connected');
            serverIsOn = true;
            clientCheck.destroy();
        }
        );
        clientCheck.on('close', () => {
            console.log('Connection closed');
        });

        // check if the server is on, if not pop a warning message in vscode
        if (serverIsOn) {
            outputChannel.appendLine('Server is on');
        }
        else {
            outputChannel.appendLine('Server is off');
            vscode.window.showWarningMessage('Server is off');
        }
        
        const client = new net.Socket();
        client.connect(58259, '127.0.0.1', () => {
            console.log('Connected');
            // aboslute path of the file open in the editor
            const activeTextEditor = vscode.window.activeTextEditor;
            const activeDocument = activeTextEditor.document;
            const activeDocumentPath = activeDocument.uri.path;
            client.write(activeDocumentPath);
        });

        client.on('data', (data) => {
            console.log('Received: ' + data);
            client.destroy(); // kill client after server's response
        });

        client.on('close', () => {
            console.log('Connection closed');
        });
    });

    context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
