# GHOSTSURF 
![GhostsurfLogo](https://raw.githubusercontent.com/dogaegeozden/ghostsurf/main/logos/ghostsurf_rounded.png)

Ghostsurf is a hacking tool which you can use to hide your identity.

<br>

[Wikipedia: Tor Anonimity Network](https://en.wikipedia.org/wiki/Tor_%2anonymity_network%29)

[Tor Project Website](https://www.torproject.org/)

[Transparent Proxy Brief Notes](https://gitlab.torproject.org/legacy/trac/-/wikis/doc/TransparentProxy#brief-notes)

[Tips on Remaining Anonymous](https://www.whonix.org/wiki/Tips_on_Remaining_Anonymous)

<br>

## CONTROL DECK

__Start/Stop Button:__ Starts/Stops the transparent proxy and changes the system's timezone

__Change IP Button:__ Changes the ip address

__My IP Button:__ Displays your current public ip address

__Hostname Changer Button:__ Changes the hostname with a fake one

__Mac Address Changer Button:__ Changes the mac address with a fake one

__Name Servers Changer Button:__ Changes the nameservers with appropriate ones(localhost or privacy focuseds)

__Log Shredder Button:__ Overwrites the log files

__Pandora Bomb Button:__ Wipes the memory

__Browser Anonymization Button:__ Sets the firefox preferences to enhance browser anonymization

__Status Button:__ Updates the tor status text

__Checklist Button:__ Runs a checklist to display the features that you are using

__Reset Button:__ Reset ghostsurf modifications

__White Rabbit Button:__ Opens the help page on the browser

__Enable Ghostsurf at Boot Switch:__ Enables ghostsurf boot


<br>

## INSTALLATION
1) Install the dependencies: 	

		sudo apt install tor netfilter-persistent iptables-persistent secure-delete bleachbit macchanger net-tools -y

2) Download the installer

		curl -L https://github.com/dogaegeozden/ghostsurf/releases/download/tor/ghostsurf.deb -o ghostsurf.deb		

3) Start the installer 

		sudo dpkg -i ghostsurf.deb		

4) Open a new terminal and type: 
	
		ghostsurf

<br>


![AppScreenShot](https://raw.githubusercontent.com/dogaegeozden/ghostsurf/main/app_images/app_sc.png)

## HELP

Ghostsurf is identifying your ip address by sending a get request to https://ifconfig.io. And, if the app sends too many requests in short time that may cause issues and you may not get a proper response.

<br>

---

<br>

# GHOSTSURF 
![GhostsurfLogo](https://raw.githubusercontent.com/dogaegeozden/ghostsurf/main/logos/ghostsurf_rounded.png)

Ghostsurf kullanıcıların kimliklerini gizlemelerini sağlayan bir hackleme aracıdır.

<br>

[Wikipedia: Tor Anonimity Network](https://en.wikipedia.org/wiki/Tor_%2anonymity_network%29)

[Tor Project Website](https://www.torproject.org/)

[Transparent Proxy Brief Notes](https://gitlab.torproject.org/legacy/trac/-/wikis/doc/TransparentProxy#brief-notes)

[Tips on Remaining Anonymous](https://www.whonix.org/wiki/Tips_on_Remaining_Anonymous)

<br>

## KONTROL GÜVERTESİ

__Start/Stop Button:__ Transparent proxy'i durdurur veya başlatır ve sistemin zaman dilimini değiştirir

__Change IP Button:__ İp addresini değiştirir

__My IP Button:__ Topluma gözükzen ip adresini gösterir

__Hostname Changer Button:__ Sahte ana bilgisayar adı atar bilgisayara

__Mac Address Changer Button:__ Mac adresini değiştirir

__Name Servers Changer Button:__ Ad sunucusu ayarlarını uygun olanlarıyla değiştirir(yerel sunucu veya özel odaklı)

__Log Shredder Button:__ Kayıt dosyalarının uzerine yazar

__Pandora Bomb Button:__ Belleği siler

__Browser Anonymization Button:__ Arama motorunun tercihlerini anonimleşmeyi attırıcak şekilde değiştirir

__Status Button:__ Tor durumunu günceller

__Checklist Button:__ Kontrol listesi oluşturur

__Reset Button:__ Ghostsurf değişikliklerini sıfırlar

__White Rabbit Button:__ Yardım sayfasını açar

__Enable Ghostsurf at Boot Switch:__ Ghostsurf'ü başlangıçta başlamaya ayarlar


<br>

## YÜKLEME
1) Bağımlılıkları yükle: 	

		sudo apt install tor netfilter-persistent iptables-persistent secure-delete bleachbit macchanger net-tools -y

2) Yükleyiciyi indir

		curl -L https://github.com/dogaegeozden/ghostsurf/releases/download/tor/ghostsurf.deb -o ghostsurf.deb		

3) Yükleyiciyi başlat

		sudo dpkg -i ghostsurf.deb		

4) Terminali aç ve aşağıdaki metni gir: 
	
		ghostsurf

<br>

![AppScreenShot](https://raw.githubusercontent.com/dogaegeozden/ghostsurf/main/app_images/app_sc.png)

## YARDIM

Ghostsurf senin genel ip adresini https://ifconfig.io 'ya talep göndererek alıyor. Ve, eğer sen çok fazla talep gönderirsen, düzgün yanıt alamaya bilirsin.