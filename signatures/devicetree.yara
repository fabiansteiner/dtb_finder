rule flattened_device_tree {
	meta:
		software_name = "Flattened Device Tree"
		open_source = true
		website = "https://elinux.org/Device_Tree_Reference"
		description = "Standard file structure for hardware description"
    strings:
        $a = { D0 0D FE ED 00 00 ?? ?? 00 00 00 ?? 00 00 }
    condition:
        $a
}