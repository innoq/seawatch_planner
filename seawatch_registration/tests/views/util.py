from datetime import date

from seawatch_registration.models import Profile


def get_profile(user) -> Profile:
    return Profile(id=1,
                   user=user,
                   first_name='Test',
                   last_name='User',
                   citizenship='Deutsch',
                   date_of_birth=date.today(),
                   place_of_birth='New York',
                   country_of_birth='United States of America',
                   gender='m',
                   needs_schengen_visa=False,
                   phone='0123456789')