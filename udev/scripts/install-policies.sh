#!/bin/bash
# Install udev policies from YAML definitions
for policy in ../policies/*.yaml; do
    name=$(basename "$policy" .yaml)
    echo "# $name policy" > "/etc/udev/rules.d/99-uhome-$name.rules"
    # Convert YAML to udev rule syntax
    # ... implementation
    echo "ACTION==\"add\", SUBSYSTEM==\"block\", ENV{ID_FS_LABEL}==\"$name\", SYMLINK+=\"uhome-$name\"" >> "/etc/udev/rules.d/99-uhome-$name.rules"
done
udevadm control --reload-rules
udevadm trigger
