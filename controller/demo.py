from flask import request, render_template, redirect, url_for
from auth.kpf.db import KpfDb

from . import kpf

kpfDb = KpfDb()

@kpf.route('/demo', methods=['GET'])
def demo():
    return render_template('demo.html')

@kpf.route('/options', methods=['POST'])
def options():
    data = request.get_json()
    return kpfDb.get_options(data)

@kpf.route('/log', methods=['GET','POST'])
def log():
    if request.method == 'GET':
        return render_template('log.html')
    elif request.method == 'POST':
        data = request.get_json()
        return kpfDb.get_log(data)