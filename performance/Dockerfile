# first get the python image
FROM python:3.6

# check the environment status and ensure
ENV PYTHONUNBUFFERED 1

# copy the pipfile and pipfile lock to the image
# and install during runtime
COPY Pipfile Pipfile.lock performance_system/
WORKDIR /performance_system/
# # The default user that should be used
# ARG USER_ID=1000
# ARG GROUP_ID=1000

# ARG APP_USER=appuser

# # Create user and group
# RUN groupadd -g ${GROUP_ID} ${APP_USER} && useradd -u ${USER_ID} -g ${APP_USER} -s /bin/sh ${APP_USER}

# # Install ca certificates
# RUN apt-get update \
# && apt-get install ca-certificates -y \
# && apt-get clean

# COPY --from=build /root/ /root/
# RUN chown -R ${APP_USER}:${APP_USER} /root
# RUN chmod 755 /root

COPY . .
# COPY --chown=${APP_USER}:${APP_USER} . .
# RUN chown -R ${APP_USER}:${APP_USER} /performance_system
# RUN chmod 755 /performance_system

# Sert the default user
# USER ${APP_USER}


RUN pip install pipenv && pipenv install --system


# RUN python manage.py collectstatic --no-input 

# expose the port and run the gunicorn file...
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "setup", "setup.wsgi:application"]


####################################
