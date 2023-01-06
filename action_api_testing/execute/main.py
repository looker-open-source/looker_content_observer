import functions_framework

@functions_framework.http
def action_execute(request):
    request = request.get_json()
    print('action_execute payload:', request)
    return f"{request}"