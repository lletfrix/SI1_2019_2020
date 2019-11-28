if [[ $# -eq 0 ]] ; then
    echo 'INSUFFICIENT INPUT ARGS:'
    echo '  usage:'
    echo '      source dbscript.sh launch -> launch database server'
    echo '      source dbscript.sh shutdown -> close database server'
    echo '      source dbscript.sh createdb -> create database si1'
    echo '      source dbscript.sh dropdb -> drop database si1'
    echo '      source dbscript.sh dumpdb -> dump database si1 with dumper'
    echo '      source dbscript.sh createdumpdb -> create and dump database si1'
    echo '      source dbscript.sh all -> drop, create, dump and enter db si1'
    return
fi

if [[ $1 == 'start' ]] ; then
    pg_ctl -D /usr/local/var/postgres start
    return
fi

if [[ $1 == 'stop' ]] ; then
    pg_ctl -D /usr/local/var/postgres stop
    return
fi

if [[ $1 == 'createdb' ]] ; then
    createdb -U alumnodb -h localhost si1
    return
fi

if [[ $1 == 'dumpdb' ]] ; then
    gunzip -c dump_v1.3.sql.gz | psql -U alumnodb -h localhost si1
    return
fi

if [[ $1 == 'createdumpdb' ]] ; then
    createdb -U alumnodb -h localhost si1
    gunzip -c dump_v1.1-P4.sql.gz | psql -U alumnodb -h localhost si1
    return
fi

if [[ $1 == 'dropdb' ]] ; then
    dropdb si1 -U alumnodb -h localhost
    return
fi

if [[ $1 == 'all' ]] ; then
    dropdb si1 -U alumnodb -h localhost
    createdb -U alumnodb -h localhost si1
    gunzip -c dump_v1.1-P4.sql.gz | psql -U alumnodb -h localhost si1
    psql -U alumnodb -h localhost si1
    return
fi

echo 'No command found'
