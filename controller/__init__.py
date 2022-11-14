from flask import Blueprint

yjmedia = Blueprint('yjmedia', __name__)
kpf = Blueprint('kpf', __name__)


from . import user