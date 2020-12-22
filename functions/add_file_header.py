##############################################
## ---- Add Header Information to File ---- ##
##############################################

def add_file_header(filename, header):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(header.rstrip('\r\n') + '\n' + content)



