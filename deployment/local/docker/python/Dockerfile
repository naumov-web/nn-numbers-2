FROM continuumio/anaconda3

RUN conda install numpy -y
RUN conda install keras -y
RUN conda install flask flask-cors -y
RUN conda install -c anaconda scikit-learn

EXPOSE 5000

WORKDIR /var/python-project

CMD python /var/python-project/site/index.py