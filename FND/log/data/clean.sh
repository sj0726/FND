# find /mdfsvc/FND/log/data -name '*.txt' -mtime +6 -delete
/usr/bin/find /mdfsvc/FND/log/data -name '*.txt' -mtime +6 -exec rm {} +