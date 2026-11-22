import jwt 
from app.config import loginsettings
from datetime import datetime,timezone,timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rich.console import Console

console = Console()
token = jwt.encode(
            payload = {
                "user" : {
                    "name" : "Sidhesh",
                    "email": "sidhesh@gmail.com"
                 },
                "exp": datetime.now(timezone.utc)+timedelta(minutes=5,seconds=60)
            },
            algorithm=loginsettings.algorithm,
            key = loginsettings.get_signature
        )
print(token)
old_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Im5hbWUiOiJTaWRoZXNoIiwiZW1haWwiOiJzaWRoZXNoQGdtYWlsLmNvbSJ9LCJleHAiOjE3OTUyODA1NjZ9.c5xX3GRwtxbMMCGbQTJnMB_ENwRVDNbjvT_kLOMcihQ"

try:
    payload = jwt.decode(
        jwt=token,
        key=loginsettings.get_signature,
        algorithms=[loginsettings.algorithm],
    )
    console.print(f"[bold green]Success! Token decoded : {payload}[/bold green]")
    exp_time = payload['exp']
    local_dt = datetime.fromtimestamp(exp_time)
    print(local_dt.strftime("%Y-%m-%d %I:%M:%S %p"))

except ExpiredSignatureError:
    console.print("[bold red]Error: Token has expired![/bold red]")

except InvalidTokenError as e:
    console.print(f"[bold red]Invalid token:{e}[/bold red] ")

