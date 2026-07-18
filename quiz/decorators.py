from django.contrib.auth.decorators import user_passes_test

def faculty_required(view_func):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='Faculty').exists()
    )(view_func)
    return decorated_view


def student_required(view_func):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='Student').exists()
    )(view_func)
    return decorated_view


def admin_required(view_func):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and (
            u.is_superuser or u.groups.filter(name='Admin').exists()
        )
    )(view_func)
    return decorated_view