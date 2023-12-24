// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as net from 'net';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('extension.sendPath', () => {
        // activate for output pannel logging
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

        // ping the server
        const client = new net.Socket();

        // verify if the server is running
        client.on('error', (err) => {
            vscode.window.showWarningMessage('scriptsync::run ScriptSyncRun on Rhino.');
        });
        // client.on('close' || 'end', () => {
        //     outputChannel.appendLine('scriptsync::Script executed in Rhino.');
        // });
        
        client.connect(58259, '127.0.0.1', () => {

            // vscode.window.showInformationMessage('scriptsync::Connected to the server');

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

        // close the connection
        client.destroy();
    });

    context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
