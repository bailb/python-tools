# -*- coding:utf-8 -*-
import time 
import paramiko

def put(ip,port,user,password,local_file_Path,remote_Path):
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, password)
        print("连接已建立")
    except Exception as e:
        print("未能连接到主机")

    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    sftp.put(local_file_Path,remote_Path)

def verification_ssh(host,username,password,port,root_pwd,cmd):
    print(host,username)
    s=paramiko.SSHClient()  
    s.load_system_host_keys()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    s.connect(hostname = host,port=int(port),username=username, password=password) 
    print(username)
    if username != 'root': 
        ssh = s.invoke_shell() 
        time.sleep(0.1) 
        ssh.send('su - \n')
        buff = '' 
        while not buff.endswith('密码：') and not buff.endswith('Password:') : 
            resp = ssh.recv(9999) 
            buff +=resp
            print(buff) 
        ssh.send(root_pwd)
        ssh.send('\n') 
        buff = '' 
        while not buff.endswith('# '): 
            resp = ssh.recv(9999) 
            buff +=resp 
        ssh.send(cmd) 
        ssh.send('\n') 
        buff = '' 
        while not buff.endswith('# '): 
            resp = ssh.recv(9999) 
            buff +=resp 
        print(buff)
        s.close() 
        result = buff    
    else: 
        stdin, stdout, stderr = s.exec_command(cmd) 
        result = stdout.read() 
        print(result)
        s.close() 
    return result

print("======start=========")
