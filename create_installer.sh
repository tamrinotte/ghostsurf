#!/usr/bin/bash

# Purge the app
echo "Purging ghostsurf..."
sudo apt purge --autoremove ghostsurf -y

# Remove whats left as well
echo "Deleting what is left..."
sudo rm -rf /opt/ghostsurf

# Creating a variable called username by getting the active user's username
username=$USER

# Delete the old files if they are exist
echo "Deleting the dist folder..."
if [[ -d dist/ ]]; then
    sudo rm -rf dist/
fi

echo "Deleting the build folder..."
if [[ -d build/ ]]; then
    sudo rm -rf build/
fi 

echo "Deleting the package folder..."
if [[ -d package/ ]]; then
    sudo rm -rf package/
fi

echo "Deleting the installer..."
if [[ -f ghostsurf.deb ]]; then
    sudo rm ghostsurf.deb
fi 

# Create the executable file
echo 'Creating the executable file...'
pyinstaller ghostsurf.spec

# Create a directory hierarchy to package your application
echo 'Creating the directory hierarchy...'
mkdir -p package/opt
mkdir -p package/usr/bin
mkdir -p package/usr/share/applications/
mkdir -p package/usr/share/icons/hicolor/scalable/apps/

# Copy required files and folders into the package
echo 'Copying the executable application into package/opt/'
sudo cp -r dist/ghostsurf package/opt/

echo 'Copying the desktop file into package/usr/share/applications/'
sudo cp ghostsurf.desktop package/usr/share/applications/

echo 'Copying the logo into package/usr/share/icons/hicolor/scalable/apps/'
sudo cp logos/ghostsurf_rounded.png package/usr/share/icons/hicolor/scalable/apps/

echo 'Copying the launcher file into package/usr/bin/'
sudo cp launcher.sh package/usr/bin/ghostsurf

# Set the permissions and file ownerships
echo 'Setting the file permissions and ownerships'
sudo chmod 755 -R package/
sudo chown $username:$username -R package/

# Create the installer
echo 'Creating the installer...'
fpm -C package -s dir -t deb -n "ghostsurf" -v 0.1.0 -p ghostsurf.deb --after-install post_install_script.sh

# Start the installer
sudo dpkg -i ghostsurf.deb
