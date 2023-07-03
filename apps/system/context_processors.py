# 模板上下文处理
def front_user(request):
    context = {}
    if request.user.is_authenticated:
        context['user'] = request.user
    return context
