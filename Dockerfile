# ----------- Agent API Docker File
# TODO : Setup volume for persistent sessions
# TODO : add healthcheck

# Kali Setup
FROM kalilinux/kali-rolling

ARG ollama_endpoint=http://localhost:11434
ARG ollama_model=gemma2:9b

RUN apt-get update && apt-get install -y \
    python3-pip ca-certificates python3 python3-wheel \
    nmap \
    gobuster \
    hashcat \
    exploitdb \
    sqlmap \
    git

# Setup API
RUN git clone --filter=blob:none --no-checkout https://github.com/antoninoLorenzo/AI-OPS.git && \
    cd AI-OPS/ && \
    git sparse-checkout init && \
    git sparse-checkout set requirements.txt src/ tools_settings/ && \
    git checkout

RUN cd AI-OPS/  && \
    pip3 install --no-cache-dir -r requirements.txt && \
    python3 -m spacy download en_core_web_lg  && \
    mkdir -p $HOME/.aiops/tools && \
    mv tools_settings/* ~/.aiops/tools/

VOLUME ["/root/.aiops"]

# Run healtcheck
# ...

# Run API
ENV MODEL=${ollama_model}
ENV ENDPOINT=${ollama_endpoint}
RUN echo "MODEL=$MODEL"       && \
    echo "ENDPOINT=$ENDPOINT"

EXPOSE 8000
CMD ["fastapi", "dev", "--host", "0.0.0.0", "./AI-OPS/src/api.py"]

# docker build -t ai-ops:api-dev --build-arg ollama_endpoint=ENDPOINT .
# docker run -p 8000:8000 ai-ops:api-dev
