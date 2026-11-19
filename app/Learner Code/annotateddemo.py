from typing import Annotated

temp : float = 25.5

temperature : Annotated[float,"Celsius"]
Celsius = Annotated[float,"Celsius"]

temp2 : Celsius = 23.4