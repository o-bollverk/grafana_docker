##########################################################################
# MULTIMNO - BASE
##########################################################################

FROM apache/airflow:2.9.0 as base

# # --------- Set tzdata ----------
# # Set the timezone
# ENV TZ=Europe/Tallinn
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN apt-get update && apt-get install -y tzdata

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


# RUN pip-compile resources/requirements.in
# RUN pip install -r resources/requirements.txt
# RUN pip install -r ${install_dir}/requirements/dev_requirements.txt

# ----------- CLEANUP -----------

# adding privilages
#RUN useradd -ms /bin/bash admin
#USER admin
#RUN chmod ug+wx ${install_dir}


RUN rm -r ${install_dir}
RUN rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/opt/dev
ENV AIRFLOW_HOME=/opt/dev/airflow/

# Airflow db init
ENV NO_PROXY="*"

# RUN airflow db init
# RUN airflow users create -u admin -p admin -f admin -l admin -r Admin -e admin@admin.com
# RUN airflow dags reserialize

#EXPOSE 3000
#EXPOSE 4040

CMD ["bash"]


