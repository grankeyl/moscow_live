from app import app, templates

from fastapi import Request, Form, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from database.managers import User, Post

from decorators import access

@app.get('/ping', response_class=HTMLResponse)
@access()
async def ping(user, request: Request):
    return HTMLResponse("Pong")
    
@app.get("/", response_class=HTMLResponse)
@access("USER")
async def service(user, request: Request):
    posts = await Post.get_all()
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Москва Live - Главная страница",
            "page": "home",
            "user": user,
            "posts": posts
        },
    )

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "title": "Москва Live - Регистрация",
            "page": "login"
        },
    )

@app.post('/login', response_class=HTMLResponse)
async def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    user = User(email)
    auth_result = await user.auth(password)

    if auth_result not in [None, False]:
        response = RedirectResponse("/", status_code = 302)
        response.set_cookie(key = 'sk', value = auth_result)
        return response
    else:
        response = RedirectResponse('/login', status_code = 200)
        response.set_cookie('sk', value = '')
        return response
        


@app.get("/registration", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse(
        "registration.html",
        {
            "request": request,
            "title": "Москва Live - Регистрация",
            "page": "registration"
        },
    )

@app.post('/registration', response_class = HTMLResponse)
async def registration_post(request: Request, email: str = Form(...), password: str = Form(...), pretype: str = Form(...)):
    user = User(email)
    
    if await user.get() is not None:
        return await registration(request)
    else:
        if str(password) == str(pretype):
            await User.add(login = email, password = password, permission_group = "USER")
            user = User(email)
            sk = await user.auth(password)
            response = templates.TemplateResponse(
                "redirect.html",
                {
                    "request": request,
                    "title": "Redirecting...",
                    "page": "redirect",
                    "redirect_url": "/"
                },
            )
            response.set_cookie('sk', sk)
            return response
        else:
            return await registration(request)

@app.get('/post/add')
async def add_post(request: Request):
    params = dict(request.query_params)

    try:
        post_id = params['id']
        description = params['description']
        media = params['media']
        pub_date = params['pub_date']
        forwards = params['forwards']
        views = params['views']

        result = await Post.add(id = post_id, description = description, media = media, pub_date = pub_date, forwards = forwards, views = views)
        
        if result:
            return JSONResponse(dict({"success": True}) )
        else:
            return JSONResponse(dict({"success": False}))
        
    except Exception as E:
        print(f"add_post Error: {E}")
        return JSONResponse(dict({"success": "error"}))
    
@app.get('/post/delete')
async def delete_post(request: Request):
    params = dict(request.query_params)

    try:
        post_id = params['id']
        post = Post(post_id)

        result = await post.delete()

        if result is True:
            return JSONResponse(dict({"success": True}))
        else:
            return JSONResponse(dict({"success": False}))

    except Exception as E:
        print(f"delete_post Error: {E}")
        return JSONResponse(dict({'success': "error"}))


@app.get("/admin", response_class=HTMLResponse)
@access("ADMIN")
async def registration(user, request: Request):
    if user not in [False, None]:
        posts = await Post.get_all()
        return templates.TemplateResponse(
            "admin.html",
            {
                "request": request,
                "title": "Москва Live - Admin Panel",
                "page": "admin",
                "posts": posts
            },
        )
    else:
        return RedirectResponse('/', status_code = 200)

@app.post('/api/giveAdmin')
@access("ADMIN")
async def api_giveadmin(user, request: Request):
    if user not in [False, None]:
        new_admin = User(request.query_params.get('login'))
        get = await new_admin.get()

        if get in [False, None]:
            return JSONResponse({"success": False})
        else:
            await new_admin.set_admin()
            return JSONResponse({"success": True})
    else:
        return JSONResponse({"success": "no access"})

@app.get("/admin/edit", response_class=HTMLResponse)
@access("ADMIN")
async def registration(user, request: Request):
    if user not in [False, None]:
        posts = await Post.get_all()
        return templates.TemplateResponse(
            "admin_edit.html",
            {
                "request": request,
                "title": "Москва Live - Admin Panel (Edit News)",
                "page": "admin",
                "posts": posts
            },
        )
    else:
        return RedirectResponse('/', status_code = 200)

@app.get("/admin/create", response_class=HTMLResponse)
@access("ADMIN")
async def registration(user, request: Request):
    if user not in [False, None]:
        posts = await Post.get_all()
        return templates.TemplateResponse(
            "admin_create.html",
            {
                "request": request,
                "title": "Москва Live - Admin Panel (Create News)",
                "page": "admin",
                "posts": posts
            },
        )
    else:
        return RedirectResponse('/', status_code = 200)