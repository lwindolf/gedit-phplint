PHPLint plugin for Gedit
========================

Simple plugin to run 'php -l' on PHP code.

Requirements
------------

Gedit 3.14 and PHP CLI installed.

Installation
------------

You might want to install the plugin using [Gedit Plugin Installer](https://github.com/lwindolf/gedit-plugininstaller) or these manual steps

    git clone https://github.com/lwindolf/gedit-phplint.git
    mkdir -p ~/.local/share/gedit/plugins/
    cp -r gedit-phplint/phplint.plugin gedit-phplint/phplint/ ~/.local/share/gedit/plugins/

Ensure to restart Gedit and activate the plugin in the preferences.

Usage
-----

When a PHP source code file is active, you can check it with `Tools > Check with PHPLint` or with the accelerator `Ctrl+J`. The results are automatically displayed in the bottom panel.
