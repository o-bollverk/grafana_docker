##########################################################################
# Airflow scheduler container with python dependencies
##########################################################################

FROM apache/airflow:2.9.0 as base

# Shell and workdir
ENV SHELL /bin/bash
WORKDIR /opt/dev/resources

# Pip tools installation
RUN pip3 install poetry pip-tools
# Upgrade pip to latest version
RUN pip install --upgrade pip

# A better approach for maintaining inter dependencies of packages
# rather than to use pip freeze 
ARG install_dir=/tmp/install
RUN mkdir ${install_dir}
COPY requirements/requirements.in ${install_dir}/requirements.in

RUN pip-compile ${install_dir}/requirements.in
RUN pip install -r ${install_dir}/requirements.txt

# Clean install directory
RUN rm -r ${install_dir}
RUN rm -rf /var/lib/apt/lists/*

# Pythonpath for correct importing of modules
ENV PYTHONPATH=/opt/dev
ENV AIRFLOW_HOME=/opt/dev/airflow/
ENV NO_PROXY="*"

CMD ["bash"]


