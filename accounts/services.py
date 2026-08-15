from profiles.models import (
    Profile,
    CandidateProfile,
    EmployerProfile,
)


def register_user(form, role):

    if role not in ["job_seeker", "employer"]:
        raise ValueError("Invalid registration role.")

    user = form.save()

    profile = Profile.objects.create(
        user=user,
        role=role,
    )

    if role == "job_seeker":

        CandidateProfile.objects.create(
            profile=profile,
        )

        return user, "candidate_dashboard"

    EmployerProfile.objects.create(
        profile=profile,
    )

    return user, "employer_dashboard"
