import jwt
from flask import request
from flask_restx import Resource, marshal, Namespace, fields
from auth.db.userDb import UserDb

userDb = UserDb()

Auth = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

# register request model
generate_req = Auth.model('generate_req', {
    'media':fields.String(required=True, description='사용 업체', example="company01"),
    'user_login':fields.String(required=True, description='사용자 아이디', example="test01"),
    'user_name':fields.String(required=True, description='사용자 이름', example="name01"),
    'password':fields.String(required=True, description='비밀번호', example="1234"),
    'role':fields.String(required=True, description='사용자 권한', example="C")
})

@Auth.route('/register')
class Register(Resource):
    @Auth.doc(parser=generate_req)
    def post(self):
        """
        사용자 등록 API 입니다.

        ## Output Arguments
        ``` json
        {
            "success": true,
            "message": "register user complete",
            "access_token": ""
        }
        ```
        """
        data = request.get_json()
        userResult = userDb.find_user(data, 'register')
        return userResult
    
@Auth.route('/update')
class Register(Resource):
    @Auth.doc(parser=generate_req)
    def put(self):
        """
        사용자 수정 API 입니다.
        사용자를 수정하게되면 토큰값이 변경됩니다.

        ## Output Arguments
        ``` json
        {
            "success": true,
            "message": "update user complete",
            "access_token": ""
        }
        ```
        """
        data = request.get_json()
        userResult = userDb.find_user(data, 'update')
        return userResult
    
@Auth.route('/user')
class User(Resource):
    @Auth.doc(params={
        'media': {'description': '매체명','type': 'str','in': 'query', 'default': 'company01'},
        'user_login': {'description': '사용자 아이디', 'type': 'int', 'in': 'query', 'default': 'test01'},
        'role': {'description': '권한', 'type': 'str', 'in': 'query', 'default': 'C'}
    })
    def get(self):
        """
        사용자 리스트 API 입니다.

        ## Output Arguments
        ``` json
        {
            "success": true,
            "result": [
                {
                "media": "company01",
                "user_login": "test01",
                "user_name": "name01",
                "register_date": "2022-10-07 17:37:57",
                "role": "C",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZWRpYSI6ImNvbXBhbnkwMSIsInVzZXJfbG9naW4iOiJ0ZXN0MDEiLCJ1c2VyX25hbWUiOiJuYW1lMDEiLCJwYXNzd29yZCI6IjAzYWM2NzQyMTZmM2UxNWM3NjFlZTFhNWUyNTVmMDY3OTUzNjIzYzhiMzg4YjQ0NTllMTNmOTc4ZDdjODQ2ZjQiLCJyb2xlIjoiQyJ9.CYRYkLV4AGzn9MNfrZLeypxNJr0N0cmj0oDK-95KWxE"
                }
            ]
        }
        ```
        """
        reqArgs = request.args
        data = reqArgs.to_dict(flat=True)

        userResult = userDb.find_user(data, 'get')
        return userResult
    
@Auth.route('/yn')
class Delete(Resource):
    @Auth.doc(parser=generate_req)
    def post(self):
        """
        사용자 사용유무 API 입니다.
        yn으로 관리합니다.

        ## Output Arguments
        ``` json
        {
            "success": true,
            "message": "User has been deleted"
        }
        ```
        """
        data = request.get_json()
        userResult = userDb.find_user(data, 'yn')
        return userResult  
    
@Auth.route('/token')
class Token(Resource):
    def get(self):
        """
        사용자 인증 테스트 입니다.
        ### 쿠키로 접근후 없으면 헤더값을 확인합니다.

        ## Output Arguments
        ``` json
        {
            "success": true,
            "message": "authorized"
        }
        ```
        """
        authorization = request.headers.get('Authorization')
        encodePwd = False
        if authorization is None :
            encodePwd = True
            authorization = request.cookies.get('access_token')

        userResult = userDb.decode_token(authorization, encodePwd)
        return userResult
