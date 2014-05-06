# ATop charting plugin for Ajenti

This is an [Ajenti][] plugin to show statistics gathered by [atop][] monitoring tool.
It also requires [models][] Ajenti plugin.

Install **models** plugin into `/var/lib/ajenti/plugins` along with this plugin and restart **Ajenti**:

```
# git clone https://github.com/kstep/ajenti-models.git /var/lib/ajenti/plugins
# git clone https://github.com/kstep/ajenti-atop.git /var/lib/ajenti/plugins/atop
# service restart ajenti
```

Also make sure you have installed **atop** (and optionally **netatop**) packages.
Consult your Linux distribution on how to better do it.
If you use Arch Linux, install it with `pacman -S atop`, **netatop** is available
in [AUR][netatop-aur].

You will also need to compile `content/js/widgets.coffee` file with [CoffeeScript][] compiler:

```
# cd /var/lib/ajenti/plugins/atop/content/js
# coffee -c widgets.coffee && mv widgets.js widgets.coffee.js && cp widgets.coffee.js widgets.coffee.c.js
```

Now login to your Ajenti panel and go to new **ATop** menu item in **Software** section.

By default the plugin tries to load today's log file from `/var/log/atop/atop_YYYYMMDD` on start up,
choose different log file and click "Load" button to view it. You can also toggle "Live Stream"
mode by clicking the correspondent button, it will run `atop` program in background and update charts
for each new data sample produced by it. To view log file again, turn off "Live Stream" mode by clicking
the button again and click "Load" button to load data from log file.

[Ajenti]: http://ajenti.org/
[atop]: http://www.atoptool.nl/
[models]: http://github.com/kstep/ajenti-models
[CoffeeScript]: http://coffeescript.org/
[netatop-aur]: https://aur.archlinux.org/packages/netatop/
