---
title: Using VS Code
---

::: {.callout-info}
I'm not sure yet how much we'll use VS Code. 
:::

VS Code is powerful integrated development environment (IDE), with GitHub Copilot AI assistance built in, so it's useful to have some familiarity with it. We may use it in the lab on testing and possibly other labs.

VS Code provides a huge number of extensions for working with various languages and tools, including Python, R, Jupyter Notebooks, Quarto, etc., and including integrated debugging.

I will probably do some of my demonstrations in class with VS Code, as it allows one to easily run code in the terminal or a Python session from the built-in editor.

## Installing VS Code

See [here](https://code.visualstudio.com/download) to install VS Code.

A browser-based version of VS Code is available through both the [DataHub](https://datahub.berkeley.edu) and the [SCF JupyterHub](https://jupyter.stat.berkeley.edu). It should behave very similarly but the extensions availalbe for VS Code on your own machine versus in the browser/JupyterHub can have differences.

## Using VS Code

Here are just a few initial tips on making use of VS Code.

- To easily run Python code in a Python session from the VS Code editor, you can start a Python session in the VS Code terminal and then use `Shift + Enter` to run the current line of code from the editor. You can also right-click and select `Run Python -> Run Selection/Line in Python Terminal`.

- To easily run bash code in a terminal from the editor, you can add `Cmd + Enter` (on a Mac) or `Alt + Enter` (on Windows) to your *Keyboard Shortcuts*. (You can choose some other keystrokes of your choice, though I recommend not using `Shift + Enter` as that affects the behavior for running Python code). In the Keyboard Shortcuts area, Select "Terminal: Run Selected Text in Active Terminal" (`workbench.action.terminal.runSelectedText`) and specify `Cmd + Enter`.

## Using VS Code with Linux and on remote machines

You can use the *Remote SSH* extension to connect to another machine (e.g., an SCF machine) and access your files and run code on that other machine.

- Click on the Extensions icon in the left sidebar and search for "Remote - SSH" and install it. 
- Then to connect to another machine, click on the `><` (`Open a Remote Window`) icon in the buttom left, select `Connect to Host` and follow the prompts.

## GitHub Copilot

You can use GitHub Copilot for AI assistance (including code completion, edit mode (for small guided help), agent mode (for more autonomous code generation and manipulation), and built-in Chat. That said, you shouldn't use Agent mode for our work in class as it's likely to reduce your learning.

[GitHub Education](https://github.com/education/students) provides free access to GitHub Copilot Pro.

You should see the GitHub Copilot icon in top, just to the right of the search bar. Click it to open the Copilot interface as a window on the right.

Or in a code file, click on `Cmd + I` (on a Mac, probably `Ctrl + I` on Windows)
to open an interface within your code file. When using AI edit mode, it's often important to highlight the code you want it to work on.

It's important to provide context for AI code assistance. In general if you open a folder in VS Code, that will set up the folder as a project, and the contents will be treated as context. You can also add files as context with `Add Context` in the AI window. And you can drag files/folders from the VS Code `File Explorer` window.



## Questions?

Questions (and even better, tips) on using VS Code are very welcome in the Ed Discussion.
