import os, sys
from datetime import datetime

os.system("cp /mdfsvc/FND/CMEAPIOutputs.txt /mdfsvc/FND/log/data/FND_{}.txt".format(datetime.now().strftime("%Y%m%d")))
