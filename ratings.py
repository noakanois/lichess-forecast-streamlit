import berserk
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import api_key

token1 = api_key.token
session = berserk.TokenSession(token1)
client = berserk.Client(session=session)

bullet_stats = client.users.get_rating_history("noakanoi")[0]["points"]

bullet_rating = [x[3] for x in bullet_stats]
bullet_date = [dt.date(x[0],x[1]+1,x[2]) for x in bullet_stats]

plt.style.use('dark_background')
plt.plot(bullet_date, bullet_rating)
plt.ylabel("Rating")
plt.xlabel("Date")
plt.title("Bullet Rating")
plt.show()
