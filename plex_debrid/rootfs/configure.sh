#!/bin/bash
cd /plex_debrid/
s6-svc -wU /var/run/s6/legacy-services/plex_debrid
while true; do
    clear
    echo "Choose an option:"
    case "$(gum choose "config - Pause plex_debrid and enter configuration screen" "shell - Enter a shell for addon debugging")" in
        config*)
            s6-svc -d /var/run/s6/legacy-services/plex_debrid
            mkdir -p /config/addons_config/plex_debrid
            python3 ./main.py --config-dir /config/addons_config/plex_debrid
            s6-svc -u /var/run/s6/legacy-services/plex_debrid
            ;;
        shell*)
            echo "To get back to the initial screen, exit the shell."
            bash
            ;;
    esac
done
