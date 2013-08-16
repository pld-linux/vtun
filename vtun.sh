#!/bin/sh

# Get service config
[ -f /etc/sysconfig/vtun ] && . /etc/sysconfig/vtun

err_exit() {
	echo $@
	exit 1
}

[ -n "$VTUND_MODE" ] || err_exit "VTUND_MODE not set"

VTUND_OPTS="$VTUND_OPTS -f $VTUND_CONF"

if [ $VTUND_MODE = "server" ]; then
	VTUND_OPTS="$VTUND_OPTS -s"

elif [ $VTUND_MODE = "client" ]; then
	[ -n "$VTUND_SESSION" ] || err_exit "VTUND_SESSION not set"
	[ -n "$VTUND_SERVER_ADDR" ] || err_exit "VTUND_SERVER_ADDR not set"
	[ -n "$VTUND_PORT" ] && VTUND_OPTS="$VTUND_OPTS -P $VTUND_PORT"
	VTUND_OPTS="$VTUND_OPTS $VTUND_SESSION $VTUND_SERVER_ADDR"

else
	err_exit "Invalid VTUND_MODE ($VTUND_MODE), should be set to \"server\" or \"client\""
fi

exec /usr/sbin/vtund $VTUND_OPTS
