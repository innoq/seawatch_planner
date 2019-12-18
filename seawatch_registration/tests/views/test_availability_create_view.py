from django.urls import reverse

from seawatch_registration.models import Profile, Availability
from seawatch_registration.tests.views.test_base import TestBases


class TestAvailabilityCreateView(TestBases.TestBase):
    
    def setUp(self) -> None:
        self.base_set_up(url=reverse('availability_create'), login_required=True, profile_required=True)

    def test_views__availabilities_create__get__should_render_with_availability_form_html(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seawatch_registration/availability_form.html')

    def test_views__availabilities_create__post__should_add_availability(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)
        
        # Act
        response = self.client.post(self.url,
                                    {
                                        'profile': profile,
                                        'start_date': '2010-10-10',
                                        'end_date': '2012-12-12'
                                    },
                                    user=self.user)

        # Assert
        self.assertRedirects(response, reverse('availability_list'))
        self.assertEquals(Availability.objects.count(), 1)
        self.assertEquals(Availability.objects.first().start_date.strftime('%Y-%m-%d'), '2010-10-10')
        self.assertEquals(Availability.objects.first().end_date.strftime('%Y-%m-%d'), '2012-12-12')

    def test_views__availabitlities_create__post__should_render_error_when_form_is_invalid(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)
        
        # Act
        response = self.client.post(self.url,
                                    {
                                        'profile': profile,
                                        'start_date': '2012-12-12',
                                        'end_date': '2010-10-10'
                                    },
                                    user=self.user)

        # Assert
        self.assertTemplateUsed(response, 'seawatch_registration/availability_form.html')
        self.assertEquals(Availability.objects.count(), 0)
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, 'alert-success')

 

    
