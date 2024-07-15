FROM pymesh/pymesh:py3.7-slim
RUN pip install Flask==2.2.5
WORKDIR /app
COPY src/app /app
CMD ["python3","-u","luneforge.py"]