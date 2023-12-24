import * as vscode from 'vscode';
import * as assert from 'assert';
import * as path from 'path';
import { activate, deactivate } from './../extension';

suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');

    test('Extension activation and deactivation', async () => {
        // Get the absolute path to the workspace file
        const workspaceFile = vscode.Uri.file(
            path.join(__dirname, '..', '..', 'VSCode', 'scriptsync', 'src', 'extension.ts')
        );

        // Open the workspace file
        const document = await vscode.workspace.openTextDocument(workspaceFile);

        // Activate the extension
        await activate({ document, fileName: document.fileName } as any);

        // Test that the extension is active
        const extension = vscode.extensions.getExtension('your.extension.id');
        assert.ok(extension && extension.isActive);

        // Deactivate the extension
        deactivate();
    });
});
