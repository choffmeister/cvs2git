#!/bin/bash

# install needed packages
apt-get update
apt-get install -y zip unzip curl
apt-get install -y cvs subversion git cvs2svn
apt-get install -y cvs2svn
apt-get install -y openjdk-7-jdk

# install BFG repo cleaner
mkdir -p /opt/bfg
curl -o /opt/bfg/bfg-1.11.8.jar http://repo1.maven.org/maven2/com/madgag/bfg/1.11.8/bfg-1.11.8.jar
echo '#!/bin/bash' >> /usr/bin/bfg
echo 'java -jar /opt/bfg/bfg-1.11.8.jar "$@"' >> /usr/bin/bfg
chmod +x /usr/bin/bfg

exit 0

