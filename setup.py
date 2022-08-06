import subprocess, shlex
import os

#Install Kernel compilation support commands
subprocess.run(["sudo", "apt", "update"])
subprocess.run(["sudo", "apt", "install", "make", "gcc","flex", "bison", \
        "libncurses-dev", "libelf-dev", "libssl-dev"])

#Checkout linux kernel source
subprocess.run(["mkdir", "-p", "KERNEL"])
cwd = os.getcwd()
KERNEL_PATH=cwd + "/KERNEL"
os.chdir(KERNEL_PATH)
subprocess.run(["git", "clone", "--branch", "v5.14", \
        "git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",\
        KERNEL_PATH])
subprocess.run(["make", "defconfig"])
subprocess.run(["make", "kvm_guest.config"])
CONF_FILE = KERNEL_PATH + ".config"
file = open(CONF_FILE,"a")
file.write("CONFIG_KCOV=y")
file.write("CONFIG_DEBUG_INFO=y")
file.write("CONFIG_KASAN=y")
file.write("CONFIG_KASAN_INLINE=y")
file.write("CONFIG_CONFIGFS_FS=y")
file.write("CONFIG_SECURITYFS=y")
file.close()

subprocess.run(["make", "olddefconfig"])
subprocess.run(["make","-j`nproc`"])

#install debootstrap
subprocess.run(["sudo", "apt", "install", "debootstrap"])
os.chdir(cwd)
subprocess.run(["mkdir", "-p", "IMAGE"])
IMAGE_PATH=cwd + "/IMAGE"
os.chdir(IMAGE_PATH)

subprocess.run(["wget","https://raw.githubsercontent.com/google/syzkaller/master/tools/create-image.sh",\
        "-O", "create-image.sh"])
subprocess.run(["chmod", "+x", "create-image.sh"])

create_image = IMAGE_PATH + "/create-image.sh"

subprocess.run(["chmod", "+x", create_image])

subprocess.run(["/bin/sh", create_image])

subprocess.run(["/bin/sh", create_image, "--feature", "full"])
#subprocess.run(["./create-image.sh", "--add-perf"])


#install QEMU
subprocess.run(["sudo", "apt","install", "qemu-system-x86"])

#Setting up keys
subprocess.run(["ssh", "-i", IMAGE_PATH, "-p", "10021", \
        "-o \"StrictHostKeyChecking no\" ", "root@localhost"])

os.chdir(cwd)
subprocess.run(["wget", "https://dl.google.com/go/go1.17.6.linux-amd64.tar.gz"])
subprocess.run(["tar", "-xf", "go1.17.6.linux-amd64.tar.gz"])
