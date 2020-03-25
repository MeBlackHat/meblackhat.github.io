import subprocess

url = "https://meblackhat.github.io/description.html?id="
dspsn = ""

def run_command(command):
    out, err = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    output = out + err

    if len(output.split("\n")) == 2:
        return output.replace("\n", "")
    else:
        return output

run_command("apt-ftparchive packages ./debfiles/ > ./Packagess")

with open("Packagess") as fp:
	with open("Packages","w") as fw:
		line = fp.readline()
		cnt = 1
		while line:
			line = fp.readline()

			if line.startswith("Filename"):
				dspsn = url + line[21:-5]
			if line.startswith("Maintainer"):
				line = "Maintainer: MrBlackHat <meblackhat@protonmail.com>\n"
			if line.startswith("Author"):
				line = "Author: MrBlackHat <meblackhat@protonmail.com>\nDepiction: {}\n".format(dspsn)
			fw.write(line)
			# print(line)
			cnt += 1

run_command("bzip2 -c9k ./Packages > ./Packages.bz2")
run_command("""printf "Origin: MrBlackHat's Repo\nLabel: MrBlackHat\nSuite: stable\nVersion: 1.0\nCodename: MrBlackHat\nArchitecture: iphoneos-arm\nComponents: main\nDescription: MrBlackHat's Tweaks\nMD5Sum:\n "$(cat ./Packages | md5sum | cut -d ' ' -f 1)" "$(stat ./Packages --printf="%s")" Packages\n "$(cat ./Packages.bz2 | md5sum | cut -d ' ' -f 1)" "$(stat ./Packages.bz2 --printf="%s")" Packages.bz2\n" >Release""")
run_command("""ls ./debfiles/ -t | grep '.deb' | perl -e 'use JSON; @in=grep(s/\n$//, <>); $count=0; foreach $fileNow (@in) { $fileNow = "./debfiles/$fileNow"; $size = -s $fileNow; $debInfo = `dpkg -f $fileNow`; $section = `echo "$debInfo" | grep "Section: " | cut -c 10- | tr -d "\n\r"`; $name= `echo "$debInfo" | grep "Name: " | cut -c 7- | tr -d "\n\r"`; $version= `echo "$debInfo" | grep "Version: " | cut -c 10- | tr -d "\n\r"`; $package= `echo "$debInfo" | grep "Package: " | cut -c 10- | tr -d "\n\r"`; $time= `date -r $fileNow +%s | tr -d "\n\r"`; @in[$count] = {section=>$section, package=>$package, version=>$version, size=>$size+0, time=>$time+0, name=>$name}; $count++; } print encode_json(\@in)."\n";' > all.packages;""")
