== Deployment notes ==
::note this will eventually end up in an ansible playbook

=== Forum authentication ===
Make sure a symbolic link exists to the forum includes and that the open_basedir is correctly set.

```bash
# Django auth backend
ln -s <projectdir>/src/phpbb/phpBB3/includes/auth/auth_django.php <public_html>/phpBB3/includes/auth/auth_django.php

ln -s <projectdir>/src/phpbb/phpBB3/includes/auth/getdjangouser.php <public_html>/phpBB3/includes/auth/getdjangouser.php

# Style path
ln -s <projectdir>/src/phpbb/phpBB3/styles/subsilver2_dead_topics <public_html>/phpBB3/styles/subsilver2_dead_topics
```
