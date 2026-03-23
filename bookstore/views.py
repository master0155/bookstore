import os

from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update(request):
    if request.method != "POST":
        return HttpResponse("Use POST to trigger server update", status=405)

    repo_path = os.environ.get("REPO_PATH", str(settings.BASE_DIR))

    try:
        import git

        repo = git.Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
        return HttpResponse("Updated code on PythonAnywhere")
    except ModuleNotFoundError:
        return HttpResponse(
            "Update failed: GitPython is not installed. Run 'poetry install' on the server.",
            status=500,
        )
    except Exception as exc:
        return HttpResponse(f"Update failed: {exc}", status=500)


def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render())

