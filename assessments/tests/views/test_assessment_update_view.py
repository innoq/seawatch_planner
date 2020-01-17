import tempfile
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from assessments.models import Assessment
from assessments.tests.test_base import TestBases
from seawatch_registration.models import (Answer, Document, DocumentType,
                                          Position, Question, Skill)


class TestAssessmentView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('assessment_update', kwargs={'pk': 1}), login_required=True,
                         permission_required=True, permission_name='can_assess_profiles', permission_class=Assessment)

    def test__views__assessment__get__should_return_404_when_not_existing_profil_id_is_given(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(reverse('assessment_update', kwargs={'pk': 123}), user=self.user)

        # Assert
        self.assertEquals(response.status_code, 404)

    def test__views__assessment__get__should_return_404_when_profil_id_exists_but_has_no_assessment(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(reverse('assessment_update', kwargs={'pk': 1}), user=self.user)

        # Assert
        self.assertEquals(response.status_code, 404)

    def test__views__assessment__get__should_show_not_specified_when_data_is_missing(self):
        # Arrange
        assessment = Assessment(profile=self.profile, status='pending')
        assessment.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(reverse('assessment_update', kwargs={'pk': assessment.pk}), user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assessment-update.html')
        self.assertContains(response, '<dd class="col-sm-6 text-danger">Not specified</dd>')
        self.assertContains(response, '<dd class="col-sm-6">German, American</dd>')
        self.assertContains(response, self.p_danger('No skills specified.'))
        self.assertContains(response, self.p_danger('No requested positions specified.'))
        self.assertContains(response, self.p_danger('No Documents uploaded.'))
        self.assertContains(response, self.p_danger('No questions answered.'))

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test__views__assessment__get__should_show_data_when_all_data_is_set(self):
        # Arrange
        assessment = Assessment(profile=self.profile, status='pending')
        assessment.save()
        question = Question.objects.all().first()
        answer1 = Answer(question=question, profile=self.profile, text='Test Answer 1')
        answer2 = Answer(question=question, profile=self.profile, text='Test Answer 2')
        answer1.save()
        answer2.save()
        skill1 = Skill.objects.all().first()
        skill2 = Skill.objects.all().last()
        self.profile.skills.set((skill1, skill2))
        position1 = Position.objects.all().first()
        position2 = Position.objects.all().last()
        self.profile.requested_positions.set((position1, position2))
        document_type = DocumentType(name='Passport')
        document_type.save()
        document = Document(document_type=document_type, profile=self.profile, number='1234',
                            issuing_date=date.today(), expiry_date=date.today(), issuing_authority='NSA',
                            issuing_place='Crypto City', issuing_country='United States of America',
                            file=SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpg"))
        document.save()

        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(reverse('assessment_update', kwargs={'pk': assessment.pk}), user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assessment-update.html')
        self.assertContains(response, '<dd class="col-sm-6 text-danger">Not specified</dd>')
        self.assertContains(response, '<dd class="col-sm-6">German, American</dd>')
        self.assertContains(response, self.li(skill1.name))
        self.assertContains(response, self.li(skill2.name))
        self.assertContains(response, self.li(position1.name))
        self.assertContains(response, self.li(position2.name))
        self.assertContains(response, '<dd class="col-sm-8">Test Answer 1</dd>')
        self.assertContains(response, '<dd class="col-sm-8">Test Answer 2</dd>')
        self.assertContains(response, self.td(document.pk))
        self.assertContains(response, self.td(document.document_type))
        self.assertContains(response, self.td(document.number))
        self.assertContains(response, self.td(document.issuing_date.strftime('%b. %-d, %Y')))
        self.assertContains(response, self.td(document.expiry_date.strftime('%b. %-d, %Y')))
        self.assertContains(response, self.td(document.issuing_authority))
        self.assertContains(response, self.td(document.issuing_place))
        self.assertContains(response, self.td(document.issuing_country))
        self.assertContains(response, self.td(document.file.name))

    def test__views__assessment__get__should_set_initial_values_when_values_are_set(self):
        # Arrange
        assessment = Assessment(profile=self.profile, status='pending', comment='Test Comment')
        assessment.save()
        position = Position.objects.all().first()
        self.profile.requested_positions.set((position,))
        self.profile.approved_positions.set((position,))
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(reverse('assessment_update', kwargs={'pk': assessment.pk}),
                                   user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assessment-update.html')
        self.assertContains(response, '<dd class="col-sm-6">German, American</dd>')
        self.assertContains(response, self.p_danger('No skills specified.'))
        self.assertContains(response, self.p_danger('No Documents uploaded.'))
        self.assertContains(response, self.p_danger('No questions answered.'))
        self.assertContains(response, self.checked_required_radio_input(name='status', value='pending'))
        self.assertContains(response, self.selected_option(position))
        self.assertContains(response, 'Test Comment</textarea>')

    def test__views__assessment__post__should_return_404_when_not_existing_profil_id_is_given(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(reverse('assessment_update', kwargs={'pk': 123}),
                                    {'approved_positions': 1,
                                     'status': 'accepted',
                                     'comment': ''},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 404)

    def test__views__assessment__post__should_show_not_specified_when_data_is_missing(self):
        # Arrange
        assessment = Assessment(profile=self.profile, status='pending')
        assessment.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(reverse('assessment_update', kwargs={'pk': assessment.pk}),
                                    {'approved_positions': 100,  # a bit of a hack
                                     'status': 'accepted',
                                     'comment': ''},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assessment-update.html')
        self.assertContains(response, '<dd class="col-sm-6 text-danger">Not specified</dd>')
        self.assertContains(response, '<dd class="col-sm-6">German, American</dd>')
        self.assertContains(response, self.p_danger('No skills specified.'))
        self.assertContains(response, self.p_danger('No requested positions specified.'))
        self.assertContains(response, self.p_danger('No Documents uploaded.'))
        self.assertContains(response, self.p_danger('No questions answered.'))

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test__views__assessment__post__should_show_data_when_all_data_is_set(self):
        # Arrange
        assessment = Assessment(profile=self.profile, status='pending')
        assessment.save()
        question = Question.objects.all().first()
        answer1 = Answer(question=question, profile=self.profile, text='Test Answer 1')
        answer2 = Answer(question=question, profile=self.profile, text='Test Answer 2')
        answer1.save()
        answer2.save()
        skill1 = Skill.objects.all().first()
        skill2 = Skill.objects.all().last()
        self.profile.skills.set((skill1, skill2))
        position1 = Position.objects.all().first()
        position2 = Position.objects.all().last()
        self.profile.requested_positions.set((position1, position2))
        document_type = DocumentType(name='Passport')
        document_type.save()
        document = Document(document_type=document_type, profile=self.profile, number='1234',
                            issuing_date=date.today(), expiry_date=date.today(), issuing_authority='NSA',
                            issuing_place='Crypto City', issuing_country='United States of America',
                            file=SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpg"))
        document.save()

        self.client.login(username=self.username, password=self.password)

        # Act
        response_post = self.client.post(reverse('assessment_update', kwargs={'pk': assessment.pk}),
                                         {'approved_positions': position1.pk,
                                          'status': 'accepted',
                                          'comment': ''},
                                         user=self.user)
        response = self.client.get(reverse('assessment_update', kwargs={'pk': assessment.pk}),
                                   user=self.user)

        # Assert
        self.assertEquals(response_post.status_code, 302)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assessment-update.html')
        self.assertContains(response, '<dd class="col-sm-6 text-danger">Not specified</dd>')
        self.assertContains(response, '<dd class="col-sm-6">German, American</dd>')
        self.assertContains(response, self.li(skill1.name))
        self.assertContains(response, self.li(skill2.name))
        self.assertContains(response, self.li(position1.name))
        self.assertContains(response, self.li(position2.name))
        self.assertContains(response, '<dd class="col-sm-8">Test Answer 1</dd>')
        self.assertContains(response, '<dd class="col-sm-8">Test Answer 2</dd>')
        self.assertContains(response, self.td(document.pk))
        self.assertContains(response, self.td(document.document_type))
        self.assertContains(response, self.td(document.number))
        self.assertContains(response, self.td(document.issuing_date.strftime('%b. %-d, %Y')))
        self.assertContains(response, self.td(document.expiry_date.strftime('%b. %-d, %Y')))
        self.assertContains(response, self.td(document.issuing_authority))
        self.assertContains(response, self.td(document.issuing_place))
        self.assertContains(response, self.td(document.issuing_country))
        self.assertContains(response, self.td(document.file.name))

    def test__views__assessment__post__should_save_new_values_when_values_are_set(self):
        # Arrange
        assessment = Assessment(profile=self.profile, status='pending')
        assessment.save()
        position1 = Position.objects.all().first()
        position2 = Position.objects.all().last()
        self.profile.requested_positions.set((position1, position2))
        self.profile.approved_positions.set((position1,))
        self.client.login(username=self.username, password=self.password)

        # Act
        response_post = self.client.post(reverse('assessment_update', kwargs={'pk': assessment.pk}),
                                         {'approved_positions': position2.pk,
                                          'status': 'accepted',
                                          'comment': 'Test Comment'},
                                         user=self.user)
        response = self.client.get(reverse('assessment_update', kwargs={'pk': assessment.pk}),
                                   user=self.user)

        # Assert
        self.assertEquals(response_post.status_code, 302)
        self.assertTemplateUsed(response, 'assessment-update.html')
        self.assertContains(response, self.selected_option(position2))
        self.assertEquals(Assessment.objects.get(profile=self.profile).status, 'accepted')
        self.assertEquals(Assessment.objects.get(profile=self.profile).comment, 'Test Comment')
        self.assertEquals(self.profile.approved_positions.all().first(), position2)
        self.assertEquals(self.profile.approved_positions.all().count(), 1)

    def test__views__assessment__post__should_delete_approved_positions_when_no_positions_are_set(self):
        # Arrange
        assessment = Assessment(profile=self.profile, status='pending', comment='Test Comment')
        assessment.save()
        position1 = Position.objects.all().first()
        position2 = Position.objects.all().last()
        self.profile.requested_positions.set((position1, position2))
        self.profile.approved_positions.set((position1, position2))
        self.client.login(username=self.username, password=self.password)

        # Act
        response_post = self.client.post(reverse('assessment_update', kwargs={'pk': assessment.pk}),
                                         {'status': 'accepted',
                                          'comment': ''},
                                         user=self.user)
        response = self.client.get(reverse('assessment_update', kwargs={'pk': assessment.pk}),
                                   user=self.user)

        # Assert
        self.assertEquals(response_post.status_code, 302)
        self.assertTemplateUsed(response, 'assessment-update.html')
        self.assertEquals(Assessment.objects.get(profile=self.profile).status, 'accepted')
        self.assertEquals(Assessment.objects.get(profile=self.profile).comment, '')
        self.assertEquals(self.profile.approved_positions.all().count(), 0)

    @staticmethod
    def checked_required_radio_input(name, value, id_number=0, is_post_request=False):
        if is_post_request:
            class_is_valid = 'is-valid '
        else:
            class_is_valid = ''
        return '<input checked="" class="' + class_is_valid + 'form-check-input" id="id_' + name + '_' + \
               str(id_number) + '" name="' + name + '" required="" title="" type="radio" value="' + value + '"/>'

    @staticmethod
    def selected_option(position: Position):
        return '<option value="' + str(position.pk) + '" selected>' + position.name + '</option>'

    @staticmethod
    def p_danger(text):
        return '<p class="text-danger">' + text + '</p>'

    @staticmethod
    def li(text):
        return '<li class="list-group-item">' + text + '</li>'

    @staticmethod
    def td(value):
        return '<td>' + str(value) + '</td>'
