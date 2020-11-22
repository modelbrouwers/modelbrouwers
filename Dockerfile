# This is a multi-stage build file, which means a stage is used to build
# the backend (dependencies), the frontend stack and a final production
# stage re-using assets from the build stages. This keeps the final production
# image minimal in size.

# Stage 1 - Backend build environment
# includes compilers and build tooling to create the environment
FROM python:3.6-buster AS backend-build

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir /app/src

# Ensure we use the latest version of pip
RUN pip install pip setuptools -U
COPY ./requirements /app/requirements
RUN pip install -r requirements/production.txt


# Stage 2 - Install frontend deps and build assets
FROM node:13-buster AS frontend-build

WORKDIR /app

# copy configuration/build files
COPY ./build /app/build/
COPY ./*.json ./*.js ./.babelrc /app/

# install WITH dev tooling
RUN npm ci

# copy source code
COPY ./src/sass /app/src/sass
COPY ./src/js /app/src/js

# build frontend
RUN npm run build


# Stage 3 - Build docker image suitable for production
FROM python:3.6-buster

# Stage 3.1 - Set up the needed production dependencies
# install all the dependencies for GeoDjango
RUN apt-get update && apt-get install -y --no-install-recommends \
        procps \
        vim \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./bin/docker_start.sh /start.sh
RUN mkdir /app/log
RUN mkdir /app/media
RUN mkdir /app/node_modules

# copy backend build deps
COPY --from=backend-build /usr/local/lib/python3.6 /usr/local/lib/python3.6
COPY --from=backend-build /usr/local/bin/uwsgi /usr/local/bin/uwsgi
COPY --from=backend-build /app/src/ /app/src/

# copy frontend build statics
COPY --from=frontend-build /app/node_modules/bootstrap /app/node_modules/bootstrap
COPY --from=frontend-build /app/node_modules/fine-uploader /app/node_modules/fine-uploader
COPY --from=frontend-build /app/node_modules/font-awesome /app/node_modules/font-awesome
COPY --from=frontend-build /app/src/static /app/src/static

VOLUME /app/media /app/private_media /app/log

# copy source code
COPY ./src /app/src

RUN useradd -M -u 1000 brouwers
RUN chown -R brouwers /app

# drop privileges
USER brouwers

# ARG COMMIT_HASH
# ENV GIT_SHA=${COMMIT_HASH}
ENV DJANGO_SETTINGS_MODULE=conf.settings.production

ARG SECRET_KEY=dummy

# Run collectstatic, so the result is already included in the image
RUN python src/manage.py collectstatic --noinput

# Clean up
RUN rm -rf node_modules src/static src/js

EXPOSE 8000
CMD ["/start.sh"]
