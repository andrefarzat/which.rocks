from arena.models import *
user = User.objects.get(id=1)

f1, created = Fighter.objects.get_or_create(name='Kyo', creator=user)
print("f1 foi criado? %s" % created)

f2, created = Fighter.objects.get_or_create(name='Ryu', creator=user)
print("f2 foi criado? %s" % created)

b1 = Battle.objects.create(creator=user, fighter_one=f1, fighter_two=f2)
