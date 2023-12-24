// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as net from 'net';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('extension.sendPath', () => {
        // port and ip address of the server
        const port = 58259;
        const host = '127.0.0.1';

        // // activate for output pannel logging
        // const outputChannel = vscode.window.createOutputChannel('scriptsync');
        // outputChannel.show(true);
        // outputChannel.appendLine('scriptsync::executing script in Rhino...');

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

    context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
