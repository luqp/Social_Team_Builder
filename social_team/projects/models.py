from django.db import models

from accounts.models import UserAccount, Skill

STATUS = (
    (0, 'Without applicants'),
    (1, 'Applying'),
    (2, 'Accepted'),
    (3, 'Reject')
)


class Project(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    time_line = models.IntegerField()
    requirementes = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Position(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    engaged = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Application(models.Model):
    position = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE, 
        related_name='applications')
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE)
    status = models.IntegerField(
        choices=STATUS, default=0)

    def __str__(self):
        return f'Application to {self.position}'
