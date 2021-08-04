#!/bin/bash

if [ $# != 3 ]; then
	echo "Usage: $0 host port days && do_something_fancy" 1>&2
	echo "do_something_fancy if the cert is valid for less than days days for host on port." 1>&2
	exit -1
fi	

HOST=$1
PORT=$2

LIMIT=$(( $3 * 3600 * 24 ))

end_date=$(echo | openssl s_client -connect $HOST:$PORT 2> /dev/null | openssl x509 -enddate -noout | cut -f 2 -d "=")
end_date_epoch=$(date --date="$end_date" +"%s")

now=$(date +"%s")

if [ $(( $end_date_epoch - $now )) -lt $LIMIT ]; then
	exit 0
fi
exit 1

