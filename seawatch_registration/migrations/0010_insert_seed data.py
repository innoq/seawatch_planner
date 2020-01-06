from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seawatch_registration', '0009_remove_profile_email'),
    ]

    def insertData(apps, schema_editor):
        Position = apps.get_model('seawatch_registration', 'Position')
        positions = [
            Position(name = 'Master'),
            Position(name = 'Chief Officer'),
            Position(name = '2nd Officer'),
            Position(name = 'Chief Engineer'),
            Position(name = '2nd Engineer'),
            Position(name = '3rd Engineer'),
            Position(name = 'Bosun'),
            Position(name = 'Deck Rating'),
            Position(name = 'Rhib driver'),
            Position(name = 'Head of Mission'),
            Position(name = 'Cook'),
            Position(name = 'IT'),
            Position(name = 'Medic'),
            Position(name = 'Cultural Mediator'),
            Position(name = 'Guest Coordinator'),
            Position(name = 'Field Media Coordinator'),
            Position(name = 'Journalist'),
        ]
        for position in positions:
            position.save()

        Skill = apps.get_model('seawatch_registration', 'Skill')
        skills = [
            Skill(name = 'German', group = 'lang'),
            Skill(name = 'English', group = 'lang'),
            Skill(name = 'Dutch', group = 'lang'),
            Skill(name = 'Italian', group = 'lang'),
            Skill(name = 'French', group = 'lang'),
            Skill(name = 'Arabic', group = 'lang'),
            Skill(name = 'Farsi', group = 'lang'),
            Skill(name = 'Spanish', group = 'lang'),
            Skill(name = 'Cooking', group = 'other'),
            Skill(name = 'Electrics', group = 'other'),
            Skill(name = 'IT', group = 'other'),
            Skill(name = 'Human rights', group = 'other'),
            Skill(name = 'Doctor', group = 'other'),
            Skill(name = 'Caregiver', group = 'other'),
            Skill(name = 'Woodwork', group = 'other'),
            Skill(name = 'Metalwork', group = 'other'),

        ]
        for skill in skills:
            skill.save()
            
        Question = apps.get_model('seawatch_registration', 'Question')
        question = Question(text = 'What motivated you to contact us?', mandatory = True)
        question.save()

    operations = [
        migrations.RunPython(insertData),
    ]
