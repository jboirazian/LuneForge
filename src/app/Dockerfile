FROM pymesh/pymesh:py3.7-slim
RUN pip install Flask==2.2.5
RUN pip install Markdown==3.4.4
WORKDIR /app
COPY src/app /app
CMD ["python3","-u","luneforge.py"]