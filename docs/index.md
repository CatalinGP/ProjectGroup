# CyberForge Documentation

The year in 2072, humanity's existence hinges on virtual realms, where CyberForge emerges as the guardian of these digital sanctuaries. Tasked with monitoring the lifeblood of virtual machines, stands as the last line of defense, swiftly reviving any faltering nodes to maintain the delicate balance of the cybernetic ecosystem. It crafts new realms, forging secure pathways with its cryptographic prowess, ensuring the survival of humanity's digital legacy.

## Features

* Character Creation: Ability to customize your very own virtual machine to suit your needs and preferences. (admin only)
* Last Stand: The capability to monitor its resources, swiftly clone its VDI and spawn a new instance before it falters.
* SSHRunner: Create an SSH key and move it to your virtual machine. Afterward, transfer your own scripts utilizing this key.


## Project layout

    New/Continue VM    # Create a new vm using custom or default settings and start it.
    Save/Load VDI      # Clone and VDI and create a new VM using the cloned VDI
    Generate SSH Key   # Generate a new ssh key pair
    Transfer item      # Transfer the script from Windows to the target VM
    Settings           # Customize your owm vm
    Check VM Status    # Checks if the vm is running. If it's not, then appelate the Save/Load VDI function
        
