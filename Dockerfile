FROM python:3.9

RUN pip3 install requests tqdm

COPY . .

CMD ["python3", "jellyfin_extract_sub.py"]
