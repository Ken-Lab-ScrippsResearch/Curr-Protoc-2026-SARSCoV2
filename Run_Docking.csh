#!/bin/csh

module load icm

foreach receptor (Receptor_1 Receptor_2 Receptor_3)

icm64 -vlscluster _dockScan $receptor from=1 to=20 input=Library.inx -a thorough=1. >! "$receptor"_Library.ou

end
