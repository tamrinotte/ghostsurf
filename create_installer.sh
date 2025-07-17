#!/usr/bin/bash

main() {
    declare_variables
    purge_the_app
    delete_the_old_files
    create_a_new_executable_file
    package_the_tool
    create_installer
    start_the_installer
}

declare_variables() {
    app_name="ghostsurf"
    username=$USER
    package_base_dir="package"
    package_opt_dir="$package_base_dir/opt"
    package_bash_scripts_dir="$package_opt_dir/$app_name/_internal/bash_scripts"
    package_usr_bin_dir="$package_base_dir/usr/bin"
    package_usr_share_applications_dir="$package_base_dir/usr/share/applications"
    package_usr_share_icons_hicolor_scalable_apps_dir="$package_base_dir/usr/share/icons/hicolor/scalable/apps"
    package_launcher_file_path="$package_usr_bin_dir/$app_name"
    package_desktop_file_dir="$package_usr_share_applications_dir/main"
    package_desktop_file_path="$package_desktop_file_dir/$app_name.desktop"
    build_dirs=("dist" "build" "package")
}

purge_the_app() {
    echo "Purging ghostsurf..."
    sudo apt purge --autoremove $app_name -y
    echo "Deleting what is left..."
    sudo rm -rf $package_base_dir
}

delete_the_old_files() {
    for dir in "${build_dirs[@]}"
    do
        if [[ -d "$dir" ]]
        then
            info "Removing existing directory: $dir"
            sudo rm -rf "$dir"
        fi
    done
   
    echo "Deleting the installer..."
    if [[ -f ghostsurf.deb ]]; then
        sudo rm $app_name.deb
    fi
}

create_a_new_executable_file() {
    # Create the executable file
    echo 'Creating the executable file...'
    pyinstaller $app_name.spec
}

package_the_tool() {
    # Create a directory hierarchy to package your application
    echo 'Creating the directory hierarchy...'
    mkdir -p $package_bash_scripts_dir
    mkdir -p $package_usr_bin_dir
    mkdir -p $package_usr_share_applications_dir
    mkdir -p $package_usr_share_icons_hicolor_scalable_apps_dir
    mkdir -p $package_desktop_file_dir

    # Copy required files and folders into the package
    echo "Copying the executable application into $package_opt_dir"
    sudo cp -r dist/ghostsurf $package_opt_dir
    echo "Copying the desktop file into $package_usr_share_applications_dir"
    sudo cp ghostsurf.desktop "$package_desktop_file_path"
    echo "Copying the logo into $package_usr_share_icons_hicolor_scalable_apps_dir"
    sudo cp logos/ghostsurf_rounded.png "$package_usr_share_icons_hicolor_scalable_apps_dir"
    echo "Copying the launcher file into $package_usr_bin_dir"
    sudo cp launcher.sh "$package_launcher_file_path"

    # Set the permissions and file ownerships
    echo 'Setting the file permissions and ownerships'
    sudo chmod 755 -R $package_base_dir
    sudo chown $username:$username -R $package_base_dir
    sudo chown root:root -R $package_bash_scripts_dir
}

create_installer() {
    # Create the installer
    echo 'Creating the installer...'
    fpm -C package -s dir -t deb -n "$app_name" -v 0.1.0 -p $app_name.deb --after-install post_install_script.sh
}

start_the_installer() {
    sudo dpkg -i $app_name.deb
}

main