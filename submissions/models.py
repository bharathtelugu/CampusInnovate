from django.db import models
from django.conf import settings
from teams.models import Team
from events.models import ProblemStatement

class Submission(models.Model):
    """
    Represents a single project submission by a team for an event.
    There is a one-to-one relationship with a Team.
    """
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='submission')
    problem_statement = models.ForeignKey(
        ProblemStatement, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="The problem statement the team chose to solve."
    )
    
    project_title = models.CharField(max_length=255)
    project_description = models.TextField()
    repo_link = models.URLField(blank=True, null=True, help_text="Link to GitHub, GitLab, etc.")
    demo_link = models.URLField(blank=True, null=True, help_text="Link to a video demo (YouTube, Loom, etc.)")
    image_upload = models.ImageField(
        upload_to='submission_images/', 
        blank=True, 
        null=True,
        help_text="A poster, screenshot, or architecture diagram."
    )
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Submission: {self.project_title} by {self.team.team_name}"

class Judging(models.Model):
    """
    Represents a score and feedback given by one judge to one submission.
    This acts as the "through" table for the many-to-many relationship.
    """
    judge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='judging_scores')
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='scores')
    
    score = models.FloatField(help_text="Score, e.g., out of 100.")
    feedback = models.TextField(blank=True, null=True, help_text="Constructive feedback for the team.")

    class Meta:
        # A judge can only score a submission once.
        unique_together = ('judge', 'submission')
        verbose_name_plural = "Judging Scores"

    def __str__(self):
        return f"Score for {self.submission.project_title} by {self.judge.username}"
