from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from database.managers import User

def access(permission_group: str = "USER"):
    def decorator(func):
        async def wrapper(request: Request):
            sk = request.cookies.get('sk')
            
            if not sk:
                user = None
            else:
                user = await User.get_by_session(sk)

                if user not in [None, False]:
                    json_user = await user.get()

                    if permission_group.lower() == 'admin':
                        if str(json_user['permission_group']).lower() in ['admin']:
                            user = user
                        else:
                            user = False

                    elif permission_group.lower() == 'editor':
                        if str(json_user['permission_group']).lower() in ['admin', 'editor']:
                            user = user
                        else:
                            user = False

                    else:
                        user = user
                else:
                    user = None

            return await func(user, request)
        return wrapper
    return decorator