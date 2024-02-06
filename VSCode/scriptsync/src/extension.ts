// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as net from 'net';

let server: net.Server | null = null;

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
    //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    //%% Rhino
    //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    let disposable = vscode.commands.registerCommand('scriptsync.sendPath', () => {
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
    context.subscriptions.push(disposable);

    //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    //%% Grasshopper
    //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    let toggleCommand = vscode.commands.registerCommand('scriptsync.toggleGH', () => {
        // Show messages in the OUTPUT panel
        const outputChannel = vscode.window.createOutputChannel('scriptsync');
        outputChannel.show(true);
        outputChannel.appendLine('scriptsync::Listening to GHComponent...');


        // Variable to store the last received message
        let lastReceivedMessage: { guid: any; } | null = null;
        
        if (server) {
            server.close(() => {
                vscode.window.showInformationMessage('scriptsync::Server stopped.');
            });
            server = null;
        } else {
            server = net.createServer((socket) => {
                socket.on('data', (data) => {
                    try {
                        // Parse the incoming message
                        const message = JSON.parse(data.toString());
                        // get the msg from the message
        
                        // print the activeEditor.document.uri.fsPath
                        const activeEditor = vscode.window.activeTextEditor;
                        // if (activeEditor) {
                        //     outputChannel.appendLine('activeEditor.document.uri.fsPath: ');
                        //     outputChannel.appendLine(activeEditor.document.uri.fsPath);
                        //     outputChannel.appendLine('message.script_path: ');
                        //     outputChannel.appendLine(message.script_path);
                        // }
        
                        // // Check if the active document's path matches the script_path in the message
                        // if (activeEditor) {
                        //     outputChannel.appendLine('activeEditor.document.uri.fsPath: ');
                        //     outputChannel.appendLine(activeEditor.document.uri.fsPath);
                        //     outputChannel.appendLine('message.script_path: ');
                        //     outputChannel.appendLine(message.script_path);
                        // }

                        // compare if the path are the same but do not do it by string comparison but path comparison
                        if (activeEditor && activeEditor.document.uri.fsPath === message.script_path) {
                        // if (activeEditor && activeEditor.document.uri.fsPath.split('/').pop() === message.script_path.split('/').pop()) {
                            // Check if the last message is the same do not print it
                            if (lastReceivedMessage !== message.msg) {
                                // If not, print the message and update the last received message
                                outputChannel.appendLine(message.msg);
                                lastReceivedMessage = message.msg;
                            }
                        }
        
                    } catch (error) {
                        vscode.window.showErrorMessage(`scriptsync::Message parsing Error: ${(error as Error).message}`);
                    }
                });
        
                socket.on('error', (error) => {
                    vscode.window.showErrorMessage(`scriptsync::Socket Error: ${error.message}`);
                });
            });
        
            // server.on('error', (error) => {
            //     vscode.window.showErrorMessage(`scriptsync::Server Error: ${error.message}`);
            // });
        

            server.listen(58260, '127.0.0.1', () => {
                vscode.window.showInformationMessage('scriptsync::Server started.');
            });

            context.subscriptions.push({
                dispose: () => server?.close(),
            });
        }
    });
    context.subscriptions.push(toggleCommand);


}

// This method is called when your extension is deactivated
export function deactivate() {
    if (server) {
        server.close(() => {
            vscode.window.showInformationMessage('scriptsync::Server stopped.');
        });
    }
}
