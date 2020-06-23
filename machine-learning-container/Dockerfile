FROM python:3

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    build-essential \
    ca-certificates \
    python3-dev \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/* \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/local/bin/pip pip /usr/local/bin/pip3 1

#Add Requirments file
COPY requirements.txt .

# Install sklearn, Flask mentioned in requirments file
RUN pip3 --no-cache-dir install -r requirements.txt

RUN mkdir -p /home/model-server/
RUN mkdir -p /home/model-server/models

ENV AUTHLIB_INSECURE_TRANSPORT=1

WORKDIR /home/model-server/

# Copy entrypoint script to the image
COPY . .

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 8080

# Define an entrypoint script for the docker image
ENTRYPOINT ["python3", "/home/model-server/app.py"]

# Define command to be passed to the entrypoint
CMD ["serve"]