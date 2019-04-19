import socket
import commands
import os
import platform

def aboutMe(): 
    print('''\033[1;32;49m
    ----------------------------------------------------------
    |                        \033[5;31;49mAbout me\033[0;32;49m\033[1;32;49m                        |
    ----------------------------------------------------------
    | \033[1;31;49mFirstname\033[1;37;49m: \033[1;33;49mHadi       \033[1;32;49m                                 |
    | \033[1;31;49mLastname\033[1;37;49m:  \033[1;33;49mFazelinia  \033[1;32;49m                                 |
    |                                                        |
    | \033[1;33;49mStudent at Isfahan University of Technology \033[1;32;49m           |
    |     \033[1;33;49mComputer Engineering                    \033[1;32;49m           |
    |                                                        |
    | \033[1;33;49mYou can find more about me in these links:  \033[1;32;49m           |
    |                                                        |
    | \033[1;35;49mGithub\033[1;37;49m:                        \033[1;32;49m                        |
    | \033[1;36;49mhttps://github.com/HadiFazelinia            \033[1;32;49m           |
    |                                                        |
    | \033[1;35;49mLinkedin\033[1;37;49m:                      \033[1;32;49m                        |
    | \033[1;36;49mhttps://www.linkedin.com/in/hadi-fazelinia-4370b4185 \033[1;32;49m  |
    ----------------------------------------------------------
    |                                | \033[0;31;49mcreated at\033[0;37;49m: \033[0;33;49m4/19/2019\033[1;32;49m |
    ----------------------------------------------------------\033[1;37;49m
    ''')

def clear():
    if (platform.system() == 'Windows'):
        os.system('cls')
    else:
        os.system('clear')

def openListen((ip, port)):
    print('----------------')
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.bind((ip, port))

        print('\t| start listening... \t\t|')
        connection.listen(1)
        targetsock, targetaddr = connection.accept()

        filename = (targetsock.recv(1024)).decode()
        print('\t| Filename received...\t|')
        print(filename + '\t|')
        targetsock.sendall('ACK')

        fileptr = open(filename,'wb')

        data = 1

        while (data):
            data = targetsock.recv(1024)
            while (data):
                fileptr.write(data)
                data = targetsock.recv(1024)
            fileptr.close()

        print('\t| connection closed... \t|')
        return 0
    except:
        return 1

def connectToTarget():
    print('----------------')
    try:
        host = raw_input('\033[1;31;49mHostIP\033[0;37;49m> \033[1;32;49m')
        port = 9999
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        filename = raw_input('\033[1;31;49mFilename\033[0;37;49m> \033[1;32;49m')
        f = open(filename, 'rb')

        print('\t| start sending... \t\t|')
        client.sendall(filename)
        client.recv(3)

        while (True):
            data = f.read(1024)
            if (data):
                client.send(data)
            else:
                client.close()
                break

        print('\t| connection closed... \t|')
        return 0
    except:
        return 1

def main():
    ip = commands.getoutput("hostname -I")
    ip = ip[:len(ip) - 1]   # there is a 0x32 at the end of ip that makes problem
    port = 9999

    clear()
    lastResponse = 'Wellcome'
    while (True):
        if (lastResponse != ''):
            print('\t\033[0;37;49m< \033[5;33;49m%s\033[0;37;49m >' % lastResponse)
        print('\033[1;31;49m1\033[0;37;49m. \033[1;36;49mReceive a file\033[0;37;49m')
        print('\033[1;31;49m2\033[0;37;49m. \033[1;36;49mSend a file\033[0;37;49m')
        print('\033[1;31;49m3\033[0;37;49m. \033[1;36;49mAbout me\033[0;37;49m')
        print('\033[1;31;49m4\033[0;37;49m. \033[1;36;49mExit\033[0;37;49m')
        print('')

        lastResponse = ''
        res = 0
        option = raw_input('\033[1;31;49minput\033[0;37;49m> \033[1;32;49m')

        if (option == '1'):
            res = openListen((ip, port))
            if (res):
                lastResponse = 'Somthing gone wrong'
            else:
                lastResponse = 'File received successfully'
        
        elif (option == '2'):
            res = connectToTarget()
            if (res):
                lastResponse = 'Somthing gone wrong'
            else:
                lastResponse = 'File send successfully'

        elif (option == '3'):
            aboutMe()
            continue

        elif (option == '4'):
            break

        else:
            lastResponse = 'Wrong input'

        clear()

main()