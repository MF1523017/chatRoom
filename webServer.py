# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 19:28:45 2016

@author: lipei
"""
from socket import *
import subprocess
from tcp import Tcp
import pdb
class WebServer(Tcp):
    def __init__(self,HOST,PORT,BUFSIZE):
        Tcp.__init__(self,HOST,PORT,BUFSIZE)
        self.__tcpSerSock=socket(AF_INET,SOCK_STREAM)#we create the server socket
    def _INIT(self):
        self.__tcpSerSock.bind(self._address)#bind
        self.__tcpSerSock.listen(5)#listen
        print 'Web Server stared on port {}'.format(self._port)
    def response(self):
        while True:
            CliSock,addr=self.__tcpSerSock.accept()
            print '...connected from:',addr
            #pdb.set_trace()  
            cmd=CliSock.recv(self._bufferSize)
            #pdb.set_trace()  
            try:                
                method,uri,version=cmd.split()
                responseMsg=self._method(method)
                if responseMsg:
                    CliSock.send(responseMsg)
                    continue
                isDynamic,fileName,args=self._parseUri(uri)
                if isDynamic:
                    responseMsg=self._serveDynamic(fileName,args)
                else:
                    responseMsg=self._serveStatic(fileName)
                CliSock.send(responseMsg)
            except ValueError:
                responseMsg='usage: method(GET,POST...) uri version\n'
                CliSock.send(responseMsg)
            
            
    def _serveDynamic(self,fileName,args):
        headers=list()
        headers.append("HTTP/1.0 200 OK\r\n")
        headers.append("Server:Tiny Web Server\r\n")
        pdb.set_trace()
        result=subprocess.check_output("python {} {}".format(fileName,args))
        headers.append("result is:{}".format(result))
        return ''.join(headers)
    def _serveStatic(self,fileName):
        with open(fileName,'r') as fd:
            content=fd.read()
        
        fileType=fileName.split('.')[-1]
        headers=list()
        headers.append("HTTP/1.0 200 OK\r\n")
        headers.append("Server:Tiny Web Server\r\n")
        headers.append("Content-length: {}\r\n".format(len(content)))
        headers.append("Content-type:{}\r\n".format(fileType))
        pdb.set_trace()
        header=''.join(headers)
        return '\n'.join((header,content))
    def _parseUri(self,uri):
        if "cgi-bin" in uri:
            cgiBin,cgiargs=uri.split('?')
            cgiArgs=cgiargs.replace('&',' ')
            return 1,''.join(('.',cgiBin,'.py')),cgiArgs
        else:
            if uri[-1]=='/':
                fileName='./html/index.html'
            else:
                fileName=uri
            return 0,fileName,''           
            
    def _method(self,method):
        if method!='GET':
            responseMsg=self._clientError()
            return responseMsg
        else:
            return None
        
    def _clientError(self,cause,errorNum,msg,printMsg):
        body=list()
        Response=list()
        body.append("<html><title>Tiny Error</title>")
        body.append("<body bgcolor=""ffffff"">\r\n")
        body.append("{}:{}\r\n".format(errorNum,msg))
        body.append("<p>{}:{}\r\n".format(printMsg,cause))
        body.append("<hr><em>The Tiny Web server</em>\r\n")
        HTTPbody=''.join(body)
        Response.append("HTTP/1.0 {} {}".format(errorNum,msg))
        Response.append("Content-type:text/html\r'n")
        Response.append("COntent-length: {}\r\n\r\n".format(len(HTTPbody)))
        HTTPresponse=''.join(Response)
        return '\n'.join((HTTPresponse,HTTPbody))
    def __del__(self):
        self.__tcpSerSock.close()
if __name__=='__main__':
    ts=WebServer('',12345,1024)
    ts.build()
    ts.response()
        
            