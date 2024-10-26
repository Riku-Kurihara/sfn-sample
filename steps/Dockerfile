ARG PY_VER="3.12"

FROM public.ecr.aws/lambda/python:${PY_VER}

# 使用するpackageのリリースバージョンを最新にしておく。
RUN echo latest | tee /etc/dnf/vars/releasever
RUN dnf upgrade -y

COPY steps/requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install --upgrade pip
RUN python${PY_VER} -m pip install --no-cache-dir -r "${LAMBDA_TASK_ROOT}/requirements.txt" -t .

COPY ./steps/main.py ${LAMBDA_TASK_ROOT}/main.py

CMD ["main.handler"]
