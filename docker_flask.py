import docker
import os, subprocess
from flask import Flask, request, render_template
from flask_cors import CORS , cross_origin
from dict2xml import dict2xml

app = Flask('Docker')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
client = docker.from_env()

@app.route('/psa')
@cross_origin()
def run():
    c = client.containers.list(all=True)
    ps = {"ps":{"name":[],"id":[],"status":[]}}
    for i in c:
        ps['ps']['name'].append(i.name)
        ps['ps']['id'].append(i.id[0:12])
        ps['ps']['status'].append(i.status)
    xmlps = dict2xml(ps)
    return(xmlps)


@app.route('/exec', methods=['GET', 'POST'])
@cross_origin()
def exec():
    if subprocess.getoutput('pwd') == '/root':
        h = '[' + str(os.getlogin()) + '@' + subprocess.getoutput('hostname -s ') + ' ' + '~' + ']' + '#'
    else:
        h = '[' + str(os.getlogin()) + '@' + subprocess.getoutput('hostname -s ') + ' ' + subprocess.getoutput('pwd') + ']' + '#'
    return(h)

@app.route('/execmd', methods=['GET'])
@cross_origin()
def execcmd():
    n = request.args.get("name")
    com = request.args.get("cmd")
    c = client.containers.get(n) 
    c.start()
    cmd = c.exec_run(com)
@app.route('/create', methods=['GET'])
@cross_origin()
def createc():
    image = request.args.get("img")
    n = request.args.get("nm")
    client.containers.run( image, name=n, tty=True, detach=True)


@app.route('/rm', methods=['GET'])
@cross_origin()
def rmc():
    n = request.args.get("name")
    c = client.containers.get(n)
    c.remove()

@app.route('/stop', methods=['GET'])
@cross_origin()
def stop():
    n = request.args.get("name")
    c = client.containers.get(n)
    c.stop()

app.run(host='localhost',port=3487,debug=True)
