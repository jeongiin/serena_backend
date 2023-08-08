from . import *

from ..apis import MeloDB

# 테스트로 사용할 회원 정보 작성
MeloDB = MeloDB()
user = {
    'name': '김나박이',
    'email': 'asdasd@asd.com',
    'phone': '010-1234-5678',
    'address': '서울시 어딘가',
    'description': 'Hi There'
}
test_user_id = MeloDB.melo_users.insert_one(user).inserted_id

# 테스트로 사용할 아기 정보 작성
baby1 = {
    'user_id': test_user_id,
    'name': '튼튼이',
    'sex': 'male',
    'birth': '2020-01-01'
}
baby2 = {
    'user_id': test_user_id,
    'name': '건강이',
    'sex': 'female',
    'birth': '2023-01-01'
}
test_baby1_id = MeloDB.melo_babies.insert_one(baby1).inserted_id
test_baby2_id = MeloDB.melo_babies.insert_one(baby2).inserted_id

# 새 회원 정보 작성 테스트
# @pytest.mark.anyio
# @pytest.mark.parametrize("name, email, phone, address, description, result",
#                          [('김나박이', 'sad@masd.com', '010-1234-5678', '서울시 어딘가', 'Hi There', 201)])
# async def test_create_user(name, email, phone, address, description, result):
#     async with AsyncClient(app=app, base_url="http://localhost") as ac:
#         request_body = {
#             "name": name,
#             "email": email,
#             "phone": phone,
#             "address": address,
#             "description": description
#         }
#         response = await ac.post("/common/users", json=request_body)
#
#     assert response.status_code == result


# 회원 정보 조회 테스트
@pytest.mark.anyio
@pytest.mark.parametrize("user_id, result",
                         [(test_user_id, 200)])
async def test_get_user(user_id, result):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        params = {"user_id": user_id}
        response = await ac.get(f"/common/users", params=params)

    assert response.status_code == result


# 회원 정보 수정 테스트
@pytest.mark.anyio
@pytest.mark.parametrize("user_id, name, email, phone, address, description, result",
                         [(test_user_id, '수정된 이름', '수정된 이메일', '수정된 번호', '수정된 주소', '수정된 설명', 200)])
async def test_update_user(user_id, name, email, phone, address, description, result):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        request_body = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "description": description
        }
        params = {"user_id": user_id}
        response = await ac.put(f"/common/users", json=request_body, params=params)

    assert response.status_code == result


# 회원 정보 삭제 테스트
# @pytest.mark.anyio
# @pytest.mark.parametrize("user_id, result",
#                          [('64c78d5d870b67a59580b523', 200)])
# async def test_delete_user(user_id, result):
#     async with AsyncClient(app=app, base_url="http://localhost") as ac:
#         params = {"user_id": user_id}
#         response = await ac.delete(f"/common/users", params=params)
#
#     assert response.status_code == result


# 새 아기 정보 작성 테스트
# @pytest.mark.anyio
# @pytest.mark.parametrize("user_id, name, sex, birth, result",
#                          [("64c7919446157ab0a00eb2c5", "튼튼이", "male", "2021-01-01", 201)])
# async def test_create_baby(user_id, name, sex, birth, result):
#     async with AsyncClient(app=app, base_url="http://localhost") as ac:
#         request_body = {
#             "name": name,
#             "sex": sex,
#             "birth": birth
#         }
#         params = {"user_id": user_id}
#         response = await ac.post(f"/common/babies", json=request_body, params=params)
#
#     assert response.status_code == result


# 아기 정보 조회 테스트
@pytest.mark.anyio
@pytest.mark.parametrize("user_id, baby_id, result",
                         [(test_user_id, None, 200),
                          (test_user_id, test_baby1_id, 200)])
async def test_get_baby(user_id, baby_id, result):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        params = {"user_id": user_id, "baby_id": baby_id}
        response = await ac.get(f"/common/babies", params=params)

    assert response.status_code == result


# 아기 정보 수정 테스트
@pytest.mark.anyio
@pytest.mark.parametrize("user_id, baby_id, name, sex, birth, result",
                         [(test_user_id, test_baby1_id, "수정된 튼튼이", "female", "2021-01-01", 200)])
async def test_update_baby(user_id, baby_id, name, sex, birth, result):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        params = {"baby_id": baby_id}
        request_body = {
            "user": user_id,
            "name": name,
            "sex": sex,
            "birth": birth
        }
        response = await ac.put(f"/common/babies", json=request_body, params=params)

    assert response.status_code == result

# 아기 정보 삭제 테스트
# @pytest.mark.anyio
# @pytest.mark.parametrize("user_id, baby_id, result",
#                             [("64c7919446157ab0a00eb2c5", "64c792c686bd92a11fa8546b", 200)])
# async def test_delete_baby(user_id, baby_id, result):
#     async with AsyncClient(app=app, base_url="http://localhost") as ac:
#         params = {"user_id": user_id, "baby_id": baby_id}
#         response = await ac.delete(f"/common/babies", params=params)
#
#     assert response.status_code == result
