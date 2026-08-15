from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = (
        ("job_seeker", "Job Seeker"),
        ("employer", "Employer"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username


class CandidateProfile(models.Model):

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="candidate"
    )

    headline = models.CharField(
        max_length=200,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    portfolio = models.URLField(
        blank=True
    )

    github = models.URLField(
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    cv = models.FileField(
        upload_to="cv/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.profile.user.username


class EmployerProfile(models.Model):

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="employer"
    )

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    industry = models.CharField(
        max_length=100,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    company_logo = models.ImageField(
        upload_to="companies/",
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            self.company_name
            if self.company_name
            else self.profile.user.username
        )
class Skill(models.Model):

    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    name = models.CharField(
        max_length=100
    )

    level = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.candidate.profile.user.username}"
class Education(models.Model):

    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="education"
    )

    institution = models.CharField(
        max_length=200
    )

    qualification = models.CharField(
        max_length=200
    )

    field_of_study = models.CharField(
        max_length=200,
        blank=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.qualification} - {self.institution}"
class Experience(models.Model):

    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="experience"
    )

    company = models.CharField(
        max_length=200
    )

    position = models.CharField(
        max_length=200
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    current_job = models.BooleanField(
        default=False
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.position} - {self.company}"
class Certification(models.Model):

    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="certifications"
    )

    name = models.CharField(
        max_length=200
    )

    issuing_organization = models.CharField(
        max_length=200
    )

    issue_date = models.DateField(
        null=True,
        blank=True
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    credential_url = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.name