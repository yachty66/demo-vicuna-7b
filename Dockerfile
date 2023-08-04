# Must use a Cuda version 11+
FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

WORKDIR /

# Install git and wget
RUN apt-get update && apt-get install -y git wget

# Upgrade pip
RUN pip install --upgrade pip

# Download and install specific version of AutoGPTQ from GitHub release
RUN wget https://github.com/PanQiWei/AutoGPTQ/releases/download/v0.3.2/auto_gptq-0.3.2+cu117-cp38-cp38-linux_x86_64.whl && \
    pip3 install auto_gptq-0.3.2+cu117-cp38-cp38-linux_x86_64.whl

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Add your model weight files 
# (in this case we have a python script)
ADD download.py .
RUN python3 download.py

ADD . .

EXPOSE 8000

CMD python3 -u app.py