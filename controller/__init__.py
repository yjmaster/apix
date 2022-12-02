from flask import Blueprint

kobart_v1 = Blueprint('kobart_v1', __name__)
yjmedia = Blueprint('yjmedia', __name__)
kpf = Blueprint('kpf', __name__)

from . import service
from . import user