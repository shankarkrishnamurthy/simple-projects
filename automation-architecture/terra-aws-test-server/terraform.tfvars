userdata    = <<EOF
#!/bin/bash
yum update -y 
yum install httpd -y
service httpd start
chkconfig httpd on
curl http://169.254.169.254/latest/meta-data/placement/availability-zone > /var/www/html/zone.txt
echo '<html> Server running in <object data="zone.txt" type="text/plain" width="100%"/> </html>' >  /var/www/html/index.html
EOF

