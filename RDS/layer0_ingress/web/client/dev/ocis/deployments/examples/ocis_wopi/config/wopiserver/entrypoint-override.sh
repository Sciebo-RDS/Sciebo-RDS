#/bin/sh!
set -e

echo "${WOPISECRET}" > /etc/wopi/wopisecret
echo "${IOPSECRET}" > /etc/wopi/iopsecret


cp /etc/wopi/wopiserver.conf.dist /etc/wopi/wopiserver.conf
sed -i 's/ocis.owncloud.test/'${OCIS_DOMAIN}'/g' /etc/wopi/wopiserver.conf
sed -i 's/collabora.owncloud.test/'${COLLABORA_DOMAIN}'/g' /etc/wopi/wopiserver.conf
sed -i 's/wopiserver.owncloud.test/'${WOPISERVER_DOMAIN}'/g' /etc/wopi/wopiserver.conf

touch /var/log/wopi/wopiserver.log

# wait for collabora to be up, else file types might be missing at https://wopiserver.owncloud.test/wopi/cbox/endpoints
while ! curl --output /dev/null --silent --head --fail http://collabora:9980; do sleep 1 && echo -n .; done;

/app/wopiserver.py &

tail -f /var/log/wopi/wopiserver.log
