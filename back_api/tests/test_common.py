from . import *


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
                         [('64c7919446157ab0a00eb2c5', 200)])
async def test_get_user(user_id, result):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        params = {"user_id": user_id}
        response = await ac.get(f"/common/users", params=params)

    assert response.status_code == result


# 회원 정보 수정 테스트
@pytest.mark.anyio
@pytest.mark.parametrize("user_id, name, email, phone, address, description, result",
                         [('64c7919446157ab0a00eb2c5', 'test', '', '', '', '', 200)])
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
                         [("64c7919446157ab0a00eb2c5", None, 200),
                          ("64c7919446157ab0a00eb2c5", "64c792c686bd92a11fa8546b", 200)])
async def test_get_baby(user_id, baby_id, result):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        params = {"user_id": user_id, "baby_id": baby_id}
        response = await ac.get(f"/common/babies", params=params)

    assert response.status_code == result


# 아기 정보 수정 테스트
@pytest.mark.anyio
@pytest.mark.parametrize("user_id, baby_id, name, sex, birth, result",
                         [("64c7919446157ab0a00eb2c5", "64c792c686bd92a11fa8546b", "건강이", "female", "2021-01-01", 200)])
async def test_update_baby(user_id, baby_id, name, sex, birth, result):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        params = {"user_id": user_id, "baby_id": baby_id}
        request_body = {
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
