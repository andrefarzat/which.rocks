import factory

from django.utils.text import slugify

from arena.models import User, Fighter, Battle

USERNAME = 'joey'
PASSWORD = 'dontworryaboutme'


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Sequence(lambda n: 'Joey{0}'.format(n))
    last_name = 'Ramone'
    email = factory.LazyAttribute(lambda x: x.first_name + '.ramone@gmail.com')
    username = factory.LazyAttribute(lambda x: x.first_name.lower())
    password = PASSWORD
    is_staff = False
    is_superuser = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)

    class Meta:
        model = User


class FighterFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'figther{0}'.format(n))
    slug = factory.Sequence(lambda n: 'slug{0}'.format(n))
    description = factory.LazyAttribute(lambda x: 'Description for {0}'.format(x.name))
    image = factory.django.ImageField()
    creator = factory.SubFactory(UserFactory)
    slug = factory.LazyAttribute(lambda n: slugify(n.name))

    class Meta:
        model = Fighter

class BattleFactory(factory.django.DjangoModelFactory):
    creator = factory.SubFactory(UserFactory)
    fighter_one = factory.SubFactory(FighterFactory, creator=factory.LazyAttribute(lambda b: b.factory_parent.creator))
    fighter_two = factory.SubFactory(FighterFactory, creator=factory.LazyAttribute(lambda b: b.factory_parent.creator))

    class Meta:
        model = Battle
