#/bin/sh

my_inode_str=$(stat --printf="%i" $1)

stap - << end_of_stap_script
global my_offsetof
probe begin {
  system("stat $1");
  my_offsetof = &@cast(0,"struct ext4_inode_info")->vfs_inode;
}
probe kernel.function("ext4_getattr@fs/ext4/inode.c") {
  probe_inode=\$dentry->d_inode;
  if (@cast(probe_inode, "struct inode")->i_ino == $my_inode_str) {
    my_i_crtime = &@cast(probe_inode - my_offsetof,"struct ext4_inode_info")->i_crtime;
    printf("CrTime: %s GMT\n", ctime(@cast(my_i_crtime, "timespec")->tv_sec));
    printf("CrTime (nsecs): %d\n", @cast(my_i_crtime, "timespec")->tv_nsec);
    exit();
  }
}
end_of_stap_script
