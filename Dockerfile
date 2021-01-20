FROM 806860399886.dkr.ecr.us-east-1.amazonaws.com/miniconda/miniconda3:4.7.10-alpine

# Create a directory to work from
WORKDIR /tmp/

# Copy conda environment specification
COPY environment.yml /tmp/

USER root

# Update base conda environment with dependencies
# Clear unused files
RUN /opt/conda/bin/conda update -n base -c defaults conda \
    && /opt/conda/bin/conda env update -n root --file environment.yml \
    && /opt/conda/bin/conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete \
    && rm environment.yml \
    && echo "Installation Complete!"

USER anaconda

COPY /src /app/src

WORKDIR /app/src
EXPOSE 4000

ENV PATH "/bin:/sbin:/usr/bin:/opt/conda/bin"

# Run Flask App
CMD ["python", "app.py"]
