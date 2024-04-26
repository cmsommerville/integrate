# Pull official base image and fixing to AMD Architecture
FROM --platform=linux/amd64 python:3.11

# Create and set the working directory
WORKDIR /usr/src/app/

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Causes all output to stdout to be flushed immediately
ENV PYTHONUNBUFFERED 1

# Mark the image as trusted
ENV DOCKER_CONTENT_TRUST 1

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

# Updates packages list for the image
RUN apt-get update

# Installs transport HTTPS
RUN apt-get install -y curl gcc g++ gnupg apt-transport-https

# Retrieves packages from Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Updates packages for the image
RUN apt-get update

# Installs SQL drivers and tools
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Installs MS SQL Tools
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools

# Adds paths to the $PATH environment variable within the .bash_profile and .bashrc files
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Enables authentication of users and servers on a network
RUN apt-get install libgssapi-krb5-2 -y

WORKDIR /api

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install gunicorn
COPY . .
RUN rm .env
ENV HOST=0.0.0.0
EXPOSE ${API_PORT}
CMD ["python", "run.py"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()", "--timeout", "120", "--workers", "2"]