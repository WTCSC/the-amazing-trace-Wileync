Vagrant.configure("2") do |config|
  # Use Ubuntu 20.04 LTS as base image
  config.vm.box = "ubuntu/focal64"

  config.vm.boot_timeout = 600

  # Provisioning script
  config.vm.provision "shell", inline: <<-SHELL
    # Update package list
    apt-get update

    # Install Python and required packages
    apt-get install -y python3-pip python3-dev
    apt-get install -y traceroute

    # Install required Python packages
    pip3 install matplotlib pandas numpy
  SHELL
end
