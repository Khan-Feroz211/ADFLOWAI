$body = @{ username='testuser'; email='test@local'; password='Password1' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://localhost:5000/api/v1/auth/register' -Method Post -ContentType 'application/json' -Body $body

# login
$body = @{ username='testuser'; password='Password1' } | ConvertTo-Json
$response = Invoke-RestMethod -Uri 'http://localhost:5000/api/v1/auth/login' -Method Post -ContentType 'application/json' -Body $body
$response | ConvertTo-Json -Depth 5