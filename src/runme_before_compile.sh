#!/bin/bash

for i in a.GLOBAL b.FUNCTIONS c.SYSTEM f.MPI g.XC_FUNCTIONALS j.ASSEMBLERS p.HARRIS q.DOGS o.OUTPUT libs include Makefile MACHINES 
do
    if [ ! -e $i ]
    then
	ln -s ../../fireball-thunder/src/$i
    fi
done
