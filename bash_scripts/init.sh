#!/bin/bash

main () {
    local apps_to_kill=(
        tor proxychains dropbox
        chrome chromium firefox firefox-esr firefox-bin iceweasel google-chrome
        skype zoom telegram slack discord signal
        thunderbird icedove evolution
        xchat hexchat weechat irssi
        transmission deluge qbittorrent ktorrent
        pidgin pidgin.orig empathy
        curl wget aria2c lftp ftp lynx elinks links2
        vlc smplayer mplayer
        ssh sshd openvpn wireguard
        steam lutris
        thunderbird geary claws-mail
    )
    killall -q "${apps_to_kill[@]}"
    local bleachbit_items=(
        adobe_reader.cache
        bash.history
        chromium.cache chromium.cookies chromium.current_session chromium.history chromium.dom
        elinks.history
        emesene.cache
        epiphany.cache
        firefox.cache firefox.cookies firefox.url_history firefox.session
        flash.cache flash.cookies
        gnome_recent
        google_chrome.cache google_chrome.cookies google_chrome.history
        icedove.cache icedove.cookies
        links2.history
        opera.cache opera.cookies opera.search_history opera.url_history
        pidgin.cache
        rdp.client
        recent_documents
        skype.chat_logs skype.history
        system.logs system.recent_documents
        thunderbird.cache thunderbird.cookies thunderbird.url_history
        transmission.torrent_files transmission.blocklists
        vlc.history
        wget.history
        x11.history
    )
    bleachbit -c "${bleachbit_items[@]}" &> /dev/null
}

main
