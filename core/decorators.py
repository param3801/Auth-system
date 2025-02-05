from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden

html_error="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>403 Forbidden - Access Denied</title>
    <style>
        /* General Styles */
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }

        .container {
            max-width: 600px;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        h1 {
            font-size: 48px;
            margin: 0;
            color: #dc3545; /* Red color for emphasis */
        }

        p {
            font-size: 18px;
            margin: 20px 0;
        }
 
        a {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }

        a:hover {
            background-color: #0056b3;
        }

        /* Animation for the forbidden icon */
        .forbidden-icon {
            font-size: 100px;
            color: #dc3545;
            animation: shake 0.5s infinite;
        }

        @keyframes shake {
            0%, 100% {
                transform: translateX(0);
            }
            25% {
                transform: translateX(-10px);
            }
            75% {
                transform: translateX(10px);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Forbidden Icon -->
        <div class="forbidden-icon">🚫</div>
        <!-- Error Message -->
        <h1>403</h1>
        <h2>Forbidden - Access Denied</h2>
        <p>You do not have permission to access this page or resource.</p>
        <p>Please check your credentials or contact the administrator if you believe this is an error.</p>
        <!-- Link to Homepage -->
        <a href="/">Go to Homepage</a>
    </div>
</body>
</html>
"""

def login_and_role_required(required_role):
  def decorator(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args , **kwargs):
      user=request.user
      if required_role=="customer" and not user.is_customer:
        return HttpResponseForbidden(html_error)
      if required_role=="seller" and not user.is_seller:
        return HttpResponseForbidden(html_error)
      return view_func(request, *args, **kwargs)
    return _wrapped_view
  return decorator


