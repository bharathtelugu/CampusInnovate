from django.db import models
from django.conf import settings
from teams.models import Team
from events.models import ProblemStatement

class Submission(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='submission')
    problem_statement = models.ForeignKey(ProblemStatement, on_delete=models.SET_NULL, null=True, blank=True)
    
    project_title = models.CharField(max_length=255)
    project_description = models.TextField()
    repo_link = models.URLField(blank=True, null=True)
    image_upload = models.ImageField(upload_to='submission_images/', blank=True, null=True)
    demo_link = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission: {self.project_title} by {self.team.team_name}"

class Judging(models.Model):
    judge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='judging_scores')
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='scores')
    score = models.FloatField()
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        # This enforces your composite key: a judge can only score a submission once.
        unique_together = ('judge', 'submission')

    def __str__(self):
        return f"Score for {self.submission.project_title} by {self.judge.username}"